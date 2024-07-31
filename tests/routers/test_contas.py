from http import HTTPStatus


def test_create_conta(client):
    response = client.post(
        '/contas/',
        json={
            'username': 'fausto',
            'email': 'fausto@fausto.com',
            'senha': '1234567',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'fausto@fausto.com',
        'username': 'fausto',
    }


def test_create_conta_already_exists_username(client, user):
    response = client.post(
        '/contas/',
        json={
            'username': user.username,
            'email': 'wrongemail@test.com',
            'senha': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Nome de usuário já existe'}


def test_create_conta_already_exists_email(client, user):
    response = client.post(
        '/contas/',
        json={
            'username': 'wrongusername',
            'email': user.email,
            'senha': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'E-mail já existe'}
