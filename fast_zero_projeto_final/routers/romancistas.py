from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.romancistas import Romancista
from fast_zero_projeto_final.sanitize import sanitize_nome
from fast_zero_projeto_final.schemas.romancistas import (
    RomancistaPublic,
    RomancistaSchema,
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
        user_id=conta.id,
    )
    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista
