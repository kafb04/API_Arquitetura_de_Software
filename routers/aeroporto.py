from fastapi import APIRouter, HTTPException, status, Depends
from database.Conexao import Conexao
from database.Aeroporto import Aeroporto

router = APIRouter()

conexao = Conexao(host="trabalhoasa.postgresql.dbaas.com.br", user="trabalhoasa", password="Asa2024!", database="trabalhoasa")
aeroporto = Aeroporto(conexao)

@router.get("/aeroportos")
def obter_aeroportos():
    aeroportos = aeroporto.obter_aeroportos()
    if aeroportos:
        return {"aeroportos": aeroportos}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao obter aeroportos")

@router.get("/aeroportos-por-origem/{codigo_origem}")
def obter_aeroportos_por_origem(codigo_origem: str):
    aeroportos_por_origem = aeroporto.obter_aeroportos_por_origem(codigo_origem)
    if aeroportos_por_origem:
        return {"aeroportos_por_origem": aeroportos_por_origem}
    else:
        raise HTTPException(status_code=404, detail="Nenhum aeroporto de destino encontrado para o aeroporto de origem fornecido")