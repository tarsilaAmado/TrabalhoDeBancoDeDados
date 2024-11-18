from conexao import *
from roles import *
from views import *
from CRUD import *

def verificar_atividades(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("CALL verificar_atividades();")
        conexao.commit()
        print("Tabela 'atividades_recentes' atualizada com a data atual!\n")
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar atividades: {err}\n")
    finally:
        cursor.close()



def conta_usuarios(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()
        args = (id_arquivo, 0)  # 0 é um placeholder para o parâmetro OUT
        
        cursor.callproc('conta_usuarios_por_arquivo', args)
        
        for result in cursor.stored_results():
            total_usuarios = result.fetchall()[0][0]
        
        print(f"Total de usuários com acesso ao arquivo {id_arquivo}: {total_usuarios}")
        return total_usuarios
    except mysql.connector.Error as err:
        print(f"Erro ao contar usuários: {err}\n")
    finally:
        cursor.close()



def chavear(conexao, id_arquivo,login):
    try:
        cursor = conexao.cursor()
        
        cursor.execute(''' SELECT id_usuario FROM arquivo WHERE id = %s ''',(id_arquivo,))
        id_usuario = cursor.fetchone()
        cursor.execute('''SELECT id FROM usuario WHERE login = %s''',(login,))
        id_login_usuario = cursor.fetchone()

        if id_usuario != id_login_usuario:
            print("Permissão negada. Apenas o dono pode alterar o arquivo.\n")
        else:
            # Chama a procedure
            cursor.callproc('chavear_prioridade', (id_arquivo,))
            
            print(f"Prioridade do arquivo {id_arquivo} foi alternada com sucesso.\n")
            conexao.commit()

    except mysql.connector.Error as err:
        if "Arquivo não encontrado" in str(err):
            print(f"Arquivo {id_arquivo} não encontrado.\n")
        else:
            print(f"Erro ao chavear prioridade: {err}\n")
    finally:
        cursor.close()



def remover_acessos(conexao, id_arquivo):
    try:
        cursor = conexao.cursor()

        # Chama a procedure
        cursor.callproc('remover_acessos', (id_arquivo,))
        
        print(f"Acessos ao arquivo {id_arquivo} foram removidos, exceto do proprietário.\n")
        conexao.commit()
    except mysql.connector.Error as err:
        if "Arquivo não encontrado" in str(err):
            print(f"Arquivo {id_arquivo} não encontrado no banco de dados.\n")
        else:
            print(f"Erro ao remover acessos: {err}\n")
    finally:
        cursor.close()
