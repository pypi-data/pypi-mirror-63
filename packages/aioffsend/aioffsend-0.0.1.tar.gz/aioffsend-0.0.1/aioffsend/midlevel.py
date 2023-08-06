from .utillies import (
    derive_auth_key,
    create_meta_cipher,
    encrypt_file_iter,
    decrypt_file_iter,
    url_b64decode
)
from .lowlevel import FFSendAPI

import os
import json
from aiohttp import ClientResponse

class FFSend(object):
    ''' High-level Pythonic methods for the Firefox Send API

    This class wraps the low-level API with appropriate cryptographic logic. '''

    def __init__(self, service, loop=None):
        self.api = FFSendAPI(service, loop=loop)

    async def upload(self, metadata, fileobj):
        ''' Upload a file to the service.

        metadata: metadata object for the file
        fileobj: file-like object (supporting .read) to upload

        Returns: (response JSON, secret)
        '''

        secret = os.urandom(16)

        auth_key = derive_auth_key(secret)
        meta_cipher = create_meta_cipher(secret)

        metadata = meta_cipher.encrypt(json.dumps(metadata).encode('utf8'))
        metadata += meta_cipher.digest()

        data = encrypt_file_iter(secret, fileobj)
        async with self.api.post_upload(metadata, auth_key, data) as response:
            response.raise_for_status()

            return (await response.json()), secret

    async def download(self, fid, secret, fileobj, password=None, url=None):
        ''' Download a file from the service.

        fid: file ID
        secret: end-to-end encryption secret
        fileobj: file-like object (supporting .write) to write to
        password: file password (optional)
        url: file share URL (must be specified if password is specified)
        '''
        auth_key = derive_auth_key(secret, password, url)

        async with self.api.get_download(fid, auth_key) as response:
            for chunk in decrypt_file_iter(secret, await response.read()):
                fileobj.write(chunk)

    async def get_metadata(self, fid, secret, password=None, url=None):
        ''' Get file metadata.

        fid: file ID
        secret: end-to-end encryption secret
        password: file password (optional)
        url: file share URL (must be specified if password is specified)
        '''

        auth_key = derive_auth_key(secret, password, url)
        meta_cipher = create_meta_cipher(secret)

        async with self.api.get_metadata(fid, auth_key) as response:
            response.raise_for_status()
            metadata = await response.json()

        md = url_b64decode(metadata['metadata'])
        md, mdtag = md[:-16], md[-16:]
        md = meta_cipher.decrypt(md)
        meta_cipher.verify(mdtag)
        metadata['metadata'] = json.loads(md)

        return metadata

    async def owner_delete(self, fid, owner_token):
        ''' Delete a file (owners only)

        fid: file ID
        owner_token: owner token returned by upload
        '''
        async with self.api.post_delete(fid, owner_token) as response:
            response.raise_for_status()

    async def owner_get_info(self, fid, owner_token):
        ''' Get file basic info (# of downloads, time remaining; owners only)

        fid: file ID
        owner_token: owner token returned by upload
        '''
        async with self.api.post_info(fid, owner_token) as response:
            response.raise_for_status()
            return await response.json()

    async def owner_set_password(self, fid, owner_token, secret, password=None, url=None):
        ''' Set a new password for the file (owners only)

        fid: file ID
        owner_token: owner token returned by upload
        secret: end-to-end encryption secret
        password: new file password (optional - if unset it removes the password)
        url: file share URL (must be specified if password is specified)
        '''
        new_auth_key = derive_auth_key(secret, password, url)
        async with self.api.post_password(fid, owner_token, new_auth_key) as resp:
            resp.raise_for_status()

    async def owner_set_params(self, fid, owner_token, new_params):
        ''' Set new parameters for the file (e.g. download limit; owners only)

        fid: file ID
        owner_token: owner token returned by upload
        new_params: new parameters as a json-compatible dict
        '''
        async with self.api.post_params(fid, owner_token, new_params) as resp:
            resp.raise_for_status()