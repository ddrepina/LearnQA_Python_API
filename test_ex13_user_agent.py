import pytest
import requests


class TestUserAgent:
    user_agent = [
        # 1
        (('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 '
          '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
         ({'platform': 'Mobile', 'browser': 'No', 'device': 'Android'})),
        # 2
        (('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 '
          '(KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
         ({'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'})),
        # 3
        (('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
         ({'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'})),
        # 4
        (('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
          '(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
         ({'platform': 'Web', 'browser': 'Chrome', 'device': 'No'})),
        # 5
        (('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
          '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'),
         ({'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}))
    ]

    @pytest.mark.parametrize("user_agents, expected_value", user_agent)
    def test_user_agent(self, user_agents,  expected_value):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {"User-Agent": user_agents}

        response = requests.get(url, headers=headers)

        response_json = response.json()

        assert "platform" in response_json, "'platform' not in the header"
        assert "browser" in response_json, "'browser' not in the header"
        assert "device" in response_json, "'device' not in the header"

        assert response_json['platform'] == expected_value['platform'], \
            f"expected platform = {expected_value['platform']}, actual = {response.json()['platform']}"
        assert response_json['browser'] == expected_value['browser'], \
            f"expected browser = {expected_value['browser']}, actual = {response.json()['browser']}"
        assert response_json['device'] == expected_value['device'], \
            f"expected device = {expected_value['device']}, actual = {response.json()['device']}"
