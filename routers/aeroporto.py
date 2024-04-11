from fastapi import APIRouter, HTTPException, status, Request
from schemas.aeroporto import Aeroporto
from database.Conexao import Conexao
from database.Aeroporto import Aeroporto
from database.Autenticacao import Autenticacao


router = APIRouter()

# instancia dos objetos das classes
conexao = Conexao(host="trabalhoasa.postgresql.dbaas.com.br", user="trabalhoasa", password="Asa2024!", database="trabalhoasa")
aeroporto = Aeroporto(conexao)
autenticacao = Autenticacao(conexao)


# retorna os aeroportos quando a chave de sessao eh valida
@router.get("/aeroportos/{chave_sessao}")
def obter_aeroportos(request: Request, chave_sessao: str):
    ip_acesso = request.client.host # pega o ip atraves do request
    if not autenticacao.validar_sessao(chave_sessao, ip_acesso): # se retornar false:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
    aeroportos = aeroporto.obter_aeroportos()
    if aeroportos:
        return {"aeroportos": aeroportos}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao obter aeroportos")

# retorna os aeroportos por origem quando a chave de sessao eh valida
@router.get("/aeroportos-por-origem/{codigo_origem}/{chave_sessao}")
def obter_aeroportos_por_origem(codigo_origem: str, request: Request, chave_sessao: str):
    ip_acesso = request.client.host
    if not autenticacao.validar_sessao(chave_sessao, ip_acesso):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
    aeroportos_por_origem = aeroporto.obter_aeroportos_por_origem(codigo_origem)
    if aeroportos_por_origem:
        return {"aeroportos_por_origem": aeroportos_por_origem}
    else:
        raise HTTPException(status_code=404, detail="Nenhum aeroporto de destino encontrado para o aeroporto de origem fornecido")