from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass
class AuthInfo:
    client_id: str
    client_secret: str

    @staticmethod
    def from_environment() -> AuthInfo:
        client_id = os.environ.get("MYGP_CLIENT_ID")
        client_secret = os.environ.get("MYGP_CLIENT_SECRET")

        if client_id is None:
            raise RuntimeError("Missing MYGP_CLIENT_ID environment variable.")
        elif client_secret is None:
            raise RuntimeError(
                "Missing MYGP_CLIENT_SECRET environment variable.")
        else:
            return AuthInfo(client_id, client_secret)
