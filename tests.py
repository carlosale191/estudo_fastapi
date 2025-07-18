import requests

#usar refresh token gerado quando usuario realiza login
headers = {
    "Authorization": "Bearer -inserir token-"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())