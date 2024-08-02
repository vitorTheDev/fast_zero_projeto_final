from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.livros import Livro
from fast_zero_projeto_final.romancistas.checar_romancista import (
    checarRomancista,
)
from fast_zero_projeto_final.sanitize import sanitize_nome
from fast_zero_projeto_final.schemas.livros import (
    LivroList,
    LivroPublic,
    LivroSchema,
)
from fast_zero_projeto_final.security import get_conta_atual

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
ContaAtual = Annotated[Conta, Depends(get_conta_atual)]

router = APIRouter(prefix='/livros', tags=['livros'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=LivroPublic)
def create_livro(
    livro: LivroSchema,
    conta: ContaAtual,
    session: Session,
):
    checarRomancista(session, conta, livro.romancista_id)
    db_livro = Livro(
        titulo=sanitize_nome(livro.titulo),
        ano=livro.ano,
        romancista_id=livro.romancista_id,
        conta_id=conta.id,
    )
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.get('/', response_model=LivroList)
def list_livros(  # noqa
    session: Session,
    conta: ContaAtual,
    titulo: str = Query(None),
    ano: int = Query(None),
    romancista_id: int = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Livro).where(Livro.conta_id == conta.id)

    if titulo:
        query = query.filter(Livro.titulo.contains(titulo))

    if ano:
        query = query.filter(Livro.ano == ano)

    if romancista_id:
        query = query.filter(Livro.romancista_id == romancista_id)

    livros = session.scalars(query.offset(offset).limit(limit)).all()

    return {'livros': livros}
