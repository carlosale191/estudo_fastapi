from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()  #carrega variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY") #procura arquivo env
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form") 
#criada dependência p/ token bearer ser enviado como header da requisição

from routes.auth_routes import auth_router
from routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

#uvicorn = servidor p/ aplicações assíncronas
#executar no terminal p/ rodar o site: uvicorn main:app --reload