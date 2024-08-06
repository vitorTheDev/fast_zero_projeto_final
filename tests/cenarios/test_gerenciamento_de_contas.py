from http import HTTPStatus

from fastapi.testclient import TestClient


def test_cenario_criacao_de_conta(client: TestClient):
    response = client.post(
        '/contas/',
        json={
            'username': 'dunossauro',
            'email': 'dudu@dudu.com',
            'senha': '123456',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'dudu@dudu.com',
        'username': 'dunossauro',
        'id': 1,
    }


def test_cenario_criacao_de_conta_ja_existente(
    client: TestClient,
    cenario_user,
):
    response = client.post(
        '/contas/',
        json={
            'username': 'dunossauro',
            'email': 'dudu@dudu.com',
            'senha': '123456',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Conta já existe no MADR'}


def test_cenario_alteracao_de_conta(
    client: TestClient,
    cenario_user,
    cenario_token,
):
    response = client.put(
        f'/contas/{cenario_user['id']}',
        json={
            'username': 'dunossauro',
            'email': 'dudu@dudu.com',
            'senha': '654321',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'dunossauro',
        'email': 'dudu@dudu.com',
        'id': cenario_user['id'],
    }


def test_cenario_delecao_de_conta(
    client: TestClient,
    cenario_user,
    cenario_token,
):
    response = client.delete(
        f'/contas/{cenario_user['id']}',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}
