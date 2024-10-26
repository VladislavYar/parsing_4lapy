from argparse import ArgumentParser

from config import Config


def parser_command_line() -> ArgumentParser:
    """Парсер командной строки."""
    parser = ArgumentParser(description='Парсер товаров с "Четыре Лапы"')
    parser.add_argument(
        '-s',
        '--sort',
        help='Сортировка товаров',
        choices=Config.SORTS,
        default='popular',
        required=False,
    )
    parser.add_argument(
        '-с',
        '--category',
        help='Id категории',
        choices=Config.CATEGORIES.keys(),
        default=3,
        required=False,
    )
    return parser
