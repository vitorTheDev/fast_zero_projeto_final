from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.schemas.token import Token
from fast_zero_projeto_final.security import (
    create_access_token,
    get_conta_atual,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2Form,
    session: Session,
):
    user = session.scalar(
        select(Conta).where(Conta.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='E-mail ou senha incorretos',
        )

    if not verify_password(form_data.password, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='E-mail ou senha incorretos',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    conta: Conta = Depends(get_conta_atual),
):
    new_access_token = create_access_token(data={'sub': conta.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
