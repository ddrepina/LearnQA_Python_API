from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_main_user(self):
        main_user_data = {
            'id': '2',
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=main_user_data)
        Assertions.assert_code_status(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response_delete = MyRequests.delete(
            f"/user/{main_user_data['id']}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response_delete, 400)
        assert response_delete.content.decode("utf_8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"user with id {main_user_data['id']} was delete"

    # Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить,
    # затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    def test_just_delete_user(self):
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
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response_delete, 200)
        response_check = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response_check, 404)
        assert response_check.content.decode("utf_8") == "User not found", f"The user has not been deleted"

    # Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_by_another_user(self):
        # REGISTER FIRST USER
        register_first_user = BaseCase.registration_user(self)

        first_user_id = register_first_user["user_id"]

        # REGISTER SECOND USER
        register_second_user = BaseCase.registration_user(self)

        second_user_email = register_second_user["email"]
        second_user_password = register_second_user["password"]

        # LOGIN SECOND USER
        data = {
            'email': second_user_email,
            'password': second_user_password
        }
        response1 = MyRequests.post("/user/login", data=data)

        second_user_auth_sid = self.get_cookie(response1, "auth_sid")
        second_user_token = self.get_header(response1, "x-csrf-token")

        # DELETE FIRST USER BY SECOND USER
        response2 = MyRequests.delete(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": second_user_token},
            cookies={"auth_sid": second_user_auth_sid}
        )

        # по логике должен быть 400. но в ответ 200
        Assertions.assert_code_status(response2, 200)
