from pydantic import BaseModel


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaUpdate(BaseModel):
    nome: str | None = None


class RomancistaPublic(RomancistaSchema):
    id: int


class RomancistaList(BaseModel):
    romancistas: list[RomancistaPublic]
