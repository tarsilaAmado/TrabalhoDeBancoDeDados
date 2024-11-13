import mysql.connector
from conexao import *

def idCheck(con,id):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM usuario_adm WHERE id_adm = %s", (id,))
        return cursor.fetchone()[0] > 0
    except mysql.connector.Error as e:
        print(f"Error ao verificar id : {e}")
        return False
    finally:
        cursor.close()

def idCheck_instituicao(con, id):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM instituicao WHERE id = %s", (id,))
        return cursor.fetchone()[0] > 0
    except mysql.connector.Error as e:
        print(f"Error ao verificar id : {e}")
        return False
    finally:
        cursor.close()
   

def acessar_arquivos_usuario(con, id):
    cursor = con.cursor()
    
    try:
        # Criando a view, se ela não existir
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS view_usuario AS 
            SELECT nome, tipo, permissao_acesso 
            FROM arquivo
            JOIN compartilhamento ON arquivo.id = compartilhamento.id_arquivo
            WHERE compartilhamento.id_compartilhado = %s
        ''', (id,))
        
        # Consultando a view para obter os dados
        cursor.execute('SELECT * FROM view_usuario')
        view_usuario = cursor.fetchall()
        
        # Exibindo os resultados
        for row in view_usuario:
            print(row)
            
    except mysql.connector.Error as err:
        print(f"Erro ao acessar arquivos do usuário: {err}")
        
    finally:
        cursor.close()

def acessar_arquivos_instituicao(con, id):
    cursor = con.cursor()

    try:
        if idCheck_instituicao(con, id):

            cursor.execute(''' 
            CREATE VIEW IF NOT EXISTS view_instituicao AS
            SELECT *
            FROM arquivo
            JOIN usuario ON arquivo.id_usuario = usuario.id
            WHERE usuario.id_instituicao = %s
            ''', (id,))

            view_instituicao = cursor.execute('''SELECT * FROM view_instituicao ''')
            for row in view_instituicao:
                print(row)
        else:
            print(f"{id} não é uma instituição")
    except mysql.connector.Error as e:
        print(f"Erro ao acessar os arquivos : {e}")
    finally:
        cursor.close()

def acessar_arquivos_ADM(con, id):
    cursor = con.cursor()
    try:
        if(idCheck(con, id)):

            cursor.execute('''  
                CREATE VIEW IF NOT EXISTS  view_adm as
                SELECT * 
                FROM arquivos


                ''')
            cursor.commit()
            view_adm = cursor.execute(''' SELECT * FROM view_adm ''')
            cursor.commit()
            

            for row in view_adm:
                print(row)
        else:
            print(f"ID {id} não é ADM!!")
    except mysql.connector.Error as err:
        print(f"Erro ao acessar arquivos do usuário: {err}")    
    finally:
        cursor.close()    

def acessar_historico_operacoes(con):
    cursor = con.cursor()
    try:
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS view_historico_operacoes AS
            SELECT 
                historico_operacoes.operacao AS Operacao,
                usuario.login AS Usuario,
                arquivo.nome AS Arquivo,
                historico_operacoes.data_operacao AS Data,
                historico_operacoes.hora_operacao AS Hora
            FROM 
                historico_operacoes
            JOIN 
                usuario ON historico_operacoes.id_usuario = usuario.id
            LEFT JOIN 
                arquivo ON historico_operacoes.id_arquivo = arquivo.id;
        ''')
        
        cursor.execute('SELECT * FROM view_historico_operacoes')
        historico_operacoes = cursor.fetchall()
        for row in historico_operacoes:
            print(row)
            
    except mysql.connector.Error as err:
        print(f"Erro ao acessar histórico de operações: {err}")
        
    finally:
        cursor.close()
