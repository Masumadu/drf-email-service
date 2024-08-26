class BulkMailTestData:
    @property
    def existing_mail(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender": "user@example.com",
            "name": "string",
            "recipients": ["example@test.com"],
            "subject": "string",
            "html_body": "string",
            "text_body": "string",
            "is_scheduled": True,
        }

    def send_mail(self, sender):
        return {
            "sender": sender,
            "name": "string",
            "recipients": ["example@test.com"],
            "subject": "string",
            "html_body": "string",
            "text_body": "string",
        }

    def consumer_send_mail(self, sender):
        return {
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sender": sender,
            "name": "string",
            "recipients": ["example@test.com"],
            "subject": "string",
            "html_body": "string",
            "text_body": "string",
        }

    def send_email_with_template(self, sender, template_id):
        return {
            "sender": sender,
            "name": "string",
            "recipients": ["user@example.com"],
            "subject": "string",
            "template_id": template_id,
        }

    @property
    def mail_task(self):
        return {
            "sender": "example@test.com",
            "sender_name": "example",
            "password": "password",
            "recipients": ["test@example.com"],
            "subject": "testing",
            "html_body": "html",
            "text_body": "",
            "delivery_id": "report_id",
            "mail_id": "single_mail_id",
        }
