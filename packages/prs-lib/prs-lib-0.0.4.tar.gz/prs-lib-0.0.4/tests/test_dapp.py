from . import now_str, get_client_buyer

import prs_utility as utility

DAPP_NAME = {}
APP_ADDRESS = {}
APP_PRIVATE_KEY = {}
KEY_PAIR = {}
CODE = {}


def get_dapp_name():
    return f'Test APP {now_str()}'


def test_name_not_exist(client_developer_user):
    dapp_name = get_dapp_name()
    # check if exist by dapp name
    res = client_developer_user.dapp.is_name_exist(dapp_name)
    assert res.status_code == 200
    data = res.json()
    assert data['isExist'] is False


def create_dapp(c):
    dapp_name = get_dapp_name()
    # create dapp
    dapp = {
        'name': dapp_name,
        'description': 'This is a testing app.',
        'url': 'http://xx.com',
        'redirect_url': f'{c.config.host}/auth',
    }
    res = c.dapp.create(dapp)
    assert res.status_code == 200
    data = res.json()
    app_address = data['address']
    assert app_address
    return dapp_name, app_address


def test_create_dapp(client_developer_user):
    env = client_developer_user.config.env
    global DAPP_NAME, APP_ADDRESS
    DAPP_NAME[env], APP_ADDRESS[env] = create_dapp(client_developer_user)
    # check if exist by dapp name
    res = client_developer_user.dapp.is_name_exist(DAPP_NAME[env])
    assert res.status_code == 200
    data = res.json()
    assert data and isinstance(data, dict)
    assert data['isExist'] is True


def test_update_dapp(client_developer_user):
    env = client_developer_user.config.env
    dapp_name = get_dapp_name()
    dapp = {
        'name': dapp_name,
        'description': f'update description for {dapp_name}',
        'url': 'http://xx.com',
        'redirect_url': f'{client_developer_user.config.host}/auth',
    }
    global APP_ADDRESS
    res = client_developer_user.dapp.update(APP_ADDRESS[env], dapp)
    data = res.json()
    APP_ADDRESS[env] = data['address']
    assert APP_ADDRESS[env]
    assert data['name'] == dapp['name']
    assert data['description'] == dapp['description']


def test_delete_dapp(client_developer_user):
    env = client_developer_user.config.env
    global APP_ADDRESS
    res = client_developer_user.dapp.delete(APP_ADDRESS[env])
    assert res.status_code == 200
    data = res.json()
    assert data and isinstance(data, dict)


def test_recreate_dapp(client_developer_user):
    env = client_developer_user.config.env
    global DAPP_NAME, APP_ADDRESS
    DAPP_NAME[env], APP_ADDRESS[env] = create_dapp(client_developer_user)
    # check if exist by dapp name
    res = client_developer_user.dapp.is_name_exist(DAPP_NAME[env])
    assert res.status_code == 200
    data = res.json()
    assert data and isinstance(data, dict)
    assert data['isExist'] is True


def test_get_dapp_by_address(client_developer_user):
    env = client_developer_user.config.env
    global APP_ADDRESS
    # get dapp by address
    res = client_developer_user.dapp.get_by_address(APP_ADDRESS[env])
    assert res.status_code == 200
    data = res.json()
    global APP_PRIVATE_KEY
    APP_PRIVATE_KEY[env] = data['privateKey']
    assert APP_PRIVATE_KEY[env]


def test_get_apps(client_developer_user):
    # get dapps
    res = client_developer_user.dapp.get_dapps()
    assert res.status_code == 200


def test_get_authorize_url(client_developer_user):
    env = client_developer_user.config.env
    global APP_ADDRESS
    auth_url = client_developer_user.dapp.get_authorize_url(APP_ADDRESS[env])
    assert auth_url


def test_web_authorize(client_with_auth):
    env = client_with_auth.config.env

    global KEY_PAIR
    KEY_PAIR[env] = utility.create_key_pair()

    res = client_with_auth.dapp.web_authorize(APP_ADDRESS[env])
    assert res.status_code == 200
    data = res.json()
    global CODE
    CODE[env] = data['code']
    assert CODE[env]


def test_auth_by_code(client_developer_user):
    env = client_developer_user.config.env
    global CODE, APP_ADDRESS, APP_PRIVATE_KEY
    res = client_developer_user.dapp.auth_by_code(
        CODE[env], APP_ADDRESS[env], APP_PRIVATE_KEY[env]
    )
    print(f'CODE = {CODE}')
    print(f'APP_ADDRESS = {APP_ADDRESS}')
    print(f'APP_PRIVATE_KEY = {APP_PRIVATE_KEY}')
    assert res.status_code == 200


def test_deauthenticate(client_with_auth):
    env = client_with_auth.config.env
    global APP_ADDRESS, KEY_PAIR
    res = client_with_auth.dapp.deauthenticate(
        APP_ADDRESS[env], KEY_PAIR[env]['address']
    )
    assert res.status_code == 200
