from http import HTTPStatus


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
