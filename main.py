from parser import Parser
from config import Config


if __name__ == '__main__':
    for city, coockie in Config.COOKIE_SITIES.items():
        Parser().parsing(
            {
                'sort': 'popular',
                'category_id': '3',
                'count': '1',
                'page': '10',
            },
            coockie,
        )
