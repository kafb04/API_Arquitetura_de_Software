from pydantic import BaseModel

class Aeroporto(BaseModel):
    codigo: str
    nome: str
    cidade: str
    estado: str