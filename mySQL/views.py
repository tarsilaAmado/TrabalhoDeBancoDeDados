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
        cursor.execute('DROP VIEW IF EXISTS view_usuario;')

        # Criando a view com a coluna id_compartilhado incluída
        cursor.execute('''
            CREATE VIEW view_usuario AS
            SELECT 
                arquivo.nome AS Nome, 
                arquivo.tipo AS Tipo, 
                arquivo.permissao_acesso AS PermissaoAcesso,
                compartilhamento.id_compartilhado AS IdCompartilhado
            FROM arquivo
            JOIN compartilhamento ON arquivo.id = compartilhamento.id_arquivo;
        ''')
        
        # Consultando a view para obter os dados
        cursor.execute('SELECT Nome, Tipo, PermissaoAcesso FROM view_usuario WHERE IdCompartilhado = %s', (id,))
        view_usuario = cursor.fetchall()
        
        # Exibindo os resultados
        for row in view_usuario:
            print(row)
        return view_usuario
            
    except mysql.connector.Error as err:
        print(f"Erro ao acessar arquivos do usuário: {err}")
        
    finally:
        cursor.close()

def acessar_arquivos_instituicao(con, id):
    cursor = con.cursor()

    try:
        if idCheck_instituicao(con, id):

            cursor.execute('DROP VIEW IF EXISTS view_instituicao;')

            cursor.execute(''' 
            CREATE VIEW view_instituicao AS
            SELECT *
            FROM arquivo
            JOIN usuario ON arquivo.id_usuario = usuario.id
            ''',)

            view_instituicao = cursor.execute('''SELECT * FROM view_instituicao ''')
            for row in view_instituicao:
                print(row)
        else:
            print(f"{id} não é uma instituição")
    except mysql.connector.Error as e:
        print(f"Erro ao acessar os arquivos : {e}")
    finally:
        cursor.close()



def acessar_historico_operacoes(con):
    cursor = con.cursor()
    try:
    
        cursor.execute('DROP VIEW IF EXISTS view_historico_operacoes;')
        
    
        cursor.execute('''
            CREATE VIEW view_historico_operacoes AS
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


def acessar_arquivos_root(con, login):
    cursor = con.cursor()

    try:
        if(login == "root"):
            cursor.execute("SELECT * from arquivo")
            arquivos = cursor.fetchall()
            for row in cursor:
                print(row)
        else :
            print("Acesso bloqueado!")
        
    except mysql.connector.Error as err:
        print(f"Erro ao acessar histórico de operações: {err}")
    
    finally:
        cursor.close()
    
