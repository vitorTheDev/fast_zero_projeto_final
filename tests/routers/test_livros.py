from http import HTTPStatus

from tests.factories import LivroFactory


def test_create_livro_romancista_not_found(client, token):
    response = client.post(
        '/livros/',
        json={
            'titulo': 'test livro',
            'ano': 1970,
            'romancista_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_create_livro(client, token, romancista):
    response = client.post(
        '/livros/',
        json={
            'titulo': 'test livro',
            'ano': 1970,
            'romancista_id': romancista.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    res = response.json()
    assert res == {
        'id': 1,
        'titulo': 'test livro',
        'ano': 1970,
        'romancista_id': romancista.id,
    }


def test_create_livro_factory(client, token, romancista):
    livro = LivroFactory(romancista_id=romancista.id)
    response = client.post(
        '/livros/',
        json={
            'titulo': livro.titulo,
            'ano': livro.ano,
            'romancista_id': romancista.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    res = response.json()
    assert res == {
        'id': 1,
        'titulo': livro.titulo,
        'ano': livro.ano,
        'romancista_id': romancista.id,
    }
