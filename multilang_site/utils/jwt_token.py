from datetime import datetime, timedelta, timezone

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from django.conf import settings

JWT_PASSWORD = settings.JWT_PASSWORD
BASE_DIR = settings.BASE_DIR


class Jwt:
    @classmethod
    def _return_expiration_time(self):
        """define here the token expiration time"""

        return datetime.now(timezone.utc) + timedelta(hours=1)

    @classmethod
    def _return_private_key(self):
        """
        Used to encode the jwt
        to generate a private key with a password, enter the CLI :
        >>> openssl genpkey -algorithm RSA -out private_key.pem -aes256

        keep secret
        """

        try:
            with open(BASE_DIR / "private_key.pem", "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=JWT_PASSWORD,
                    backend=default_backend(),
                )

            return private_key

        except Exception as e:
            print("JWT._return_private_key() error : ", e)

    @classmethod
    def _return_public_key(self):
        """
        Used to decode the jwt
        to generate a plublic key from a private key, enter the CLI :
        >>> openssl rsa -pubout -in private_key.pem -out public_key.pem

        keep public
        """

        try:
            with open(BASE_DIR / "public_key.pem", "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(), backend=default_backend()
                )

            return public_key

        except Exception as e:
            print("JWT._return_public_key() error : ", e)

    @classmethod
    def encode(self, payload_data: dict) -> str:
        # add an expiration time
        payload_data["exp"] = self._return_expiration_time()

        try:
            token = jwt.encode(
                payload=payload_data,
                key=self._return_private_key(),
                algorithm="RS256",
            )

            return token

        except Exception as e:
            print("Jwt.encode() error :", e)

            return None

    @classmethod
    def decode(self, token: str) -> dict:
        """return the payload data if the token is valid"""

        if self.verify(token):
            return jwt.decode(
                token, key=self._return_public_key(), algorithms=["RS256"]
            )

    @classmethod
    def verify(self, token: str) -> bool:
        try:
            jwt.decode(token, key=self._return_public_key(), algorithms=["RS256"])

            return True

        except Exception as e:
            print("Jwt.decode() error :", e)

            return False
