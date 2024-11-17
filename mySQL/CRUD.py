import mysql.connector
from mysql.connector import Error
from conexao import *
from datetime import datetime
from views import *
from roles import *

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
        sql = "INSERT INTO instituicao (nome, endereco, causa_social,plano) values (%s, %s, %s,%s)"
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
        debug = atribuir_role(con,login,escolha)
        #debug
        
        
        #fim do debug
        print("Usuário adicionado com sucesso!")

        

    except mysql.connector.Error as e:
        print(f"Erro ao criar o usuário no MySQL: {e}")
        con.rollback()  
    finally:
        cursor.close()


def insere_plano(con, nome, duracao, data_aquisicao, espaco_usuario): # insere um plano
    cursor = con.cursor()
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

def inserir_adm(con, login):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT id FROM usuario WHERE login = %s", (login,))  # busca o id do usuário com base no login
        resultado = cursor.fetchone()
        
        if resultado:
            id_usuario = resultado[0]
            cursor.execute("INSERT INTO adm (id) VALUES (%s)", (id_usuario,))  # insere o id do usuário na tabela adm
            con.commit()

            # Obtém o id do novo administrador inserido
            cursor.execute("SELECT id FROM adm WHERE id = %s", (id_usuario,))
            id_adm = cursor.fetchone()[0]

            # Insere na tabela usuario_adm
            cursor.execute(
                "INSERT INTO usuario_adm (id_usuario, id_adm) VALUES (%s, %s)",
                (id_usuario, id_adm)
            )
            con.commit()
            print("Administrador inserido com sucesso e vinculado ao usuário.")
        else:
            print("Erro: usuário com o login especificado não encontrado.")
            
    except mysql.connector.Error as e:
        print(f"Erro ao inserir administrador: {e}")
    finally:
        cursor.close()

def fazerComentario(con, id_arquivo, conteudo, login):
    cursor = con.cursor(buffered=True)
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
        #obtem o id_usuario
        cursor.execute('''SELECT id FROM usuario WHERE login = %s ''', (login,))
        id_usuario = cursor.fetchone()
        #insere id_usuario e d_comentario na tabela usuario_comentario
        if id_usuario:
            cursor.execute(''' 
                INSERT INTO usuario_comentario (id_usuario, id_comentario)
                VALUES (%s, %s)
            ''', (id_usuario[0], id_comentario))
            con.commit()
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

def remover_arquivo(con, id_arquivo):
    cursor = con.cursor()
    try:
        sql = '''
        SELECT id FROM arquivo WHERE id = %s
    '''
        cursor.execute(sql,(id_arquivo,))
        valor = cursor.fetchone()

        if valor:
            sql_deletar = '''
            DELETE FROM arquivo WHERE id = %s 
        '''
            cursor.execute(sql_deletar, (id_arquivo,))
            con.commit()
            print("Arquivo removido com sucesso!")
        else:
            print("Arquivo não econtrado")
    
    except mysql.connector.Error as e:
        print(f"Erro ao remover o arquivo: {e}")
    finally:
        cursor.close()

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

def acessar_arquivo(con,nome_arquivo):
    cursor = con.cursor()
    try:

        
        #pega o id do arquivo e procura ele pelo nome do arquivo
        cursor.execute('''SELECT id, permissao_acesso FROM arquivo WHERE nome = %s 
                       ''',(nome_arquivo,))

        id_arquivo = cursor.fetchone()
        acessar_arquivos_usuario(con,id_arquivo)
        #pega a permissao de acesso
        permissao_acesso = cursor.fetchone(1)
        #faz o check se o usuario tem acesso
        if permissao_acesso == "público" or permissao_acesso == "público/compartilhado" or permissao_acesso == "privado/compartilhado": 
            #usando o id_arquivo faz os select necessarios
            cursor.execute(''' SELECT nome, tipo, url, id_usuario FROM arquivo WHERE id = %s'''(id_arquivo,))

        else :
            print(f"Usuario não tem acesso a arquivo {id_arquivo}")
    except mysql.connector.Error as e:
        print(f"Erro ao procurar arquivo : {e}")

    finally:
        cursor.close()


def verificacaoDe100Dias(con, id_arquivo):
    cursor = con.cursor()
    try:
        sql = "SELECT ultima_versao FROM ATIVIDADES_RECENTES WHERE id_arquivo = %s" #vê a data de modificaçõ pelo id do arq
        cursor.execute(sql, (id_arquivo,))
        resultado = cursor.fetchone()
        if resultado is None: #verifica se o arquivo existe
            cursor.close()
            raise ValueError("Arquivo não encontrado!\n")
        data_modificacao = resultado[0]
        if not isinstance(data_modificacao, datetime): # faz uma verificação para ver se tá em datetime
            cursor.close()
            raise TypeError("A data de modificação não é um datetime")
        diferenca_dias = (datetime.now() - data_modificacao).days #calcula a diferença dos dias da data atual até a ultima mod
        cursor.close()
        return diferenca_dias > 100
    except mysql.connector.Error as e:
        print(f"Erro: {e}")
    finally:
            cursor.close()

def compartilhar(con, id_arquivo, id_usuario_dono, id_usuario_compartilhado):
    cursor = con.cursor()
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
            print(" Arquivo nao encontrado.")
    
    except mysql.connector.Error as e:
        print(f"Erro ao compartilhar arquivo: {e}")
    
    finally:
        cursor.close()


def visualizar_atividades_R (con,login):
    cursor = con.cursor()
    role = role_check(login)
    if login == "root" or any('papelADM' in i[0] for i in role):
        try:
            sql = "SELECT id_arquivo, ultima_versao, acesso FROM atividades_recentes"
            cursor.execute(sql)
            print("")
            for (id_arquivo, ultima_versao, acesso) in cursor:
                print(id_arquivo, "| ", ultima_versao, "| ", acesso)
            print("")
        except:
            print("Erro ao visualizar atividades recentes!\n")
        finally:
            cursor.close()
    else:
        print("Erro: acesso negado!\n")

def get_id(con, login):
    cursor = con.cursor()
    cursor.execute("SELECT id FROM usuario WHERE login = %s", (login,)) # busca o id do usuário com base no login
    resultado = cursor.fetchone()
    return resultado[0]

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
        
        
