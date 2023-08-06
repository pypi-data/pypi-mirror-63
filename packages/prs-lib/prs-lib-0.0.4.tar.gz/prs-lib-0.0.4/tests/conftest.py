import shutil
from . import now_str, get_client_buyer, DEV_USER, BETA_USER, PROD_USER, DEVELOPER

import pytest
from prs_lib import PRS
import prs_utility as utility


@pytest.fixture(params=['prod'])
def client_without_auth(request):
    print('request.param:', request.param)
    client = PRS({'env': request.param, 'debug': True})
    yield client


@pytest.fixture(params=['prod'])
def client_with_auth(request):  # user
    print('request.param:', request.param)
    if request.param == 'dev':
        user = DEV_USER
    elif request.param == 'prod':
        user = PROD_USER
    else:
        raise ValueError(
            f'env: {request.param} should in {"dev", "prod"}'
        )

    private_key = utility.recover_private_key(
        user['keystore'], user['password']
    )
    client = PRS({
        'env': request.param,
        'private_key': private_key,
        'address': user['address'],
        'debug': True
    })
    yield client


@pytest.fixture(params=['prod'])
def client_developer_user(request):  # developer
    private_key = utility.recover_private_key(
        DEVELOPER['keystore'], DEVELOPER['password']
    )
    client = PRS({
        'env': request.param,
        'private_key': private_key,
        'address': DEVELOPER['address'],
        'debug': True
    })
    yield client


@pytest.fixture(params=['prod'])
def client_buyer(request):
    yield get_client_buyer(request.param)


@pytest.fixture()
def markdown_file(tmpdir):
    filename = "%s.md" % now_str()
    file_path = tmpdir.join(filename)
    file_path.write(filename)
    yield file_path
    shutil.rmtree(tmpdir)
