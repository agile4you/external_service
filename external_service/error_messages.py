class HttpClientError:

    @staticmethod
    def service_status_code_error(service_name, code):
        return {'service_error': '{} service is not responding with status code {}'.format(service_name, code)}

    @staticmethod
    def transform_error():
        return {'transform_error': 'transform should be a callable'}

    @staticmethod
    def transform_exception(e):
        return {'transform_error': 'error processing data : {} ,  {}'.format(e.__class__.__name__, e.args[0])}

    @staticmethod
    def requests_error(requests_error):
        return {'requests_error': requests_error}

    @staticmethod
    def method_error(method):
        return {'http_method_error': '{} not supported type of HTTP method. Choose from (get,post)'.format(method)}