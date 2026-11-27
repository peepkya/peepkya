import unittest

from src.core.security import DecryptionError, FieldEncryptor
from cryptography.fernet import Fernet


class FieldEncryptorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = "MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA="
        self.encryptor = FieldEncryptor(self.key)

    def test_round_trips_sensitive_text(self) -> None:
        encrypted = self.encryptor.encrypt("private caregiver contact")

        self.assertNotEqual(encrypted, "private caregiver contact")
        self.assertEqual(self.encryptor.decrypt(encrypted), "private caregiver contact")

    def test_ciphertext_cannot_be_decrypted_with_a_different_key(self) -> None:
        encrypted = self.encryptor.encrypt("private health information")
        other_encryptor = FieldEncryptor(
            "MDEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA="
        )

        with self.assertRaises(DecryptionError):
            other_encryptor.decrypt(encrypted)

    def test_invalid_key_fails_instead_of_using_plaintext(self) -> None:
        with self.assertRaises(ValueError):
            FieldEncryptor("not-a-fernet-key")

    def test_generated_fernet_key_is_accepted(self) -> None:
        encryptor = FieldEncryptor(Fernet.generate_key())

        self.assertEqual(encryptor.decrypt(encryptor.encrypt("check")), "check")


if __name__ == "__main__":
    unittest.main()
