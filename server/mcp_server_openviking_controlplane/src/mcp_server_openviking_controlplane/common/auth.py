"""Pluggable authentication for the OpenViking control plane.

During the development phase we simply replay request headers captured from the
browser (``ManualHeadersAuth``). The ``AuthProvider`` protocol leaves room to plug
in a dedicated API-key or AK/SK signature provider later without touching
``client.py`` or the tool/CLI layers.
"""

from typing import Dict, Protocol


class AuthProvider(Protocol):
    """Produces the auth/identity headers for a single control-plane request."""

    def auth_headers(
        self, method: str, path: str, query: Dict[str, str], body_str: str
    ) -> Dict[str, str]:
        ...


class ManualHeadersAuth:
    """Replay a static set of headers supplied manually (e.g. copied from the browser).

    Ignores the per-request method/path/body: the captured headers already carry
    whatever cookie / token the gateway needs during development. This works as long
    as the console uses session/cookie/token auth (independent of the request body);
    once we move to per-request AK/SK signing, swap in ``SignatureAuth`` below.
    """

    def __init__(self, headers: Dict[str, str]):
        self._headers = dict(headers)

    def auth_headers(
        self, method: str, path: str, query: Dict[str, str], body_str: str
    ) -> Dict[str, str]:
        return dict(self._headers)


# --- Future: signature-based auth (intentionally NOT implemented yet) ----------
#
# class SignatureAuth:
#     """AK/SK HMAC-SHA256 (volcengine V4 style) signer for the control plane.
#
#     Port the reference implementation from
#     OpenViking_kb_volc/test/openviking/create_collection_01.py (ClientForConsole):
#       - SignedHeaders = content-type;host;x-content-sha256;x-date
#       - CredentialScope = {yyyyMMdd}/{region}/{service}/request
#       - derive: kDate -> kRegion -> kService -> kSigning -> Signature
#       - plus identity headers: X-Top-Service / X-Top-Region / X-Top-Account-Id /
#         V-Account-Id, and query params Action + Version.
#     Implemented with stdlib hmac/hashlib only (no volcengine SDK dependency).
#     """
#
#     def __init__(self, ak, sk, region, service, account):
#         ...
#
#     def auth_headers(self, method, path, query, body_str):
#         ...
