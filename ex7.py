import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
methods = ["GET",
           "POST",
           "PUT",
           "DELETE"]


def res(num, text, status_code):
    print(f'{num} \n'
          f'text = {text} \n'
          f'status_code = {status_code}')


def check(real_method, send_param, resp_text):
    if send_param == real_method and resp_text != '{"success":"!"}':
        print(f"Запрос {real_method}, отправлен method = {send_param},"
              f" получено = {resp_text}, а должно success")
    elif send_param != real_method and resp_text != 'Wrong method provided':
        print(f"Запрос {real_method}, отправлен method = {send_param},"
              f" получено = {resp_text}, а должно 'Wrong method provided'")


# 1
# Возвращается text = Wrong method provided
# status_code = 200
response = requests.get(url)
res('# 1', response.text, response.status_code)

# 2
# text =
# status_code = 400
response = requests.head("https://playground.learnqa.ru/api/compare_query_type", data={"method": "HEAD"})
res('# 2', response.text, response.status_code)

# 3
# text = {"success":"!"}
# status_code = 200
response = requests.get("https://playground.learnqa.ru/api/compare_query_type", params={"method": "GET"})
res('# 3', response.text, response.status_code)

# 4
# Запрос DELETE, отправлен method = GET, получено = {"success":"!"}, а должно 'Wrong method provided'
for elem in methods:
    GET = requests.get("https://playground.learnqa.ru/api/compare_query_type", params={"method": elem})
    print(f"# 4 GET {elem} {GET.text} {GET.status_code}")
    check('GET', elem, GET.text)

    POST = requests.post("https://playground.learnqa.ru/api/compare_query_type", data={"method": elem})
    print(f"# 4 POST {elem} {POST.text} {POST.status_code}")
    check('POST', elem, POST.text)

    PUT = requests.put("https://playground.learnqa.ru/api/compare_query_type", data={"method": elem})
    print(f"# 4 PUT {elem} {PUT.text} {PUT.status_code}")
    check('PUT', elem, PUT.text)

    DELETE = requests.delete("https://playground.learnqa.ru/api/compare_query_type", data={"method": elem})
    print(f"# 4 DELETE {elem} {DELETE.text} {DELETE.status_code}")
    check('DELETE', elem, DELETE.text)
