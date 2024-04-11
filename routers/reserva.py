from fastapi import APIRouter, HTTPException, status, Request
from database.Conexao import Conexao
from database.Reserva import Reserva
from database.Autenticacao import Autenticacao

router = APIRouter()

# instancia dos objetos das classes
conexao = Conexao(host="trabalhoasa.postgresql.dbaas.com.br", user="trabalhoasa", password="Asa2024!", database="trabalhoasa")
reserva = Reserva(conexao)
autenticacao = Autenticacao(conexao)


@router.post("/compra/{codigo_voo}/{qtd_passageiros}/{chave_sessao}")
def efetuar_compra(codigo_voo: str, qtd_passageiros: int, chave_sessao: str, request: Request):
    ip_acesso = request.client.host
    if not autenticacao.validar_sessao(chave_sessao, ip_acesso): # se retornar false:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
    dados_reserva = reserva.efetuar_compra(codigo_voo, qtd_passageiros)
    if dados_reserva is not None:
        return {"dados_reserva": dados_reserva}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao efetuar a compra")

