from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

#função auxiliar p/ criar token
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}  #informações que serão codificadas
    jwt_codif = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codif

#processo p/ autenticar informações recebidas de login
def autenticar_usuario(email, senha, session):
    usuario = session.query(User).filter(User.email == email).first()
    #verifica se a senha recebido é igual a hash armazenada
    if not usuario: #se nao existir usuario com email passado
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): #compara senha recebida com a armazenada
        return False
    return usuario


@auth_router.get("/")
async def autenticar():
    return {"mensagem":"autenticação solicitada", "autenticação":False}

@auth_router.post("/create_user")
async def criar_conta(user_schema = UserSchema, session: Session = Depends(pegar_sessao)): #depends faz injeção de dependência, iniciando no parâmetro da rota
    usuario = session.query(User).filter(User.email == user_schema.email).first() #verifica o primeiro item no db
    if usuario:
        #retorna usuário com esse email já cadastrado
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(user_schema.senha)
        novo_usuario = User(user_schema.nome, user_schema.email, senha_criptografada, user_schema.ativo, user_schema.admin)
        session.add(novo_usuario)
        session.commit()  #salva alterações
        return {"mensagem": f"usuário cadastrado com sucesso {user_schema.email}"}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        } #jwt do tipo bearer
    
#p/ fazer validação via formulário authorization da documentação
@auth_router.post("/login-form")
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

#gera o refresh token
@auth_router.get("/refresh")
async def use_refresh_token(token, usuario: User = Depends(verificar_token)):
    #verifica o token via param. com instância que injeta dependência
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }