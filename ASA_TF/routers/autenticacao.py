from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas.usuario import Usuario
from database.Conexao import Conexao
from database.Autenticacao import Autenticacao

router = APIRouter()

conexao = Conexao(host="trabalhoasa.postgresql.dbaas.com.br", user="trabalhoasa", password="Asa2024!", database="trabalhoasa")
autenticacao = Autenticacao(conexao)

@router.post("/login")
def login(usuario: Usuario, request: Request):
    sucesso, mensagem = autenticacao.verificar_login(usuario.email, usuario.senha, request)
    if sucesso:
        return mensagem
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=mensagem)

@router.post("/logout")
def logout(chave_sessao: str):
    sucesso, mensagem = autenticacao.logout(chave_sessao)
    if sucesso:
        return mensagem
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mensagem)
    

@router.post("/validar-sessao")
def validar_sessao(chave_sessao: str, ip_acesso: str):
    sessao_valida = autenticacao.validar_sessao(chave_sessao, ip_acesso)
    if sessao_valida:
        return {"mensagem": "Sessão válida"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida")
        

