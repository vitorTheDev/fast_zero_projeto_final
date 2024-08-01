import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero_projeto_final.app import app
from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.registry import table_registry
from fast_zero_projeto_final.models.romancistas import Romancista
from fast_zero_projeto_final.security import get_password_hash


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    senha = 'testtest'
    user = ContaFactory(senha=get_password_hash(senha))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.senha_limpa = 'testtest'

    return user


@pytest.fixture
def other_user(session):
    senha = 'testtest'
    user = ContaFactory(senha=get_password_hash(senha))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.senha_limpa = 'testtest'

    return user


@pytest.fixture
def romancista(session, user: Conta):
    entry = Romancista(nome='romancista teste', user_id=user.id)

    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.senha_limpa},
    )
    token = response.json()['access_token']
    client.headers.update({'Authorization': f'Bearer {token}'})
    return token


class ContaFactory(factory.Factory):
    class Meta:
        model = Conta

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
