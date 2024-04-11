from fastapi import APIRouter, HTTPException, Depends, status, Request
from datetime import datetime
from database.Conexao import Conexao
from database.Voos import Voos
from database.Autenticacao import Autenticacao


router = APIRouter()

# instancia dos objetos das classes
conexao = Conexao(host="trabalhoasa.postgresql.dbaas.com.br", user="trabalhoasa", password="Asa2024!", database="trabalhoasa")
voos = Voos(conexao)
autenticacao = Autenticacao(conexao)

@router.get("/voos/{data}/{chave_sessao}")
def obter_voos(data: str, request: Request, chave_sessao: str):
    ip_acesso = request.client.host
    if not autenticacao.validar_sessao(chave_sessao, ip_acesso):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
    try:
        # formatando data para fazermos a entrada no estilo: 05-12-2024
        data_formatada = datetime.strptime(data, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato dd-mm-yyyy")
    
    voos_data = voos.obter_voos(data_formatada)
    if voos_data:
        return {"voos": voos_data}
    else:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para a data fornecida")

@router.get("/voos/pesquisar/{data}/{numero_passageiros}/{chave_sessao}")
def pesquisar_voos(data: str, numero_passageiros: int, request: Request, chave_sessao = str):
    ip_acesso = request.client.host
    if not autenticacao.validar_sessao(chave_sessao, ip_acesso):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
    try:
        # formatando data para fazermos a entrada no estilo: 05-12-2024
        data_formatada = datetime.strptime(data, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato dd-mm-yyyy")
    
    voos_data = voos.pesquisar_voos(data_formatada, numero_passageiros)
    if voos_data:
        return {"voos": voos_data}
    else:
        raise HTTPException(status_code=404, detail="Nenhum voo encontrado para a data e número de passageiros fornecidos")