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
 
