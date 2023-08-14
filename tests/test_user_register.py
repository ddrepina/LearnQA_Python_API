from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import string
import pytest
import random


class TestUserRegister(BaseCase):
    exclude_params = [
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email"),
        ("password")
    ]

    def test_create_user_successfuly(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    # Создание с уже существующей почтой
    def test_crete_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    # Создание пользователя с некорректным email - без символа @
    def test_create_user_with_email_without_sym(self):
        email = f"test" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "test.ru"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить,
    # что отсутствие любого параметра не дает зарегистрировать пользователя
    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_param(self, condition):
        data = self.prepare_registration_data()
        self.data = data.pop(condition)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"User registered without param '{condition}'"

    # Создание пользователя с очень коротким именем в один символ
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = random.choice(string.ascii_letters)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short",\
            f"User registerd with short First name = {data['firstName']}"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = ''.join(random.choices(string.ascii_lowercase, k=255))

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long",\
            f"User registerd with long First name = {data['firstName']}"
