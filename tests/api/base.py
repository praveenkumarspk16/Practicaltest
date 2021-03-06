from urllib.parse import parse_qs, urlparse

from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import resolve
from rest_framework import status
from rest_framework.test import APIRequestFactory

from tests.utils import BaseViewTestCase


class APIViewTestCase(BaseViewTestCase):
    APP_NAME = 'rest_registration'

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self._view_func = None

    def view_func(self, *args, **kwargs):
        if self._view_func is None:
            match = resolve(self.view_url)
            self._view_func = match.func
        return self._view_func(*args, **kwargs)

    def create_post_request(self, data=None):
        return self.factory.post(self.view_url, data)

    def create_patch_request(self, data=None):
        return self.factory.patch(self.view_url, data)

    def create_get_request(self):
        return self.factory.get(self.view_url)

    def add_session_to_request(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

    def assert_response(
            self, response, expected_valid_response=True,
            expected_status_code=None):
        status_code = response.status_code
        msg_format = "Response returned with code {status_code}, body {response.data}"  # noqa: E501
        msg = msg_format.format(
            status_code=status_code,
            response=response,
        )
        if expected_status_code is not None:
            self.assertEqual(status_code, expected_status_code, msg=msg)
        elif expected_valid_response:
            self.assert_is_between(status_code, 200, 400, msg=msg)
        else:
            self.assert_is_not_between(status_code, 200, 400, msg=msg)

    def assert_valid_response(self, response, expected_status_code=None):
        self.assert_response(
            response,
            expected_valid_response=True,
            expected_status_code=expected_status_code)

    def assert_invalid_response(self, response, expected_status_code=None):
        self.assert_response(
            response,
            expected_valid_response=False,
            expected_status_code=expected_status_code)

    def assert_response_is_ok(self, response):
        self.assert_valid_response(
            response,
            expected_status_code=status.HTTP_200_OK,
        )

    def assert_response_is_bad_request(self, response):
        self.assert_invalid_response(
            response,
            expected_status_code=status.HTTP_400_BAD_REQUEST,
        )

    def assert_response_is_not_found(self, response):
        self.assert_invalid_response(
            response,
            expected_status_code=status.HTTP_404_NOT_FOUND,
        )

    def assert_valid_verification_url(
            self, url, expected_path=None, expected_query_keys=None):
        parsed_url = urlparse(url)
        if expected_path is not None:
            self.assertEqual(parsed_url.path, expected_path)
        query = parse_qs(parsed_url.query, strict_parsing=True)
        if expected_query_keys is not None:
            self.assertSetEqual(set(query), set(expected_query_keys))

        for values in query.values():
            self.assert_len_equals(values, 1)

        verification_data = {key: values[0] for key, values in query.items()}
        return verification_data
