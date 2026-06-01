from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.produto_model import Peca
import repositories.produto_repository as repo

def criar_produto(dados, db: Session) -> Peca:
    novo_produto = Peca(
        nome=dados.nome,
        descricao=dados.descricao,
        quantidade_estoque=dados.quantidade_estoque,
        preco=dados.preco
    )
    return repo.salvar(novo_produto, db)

def listar_produtos(db: Session):
    return repo.listar_todos(db)

def buscar_produto(produto_id: int, db: Session) -> Peca:
    produto = repo.buscar_por_id(produto_id, db)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto/Peça não encontrado")
    return produto