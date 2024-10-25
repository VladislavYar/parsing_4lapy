import hashlib
import asyncio
import copy
from urllib import parse

import aiohttp

from config import Config
from typings import (
    ProductsData,
    Params,
    ResponseData,
    ResponseProducts,
    PriceAndStatus,
    PackingVariants,
)


class Parser:
    """Парсер магазина 'Четыре Лапы'

    Attributes:
        config (Config): конфигурация проекта.
    """

    config = Config()
    __default = object()

    def _get_hash(self, value: str | int) -> str:
        """Хеширует параметр запроса.

        Args:
            value (str | int): значение для хеширования.

        Returns:
            str: хешированный параметр запроса.
        """
        md5_hash = hashlib.md5()
        md5_hash.update(str(value).encode('utf-8'))
        digest = md5_hash.digest()
        return ''.join(f'{byte:02x}' for byte in digest)

    def _get_sign(self, params: Params) -> str:
        """Формирует хеш запроса.

        Args:
            params (Params): параметры запроса.

        Returns:
            str: хеш запроса.
        """
        values = []
        for value in params.values():
            values.append(self._get_hash(value))
        values.sort()
        sign = self.config.SALT
        for value in values:
            sign += value
        return self._get_hash(sign)

    async def _get_token(self) -> str:
        """Отдаёт токен.

        Returns:
            str: токен.
        """
        headers = {'Authorization': self.config.AUTHORIZATION}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.config.URL_GET_TOKEN,
                headers=headers,
            ) as response:
                data = await response.json()
        return data['data']['token']

    def _get_url_products_page(self, params: Params) -> str:
        """Отдаёт URL страницы продуктов.

        Args:
            params (Params): параметры запроса.

        Returns:
            str: URL страницы продуктов.
        """
        params = copy.deepcopy(params)
        params['sign'] = self._get_sign(params)
        params = parse.urlencode(params)
        return f'{self.config.URL_PRODUCTS_CATALOG}?{params}'

    def _get_all_url_products_page(
        self,
        params: Params,
        total_pages: int,
    ) -> list[str]:
        """Отдаёт список URLs всех страниц товаров.

        Args:
            params (Params): параметры запроса.
            total_pages (int): количество страниц в категории.

        Returns:
            list[str]: список URLs всех страниц товаров.
        """
        urls = []
        for page in range(2, total_pages + 1):
            params['page'] = page
            urls.append(self._get_url_products_page(params))
        return urls

    def _get_form_data_products_info(
        self, ids_products: list[int], params: Params
    ) -> Params:
        """Отдаёт данные по форме.

        Args:
            ids_products (list[int]): ids продуктов.
            params (Params): параметры запроса.

        Returns:
            Params: данные по форме.
        """
        form_data = {'sort': params['sort'], 'token': params['token']}
        for index, id_product in enumerate(ids_products):
            form_data[f'offers[{index}]'] = id_product
        form_data['sign'] = self._get_sign(form_data)
        return form_data

    async def _get_price_and_status(
        self, ids_products: list[int], params: Params
    ) -> PriceAndStatus:
        """Отдаёт цены и статус по продуктам.

        Args:
            ids_products (list[int]): ids продуктов.
            params (Params): параметры запроса.

        Returns:
            PriceAndStatus: цены и статус продуктов.
        """
        params = self._get_form_data_products_info(ids_products, params)
        headers = {'Authorization': self.config.AUTHORIZATION}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.config.URL_PRODUCTS_CATALOG_INFO,
                headers=headers,
                data=params,
            ) as response:
                data = await response.json()
                return data['data']['products']

    def _get_ids_products_and_packings_variants(
        self, products: ResponseProducts
    ) -> tuple[list[int], PackingVariants]:
        ids_products = []
        packings_variants = []
        for product_response in products:
            packing_variants = product_response['packingVariants']
            for packing_variant in packing_variants:
                if not packing_variant['isAvailable']:
                    continue
                packings_variants.append(packing_variant)
                ids_products.append(packing_variant['id'])
        return ids_products, packings_variants

    def _set_price_and_status_in_data_packings_variants(
        self,
        prices_statuses: PriceAndStatus,
        packings_variants: list[PackingVariants],
    ) -> None:
        """Устанавливает цену и статус в 'packingVariants'.

        Args:
            prices_statuses (PriceAndStatus): цены и статусы.
            packings_variants (list[PackingVariants]):
                список 'packingVariants'.
        """
        # Да, это выглядит ужасно :)
        for price_statuse in prices_statuses:
            for variant in price_statuse['variants']:
                for packing_variant in packings_variants:
                    if variant['id'] == packing_variant['id']:
                        packing_variant['price'] = variant['price']

    async def _set_price_and_status_in_data(
        self, data: ResponseData, params: Params
    ) -> ResponseData:
        """Добавляет цену и статус к данным.

        Args:
            data (ResponseData): данные из запроса.
            params (Params): параметры запроса.

        Returns:
            ResponseData: данные из запроса с ценой и статусом.
        """
        ids_products, packings_variants = (
            self._get_ids_products_and_packings_variants(data['data']['goods'])
        )
        if not ids_products:
            return data
        prices_statuses = await self._get_price_and_status(
            ids_products, params
        )
        self._set_price_and_status_in_data_packings_variants(
            prices_statuses, packings_variants
        )
        return data

    async def _get_products_page(
        self,
        url: str,
        params: Params,
        cookies: dict[str, str] | object = __default,
    ) -> ResponseData:
        """Отдаёт данные со страницы категории товаров.

        Args:
            url (str): URL страницы продуктов.
            params (Params): параметры запроса.
            cookies (dict[str, str] | object, optional):
                куки. По умолчанию __default.

        Returns:
            ResponseData: данные ответа.
        """
        if cookies is self.__default:
            cookies = ''
        headers = {'Authorization': self.config.AUTHORIZATION}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=headers,
                cookies=cookies,
            ) as response:
                return await self._set_price_and_status_in_data(
                    await response.json(), params
                )

    async def _get_start_products_page(
        self,
        params: Params,
        cookies: dict[str, str] | object = __default,
    ) -> ResponseData:
        """Отдаёт данные со стартовой страницы категории товаров.

        Args:
            params (Params): параметры запроса.
            cookies (dict[str, str] | object, optional):
                куки. По умолчанию __default.

        Returns:
            ResponseData: данные ответа.
        """
        url = self._get_url_products_page(params)
        return await self._get_products_page(url, params, cookies)

    async def _get_all_products_page(
        self,
        params: Params,
        total_pages: int,
        start_products: ResponseProducts,
    ) -> ResponseData:
        """_summary_

        Args:
            params (Params): параметры запроса.
            total_pages (int): количество страниц.
            start_products (ResponseProducts): продукты стартовой страницы.

        Returns:
            ResponseData: список всех продуктов категории.
        """
        lists_products = await asyncio.gather(
            *[
                self._get_products_page(url, params)
                for url in self._get_all_url_products_page(params, total_pages)
            ]
        )
        for data in lists_products:
            start_products.extend(data['data']['goods'])
        return start_products

    def _filter_products_data(self, data: ResponseProducts) -> ProductsData:
        """Фильтрует данные по продуктам из запроса.

        Args:
            data (ResponseProducts): продукты из запроса.

        Returns:
            ProductsData: отфильтрованные продукты.
        """
        products = []
        for product_response in data:
            packing_variants = product_response['packingVariants']
            product = {
                'brand': product_response['brand_name'],
                'packing_variant': [],
            }
            for packing_variant in packing_variants:
                if not packing_variant['isAvailable']:
                    continue
                id = packing_variant['id']
                product['packing_variant'].append(
                    {
                        'id': id,
                        'title': packing_variant['title'],
                        'price': packing_variant['price'],
                        'url': f'{self.config.URL_PRODUCT}?offerId={id}',
                    }
                )
            if product['packing_variant']:
                products.append(product)
        return products

    async def _get_products(
        self,
        params: Params,
        cookies: dict[str, str] | object = __default,
    ) -> ProductsData:
        """Отдаёт список товаров.

        Args:
            params (Params): параметры запроса.
            cookies (dict[str, str] | object, optional):
                куки. По умолчанию __default.

        Returns:
            ProductsData: список товаров.
        """
        params['token'] = await self._get_token()
        data = await self._get_start_products_page(params, cookies)
        total_pages = data['data']['total_pages']
        products = data['data']['goods']
        if total_pages == 1:
            return self._filter_products_data(products)
        products = await self._get_all_products_page(
            params, total_pages, products
        )
        return self._filter_products_data(products)

    def parsing(
        self,
        params: Params,
        cookies: dict[str, str] | object = __default,
    ) -> ProductsData:
        """Старт парсинга товаров.

        Args:
            params (Params): параметры запроса.
            cookies (dict[str, str] | object, optional):
                куки. По умолчанию __default.

        Returns:
            ProductsData: список товаров.
        """
        return asyncio.run(self._get_products(params, cookies))