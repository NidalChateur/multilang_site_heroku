from cryptography.fernet import Fernet
from django.conf import settings


class Encryptor:
    # FERNET_KEY = settings.FERNET_KEY

    @classmethod
    def _cipher(self) -> Fernet:
        return Fernet(settings.FERNET_KEY)

    @staticmethod
    def generate_key() -> str:
        """Generate a key once and store it securely"""

        return Fernet.generate_key().decode()

    @classmethod
    def encrypt(self, clear_str: str) -> str:
        # Encrypt the string
        return self._cipher().encrypt(clear_str.encode()).decode()

    @classmethod
    def decrypt(self, encrypted_str: str) -> str:
        # Decrypt the string
        return self._cipher().decrypt(encrypted_str.encode()).decode()
