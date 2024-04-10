from fastapi import FastAPI
from routers import autenticacao, aeroporto, voos

# Criar uma instância da aplicação FastAPI
app = FastAPI()
app.include_router(autenticacao.router)
app.include_router(aeroporto.router)
app.include_router(voos.router)
