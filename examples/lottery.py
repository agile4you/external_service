from external_service.service import Service

random_numbers_service = Service('random org', 'http')


def get_random_numbers(data):
    return data.get('results').get('random').get('data')

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


class Lottery:
    history = []

    def __init__(self, choice, win=None):
        self.choice = choice
        if win or self._lottery_result():
            self.history.append('YOU WIN!!! \n with number {}'.format(self.choice))
        else:
            self.history.append('Damn {} was not a good choice. \n Try again!!'.format(self.choice))
        print(self.history[-1])

    def _lottery_result(self):
        query = random_numbers_service.client.fetch_data('https://api.random.org/json-rpc/1/invoke',
                                                         method='post',
                                                         data=post_data,
                                                         transform=get_random_numbers)
        if not query.errors:
            return self.choice in query.data
        # Do something with errors


if __name__ == '__main__':
    '''
    Challenge your luck!!!!!!
    '''
    choices = [23, 74, 13, 42, 27]
    for choice in choices:
        lottery = Lottery(choice)
    # force win!
    lottery = Lottery(1337, win=True)
