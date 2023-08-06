import os
from hashlib import sha256
import mimetypes
import base64
import json
import re
import hmac
import struct
import sys

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


### General utilities
def url_b64encode(s):
    return base64.urlsafe_b64encode(s).decode().rstrip('=')

def url_b64decode(s):
    # accept unicode (py2), str (py2) and str (py3) inputs
    s = str(s)
    s += '==='[(len(s) + 3) % 4:]
    return base64.urlsafe_b64decode(s)

### Cryptography
def hkdf(length, ikm, hashfunc=sha256, salt=b"", info=b""):
    prk = hmac.new(salt, ikm, hashfunc).digest()
    t = b""
    i = 0
    okm = bytearray()
    while len(okm) < length:
        i += 1
        t = hmac.new(prk, t + info + bytes(bytearray([i])), hashfunc).digest()
        okm += t
    return bytes(okm[:length])

def derive_auth_key(secret, password=None, url=None):
    if password is None:
        return hkdf(64, secret, info=b'authentication')
    else:
        return PBKDF2(password.encode('utf8'), url.encode('utf8'), 64, 100,
                      lambda x, y: hmac.new(x, y, sha256).digest())

def create_meta_cipher(secret):
    meta_key = hkdf(16, secret, info=b'metadata')
    return AES.new(meta_key, AES.MODE_GCM, b'\x00' * 12, mac_len=16)

def file_cipher_generator(secret, salt):
    key = hkdf(16, secret, salt=salt, info=b'Content-Encoding: aes128gcm\0')
    nonce_base = hkdf(12, secret, salt=salt, info=b'Content-Encoding: nonce\0')
    seq = 0
    while True:
        if seq >= (1 << 32):
            raise ValueError("Tried to encrypt too many chunks!")
        tail, = struct.unpack('>I', nonce_base[-4:])
        tail ^= seq
        nonce = nonce_base[:-4] + struct.pack('>I', tail)
        yield AES.new(key, AES.MODE_GCM, nonce, mac_len=16)
        seq += 1

def encrypt_file_iter(secret, file, recordsize=65536):
    # 1 byte padding (minimum) + 16 byte tag
    padtaglen = 17
    assert recordsize > padtaglen, "record size too small"

    idlen = 0
    salt = os.urandom(16)
    header = struct.pack('>16sIB', salt, recordsize, idlen)
    yield header

    ciphergen = file_cipher_generator(secret, salt)
    chunksize = recordsize - padtaglen
    # this loop structure allows us to handle zero-byte files properly
    chunk = file.read(chunksize)
    while True:
        nextchunk = file.read(chunksize)
        # add padding
        if not nextchunk:
            # reached EOF, this is the last chunk
            chunk += b'\x02'
        else:
            chunk += b'\x01' + b'\x00' * (recordsize - len(chunk) - padtaglen)

        # encrypt and append GCM tag
        cipher = next(ciphergen)
        res = cipher.encrypt(chunk)
        res += cipher.digest()

        yield res

        if not nextchunk:
            break
        chunk = nextchunk

def decrypt_file_iter(secret, file):
    # ensure we read the whole header even if we get a short read
    header = bytearray()
    while len(header) < 21:
        chunk = file.read(21 - len(header))
        if not chunk:
            raise EOFError()
        header += chunk

    salt, recordsize, idlen = struct.unpack('>16sIB', header)
    # TODO handle nonzero idlen
    assert idlen == 0, "unexpected idlen"
    assert recordsize > 17, "record size too small"

    ciphergen = file_cipher_generator(secret, salt)
    while True:
        # try to get a full record if at all possible
        record = bytearray()
        while len(record) < recordsize:
            chunk = file.read(recordsize - len(record))
            if not chunk:
                break
            record += chunk
        if len(record) < 17:
            raise ValueError("Bad record received")
        record = bytes(record)

        cipher = next(ciphergen)
        res = cipher.decrypt(record[:-16])
        cipher.verify(record[-16:])

        # verify and remove padding
        res = res.rstrip(b'\x00')
        if res.endswith(b'\x01'):
            yield res[:-1]
        elif res.endswith(b'\x02'):
            # final block
            yield res[:-1]
            break
        else:
            raise ValueError("Bad padding")


def single_file_metadata(filename, filesize, mimetype='application/octet-stream'):
    return {
        "name": filename,
        "size": filesize,
        "type": mimetype,
        "manifest": {
            "files": [
                {"name": filename, "size": filesize, "type": mimetype}
            ]
        }
    }