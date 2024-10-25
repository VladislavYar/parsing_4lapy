import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Кофигурация проекта.

    Attributes:
        AUTHORIZATION (str): данные для авторизации.
        URL_GET_TOKEN (str): URL получения токена.
        URL_PRODUCTS_CATALOG (str): URL категории продуктов.
        URL_PRODUCTS_CATALOG_INFO (str): URL продуктов с доп. информацией.
        URL_PRODUCT (str): URL продукта.
        SALT (str): соль для формирования 'sign'.
        COOKIE_SITIES (dict[str, str]):
            словарь город-значение в cookie.
        SORT (str): параметр сортировки запрашиваемых данных.
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
    SORT = 'popular'
