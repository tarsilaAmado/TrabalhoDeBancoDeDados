from conexao import *
from roles import *
from views import *
from CRUD import *

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
        WHERE id = %s
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
            print(f"Prioridade do arquivo {id_arquivo} atualizada para '{nova_prioridade}'.\n")
        else:
            print(f"Arquivo não encontrado.\n")
    except mysql.connector.Error as err:
        print(f"Erro ao chavear prioridade: {err}\n")
    finally:
        cursor.close()



def remover_acessos(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()

        # Verificar o proprietário do arquivo
        query_proprietario = """
        SELECT id_usuario
        FROM arquivo
        WHERE id = %s
        """
        cursor.execute(query_proprietario, (id_arquivo,))
        resultado = cursor.fetchone()

        if resultado:
            id_proprietario = resultado[0]

            # Remover todos os acessos, exceto do proprietário
            query_remover = """
            DELETE FROM compartilhamento
            WHERE id = %s AND id_compartilhado != %s
            """
            cursor.execute(query_remover, (id_arquivo, id_proprietario))
            conexao.commit()
            print(f"Acessos ao arquivo {id_arquivo} foram removidos, exceto do proprietário (ID {id_proprietario}).\n")
        else:
            print(f"Arquivo não encontrado.\n")
    except mysql.connector.Error as err:
        print(f"Erro ao remover acessos: {err}\n")
    finally:
        cursor.close()
