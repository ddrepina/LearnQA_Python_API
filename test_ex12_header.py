import requests


def test_header():
    response = requests.post("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    assert response.headers["x-secret-homework-header"] == 'Some secret value', \
        f"header NOT x-secret-homework-header != Some secret value"
