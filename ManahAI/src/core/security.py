from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken


class DecryptionError(Exception):
    """Raised when ciphertext cannot be authenticated and decrypted."""


class FieldEncryptor:
    """Encrypts sensitive UTF-8 fields with an explicitly configured Fernet key."""

    def __init__(self, key: str | bytes) -> None:
        encoded_key = key.encode("ascii") if isinstance(key, str) else key
        self._fernet = Fernet(encoded_key)

    def encrypt(self, plaintext: str) -> str:
        if not isinstance(plaintext, str):
            raise TypeError("Sensitive field values must be text.")
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("ascii")

    def decrypt(self, ciphertext: str) -> str:
        if not isinstance(ciphertext, str):
            raise TypeError("Encrypted field values must be text.")
        try:
            return self._fernet.decrypt(ciphertext.encode("ascii")).decode("utf-8")
        except (InvalidToken, UnicodeEncodeError, UnicodeDecodeError) as error:
            raise DecryptionError("Encrypted field could not be authenticated.") from error
