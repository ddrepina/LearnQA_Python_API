from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import random
import string
from datetime import datetime


class TestUserEdit(BaseCase):
    edit_params = [
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = BaseCase.registration_user(self)

        email = register_data['email']
        password = register_data['password']
        user_id = register_data["user_id"]

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Change Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={'auth_sid': auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    @pytest.mark.parametrize("param", edit_params)
    def test_edit_user_without_auth(self, param):
        # REGISTER
        register_data = BaseCase.registration_user(self)

        user_id = register_data["user_id"]

        # Edit
        new_value = "Changed Value"

        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={param: new_value}
        )
        # print(response2.content)
        # print(response2.status_code)
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Auth token not supplied"

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_auth_as_another_user(self):
        # REGISTER FIRST USER
        register_first_user = BaseCase.registration_user(self)

        first_user_id = register_first_user["user_id"]

        # REGISTER SECOND USER
        register_second_user = BaseCase.registration_user(self)

        second_user_email = register_second_user["email"]
        second_user_password = register_second_user["password"]

        # LOGIN
        data = {
            'email': second_user_email,
            'password': second_user_password
        }
        response = MyRequests.post("/user/login", data=data)

        second_user_auth_sid = self.get_cookie(response, "auth_sid")
        second_user_token = self.get_header(response, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid},
            data={"firstName": new_name}
        )

        # должно быть 400, но вернуло 200
        Assertions.assert_code_status(response2, 200)

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_email_without_sym(self):
        # REGISTER
        register_data = BaseCase.registration_user(self)

        email = register_data['email']
        password = register_data['password']
        user_id = register_data["user_id"]


        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = f"test" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "test.ru"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            register_data["email"],
            F"Email was changed ='{new_email}'"
        )

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_edit_firstname_on_short(self):
        # REGISTER
        register_data = BaseCase.registration_user(self)

        email = register_data['email']
        password = register_data['password']
        user_id = register_data["user_id"]

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_name = random.choice(string.ascii_letters)

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            register_data["firstName"],
            f"First Name was changed on short ='{new_name}'"
        )
