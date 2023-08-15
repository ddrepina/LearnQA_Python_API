import json
from requests import Response
from datetime import datetime
from lib.my_requests import MyRequests
from lib.assertions import Assertions


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecoder:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "bk.ru"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S%f")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def registration_user(self, email=None):
        register_data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        return {
            'user_id': self.get_json_value(response, "id"),
            'username': register_data['username'],
            'password': register_data["password"],
            'email': register_data["email"],
            'firstName': register_data["firstName"],
            'lastName': register_data['lastName']
        }
