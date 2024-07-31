from pydantic import BaseModel, ConfigDict, EmailStr


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class ContaPublico(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class ContaLista(BaseModel):
    contas: list[ContaPublico]
