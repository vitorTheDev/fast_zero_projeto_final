from fastapi import FastAPI

from fast_zero_projeto_final.routers import auth, contas

app = FastAPI()

app.include_router(auth.router)
app.include_router(contas.router)
