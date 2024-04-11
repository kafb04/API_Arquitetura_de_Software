import bcrypt
import uuid
import psycopg2
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request

class Autenticacao:
    def __init__(self, conexao):
        self.conexao = conexao

    # metodo para realizar o login
    def verificar_login(self, email, senha, request: Request):
        # estabelecendo conexao
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE email=%s", (email,))
            hashed_senha_db = cursor.fetchone() #pega a senha criptografada

            if hashed_senha_db:
                if bcrypt.checkpw(senha.encode('utf-8'), hashed_senha_db[0].encode('utf-8')): # verifica se a senha fornecida eh a mesma que a senha criptografada
                    chave_sessao = str(uuid.uuid4()) # gera uma chave de sessao
                    ip_acesso = request.client.host # pega o ip do cliente
                    data_expiracao = datetime.now() + timedelta(days=1)

                    cursor.execute("UPDATE usuarios SET chave_sessao=%s, ip_acesso=%s, data_expiracao=%s WHERE email=%s",
                                   (chave_sessao, ip_acesso, data_expiracao, email))
                    connection.commit() #confirmando a operacao no banco

                    return True, {"chave_sessao": chave_sessao} # retorna a chave de sessao
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha inválida")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email não encontrado")
        
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()

    # metodo para realizar o logout
    def logout(self, chave_sessao): # recebe uma chave de sessao valida
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE usuarios SET chave_sessao = NULL, ip_acesso = NULL, data_expiracao = NULL WHERE chave_sessao = %s", (chave_sessao,)) # Limpa os campos que sao referentes a uma sessao
            connection.commit()
            return True, {"mensagem": "Logout realizado com sucesso"}
        
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()

    # metodo para verificar se a sessao esta valida
    def validar_sessao(self, chave_sessao, ip_acesso):
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT ip_acesso, data_expiracao FROM usuarios WHERE chave_sessao = %s", (chave_sessao,))
            resultado = cursor.fetchone() #retorna uma tupla com ip_acesso no index = 0 e data_expiracao no index = 1
            if resultado is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave de sessão não encontrada")
            
            ip_registrado, data_expiracao = resultado # atribui automaticamente ip_registrado = resultado[0] e data_expiracao = resultado[1]
            if ip_registrado != ip_acesso:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="IP de acesso sem sessão")
            
            if data_expiracao < datetime.now():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão expirou")
            
            return True, {"mensagem": "Sessão válida"} # Sessão válida
        
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()



