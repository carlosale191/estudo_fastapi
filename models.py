from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#cria conexão
db = create_engine("sqlite:///banco.db")

#cria base do db
Base = declarative_base()

#criar classes/tabelas do banco
class User(Base):
    __tablename__ = "usuarios"

    #definição colunas da tabela, nome, tipo e outros incrementos
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    #construtor. o self indica a própria classe
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Order(Base):
    __tablename__ = "pedidos"

    # restringido para evitar erro de compatibilidade, restringir depois com schemas
    # STATUS_PEDIDOS = (
    #     ("PENDENTE","PENDENTE"),
    #     ("CANCELADO","CANCELADO"),
    #     ("FINALIZADO","FINALIZADO")
    # ) #no valor é possível escrever outro texto com mais detalhes

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #poderia colocar default="PENDENTE" mas já está assim no init
    usuario = Column("usuario", ForeignKey("usuarios.id")) #vinculo com outra tabela
    preco = Column("preco", Float)
    #item =

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

class OrderItens(Base):
    __tablename__ = "pedido_itens"

    id = id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unit = Column("preco_unit", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    
    def __init__(self, quantidade, sabor, tamanho, preco_unit, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unit = preco_unit
        self.pedido = pedido


#executa criação dos metadados do banco (cria efetivamente o db)
# criar nova migration/versão db: alembic revision --autogenerate -m "initial migration"
# executa mudanças no db após gerar migration: alembic upgrade head