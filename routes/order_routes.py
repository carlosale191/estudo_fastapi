from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import OrderSchema
from models import Order

order_router = APIRouter(prefix="/orders", tags=["pedidos"])

@order_router.get("/")  #mapeia o endpoint pós prefixo (se não houver é apenas /)
async def pedidos():
    """
    Essa é a rota padrão de pedidos.
    """
    return {"mensagem":"acessou ae"}

@order_router.post("/pedido")
async def criar_pedido(order_schema: OrderSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Order(usuario = order_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}