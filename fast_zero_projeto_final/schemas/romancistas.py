from pydantic import BaseModel, Field


class RomancistaSchema(BaseModel):
    nome: str = Field(max_length=255)


class RomancistaUpdate(BaseModel):
    nome: str | None = Field(max_length=255, default=None)


class RomancistaPublic(RomancistaSchema):
    id: int


class RomancistaList(BaseModel):
    romancistas: list[RomancistaPublic]
