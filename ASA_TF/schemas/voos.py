from pydantic import BaseModel

class Voo(BaseModel):
    id: int
    rota_id: int
    codigo_voo: str
    data: str
    horario: str
    tarifa: float