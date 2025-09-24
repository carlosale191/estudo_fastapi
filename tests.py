import requests

#usar refresh token gerado quando usuario realiza login
headers = {
    "Authorization": "ahuyba786dabd86a5vdba865dvad786and"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())