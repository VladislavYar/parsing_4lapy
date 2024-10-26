import asyncio

from parser import Parser
from config import Config
from command_line import parser_command_line


async def main() -> None:
    arg_parser = parser_command_line()
    args = arg_parser.parse_args()
    params = {
        'count': Config.COUNT,
        'page': Config.PAGE,
        'sort': args.sort,
        'category_id': args.category,
    }
    await asyncio.gather(
        *[
            Parser().parsing(params, city, coockie)
            for city, coockie in Config.COOKIE_SITIES.items()
        ]
    )


if __name__ == '__main__':
    asyncio.run(main())
