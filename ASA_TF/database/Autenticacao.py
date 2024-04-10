import bcrypt
import uuid
import psycopg2
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi import Request

class Autenticacao:
    def __init__(self, conexao):
        self.conexao = conexao

    def verificar_login(self, email, senha, request: Request):
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE email=%s", (email,))
            hashed_senha_db = cursor.fetchone()

            if hashed_senha_db:
                if bcrypt.checkpw(senha.encode('utf-8'), hashed_senha_db[0].encode('utf-8')):
                    chave_sessao = str(uuid.uuid4())
                    ip_acesso = request.client.host
                    data_expiracao = datetime.now() + timedelta(days=1)

                    cursor.execute("UPDATE usuarios SET chave_sessao=%s, ip_acesso=%s, data_expiracao=%s WHERE email=%s",
                                   (chave_sessao, ip_acesso, data_expiracao, email))
                    connection.commit()

                    return True, {"chave_sessao": chave_sessao}
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email não encontrado")
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()

    def logout(self, chave_sessao):
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE usuarios SET chave_sessao = NULL, ip_acesso = NULL, data_expiracao = NULL WHERE chave_sessao = %s", (chave_sessao,))
            connection.commit()
            return True, "Logout realizado com sucesso"
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()

    def validar_sessao(self, chave_sessao, ip_acesso) -> bool:
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT ip_acesso, data_expiracao FROM usuarios WHERE chave_sessao = %s", (chave_sessao,))
            resultado = cursor.fetchone()
            if resultado is None:
                return False  # Chave de sessão não encontrada
            
            ip_registrado, data_expiracao = resultado
            if ip_registrado != ip_acesso:
                return False  # Endereço IP não corresponde
            
            if data_expiracao < datetime.now():
                return False  # Sessão expirou
            
            return True  # Sessão válida
        except psycopg2.Error as e:
            print("Erro ao executar a consulta:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()



