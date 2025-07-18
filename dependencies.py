from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError

#função dedicada p/ criar sessão com db de forma desacoplada, que é enviada p/ rota via Depends
def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)  #instância de classe, conexão ao banco
        session = Session()  #instância p/ criar sessão com db
        yield session  #retorna um valor sem encerrar a execução da função
    finally: 
        session.close() #fecha sessão independente do êxito do try

#movida p/ cá p/ virar dependência
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    #verificar se o token é válido e extrair o id de usuario do token
    try:
        dic_info = jwt.decode(token,SECRET_KEY,ALGORITHM) #decode do token recebido
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique validade do token")
    usuario = session.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario