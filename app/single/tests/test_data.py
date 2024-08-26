class SingleMailTestData:
    @property
    def existing_mail(self):
        return {
            "id": "c245370c-2442-45d9-843e-02e20f499b8b",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender": "user@example.com",
            "name": "string",
            "recipient": "example@test.com",
            "subject": "string",
            "html_body": "string",
            "text_body": "string",
            "is_scheduled": True,
        }

    def send_mail(self, sender):
        return {
            "sender": sender,
            "name": "string",
            "recipient": "example@test.com",
            "subject": "string",
            "html_body": "string",
            "text_body": "string",
        }

    def send_email_with_template(self, sender, template_id):
        return {
            "sender": sender,
            "name": "string",
            "recipient": "user@example.com",
            "subject": "string",
            "template_id": template_id,
        }

    @property
    def mail_task(self):
        return {
            "sender": "example@test.com",
            "sender_name": "example",
            "password": "password",
            "recipients": "test@example.com",
            "subject": "testing",
            "html_body": "html",
            "text_body": "",
            "report_id": "report_id",
            "single_mail_id": "single_mail_id",
        }
