from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from database.Conexao import Conexao
from database.Voos import Voos

router = APIRouter()

conexao = Conexao(host="trabalhoasa.postgresql.dbaas.com.br", user="trabalhoasa", password="Asa2024!", database="trabalhoasa")
voos = Voos(conexao)

@router.get("/voos/{data}")
def obter_voos(data: str):
    try:
        data_formatada = datetime.strptime(data, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato dd-mm-yyyy")
    
    voos_data = voos.obter_voos(data_formatada)
    if voos_data:
        return {"voos": voos_data}
    else:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para a data fornecida")

@router.get("/voos/pesquisar/{data}/{numero_passageiros}")
def pesquisar_voos(data: str, numero_passageiros: int):
    try:
        data_formatada = datetime.strptime(data, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato dd-mm-yyyy")
    
    voos_data = voos.pesquisar_voos(data_formatada, numero_passageiros)
    if voos_data:
        return {"voos": voos_data}
    else:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para a data e número de passageiros fornecidos")