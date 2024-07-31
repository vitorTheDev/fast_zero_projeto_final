from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.schemas.contas import (
    ContaPublico,
    ContaSchema,
)
from fast_zero_projeto_final.security import (
    get_conta_atual,
    get_password_hash,
)

router = APIRouter(prefix='/contas', tags=['contas'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[Conta, Depends(get_conta_atual)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ContaPublico)
def create_user(conta: ContaSchema, session: Session):
    conta_existente = session.scalar(
        select(Conta).where(
            (Conta.username == conta.username) | (Conta.email == conta.email)
        )
    )

    if conta_existente:
        if conta_existente.username == conta.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Nome de usuário já existe',
            )
        elif conta_existente.email == conta.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='E-mail já existe',
            )

    hashed_password = get_password_hash(conta.senha)

    conta_existente = Conta(
        username=conta.username, senha=hashed_password, email=conta.email
    )
    session.add(conta_existente)
    session.commit()
    session.refresh(conta_existente)

    return conta_existente
