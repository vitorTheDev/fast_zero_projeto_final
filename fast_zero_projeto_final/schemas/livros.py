from pydantic import BaseModel, Field


class LivroSchema(BaseModel):
    titulo: str = Field(max_length=500)
    ano: int
    romancista_id: int


class LivroUpdate(BaseModel):
    titulo: str | None = Field(max_length=500, default=None)
    ano: int | None = None
    romancista_id: int | None = None


class LivroPublic(LivroSchema):
    id: int


class LivroList(BaseModel):
    livros: list[LivroPublic]
