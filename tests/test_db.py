from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta


def test_get_session():
    session = next(get_session())
    assert session is not None
    assert isinstance(session, Session)


def test_create_conta(session):
    new_conta = Conta(username='alice', senha='secret', email='teste@test')
    session.add(new_conta)
    session.commit()

    conta = session.scalar(select(Conta).where(Conta.username == 'alice'))

    assert conta.username == 'alice'
    assert conta.email == 'teste@test'
