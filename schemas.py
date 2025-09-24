from pydantic import BaseModel
from typing import Optional, List

#objeto p/ padronizar forma de enviar e receber informações
class UserSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True 
        #p/ ser considerado um ORM, se relacionar ao modelo

class OrderSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class OrderItensSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unit: float

    class Config:
        from_attributes = True

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[OrderItensSchema] #lista com referência a outro schema

    class Config:
        from_attributes = True