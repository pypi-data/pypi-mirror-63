import re
from .utillies import url_b64decode, url_b64encode, single_file_metadata

import os
import mimetypes
from .midlevel import FFSend

def parse_url(url):
    secret = None
    m = re.match(r'^https://(.*)/download/(\w+)/?#?([\w_-]+)?$', url)
    if m:
        service = 'https://' + m.group(1) + '/'
        fid = m.group(2)
        if m.group(3):
            secret = url_b64decode(m.group(3))
    else:
        raise Exception("Failed to parse URL %s" % url)

    return service, fid, secret

async def _upload(firefox_send: FFSend, filename, file, password=None, timeLimit: int = None):
    filename = os.path.basename(filename)

    mimetype = mimetypes.guess_type(filename, strict=False)[0] or 'application/octet-stream'

    file.seek(0, 2)
    filesize = file.tell()
    file.seek(0)
    metadata = single_file_metadata(filename, filesize, mimetype=mimetype)

    res, secret = await firefox_send.upload(metadata, file)
    url = res['url'] + '#' + url_b64encode(secret)
    owner_token = res['owner']

    if any([password, timeLimit]):
        fid, secret = parse_url(url)[1:]
        if password:
            await firefox_send.owner_set_password(fid, owner_token, secret, password, url)
        if timeLimit:
            await firefox_send.owner_set_params(fid, owner_token, {
                "timeLimit": timeLimit
            })

    return url, owner_token

async def upload(service, filename, file=None, password=None, timeLimit=None):
    ''' Upload a file to the Send service.

    service: the service, must be a FFSend object.
    filename: filename to upload
    file: readable file-like object (supporting .read, .seek, .tell)
        if not specified, defaults to opening `filename`
    password: optional password to protect the file

    returns the share URL and owner token for the file
    '''

    if file is None:
        with open(filename, "rb") as file:
            return await _upload(service, filename, file, password, timeLimit)
    else:
        return await _upload(service, filename, file, password)

async def delete(service: FFSend, fid, token):
    await service.owner_delete(fid, token)

async def set_params(service: FFSend, fid, token, **params):
    await service.owner_set_params(fid, token, params)

async def get_metadata(service: FFSend, fid, secret, password=None, url=None):
    return await service.get_metadata(fid, secret, password, url)

async def get_owner_info(service: FFSend, fid, token):
    return await service.owner_get_info(fid, token)

async def download(service, fid, secret, dest, password=None, url=None):
    send = FFSend(service)
    metadata = send.get_metadata(fid, secret, password, url)

    filename = metadata['metadata']['name']

    if os.path.isdir(dest):
        filename = os.path.join(dest, filename)
    else:
        filename = dest

    try:
        with open(filename + '.tmp', 'wb') as outf:
            await send.download(fid, secret, outf, password, url)
    except Exception:
        os.unlink(filename + '.tmp')
    else:
        os.rename(filename + '.tmp', filename)