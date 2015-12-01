from src.service import Service


def find_top(data):
    return data


def get_url(data):
    return {'title': data.get('title'), 'url': data.get('url')}


def hottest_news():
    hacker_news_service = Service('hacker news', 'http')
    get_top = hacker_news_service.register('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty',
                                           transform=find_top)
    get_info = hacker_news_service.register('https://hacker-news.firebaseio.com/v0/item/{name}.json?print=pretty',
                                            transform=get_url)

    top_stories_query = get_top()
    if top_stories_query.errors:
        print(top_stories_query.errors)
        return
    detail_info_first = get_info(name=top_stories_query.data[0])
    if detail_info_first.errors:
        print(detail_info_first.errors)
        return
    print(detail_info_first.data)
    detail_info_second = get_info(name=top_stories_query.data[1])
    if detail_info_second.errors:
        print(detail_info_second.errors)
        return
    print(detail_info_second.data)

if __name__ == '__main__':
    '''
    Show detail info about the 2 hottest hacker news posts!
    '''
    hottest_news()
