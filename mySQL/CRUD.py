import mysql.connector
from mysql.connector import Error
from conexao import *
from datetime import datetime
from views import *
from roles import atribuir_role


def check_login(con, login, senha): 
    cursor = con.cursor(buffered=True)  # Adiciona buffered=True (limpa o buffer do cursor)
    try:
        cursor.execute('''SELECT id, senha 
                          FROM usuario
                          WHERE login = %s''', (login,))
        informacoes = cursor.fetchone()  # Obtenha apenas uma linha

        # Verifique se o usuário foi encontrado e se a senha corresponde
        if informacoes is not None and informacoes[1] == senha:
            return True
        else:
            return False

    except mysql.connector.Error as e:
        print(f"Erro ao realizar login: {e}")
    finally:
        cursor.close()  # Feche o cursor apenas no final



def insere_instituicao(con, nome, endereco, causa_social,plano): # insere uma instituição
    cursor = con.cursor()
    try:
        cursor = con.cursor()
        sql = "INSERT INTO instituicao (nome, endereco, causa_social,id_plano) values (%s, %s, %s,%s)"
        valores = (nome, endereco, causa_social,plano)
        cursor.execute(sql, valores)
        cursor.close()
        con.commit() # dando commit pois foi feita uma alteração no banco de dados

        print(f"Instituição {nome} criada no MySQL e inserida na tabela insituição.\n")
 
    except mysql.connector.Error as e:
        print(f"Erro ao criar insituição no MySQL: {e}\n")
        con.rollback()  
 
    finally:
        cursor.close()


def insere_usuario(con, login, senha, email, data_ingresso, id_instituicao): 
    cursor = con.cursor()
    try:
        
        create_user_sql = "CREATE USER %s@'localhost' IDENTIFIED BY %s;"
        cursor.execute(create_user_sql, (login, senha,))
        alter_user_sql = '''ALTER USER %s@'localhost' IDENTIFIED WITH mysql_native_password BY %s;'''
        cursor.execute(alter_user_sql, (login, senha,))
        cursor.execute("FLUSH PRIVILEGES;")
            
        
        sql = "INSERT INTO usuario (login, senha, email, data_ingresso, id_instituicao) VALUES (%s, %s, %s, %s, %s)"
        valores = (login, senha, email, data_ingresso, id_instituicao)
        cursor.execute(sql, valores)
        con.commit()
        
        print(f"Usuário {login} criado no MySQL e inserido na tabela usuario.")

        print("Qual o role do novo usuario ?")
        print("1 - Usuario")
        print("2 - EMpresa")
        print("3 - ADM")
        escolha = input()
        atribuir_role(con,login,escolha)
        print("Usuário adicionado com sucesso!")

        

    except mysql.connector.Error as e:
        print(f"Erro ao criar o usuário no MySQL: {e}")
        con.rollback()  
    finally:
        cursor.close()


def insere_plano(con, nome, duracao, data_aquisicao, espaco_usuario): # insere um plano
    cursor = con.cursor()

    role = role_check(con,login)
    if (any('papelEmpresa' in i[0] for i in role) or any('papelUsuario' in i[0] for i in role)):
        print("Permissão negada para compartilhamento.\n")
        return

    try:
        sql = "INSERT INTO plano (nome, duracao, data_aquisicao, espaco_usuario) values (%s, %s, %s, %s)"
        valores = (nome, duracao, data_aquisicao, espaco_usuario)
        cursor.execute(sql, valores)
        con.commit() # dando commit pois foi feita uma alteração no banco de dados
 
        print(f"Plano {nome} criado no MySQL e inserido na tabela planos.\n")
 
    except mysql.connector.Error as e:
        print(f"Erro ao criar o usuário no MySQL: {e}")
        con.rollback()  
    finally:
        cursor.close()


def fazerComentario(con, id_arquivo, conteudo, id_usuario):
    cursor = con.cursor(buffered=True)

    role = role_check(con,login)
    if any('papelEmpresa' in i[0] for i in role):
        print("Empresa com permissão negada para compartilhamento.\n")
        return

    try:
        #obter data e hora
        data = datetime.now().date()
        hora = datetime.now().time()

        #inserir na tabela comentario
        cursor.execute(''' 
            INSERT INTO comentario(conteudo, id_arquivo, data_c, hora)
            VALUES (%s, %s, %s, %s)
        ''', (conteudo, id_arquivo, data, hora)) 

        con.commit()
        #obtem o id_comentario que é AUTO_INCREMENT
        id_comentario = cursor.lastrowid
        #insere id_usuario e d_comentario na tabela usuario_comentario
        cursor.execute(''' 
            INSERT INTO usuario_comentario (id_usuario, id_comentario)
            VALUES (%s, %s)
        ''', (id_usuario, id_comentario))
        con.commit()
        print("Comentário feito!\n")
    except mysql.connector.Error as e:
        print(f"Erro ao inserir comentario : {e}")
    finally:
        cursor.close()
        #confirmar a insercao
        
    
def remover_acesso(con,id_arquivo, id_compartilhamento):
    cursor = con.cursor()
    try:
        cursor.execute('''
            SELECT ID_us FROM Arquivo WHERE ID_arq = ?         
        ''', (id_arquivo))
        resultado = cursor.fetchone()

        if resultado:
            # O id_proprieário vai receber a primeria informação do fetchone(id_us)
            id_proprietario = resultado[0]

            cursor.execute('''
                DELETE FROM Compartilhamento
                WHERE ID_arq = ? AND ID_us <> ?               
            ''', (id_arquivo, id_proprietario))
            con.commit()

            print("Acessos removidos!")
        else:
            print("Arquivo não encontrado.")

    except mysql.connector.Error as e:
        print(f"Erro ao remover acessos: {e}")
    finally:
        cursor.close()
        
def pedir_suporte(con, id_arquivo, mensagem, login):
    cursor = con.cursor()

    role = role_check(con,login)
    if any('papelEmpresa' in i[0] for i in role):
        print("Empresa com permissão negada para compartilhamento.\n")
        return

    try:
        data_pedido = datetime.now().date() #pede data e hora atual
        hora_pedido = datetime.now().time()
        
        sql = """
            INSERT INTO suporte (id_arquivo, descricao, dia, hora)
            VALUES (%s, %s, %s, %s)
        """ #faz um pedido de suporte enviando uma mensagem, exemplo: não consigo acessar meu arquivo
        valores = (id_arquivo, mensagem, data_pedido, hora_pedido)
        cursor.execute(sql, valores)

        con.commit()

        #pega o id_suporte
        id_suporte = cursor.lastrowid
        #pega o id do usuario
        cursor.execute('''SELECT id FROM usuario WHERE login = %s ''', (login,))
        id_usuario = cursor.fetchone()
        #inserir na tabela usuario_suporte o id_usuario e id_supor  te

        if id_usuario:
            # Acessa o valor dentro da tupla para obter o id_usuario
            id_usuario = id_usuario[0]
            cursor.execute(''' INSERT INTO usuario_suporte (id_usuario, id_suporte)
                        VALUES (%s, %s)'''
                        ,(id_usuario, id_suporte,))
            con.commit()
            print("Pedido de suporte enviado com sucesso. Aguarde nosso retorno")
        else:
            print(f"Usuário {login} não encontrado.")

    except mysql.connector.Error as e:
        print(f"Erro: você não conseguiu enviar um pedido de suporte: {e}")
    finally:
        cursor.close()

import mysql.connector

def remover_arquivo(con, id_arquivo,login):
    cursor = con.cursor()

    role = role_check(con,login)
    if any('papelEmpresa' in i[0] for i in role):
        print("Empresa com permissão negada para compartilhamento.\n")
        return

    try:

        cursor.execute(''' SELECT id_usuario FROM arquivo WHERE id = %s ''',(id_arquivo,))
        id_usuario = cursor.fetchone()
        cursor.execute('''SELECT id FROM usuario WHERE login = %s''',(login,))
        id_login_usuario = cursor.fetchone()

        if id_usuario != id_login_usuario:
            print("Permissão negada. Apenas o dono pode remover o arquivo.\n")
        else:
            # Desabilita temporariamente as verificações de chaves estrangeiras
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

            
            cursor.execute('DELETE FROM arquivo WHERE id = %s', (id_arquivo,))
            cursor.execute('DELETE FROM comentario WHERE %s', (id_arquivo,))
            
            # Commit das alterações no banco
            con.commit()
            print("Arquivo e dependências removidos com sucesso!")

    except mysql.connector.Error as e:
        print(f"Erro ao remover o arquivo: {e}")
    finally:
        # Reabilita as verificações de chaves estrangeiras
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
        cursor.close()



# Exemplo de uso
# Supondo que você tenha uma conexão com o banco de dados chamada 'con'
# remover_arquivo_forcado(con, 1)  # Onde '1' é o ID do arquivo a ser removido


def adicionar_arquivo(con, nome, tipo, permissao_acesso, id_usuario, url):
    cursor = con.cursor()
    try:
        #NAO ACHO QUE PRECISA, MAS TRY EXEPT P VER SE USUARIO EXISTE OU NAO 
        cursor.execute("SELECT id FROM usuario WHERE id = %s", (id_usuario,))
        usuario_existe = cursor.fetchone()
        
        if usuario_existe:
            # INSERE ARQUIVO, CASO O USUARIO EXISTA
            sql = """
                INSERT INTO arquivo (nome, tipo, permissao_acesso, id_usuario, URL)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nome, tipo, permissao_acesso, id_usuario, url)
            cursor.execute(sql, valores)
            con.commit()
            print("Arquivo adicionado com sucesso!\n")
            
        else:
            print("Usuário não encontrado. Verifique o ID do usuário.\n")
        #CASO DER ERRO
    except mysql.connector.Error as e:
        print(f"Erro ao adicionar arquivo: {e}\n")
    
    finally:
        cursor.close()

def acessar_arquivo(con, nome_arquivo):
    cursor = con.cursor()
    try:
        
        cursor.execute('''SELECT id, permissao_acesso FROM arquivo WHERE nome = %s''', (nome_arquivo,))
        id_arquivo = cursor.fetchone()

        if id_arquivo is None:
            print(f"Arquivo '{nome_arquivo}' não encontrado.")
            return

       
        id, permissao_acesso = id_arquivo

        
        if permissao_acesso in ("publi", "publi/compa", "priv/compa"):
           
            cursor.execute('''SELECT nome, tipo, url, id_usuario FROM arquivo WHERE id = %s''', (id,))
            arquivo_info = cursor.fetchone()

            if arquivo_info:
                print("Informações do arquivo:")
                print(f"Nome: {arquivo_info[0]}")
                print(f"Tipo: {arquivo_info[1]}")
                print(f"URL: {arquivo_info[2]}")
                print(f"ID do Usuário: {arquivo_info[3]}")
            else:
                print(f"Arquivo com ID {id} não encontrado.")
        else:
            print(f"Usuário não tem acesso ao arquivo '{nome_arquivo}'.")
    except mysql.connector.Error as e:
        print(f"Erro ao procurar arquivo: {e}")
    finally:
        cursor.close()



from datetime import datetime, date

def verificacaoDe100Dias(con, id_arquivo):
    cursor = con.cursor()
    try:
        sql = "SELECT ultima_versao FROM ATIVIDADES_RECENTES WHERE id_arquivo = %s"  # vê a data de modificação pelo id do arq
        cursor.execute(sql, (id_arquivo,))
        resultado = cursor.fetchone()

        if resultado is None:  # verifica se o arquivo existe
            cursor.close()
            raise ValueError("Arquivo não encontrado!\n")
        
        data_modificacao = resultado[0]

        # Verifica se a data de modificação é do tipo datetime.date
        if not isinstance(data_modificacao, date):  
            cursor.close()
            raise TypeError("A data de modificação não é um datetime.date")
        
        diferenca_dias = (datetime.now().date() - data_modificacao).days  # calcula a diferença dos dias
        cursor.close()
        return diferenca_dias > 100
    except mysql.connector.Error as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()



def role_check(con, login):
    #função que checa os grants do usuario
    cursor = con.cursor()
    try:
        cursor.execute(f"SHOW GRANTS FOR '{login}'@'localhost';")
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as e:
        print(f"Erro ao checar grants arquivo: {e}")

    finally:
        cursor.close()


def compartilhar(con, id_arquivo, id_usuario_dono, id_usuario_compartilhado,login):
    cursor = con.cursor()

    role = role_check(con,login)
    if any('papelEmpresa' in i[0] for i in role):
        print("Empresa com permissão negada para compartilhamento.\n")
        return

    try:
        cursor.execute("SELECT id FROM arquivo WHERE id = %s AND id_usuario = %s", (id_arquivo, id_usuario_dono))
        arquivo_existe = cursor.fetchone()

        if arquivo_existe != None:
            sql = """
                INSERT INTO compartilhamento (id_arquivo, id_dono, id_compartilhado, data_c)
                VALUES (%s, %s, %s, %s)
            """
            data_compartilhamento = datetime.now().date()
            valores = (id_arquivo, id_usuario_dono, id_usuario_compartilhado, data_compartilhamento)
            cursor.execute(sql, valores)
            con.commit()
            print("Arquivo compartilhado com sucesso!")

            id_c = '''
                SELECT id FROM compartilhamento WHERE id_arquivo = %s AND id_compartilhado = %s
            '''
            cursor.execute(id_c, (id_arquivo, id_usuario_compartilhado))
            id_compartilhamento = cursor.fetchone()[0]

            sql = '''
                INSERT INTO usuario_compartilhamento (id_usuario, id_compartilhamento)
                VALUES(%s,%s)
            '''
            valoresIII = (id_usuario_compartilhado, id_compartilhamento)
            cursor.execute(sql,valoresIII)
            con.commit()
        else:
            print("Arquivo nao encontrado ou permissão negada (id não é o dono!\n)")
    
    except mysql.connector.Error as e:
        print(f"Erro ao compartilhar arquivo: {e}")
    
    finally:
        cursor.close()

def visualizar_atividades_R(con, login):
    cursor = con.cursor()
    
    # Verificar se a função role_check está funcionando corretamente
    role = role_check(con, login)  # Passando a conexão para a função
    
    # Verificar se a conexão foi feita corretamente e o papel do usuário
    if login == "root" or any('papelADM' in i[0] for i in role):
        try:
            sql = "SELECT id_arquivo, ultima_versao, acesso FROM atividades_recentes"
            cursor.execute(sql)
            print("\nAtividades Recentes:\n")
            for (id_arquivo, ultima_versao, acesso) in cursor:
                print(f"{id_arquivo} | {ultima_versao} | {acesso}")
            print("")
        except Exception as e:
            print(f"Erro ao visualizar atividades recentes! Detalhes: {e}\n")
        finally:
            cursor.close()
    else:
        print("Erro: acesso negado!\n")


def alterar_url_arquivo(con, id_arquivo, nova_url):
    cursor = con.cursor()
    try:
        # Verifica se o arquivo existe
        cursor.execute('SELECT id FROM arquivo WHERE id = %s', (id_arquivo,))
        valor = cursor.fetchone()

        if valor:
            # Atualiza a URL do arquivo
            cursor.execute('UPDATE arquivo SET URL = %s WHERE id = %s', (nova_url, id_arquivo))
            con.commit()
            print("URL do arquivo atualizada com sucesso!")
        else:
            print("Arquivo não encontrado")
    
    except mysql.connector.Error as e:
        print(f"Erro ao alterar a URL do arquivo: {e}")
    finally:
        cursor.close()

def alterar_tipo_arquivo(con, id_arquivo, novo_tipo):
    cursor = con.cursor()
    try:
        # Verifica se o arquivo existe
        cursor.execute('SELECT id FROM arquivo WHERE id = %s', (id_arquivo,))
        valor = cursor.fetchone()

        if valor:
            # Atualiza a URL do arquivo
            cursor.execute('UPDATE arquivo SET tipo = %s WHERE id = %s', (novo_tipo, id_arquivo))
            con.commit()
            print("Tipo do arquivo atualizada com sucesso!")
        else:
            print("Arquivo não encontrado")
    
    except mysql.connector.Error as e:
        print(f"Erro ao alterar o tipo do arquivo: {e}")
    finally:
        cursor.close()

def get_id(con, login):
    cursor = con.cursor()
    cursor.execute("SELECT id FROM usuario WHERE login = %s", (login,)) # busca o id do usuário com base no login
    resultado = cursor.fetchone()
    return resultado[0]
