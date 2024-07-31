from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from fast_zero_projeto_final.models.registry import table_registry


@table_registry.mapped_as_dataclass
class Conta:
    __tablename__ = 'contas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    # todos: Mapped[list['Todo']] = relationship(
    #     init=False, cascade='all, delete-orphan'
    # )
