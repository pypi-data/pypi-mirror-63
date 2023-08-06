from __future__ import annotations

from dataclasses import dataclass
import os

from typing_extensions import Final


@dataclass(frozen=True)
class ClientId:
    value: str


@dataclass(frozen=True)
class ClientSecret:
    value: str


ENVAR_CLIENT_ID: Final[str] = "MYGP_CLIENT_ID"
ENVAR_CLIENT_SECRET: Final[str] = "MYGP_CLIENT_SECRET"


@dataclass(frozen=True)
class AuthInfo:
    client_id: ClientId
    client_secret: ClientSecret

    @staticmethod
    def from_environment() -> AuthInfo:
        client_id = os.environ.get(ENVAR_CLIENT_ID)
        client_secret = os.environ.get(ENVAR_CLIENT_SECRET)

        if client_id is None:
            raise RuntimeError(
                f"Missing ${ENVAR_CLIENT_ID} environment variable.")
        elif client_secret is None:
            raise RuntimeError(
                f"Missing ${ENVAR_CLIENT_SECRET} environment "
                f"variable.")
        else:
            return AuthInfo(ClientId(client_id), ClientSecret(client_secret))
