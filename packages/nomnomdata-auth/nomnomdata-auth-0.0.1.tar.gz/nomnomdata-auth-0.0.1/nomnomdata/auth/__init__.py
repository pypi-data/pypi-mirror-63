import hashlib
import hmac
from calendar import timegm
from datetime import datetime, timedelta
from urllib.parse import urlencode

from requests.auth import AuthBase


class KeyAuth(AuthBase):
    def __init__(self, secret: str):
        self.secret = secret

    def __call__(self, request):
        body = request.body or b""
        if not isinstance(body, bytes):
            body = body.encode("utf-8")
        url = request.url
        ts = generate_request_timestamp()
        request.headers["X-NomNom-Signature"] = generate_sig(self.secret, ts, body, url)
        request.headers["X-NomNom-SigTimestamp"] = ts
        return request


def generate_sig(secret: str, ts: int, body: bytes, url: str):
    data = b"".join([str(ts).encode("utf-8"), body, url.encode("utf-8")])
    signer = hmac.new(secret.encode("utf-8"), data, hashlib.sha512)
    return signer.hexdigest()


def generate_request_timestamp():
    return timegm(datetime.utcnow().utctimetuple())
