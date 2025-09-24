from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import OrderSchema, OrderItensSchema, ResponseOrderSchema
from models import Order, User, OrderItens
from typing import List

order_router = APIRouter(prefix="/orders", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")  #mapeia o endpoint pós prefixo (se não houver é apenas /)
async def pedidos():
    """
    Essa é a rota padrão de pedidos.
    """
    return {"mensagem":"acessou ae"}

@order_router.post("/pedido")
async def criar_pedido(order_schema: OrderSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Order(usuario = order_schema.id_usuario)
    #adiciona a sessão, commita no db e retorna mensagem
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: User = Depends(verificar_token)):
    pedido = session.query(Order).filter(Order.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    #apenas pode deletar o pedido se for admin e user vinculado ao pedido(ambos com token previamente verificado)
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não é autorizado para fazer essa operação")

    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número {id_pedido} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: User = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para essa ação")
    else:
        pedidos = session.query(Order).all()
        return {
            "pedidos": pedidos
        }

@order_router.post("/pedido/adicionar-item/{id_pedido}") #id do pedido já passado via parametro
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: OrderItensSchema, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: User = Depends(verificar_token)):
    pedido = session.query(Order).filter(Order.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    #se usuario não for admin e id do usuario for diferente do usuario dono do pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não é autorizado para fazer essa operação")
    item_pedido = OrderItens(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unit, id_pedido)
    pedido.calcular_preco()
    session.add(item_pedido)
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_unitario": item_pedido.preco_unit
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                                session: Session = Depends(pegar_sessao), 
                                usuario: User = Depends(verificar_token)):
    item_pedido = session.query(OrderItens).filter(OrderItens.id==id_item_pedido).first()
    pedido = session.query(Order).filter(Order.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no Pedido não existente")
    #se usuario não for admin e id do usuario for diferente do usuario dono do pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não é autorizado para fazer essa operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int,
                            session: Session = Depends(pegar_sessao), 
                            usuario: User = Depends(verificar_token)):
    pedido = session.query(Order).filter(Order.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Item no Pedido não existente")
    #se usuario não for admin e id do usuario for diferente do usuario dono do pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não é autorizado para fazer essa operação")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido número {pedido.id} finalizado com sucesso",
        "pedido": pedido
    }

#visualiza um pedido
@order_router.post("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int,
                            session: Session = Depends(pegar_sessao), 
                            usuario: User = Depends(verificar_token)):
    pedido = session.query(Order).filter(Order.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Item no Pedido não existente")
    #se usuario não for admin e id do usuario for diferente do usuario dono do pedido
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não é autorizado para fazer essa operação")
    return {
     "quantidade_itens_pedido": len(pedido.itens),
     "pedido": pedido
    }

#listar todos pedidos de um usuário
@order_router.get("listar/pedidos-usuario", response_model=List(ResponseOrderSchema))
async def listar_pedidos(session: Session = Depends(pegar_sessao), 
                        usuario: User = Depends(verificar_token)):
    pedidos = session.query(Order).filter(Order.usuario==usuario.id).all()
    return pedidos
    #agora ao invés de retornar um dicionário, retorna um objeto seguindo o padrão do schema de saída
