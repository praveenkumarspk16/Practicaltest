import math
import time
from unittest.mock import patch

from django.test.utils import override_settings
from rest_framework import status

from rest_registration.api.views.reset_password import ResetPasswordSigner

from .base import APIViewTestCase

RESET_PASSWORD_VERIFICATION_URL = '/reset-password/'
REST_REGISTRATION_WITH_RESET_PASSWORD = {
    'RESET_PASSWORD_VERIFICATION_URL': RESET_PASSWORD_VERIFICATION_URL,
    'VERIFICATION_FROM_EMAIL': 'no-reply@example.com',
}


@override_settings(
    REST_REGISTRATION=REST_REGISTRATION_WITH_RESET_PASSWORD,
)
class BaseResetPasswordViewTestCase(APIViewTestCase):
    pass


class SendResetPasswordLinkViewTestCase(BaseResetPasswordViewTestCase):
    VIEW_NAME = 'send-reset-password-link'

    def test_send_link_ok(self):
        user = self.create_test_user(username='testusername')
        request = self.create_post_request({
            'login': user.username,
        })
        time_before = math.floor(time.time())
        with self.assert_one_mail_sent() as sent_emails:
            response = self.view_func(request)
            time_after = math.ceil(time.time())
            self.assert_valid_response(response, status.HTTP_200_OK)
        sent_email = sent_emails[0]
        self.assertEqual(
            sent_email.from_email,
            REST_REGISTRATION_WITH_RESET_PASSWORD['VERIFICATION_FROM_EMAIL'],
        )
        self.assertListEqual(sent_email.to, [user.email])
        url = self.assert_one_url_line_in_text(sent_email.body)
        verification_data = self.assert_valid_verification_url(
            url,
            expected_path=RESET_PASSWORD_VERIFICATION_URL,
            expected_query_keys={'signature', 'user_id', 'timestamp'},
        )
        self.assertEqual(int(verification_data['user_id']), user.id)
        url_sig_timestamp = int(verification_data['timestamp'])
        self.assertGreaterEqual(url_sig_timestamp, time_before)
        self.assertLessEqual(url_sig_timestamp, time_after)
        signer = ResetPasswordSigner(verification_data)
        signer.verify()

    def test_send_link_inactive_user(self):
        user = self.create_test_user(username='testusername', is_active=False)
        request = self.create_post_request({
            'login': user.username,
        })
        with self.assert_no_mail_sent():
            response = self.view_func(request)
            self.assert_response_is_not_found(response)

    def test_send_link_invalid_login(self):
        user = self.create_test_user(username='testusername')
        request = self.create_post_request({
            'login': user.username + 'b',
        })
        with self.assert_mails_sent(0):
            response = self.view_func(request)
            self.assert_response_is_not_found(response)


class ResetPasswordViewTestCase(BaseResetPasswordViewTestCase):
    VIEW_NAME = 'reset-password'

    def test_reset_ok(self):
        old_password = 'password1'
        new_password = 'eaWrivtig5'
        user = self.create_test_user(password=old_password)
        signer = ResetPasswordSigner({'user_id': user.pk})
        data = signer.get_signed_data()
        data['password'] = new_password
        request = self.create_post_request(data)
        response = self.view_func(request)
        self.assert_response_is_ok(response)
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))

    def test_reset_inactive_user(self):
        old_password = 'password1'
        new_password = 'eaWrivtig5'
        user = self.create_test_user(password=old_password, is_active=False)
        signer = ResetPasswordSigner({'user_id': user.pk})
        data = signer.get_signed_data()
        data['password'] = new_password
        request = self.create_post_request(data)
        response = self.view_func(request)
        self.assert_response_is_not_found(response)
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))

    def test_reset_short_password(self):
        old_password = 'password1'
        new_password = 'c'
        user = self.create_test_user(password=old_password)
        signer = ResetPasswordSigner({'user_id': user.pk})
        data = signer.get_signed_data()
        data['password'] = new_password
        request = self.create_post_request(data)
        response = self.view_func(request)
        self.assert_response_is_bad_request(response)
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))

    def test_reset_numeric_password(self):
        old_password = 'password1'
        new_password = '563495763456'
        user = self.create_test_user(password=old_password)
        signer = ResetPasswordSigner({'user_id': user.pk})
        data = signer.get_signed_data()
        data['password'] = new_password
        request = self.create_post_request(data)
        response = self.view_func(request)
        self.assert_response_is_bad_request(response)
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))

    def test_reset_password_same_as_username(self):
        username = 'albert.einstein'
        old_password = 'password1'
        new_password = username
        user = self.create_test_user(username=username, password=old_password)
        signer = ResetPasswordSigner({'user_id': user.pk})
        data = signer.get_signed_data()
        data['password'] = new_password
        request = self.create_post_request(data)
        response = self.view_func(request)
        self.assert_response_is_bad_request(response)
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))

    def test_reset_tampered_timestamp(self):
        old_password = 'password1'
        new_password = 'eaWrivtig5'
        user = self.create_test_user(password=old_password)
        signer = ResetPasswordSigner({'user_id': user.pk})
        data = signer.get_signed_data()
        data['timestamp'] += 1
        data['password'] = new_password
        request = self.create_post_request(data)
        response = self.view_func(request)
        self.assert_invalid_response(response, status.HTTP_400_BAD_REQUEST)
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))

    def test_reset_expired(self):
        timestamp = int(time.time())
        old_password = 'password1'
        new_password = 'eaWrivtig5'
        user = self.create_test_user(password=old_password)
        with patch('time.time',
                   side_effect=lambda: timestamp):
            signer = ResetPasswordSigner({'user_id': user.pk})
            data = signer.get_signed_data()
        data['password'] = new_password
        request = self.create_post_request(data)
        with patch('time.time',
                   side_effect=lambda: timestamp + 3600 * 24 * 8):
            response = self.view_func(request)
        self.assert_invalid_response(response, status.HTTP_400_BAD_REQUEST)
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))
