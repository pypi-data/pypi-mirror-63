import prs_utility as utility

from .request import request
from . import validator

__all__ = [
    'sign_by_token', 'hash_by_password', 'hash_by_filename',
    'hash_by_readable_stream'
]


def sign_by_token(data, token, host):
    validator.assert_exc(data, 'data cannot be null')
    validator.assert_exc(token, 'token cannot be null')
    return request(
        host=host, method='post', path='/sign', data=data,
        auth_opts={'token': token}
    )


def hash_by_password(email, password, hash_alg='keccak256'):
    return utility.hash_text(f'{password}{email}', hash_alg=hash_alg)


def hash_by_filename(filename, hash_alg='keccak256'):
    # FIXME: eth_utils.keccak do not support `update`
    # so, load all data to memory, maybe OOM
    with open(filename, 'r') as fp:
        data = fp.read()
        return utility.hash_text(data, hash_alg=hash_alg)


def hash_by_readable_stream(stream, hash_alg='keccak256'):
    data = stream.read()
    _data = data.decode() if isinstance(data, bytes) else data
    _hash = utility.hash_text(_data, hash_alg=hash_alg)
    return data, _hash
