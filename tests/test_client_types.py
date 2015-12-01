import json

import pytest
from src.service import Service

VALID_URL_GET = 'https://randomuser.me/api/'


@pytest.fixture(scope='module')
def members_service():
    return Service('members', 'http')


def test_simple_get(members_service):
    """
    :param members_service:
    Tets simple get
    """
    d = members_service.client.fetch_data(VALID_URL_GET)
    assert d.errors is None
    assert hasattr(d.response, 'json')
    assert hasattr(d, 'data')


def test_simple_post(members_service):
    post_data = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": "c3292e99-4221-441c-a74f-e81987876f89",
            "n": 12,
            "min": 1,
            "max": 80
        },
        "id": 42
    }
    headers = {'Content-type': 'application/json'}
    d = members_service.client.fetch_data('https://api.random.org/json-rpc/1/invoke',
                                          data=json.dumps(post_data), method='post', headers=headers)
    assert d.errors is None
    assert hasattr(d.response, 'json')


def test_error_service_method(members_service):
    d = members_service.client.fetch_data(VALID_URL_GET,
                                          method='peinaw')
    assert d.errors is not None
    assert isinstance(d.errors, dict)
    assert d.errors.get('http_method_error') == 'peinaw not supported type of HTTP method. Choose from (get,post)'


def test_error_service_down(members_service):
    """
    :param members_service
    Test error remote service is down
    """
    d = members_service.client.fetch_data('https://randomuser.me/api/dhdjdhd')
    assert d.errors is not None
    assert d.errors.get('service_error') == '{} service is not responding with status code 404' \
        .format(members_service.name)


def test_error_requests(members_service):
    """
    propagade requests errors as e.g Invalid Url
    :param members_service:
    """
    d = members_service.client.fetch_data('no a valid url')
    assert d.errors is not None
    assert d.errors.get('requests_error') is not None


def test_error_fake_transform(members_service):
    fake = '5'
    d = members_service.client.fetch_data(VALID_URL_GET, transform=fake)
    assert d.errors is not None
    assert d.errors.get('transform_error') == 'transform should be a callable'


def test_error_at_transform(members_service):
    def list_user_email(data):
        return [user['peinaw'] for user in data['results']]

    d = members_service.client.fetch_data(VALID_URL_GET, transform=list_user_email)
    assert d.errors is not None
    assert d.errors['transform_error'] == 'error processing data : KeyError ,  peinaw'


def test_service_transform(members_service):
    def list_user_emails(data):
        return [user.get('email') for user in data.get('results')]

    d = members_service.client.fetch_data(VALID_URL_GET, transform=list_user_emails)
    assert d.data is not None
    assert isinstance(d.data, list)


def test_service_transform_class(members_service):

    class User:
        def __init__(self, gender):
            self.gender = gender

        def __call__(self, data, **kwargs):
            return [user.get('email') for user in data.get('results') if user.get('gender') == self.gender]

    users = User('male')
    d = members_service.client.fetch_data(VALID_URL_GET, transform=users)
    assert d.data is not None
    assert isinstance(d.data, list)
