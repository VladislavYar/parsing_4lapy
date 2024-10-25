type PackingVariants = list[
    int
    | str
    | dict[str, str | int | bool | None | dict[str, str | int] | list[int]]
]
type ResponseProducts = list[
    dict[str, str | int | bool | None | dict[str, str | int] | PackingVariants]
]
type ResponseData = dict[dict[str, ResponseProducts | int] | list]
type ProductsData = list[dict[str, str | list[dict[str, str | int]]]]
type Params = dict[str, str | int]
type PriceAndStatus = list[
    dict[str, int | list[dict[str, str | int | bool | dict[str, int]]]]
]
