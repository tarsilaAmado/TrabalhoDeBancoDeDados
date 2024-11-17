from conexao import *
from roles import *
from views import *
from CRUD import *

def chavear(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        query_selecionar = """
        SELECT acesso
        FROM atividades_recentes
        WHERE id_arquivo = %s
        """
        cursor.execute(query_selecionar, (id_arquivo,))
        prioridade_atual = cursor.fetchone()
       
        if prioridade_atual:
            nova_prioridade = "não prioritário" if prioridade_atual[0] == "prioritário" else "prioritário"
            query_atualizar = """
            UPDATE atividades_recentes
            SET acesso = %s
            WHERE id_arquivo = %s
            """
            cursor.execute(query_atualizar, (nova_prioridade, id_arquivo))
            conexao.commit()
            print(f"Prioridade do arquivo {id_arquivo} atualizada para '{nova_prioridade}'.")
        else:
            print(f"Arquivo não encontrado.")
    except mysql.connector.Error as err:
        print(f"Erro ao chavear prioridade: {err}")
    finally:
        cursor.close()
 
def verificar_atividades(conexao):
    try:
        cursor = conexao.cursor()
        query = """
        UPDATE atividades_recentes
        SET ultima_versao = CURDATE()
        """
        cursor.execute(query)
        conexao.commit()
        print("Tabela 'atividades_recentes' atualizada com a data atual!\n")
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar atividades: {err}\n")
    finally:
        cursor.close()



def conta_usuarios(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        query = """
        SELECT COUNT(DISTINCT id_compartilhado) AS total_usuarios
        FROM compartilhamento
        WHERE id_arquivo = %s
        """
        cursor.execute(query, (id_arquivo,))
        resultado = cursor.fetchone()
        if resultado:
            print(f"Total de usuários com acesso ao arquivo {id_arquivo}: {resultado[0]}")
            return resultado[0]
        else:
            print(f"Arquivo {id_arquivo} não possui usuários com acesso.\n")
            return 0
    except mysql.connector.Error as err:
        print(f"Erro ao contar usuários: {err}\n")
    finally:
        cursor.close()
