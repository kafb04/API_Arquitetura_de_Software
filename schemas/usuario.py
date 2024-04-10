from pydantic import BaseModel

class Usuario(BaseModel):
    email: str
    senha: str