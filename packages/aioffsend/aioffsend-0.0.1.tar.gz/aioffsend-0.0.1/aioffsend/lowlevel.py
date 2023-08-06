import hmac
from hashlib import sha256
import base64
from aiohttp import ClientSession
import asyncio
from .utillies import url_b64decode, url_b64encode
from contextlib import asynccontextmanager

class FFSendAPI(object):
    # TODO: support Firefox Accounts login
    ''' Low-level Send API wrappers.

    These are fairly thin wrappers around the API.
    Each function returns a requests.Response, and some have simple retry logic.
    '''

    def __init__(self, baseurl, session=None, loop=None):
        self.baseurl = baseurl
        # map from file id to nonce
        self._nonce_cache = {}
        self.session = session or ClientSession(loop=loop or asyncio.get_event_loop())

    def _auth_header(self, auth_key, nonce):
        sig = hmac.new(auth_key, nonce, sha256).digest()
        return 'send-v1 ' + url_b64encode(sig)

    def _get_nonce(self, id):
        if id not in self._nonce_cache:
            resp = self.get_exists(id)
            resp.raise_for_status()
            self._set_nonce(id, resp)

        return self._nonce_cache[id]

    def _set_nonce(self, id, resp):
        header = resp.headers.get('WWW-Authenticate')
        if header and header.startswith('send-v1 '):
            self._nonce_cache[id] = base64.b64decode(header.split()[1])

    ### Basic endpoints
    @asynccontextmanager
    async def post_upload(self, metadata, auth_key, data):
        ''' POST /api/upload

        metadata: raw encrypted file metadata
        auth_key: file's new auth key
        data: raw encrypted file data to upload
        '''
        data = b"".join(list(data))
        async with self.session.post(self.baseurl + "api/upload", data=data, headers={
            'X-File-Metadata': url_b64encode(metadata),
            'Authorization': 'send-v1 ' + url_b64encode(auth_key),
            'Content-Type': 'application/octet-stream'
        }) as response:
            if response.status == 200:
                id = (await response.json())['id']
                self._set_nonce(id, response)
            yield response

    async def get_exists(self, id):
        ''' GET /api/exists/:id

        id: file id
        '''
        async with self.session.get(self.baseurl + "api/exists/" + id) as response:
            assert response.status == 200

    @asynccontextmanager
    async def get_download(self, id, auth_key):
        ''' GET /api/download/:id

        id: file id
        auth_key: file's auth key

        Reading the resulting request will produce raw encrypted file data.
        '''
        # TODO configurable retries
        for _ in range(5):
            nonce = self._get_nonce(id)
            async with self.session.get(
                self.baseurl + "api/download/" + id,
                stream=True,
                headers={'Authorization': self._auth_header(auth_key, nonce)}
            ) as response:
                self._set_nonce(id, response)
                if response.status_code == 401:
                    continue
                yield response

    @asynccontextmanager
    async def get_metadata(self, id, auth_key):
        ''' GET /api/metadata/:id

        id: file id
        auth_key: file's auth key

        The response's json will include raw encrypted file metadata.
        '''

        # TODO configurable retries
        for _ in range(5):
            nonce = self._get_nonce(id)
            async with self.session.get(
                self.baseurl + "api/metadata/" + id,
                stream=True,
                headers={'Authorization': self._auth_header(auth_key, nonce)}
            ) as response:
                self._set_nonce(id, response)
                if response.status_code == 401:
                    continue
                yield response

    ### Owner-only endpoints
    @asynccontextmanager
    async def post_delete(self, id, owner_token):
        ''' POST /api/delete/:id

        id: file id
        owner_token: owner token from upload
        '''
        async with self.session.get(
            self.baseurl + 'api/delete/' + id,
            headers={'Content-Type': 'application/json'},
            json={'owner_token': owner_token}
        ) as response:
            yield response

    @asynccontextmanager
    async def post_password(self, id, owner_token, auth_key):
        ''' POST /api/password/:id

        id: file id
        owner_token: owner token from upload
        auth_key: file's new auth key
        '''
        async with self.session.get(
            self.baseurl + 'api/password/' + id,
            headers={'Content-Type': 'application/json'},
            json={'auth': url_b64encode(auth_key), 'owner_token': owner_token}
        ) as response:
            yield response

    @asynccontextmanager
    async def post_info(self, id, owner_token):
        ''' POST /api/info/:id

        id: file id
        owner_token: owner token from upload
        '''
        async with self.session.post(
            self.baseurl + 'api/info/' + id,
            headers={'Content-Type': 'application/json'},
            json={'owner_token': owner_token}
        ) as response:
            yield response

    @asynccontextmanager
    async def post_params(self, id, owner_token, new_params):
        ''' POST /api/params/:id

        id: file id
        owner_token: owner token from upload
        new_params: file's new parameters (e.g. download limit)
        '''
        params = new_params.copy()
        params['owner_token'] = owner_token
        async with self.session.post(
            self.baseurl + 'api/params/' + id,
            headers={'Content-Type': 'application/json'},
            json=params
        ) as response:
            yield response