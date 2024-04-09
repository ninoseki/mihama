from .api_model import APIModel


class Ecosystem(APIModel):
    name: str
    total: int


class Ecosystems(APIModel):
    ecosystems: list[Ecosystem]
    total: int
