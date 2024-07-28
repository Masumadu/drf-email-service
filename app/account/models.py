import base64
import uuid

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.db import models

from core.models import BaseModel

# Create your models here.


class MailAccountModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    user_id = models.UUIDField(null=False, db_index=True)
    mail_address = models.EmailField(null=False, unique=True, db_index=True)
    sender_name = models.CharField(null=False)
    _password = models.CharField(db_column="password", null=False)
    is_default = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "mail_accounts"
        ordering = ["created_at"]

    def __str__(self):
        return self.sender_name or self.mail_address

    def __repr__(self):
        return self.sender_name or self.mail_address

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # reminder: generate a key for encrypting password
        key = MailAccountModel.generate_key_from_string(passkey=str(self.mail_address))
        # reminder: encrypt password
        self._password = MailAccountModel.encrypt_text(key=key, text=value)

    # noinspection PyMethodMayBeStatic
    @staticmethod
    def generate_key_from_string(passkey):
        # reminder: generate a passphrase and salt for encryption key
        passphrase = passkey.encode("utf-8").lower()[::-1]
        salt = passkey.encode("utf-8").upper()
        # reminder: derive the key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(passphrase)
        # reminder: return a url-safe base64-encoded key as a string
        return base64.urlsafe_b64encode(key).decode("utf-8")

    # noinspection PyMethodMayBeStatic
    @staticmethod
    def encrypt_text(key: str, text: str):
        cipher_suite = Fernet(key)
        raw_encryption = cipher_suite.encrypt(text.encode("utf-8"))
        return base64.urlsafe_b64encode(raw_encryption).decode("utf-8")

    @staticmethod
    def decrypt_text(passkey: str, encrypted_text: str):
        # reminder: generate key for decrypting text
        key = MailAccountModel.generate_key_from_string(passkey=passkey)
        cipher_suite = Fernet(key)
        convert_to_byte = base64.urlsafe_b64decode(encrypted_text.encode("utf-8"))
        return cipher_suite.decrypt(convert_to_byte).decode("utf-8")
