from http import HTTPStatus

import pytest
from sqlalchemy.exc import InvalidRequestError

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


def test_create_livro_romancista_not_found_other_romancista(
    client, token, other_romancista
):
    response = client.post(
        '/livros/',
        json={
            'titulo': 'test livro',
            'ano': 1970,
            'romancista_id': other_romancista.id,
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


def test_list_livros_should_return_5_livros(
    session, client, user, token, romancista
):
    expected_livros = 5
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            romancista_id=romancista.id,
        )
    )
    session.commit()

    response = client.get(
        '/livros/',
    )

    assert len(response.json()['livros']) == expected_livros


def test_list_livros_filter_titulo_should_return_5_livros(
    session, user, client, token, romancista
):
    expected_livros = 5
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            titulo='Blablabla',
            romancista_id=romancista.id,
        )
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            titulo='test livro 1',
            romancista_id=romancista.id,
        )
    )
    session.commit()

    response = client.get(
        '/livros/?titulo=test livro 1',
    )

    assert len(response.json()['livros']) == expected_livros


def test_list_livros_filter_ano_should_return_5_livros(
    session,
    user,
    client,
    token,
    romancista,
):
    expected_livros = 5
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            ano=1970,
            romancista_id=romancista.id,
        )
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            ano=1950,
            romancista_id=romancista.id,
        )
    )
    session.commit()

    response = client.get(
        '/livros/?ano=1970',
    )

    assert len(response.json()['livros']) == expected_livros


def test_list_livros_filter_romancista_should_return_5_livros(  # noqa
    session,
    user,
    client,
    token,
    romancista,
    romancista2,
):
    expected_livros = 5
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5, conta_id=user.id, romancista_id=romancista.id
        )
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5, conta_id=user.id, romancista_id=romancista2.id
        )
    )
    session.commit()

    response = client.get(
        f'/livros/?romancista_id={romancista.id}',
    )

    assert len(response.json()['livros']) == expected_livros


def test_list_livros_filter_combined_should_return_5_livros(  # noqa
    session,
    user,
    client,
    token,
    romancista,
    romancista2,
):
    expected_livros = 5
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            romancista_id=romancista.id,
            titulo='test livro 1',
            ano=1970,
        )
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5,
            conta_id=user.id,
            romancista_id=romancista2.id,
            titulo='blabla',
            ano=1970,
        )
    )
    session.commit()

    response = client.get(
        f'/livros/?romancista_id={romancista.id}&ano=1970&titulo=test',
    )

    assert len(response.json()['livros']) == expected_livros


def test_list_livros_other_user_livro_should_return_0(
    client, session, other_user, romancista, token
):
    expected_livros = 0
    session.bulk_save_objects(
        LivroFactory.create_batch(
            5, conta_id=other_user.id, romancista_id=romancista.id
        )
    )

    response = client.get(
        '/livros/',
    )

    assert len(response.json()['livros']) == expected_livros


def test_patch_livro_not_found(client, token):
    response = client.patch(
        '/livros/1',
        json={},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_patch_livro_romancista_not_found(
    client, user, token, session, romancista
):
    livro = LivroFactory(conta_id=user.id, romancista_id=romancista.id)
    session.add(livro)
    session.commit()
    session.refresh(livro)
    response = client.patch(
        f'/livros/{livro.id}',
        json={
            'romancista_id': 99,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_livro_other_romancista_not_found(
    client, user, session, token, other_romancista
):
    livro = LivroFactory(conta_id=user.id, romancista_id=other_romancista.id)
    session.add(livro)
    session.commit()
    session.refresh(livro)
    response = client.patch(
        f'/livros/{livro.id}',
        json={
            'romancista_id': other_romancista.id,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_livro(client, user, session, token, romancista, romancista2):  # noqa
    livro = LivroFactory(conta_id=user.id, romancista_id=romancista.id)
    session.add(livro)
    session.commit()
    session.refresh(livro)
    response = client.patch(
        f'/livros/{livro.id}',
        json={
            'titulo': 'teste livro',
            'romancista_id': romancista2.id,
            'ano': 1970,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'teste livro'
    assert response.json()['romancista_id'] == romancista2.id
    assert response.json()['ano'] == 1970  # noqa


def test_patch_livro_sanitized(  # noqa
    client, user, session, token, romancista, romancista2
):
    livro = LivroFactory(conta_id=user.id, romancista_id=romancista.id)
    session.add(livro)
    session.commit()
    session.refresh(livro)
    response = client.patch(
        f'/livros/{livro.id}',
        json={
            'titulo': "TESTE LivrO!!<script>alert('xss')</script>",
            'romancista_id': romancista2.id,
            'ano': 1970,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['titulo'] == 'teste livroalertxss'
    assert response.json()['romancista_id'] == romancista2.id
    assert response.json()['ano'] == 1970  # noqa


def test_delete_livro(client, session, user, romancista, token):
    livro = LivroFactory(conta_id=user.id, romancista_id=romancista.id)
    session.add(livro)
    session.commit()
    session.refresh(livro)
    response = client.delete(
        f'/livros/{livro.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}
    pytest.raises(InvalidRequestError, lambda: session.refresh(livro))


def test_delete_livro_not_found(client, token):
    response = client.delete('/livros/99')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}
