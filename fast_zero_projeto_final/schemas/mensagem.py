from pydantic import BaseModel


class Mensagem(BaseModel):
    message: str
