from urllib.parse import urlencode

from django.test import tag
from django.urls import reverse
from rest_framework import status

from .base_test_case import MailAccountTestCase


@tag("app.account.view")
class TestAccountView(MailAccountTestCase):
    def test_view_all_accounts(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        query_params = {"page": 1, "page_size": 1}
        response = self.client.get(
            f"{reverse('view_all_accounts')}?{urlencode(query_params)}",
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)
        self.assertIn("count", response_data)
        self.assertIn("next", response_data)
        self.assertIn("previous", response_data)
        self.assertIsInstance(response_data.get("results"), list)
        self.assertEqual(
            len(response_data.get("results")), query_params.get("page_size")
        )

    def test_get_all_account_unauthorized_exc(self):
        response = self.client.get(
            f"{reverse('view_all_accounts')}?{urlencode({'page': 1, 'page_size': 1})}"
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_get_account(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.get(
            reverse(
                "get_account",
                kwargs={"account_id": self.mail_account_model.id},
            ),
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)

    def test_get_account_unauthorized_exc(self):
        response = self.client.get(
            reverse(
                "get_account",
                kwargs={"account_id": self.mail_account_model.id},
            )
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_add_account(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.post(
            reverse("add_account"),
            data=self.mail_account_test_data.add_account(),
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response_data, dict)

    def test_add_account_invalid_data_exc(self):
        response = self.client.post(
            reverse("add_account"),
            data=self.mail_account_test_data.add_account(mail="invalid"),
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(response_data, dict)

    def test_add_account_unauthorize_exc(self):
        response = self.client.post(
            reverse("add_account"),
            data=self.mail_account_test_data.add_account(),
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_update_account(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.patch(
            reverse(
                "update_account", kwargs={"account_id": self.mail_account_model.id}
            ),
            data=self.mail_account_test_data.update_account,
            format=self.data_format,
            headers=self.headers,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_data, dict)

    def test_update_account_unauthorize_exc(self):
        response = self.client.post(
            reverse(
                "update_account", kwargs={"account_id": self.mail_account_model.id}
            ),
            data=self.mail_account_test_data.update_account,
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)

    def test_delete_account(self):
        self.jwt_decode.return_value = self.mock_decode_token()
        response = self.client.delete(
            reverse(
                "delete_account", kwargs={"account_id": self.mail_account_model.id}
            ),
            format=self.data_format,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_account_unauthorize_exc(self):
        response = self.client.delete(
            reverse(
                "delete_account", kwargs={"account_id": self.mail_account_model.id}
            ),
            format=self.data_format,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsInstance(response_data, dict)
