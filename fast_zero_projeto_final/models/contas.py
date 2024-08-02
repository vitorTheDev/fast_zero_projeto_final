from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_zero_projeto_final.models.livros import Livro
from fast_zero_projeto_final.models.registry import table_registry
from fast_zero_projeto_final.models.romancistas import Romancista


@table_registry.mapped_as_dataclass
class Conta:
    __tablename__ = 'contas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    senha: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    romancistas: Mapped[list['Romancista']] = relationship(
        init=False, cascade='all, delete-orphan'
    )
    livros: Mapped[list['Livro']] = relationship(
        init=False, cascade='all, delete-orphan'
    )
