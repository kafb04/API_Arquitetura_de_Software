from fastapi import FastAPI
from routers import autenticacao, aeroporto, voos, reserva

# Criar uma instância da aplicação de FastAPI
app = FastAPI()
app.include_router(autenticacao.router)
app.include_router(aeroporto.router)
app.include_router(voos.router)
app.include_router(reserva.router)
