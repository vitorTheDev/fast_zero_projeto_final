from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
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
    LivroUpdate,
)
from fast_zero_projeto_final.schemas.mensagem import Mensagem
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


@router.get('/{livro_id}', response_model=LivroPublic)
def read_livro(
    livro_id: int,
    session: Session,
    conta: ContaAtual,
):
    livro_existente = session.scalar(
        select(Livro).where(
            (Livro.conta_id == conta.id) | (Livro.id == livro_id)
        )
    )

    if not livro_existente:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    return livro_existente


@router.patch('/{livro_id}', response_model=LivroPublic)
def patch_livro(
    livro_id: int,
    session: Session,
    conta: ContaAtual,
    livro: LivroUpdate,
):
    livro_existente = session.scalar(
        select(Livro).where(
            (Livro.conta_id == conta.id) | (Livro.id == livro_id)
        )
    )

    if not livro_existente:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    checarRomancista(session, conta, livro.romancista_id)
    for key, value in livro.model_dump(exclude_unset=True).items():
        if key == 'titulo':
            setattr(livro_existente, key, sanitize_nome(value))
        else:
            setattr(livro_existente, key, value)

    session.add(livro_existente)
    session.commit()
    session.refresh(livro_existente)

    return livro_existente


@router.delete('/{livro_id}', response_model=Mensagem)
def delete_livro(livro_id: int, session: Session, conta: ContaAtual):
    livro_existente = session.scalar(
        select(Livro).where(
            (Livro.conta_id == conta.id) | (Livro.id == livro_id)
        )
    )

    if not livro_existente:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    session.delete(livro_existente)
    session.commit()

    return {'message': 'Livro deletado no MADR'}
