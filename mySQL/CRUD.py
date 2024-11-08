import mysql.connector
from mysql.connector import Error
from conexao import criar_conexao
import datetime

def insere_instituicao(con, nome, endereco, causa_social): # insere uma instituição
    cursor = con.cursor()
    sql = "INSERT INTO instituicao (nome, endereco, causa_social) values (%s, %s, %s)"
    valores = (nome, endereco, causa_social)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit() # dando commit pois foi feita uma alteração no banco de dados

def insere_usuario(con, login, senha, email, data_ingresso, id_instituicao): # insere um usuário
    cursor = con.cursor()
    sql = "INSERT INTO usuario (login, senha, email, data_ingresso, id_instituicao) values (%s, %s, %s, %s, %s)"
    valores = (login, senha, email, data_ingresso, id_instituicao)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit() # dando commit pois foi feita uma alteração no banco de dados

def insere_plano(con, nome, duracao, data_aquisicao, espaco_usuario): # insere um plano
    cursor = con.cursor()
    sql = "INSERT INTO plano (nome, duracao, data_aquisicao, espaco_usuario) values (%s, %s, %s, %s)"
    valores = (nome, duracao, data_aquisicao, espaco_usuario)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit() # dando commit pois foi feita uma alteração no banco de dados

def inserir_adm(con, login):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT id FROM usuario WHERE login = %s", (login,)) # busca o id do usuário com base no login
        resultado = cursor.fetchone()
        
        if resultado:
            id_usuario = resultado[0]
            cursor.execute("INSERT INTO adm (id) VALUES (%s)", (id_usuario,)) # insere o id do usuário na tabela adm
            con.commit()
        else:
            print("Erro: usuário com o login especificado não encontrado.")
            
    except mysql.connector.Error as e:
        print(f"Erro ao inserir administrador: {e}")
    finally:
        cursor.close()

def select_todos_usuarios(con): # irá mostrar todos os usuários já inseridos
    cursor = con.cursor()
    sql = "SELECT login, email, data_ingresso, id_instituicao FROM usuario" # não vai exibir a senha. escolha não inteligente.
    cursor.execute(sql)

    for (login, email, data_ingresso, id_instituicao) in cursor:
        print(login, email, data_ingresso, id_instituicao)

    cursor.close()
    # não precisa dar commit porque não fez nenhuma alteração no banco de dados

def fazerComentario(con, id_arquivo, conteudo, login):
    cursor = con.cursor()
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
        cursor.execute(''' 
            INSERT INTO usuario_comentario (id_usuario, id_comentario)
            VALUES (%s, %s)
        ''', (id_usuario, id_comentario))
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
        data_pedido = datetime.datetime.now().date() #pede data e hora atual
        hora_pedido = datetime.datetime.now().time()
        
        sql = """
            INSERT INTO suporte (id_arquivo, mensagem, data_pedido, hora_pedido)
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
        #inserir na tabela usuario_suporte o id_usuario e id_suporte

        cursor.execute(''' INSERT INTO usuario_suporte (id_usuario, id_suporte)
                       VALUES (%s, %s)'''
                       ,(id_usuario, id_suporte,))
        con.commit()
        print("Pedido de suporte enviado com sucesso. Aguarde nosso retorno")
    except mysql.connector.Error as e:
        print(f"Erro: você não conseguiu enviar um pedido de suporte: {e}")
    finally:
        cursor.close()

def remover_arquivo(con, id_arquivo):
    cursor = con.cursor()
    try:
        sql = '''
        SELECT ID_arq FROM Arquivo WHERE ID_arq = %s
    '''
        cursor.execute(sql,(id_arquivo,))
        valor = cursor.fetchone()

        if valor:
            sql_deletar = '''
            DELETE FROM Arquivo WHERE Id_arq = %s 
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
            print("Arquivo adicionado com sucesso!")
            
        else:
            print("Usuário não encontrado. Verifique o ID do usuário.")
        #CASO DER ERRO
    except mysql.connector.Error as e:
        print(f"Erro ao adicionar arquivo: {e}")
    
    finally:
        cursor.close()



