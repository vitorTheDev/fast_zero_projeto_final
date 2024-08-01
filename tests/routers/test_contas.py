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


def test_update_conta(client, user, token):
    response = client.put(
        f'/contas/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'senha': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_conta_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/contas/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'senha': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Permissões insuficientes'}
