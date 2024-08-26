from django.core.files.uploadedfile import SimpleUploadedFile


class MailTemplateTestData:
    def existing_template(self, user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6"):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": user_id,
            "name": "test_template.html",
            "file_system_id": "test_template.html",
            "placeholders": [
                {
                    "key": "9K8R_3b332m9I9p5J55ryw5979d54C5C5w6",
                    "description": "string",
                    "is_sensitive": True,
                }
            ],
        }

    @property
    def add_placeholders(self):
        return [
            {
                "key": "0KQ2q2453u93Q50MA03C7Q9T11ud7g4gx2C247G13965687A5a016",
                "description": "string",
                "is_sensitive": False,
            }
        ]

    def add_template(self, file, name="new_template"):
        return {"name": name, "file": file}

    @property
    def upload_template(self):
        return self.template_file

    def update_template(self, file):
        return {"file": file}

    def template_file(self, file):
        return SimpleUploadedFile(
            content=file, name="test.html", content_type="text/html"
        )
