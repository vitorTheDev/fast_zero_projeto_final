from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from fast_zero_projeto_final.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Romancista:
    __tablename__ = 'romancistas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))

    conta_id: Mapped[int] = mapped_column(
        ForeignKey('contas.id', ondelete='cascade', onupdate='cascade')
    )
