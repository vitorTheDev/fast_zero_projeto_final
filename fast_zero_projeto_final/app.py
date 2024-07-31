from fastapi import FastAPI

from fast_zero_projeto_final.routers import contas

app = FastAPI()

app.include_router(contas.router)
