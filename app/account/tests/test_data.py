class MailAccountTestData:
    @property
    def existing_mail_account(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "mail_address": "user@example.com",
            "sender_name": "string",
            "password": "account_password",
            "is_default": True,
        }

    def add_account(self, mail="example@example.com"):
        return {
            "mail_address": mail,
            "sender_name": "string",
            "password": "string",
            "is_default": False,
        }

    @property
    def update_account(self):
        return {
            "sender_name": "string",
            "password": "1234",
            "is_default": True,
        }
