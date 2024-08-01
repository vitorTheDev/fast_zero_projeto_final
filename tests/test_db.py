from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.livros import Livro
from fast_zero_projeto_final.models.romancistas import Romancista


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


def test_create_romancista(session, user):
    new_romancista = Romancista(nome='Clarice Lispector', conta_id=user.id)
    session.add(new_romancista)
    session.commit()

    romancista = session.scalar(
        select(Romancista).where(Romancista.conta_id == user.id)
    )

    assert romancista.nome == 'Clarice Lispector'


def test_create_livro(session, user, romancista: Romancista):
    new_livro = Livro(
        titulo='o hobbit',
        ano=1937,
        romancista_id=romancista.id,
        conta_id=user.id,
    )
    session.add(new_livro)
    session.commit()

    livro = session.scalar(select(Livro).where(Livro.conta_id == user.id))

    assert livro.titulo == 'o hobbit'
    assert livro.ano == 1937  # noqa
    assert livro.romancista_id == romancista.id
    assert livro.conta_id == user.id
