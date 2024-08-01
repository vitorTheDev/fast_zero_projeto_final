from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_zero_projeto_final.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str]
    ano: Mapped[int]

    romancista_id: Mapped[int] = mapped_column(ForeignKey('romancistas.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('contas.id'))

