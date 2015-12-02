import pytest
from external_service import protocols
from external_service.client_types import HTTPClient
from external_service.exceptions import ServiceTypeException
from external_service.service import Service


def test_proper_initializing_service():
    tiv_api = Service('api tripinview', protocols.HTTP)
    assert hasattr(tiv_api, 'name')
    assert hasattr(tiv_api, 'client')
    assert isinstance(tiv_api.client, HTTPClient)


def test_errors_initializing_service_name():
    with pytest.raises(ServiceTypeException) as e:
        fail_name = Service(45, protocols.DB)
    assert 'Name of service' in str(e.value)


def test_errors_initializing_service_protocol():
    with pytest.raises(ServiceTypeException) as e:
        fail_type = Service('test service', 'peinaw')
    assert 'protocol type' in str(e.value)


def test_pretty_service_info():
    github_service = Service('my github repo', protocols.HTTP)
    assert str(github_service) == 'my github repo Service'
    assert repr(github_service) == 'Name: my github repo, Type: http, Instances: 1'


def test_service_register_method():
    multi_resource_service = Service('members', protocols.HTTP)
    assert hasattr(multi_resource_service, 'register')
    get_all_users = multi_resource_service.register('get all users')
    assert hasattr(get_all_users, '__call__')



