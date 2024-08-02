from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from fast_zero_projeto_final.models.romancistas import Romancista


def checarRomancista(session, conta, romancista_id):
    romancista = session.scalar(
        select(Romancista).where(
            Romancista.conta_id == conta.id, Romancista.id == romancista_id
        )
    )

    if not romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    return romancista
