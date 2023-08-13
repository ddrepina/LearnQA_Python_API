import requests


def test_cookie():
    response = requests.post("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    assert response.cookies["HomeWork"] == 'hw_value', f"cookie NOT HomeWork=hw_value for .playground.learnqa.ru"
