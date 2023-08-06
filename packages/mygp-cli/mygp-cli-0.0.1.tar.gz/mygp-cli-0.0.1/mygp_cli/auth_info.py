from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class AuthInfo:
    client_id: str
    client_secret: str

    @staticmethod
    def from_environment() -> AuthInfo:
        client_id = os.environ["MYGP_CLIENT_ID"]
        client_secret = os.environ["MYGP_CLIENT_SECRET"]
        return AuthInfo(client_id, client_secret)
