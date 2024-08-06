import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero_projeto_final.app import app
from fast_zero_projeto_final.database import get_session
from fast_zero_projeto_final.models.contas import Conta
from fast_zero_projeto_final.models.registry import table_registry
from fast_zero_projeto_final.security import get_password_hash
from tests.factories import ContaFactory, RomancistaFactory


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
def cenario_user(client):
    response = client.post(
        '/contas/',
        json={
            'username': 'dunossauro',
            'email': 'dudu@dudu.com',
            'senha': '123456',
        },
    )
    json = response.json()
    json['senha_limpa'] = '123456'
    return json


@pytest.fixture
def cenario_romancista(
    client: TestClient,
    cenario_token,
):
    response = client.post(
        '/romancistas/',
        json={'nome': 'Clarice Lispector'},
    )
    return response.json()


@pytest.fixture
def romancista(session, user: Conta):
    entry = RomancistaFactory(conta_id=user.id)

    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry


@pytest.fixture
def romancista2(session, user: Conta):
    entry = RomancistaFactory(conta_id=user.id)

    session.add(entry)
    session.commit()
    session.refresh(entry)

    return entry


@pytest.fixture
def other_romancista(session, other_user: Conta):
    entry = RomancistaFactory(conta_id=other_user.id)

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


@pytest.fixture
def cenario_token(client, cenario_user):
    response = client.post(
        '/auth/token',
        data={
            'username': cenario_user['email'],
            'password': cenario_user['senha_limpa'],
        },
    )
    token = response.json()['access_token']
    client.headers.update({'Authorization': f'Bearer {token}'})
    return token
