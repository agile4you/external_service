class Response:
    """
    the service response object
    """
    def __init__(self, errors=None, res=None, data=None):
        self.errors = errors
        self.response = res
        self.data = data

    def __call__(self):
        return self.response

    def __str__(self):
        return '{}'.format(self.data)

    def __repr__(self):
        return '{}'.format(self.data)
