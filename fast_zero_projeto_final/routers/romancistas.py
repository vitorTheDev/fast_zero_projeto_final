from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.romancistas import Romancista
from fast_zero_projeto_final.romancistas.checar_romancista import (
    checarRomancista,
)
from fast_zero_projeto_final.sanitize import sanitize_nome
from fast_zero_projeto_final.schemas.mensagem import Mensagem
from fast_zero_projeto_final.schemas.romancistas import (
    RomancistaList,
    RomancistaPublic,
    RomancistaSchema,
    RomancistaUpdate,
)
from fast_zero_projeto_final.security import get_conta_atual

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
ContaAtual = Annotated[Conta, Depends(get_conta_atual)]

router = APIRouter(prefix='/romancistas', tags=['romancistas'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=RomancistaPublic
)
def create_romancista(
    romancista: RomancistaSchema,
    conta: ContaAtual,
    session: Session,
):
    db_romancista = Romancista(
        nome=sanitize_nome(romancista.nome),
        conta_id=conta.id,
    )
    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.get('/', response_model=RomancistaList)
def list_romancistas(  # noqa
    session: Session,
    conta: ContaAtual,
    nome: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Romancista).where(Romancista.conta_id == conta.id)

    if nome:
        query = query.filter(Romancista.nome.contains(nome))

    romancistas = session.scalars(query.offset(offset).limit(limit)).all()

    return {'romancistas': romancistas}


@router.patch('/{romancista_id}', response_model=RomancistaPublic)
def patch_romancista(
    romancista_id: int,
    session: Session,
    conta: ContaAtual,
    romancista: RomancistaUpdate,
):
    romancista_existente = checarRomancista(session, conta, romancista_id)

    for key, value in romancista.model_dump(exclude_unset=True).items():
        setattr(romancista_existente, key, value)

    session.add(romancista_existente)
    session.commit()
    session.refresh(romancista_existente)

    return romancista_existente


@router.delete('/{romancista_id}', response_model=Mensagem)
def delete_romancista(romancista_id: int, session: Session, conta: ContaAtual):
    romancista = checarRomancista(session, conta, romancista_id)

    session.delete(romancista)
    session.commit()

    return {'message': 'Livro deletado no MADR'}
