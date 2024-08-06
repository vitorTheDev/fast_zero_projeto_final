from http import HTTPStatus

from fastapi.testclient import TestClient


def test_cenario_criacao_de_romancista(
    client: TestClient,
    cenario_token,
):
    response = client.post(
        '/romancistas/',
        json={'nome': 'Clarice Lispector'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'clarice lispector',
    }


def test_cenario_buscar_romancista_por_id(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    response = client.get(
        f'/romancistas/{cenario_romancista['id']}',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': cenario_romancista['id'],
        'nome': 'clarice lispector',
    }


def test_cenario_alteracao_de_romancista(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    response = client.patch(
        f'/romancistas/{cenario_romancista['id']}',
        json={
            'nome': 'manuel bandeira',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': cenario_romancista['id'],
        'nome': 'manuel bandeira',
    }


def test_cenario_delecao_de_romancista(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    response = client.delete(
        f'/romancistas/{cenario_romancista['id']}',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado no MADR'}


def test_cenario_buscar_romancista_por_filtro(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    response_manuel = client.post(
        '/romancistas/',
        json={'nome': 'manuel bandeira'},
    )
    response_paulo = client.post(
        '/romancistas/',
        json={'nome': 'paulo leminski'},
    )
    response = client.get(
        '/romancistas?nome=a',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancistas': [
            {'nome': 'clarice lispector', 'id': cenario_romancista['id']},
            {'nome': 'manuel bandeira', 'id': response_manuel.json()['id']},
            {'nome': 'paulo leminski', 'id': response_paulo.json()['id']},
        ]
    }
