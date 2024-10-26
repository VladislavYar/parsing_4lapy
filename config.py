import os
import json

from dotenv import load_dotenv

load_dotenv()

with open('categories.json', 'r', encoding='utf-8') as file:
    CATEGORIES = json.load(file)


class Config:
    """Кофигурация проекта.

    Attributes:
        AUTHORIZATION (str): данные для авторизации.
        URL_GET_TOKEN (str): URL получения токена.
        URL_PRODUCTS_CATALOG (str): URL категории товаров.
        URL_PRODUCTS_CATALOG_INFO (str): URL товаров с доп. информацией.
        URL_PRODUCT (str): URL товара.
        SALT (str): соль для формирования 'sign'.
        COOKIE_SITIES (dict[str, dict[str, str]]):
            словарь город-значение в cookie.
        COUNT (int): количество товаров на странице.
        PAGE (int): страница начала парсинга.
        SORTS (tuple[str, ...]): возможные сортировки товаров.
        CATEGORIES (dict[int, dict[str, str]]): категории.
    """

    AUTHORIZATION = os.getenv(
        'AUTHORIZATION',
        default='Basic NGxhcHltb2JpbGU6eEo5dzFRMyhy',
    )
    URL_GET_TOKEN = 'https://4lapy.ru/api/start/'
    URL_PRODUCTS_CATALOG = 'https://4lapy.ru/api/v2/catalog/product/list/'
    URL_PRODUCTS_CATALOG_INFO = (
        'https://4lapy.ru/api/v2/catalog/product/info-list/'
    )
    URL_PRODUCT = 'https://4lapy.ru/api/product_variant_info/'
    SALT = 'ABCDEF00G'
    COOKIE_SITIES = {
        'moscow': {'selected_city_code': '0000073738'},
        'saint-petersburg': {'selected_city_code': '0000103664'},
    }
    SORTS = ('popular', 'up-price', 'down-price', 'novinki')
    CATEGORIES = CATEGORIES
    COUNT = 10
    PAGE = 1
