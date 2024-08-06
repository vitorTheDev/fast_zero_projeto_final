from http import HTTPStatus

from fastapi.testclient import TestClient


def test_cenario_criacao_de_livro(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    response = client.post(
        '/livros/',
        json={
            'ano': 1973,
            'titulo': 'Café Da Manhã Dos Campeões',
            'romancista_id': cenario_romancista['id'],
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'ano': 1973,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': cenario_romancista['id'],
    }


def test_cenario_buscar_livro_por_id(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    post = client.post(
        '/livros/',
        json={
            'ano': 1974,
            'titulo': 'café da manhã dos campeões',
            'romancista_id': cenario_romancista['id'],
        },
    ).json()
    response = client.get(
        f'/livros/{post['id']}',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': post['id'],
        'ano': 1974,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': cenario_romancista['id'],
    }


def test_cenario_alteracao_de_livro(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    post = client.post(
        '/livros/',
        json={
            'ano': 1973,
            'titulo': 'Café Da Manhã Dos Campeões',
            'romancista_id': cenario_romancista['id'],
        },
    ).json()
    response = client.patch(
        f'/livros/{post['id']}',
        json={
            'ano': 1974,
            'titulo': 'café da manhã dos campeões',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': post['id'],
        'ano': 1974,
        'titulo': 'café da manhã dos campeões',
        'romancista_id': cenario_romancista['id'],
    }


def test_cenario_delecao_de_livro(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    post = client.post(
        '/livros/',
        json={
            'ano': 1973,
            'titulo': 'Café Da Manhã Dos Campeões',
            'romancista_id': cenario_romancista['id'],
        },
    ).json()
    response = client.delete(
        f'/livros/{post['id']}',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_cenario_buscar_livro_por_filtro(
    client: TestClient,
    cenario_token,
    cenario_romancista,
):
    response_cafe = client.post(
        '/livros/',
        json={
            'ano': 1900,
            'titulo': 'Café Da Manhã Dos Campeões',
            'romancista_id': cenario_romancista['id'],
        },
    )
    response_bras = client.post(
        '/livros/',
        json={
            'ano': 1900,
            'titulo': 'Memórias Póstumas de Brás Cubas',
            'romancista_id': cenario_romancista['id'],
        },
    )
    client.post(
        '/livros/',
        json={
            'ano': 1865,
            'titulo': 'Iracema',
            'romancista_id': cenario_romancista['id'],
        },
    )
    response = client.get(
        '/livros?titulo=a&ano=1900',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'ano': 1900,
                'titulo': 'café da manhã dos campeões',
                'romancista_id': cenario_romancista['id'],
                'id': response_cafe.json()['id'],
            },
            {
                'ano': 1900,
                'titulo': 'memórias póstumas de brás cubas',
                'romancista_id': cenario_romancista['id'],
                'id': response_bras.json()['id'],
            },
        ]
    }
