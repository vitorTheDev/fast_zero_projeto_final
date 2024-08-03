from http import HTTPStatus

import pytest
from sqlalchemy.exc import InvalidRequestError

from tests.factories import RomancistaFactory


def test_create_romancista(client, token):
    response = client.post(
        '/romancistas/',
        json={
            'nome': 'test romancista',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    res = response.json()
    assert res == {
        'id': 1,
        'nome': 'test romancista',
    }


def test_create_romancista_sanitized(client, token):
    response = client.post(
        '/romancistas/',
        json={
            'nome': "    Manuel     Bandeira !!!<script>alert('xss')</script>",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    res = response.json()
    assert res == {
        'id': 1,
        'nome': 'manuel bandeira alertxss',
    }


def test_list_romancistas_should_return_5_romancistas(
    session, client, user, token
):
    expected_romancistas = 5
    session.bulk_save_objects(
        RomancistaFactory.create_batch(5, conta_id=user.id)
    )
    session.commit()

    response = client.get(
        '/romancistas/',
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_list_romancistas_filter_nome_should_return_5_romancistas(
    session, user, client, token
):
    expected_romancistas = 5
    session.bulk_save_objects(
        RomancistaFactory.create_batch(5, conta_id=user.id, nome='Blablabla')
    )
    session.bulk_save_objects(
        RomancistaFactory.create_batch(
            5, conta_id=user.id, nome='test romancista 1'
        )
    )
    session.commit()

    response = client.get(
        '/romancistas/?nome=test romancista 1',
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_list_romancistas_other_user_data_should_return_0(
    client, other_romancista, token
):
    expected_romancistas = 0

    response = client.get(
        '/romancistas/',
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_list_romancistas_filtered_other_user_data_should_return_0(
    client, other_romancista, token
):
    expected_romancistas = 0

    response = client.get(
        f'/romancistas/?nome={other_romancista.nome}',
    )

    assert len(response.json()['romancistas']) == expected_romancistas


def test_patch_romancista_not_found(client, token):
    response = client.patch(
        '/romancistas/1',
        json={},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_patch_romancista(client, token, romancista):
    response = client.patch(
        f'/romancistas/{romancista.id}',
        json={'nome': 'teste romancista'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['nome'] == 'teste romancista'


def test_delete_romancista(client, romancista, session, token):
    response = client.delete(
        f'/romancistas/{romancista.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}
    pytest.raises(InvalidRequestError, lambda: session.refresh(romancista))


def test_delete_romancista_not_found(client, token):
    response = client.delete('/romancistas/99')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}
