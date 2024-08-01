from pydantic import BaseModel


class LivroSchema(BaseModel):
    titulo: str
    ano: int
    romancista_id: int


class LivroUpdate(BaseModel):
    titulo: str | None = None
    ano: int | None = None
    romancista_id: int | None = None


class LivroPublic(LivroSchema):
    id: int


class LivroList(BaseModel):
    livros: list[LivroPublic]
