import requests

from .error_messages import HttpClientError
from .protocols import HTTP, DB
from .response import Response


class Client:
    def fetch_data(self, *args, **kwargs):
        raise NotImplementedError
    pass


class HTTPClient(Client):
    '''
    http client class
    using requests http://docs.python-requests.org/en/latest/
    '''

    error_class = HttpClientError

    def __init__(self, name):
        self.name = name

    def fetch_data(self, url, params=None, data=None, method='get', headers=None, transform=None):
        """

        :param url: the url to fetch data from
        :param params: dictionary of query string params
        :param data: dictionary of body data
        :param err_message: custom error message
        :param method: http method (get,post)
        :param headers: dictionary of headers
        :param transform: the transform function to manipulate response data
        :return:
        """
        if not hasattr(requests, method):
            return Response(self.error_class.method_error(method))
        if not headers:
            headers = {}
        method_func = getattr(requests, method)
        try:
            res = method_func(url, data=data, params=params, headers=headers)
        except Exception as e:
            return Response(self.error_class.requests_error(e.args[0]))
        if res.status_code != 200:
            return Response(self.error_class.service_status_code_error(self.name, res.status_code))
        if not transform:
            return Response(res=res, data=res.json())
        if not hasattr(transform, '__call__'):
            return Response(self.error_class.transform_error())
        try:
            final = transform(res.json())
        except Exception as e:
            return Response(self.error_class.transform_exception(e))
        return Response(res=res, data=final)

    def __str__(self):
        return HTTP


class DBClient(Client):

    def fetch_data(self, *args, **kwargs):
        pass

