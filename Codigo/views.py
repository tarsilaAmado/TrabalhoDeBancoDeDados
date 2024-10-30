import sqlite3


# Conectar ao banco de dados SQLite
conexao = sqlite3.connect('Banco_de_Dados.db')  # Certifique-se de usar '.db' na extensão
cursor = conexao.cursor()

def id_check(id):
    cursor.execute(''' SELECT COUNT(*) FROM ADM WHERE ID_adm = ?''', (id))
    return cursor.fetchone()[0] > 0


#Usuario so pode ver e operar arquivos que ele tem acesso
def acessar_arquivos_usuario(id_usuario):
    view= cursor.execute('''
        CREATE VIEW IF NOT EXISTS view_usuario as 
        SELECT nome, tipo, PA 
        FROM Arquivo
        JOIN Compartilhamento ON Arquivo.ID_arq = Compartilhamento.ID_arq
        WHERE Compartilhamento.ID_us = ?

        ''' ,(id_usuario))
    
    view_usuario = cursor.execute(''' SELECT * FROM view''')
    print(view_usuario.fetchall())

def acessar_arquivos_adm(id_adm):
    if id_check(id_adm):

        view= cursor.execute('''  
            CREATE VIEW IF NOT EXISTS  view_adm as
            SELECT * 
            FROM Arquivos


            ''')

        view_ADM = cursor.execute(''' SELECT * FROM view''')
        print(view_ADM.fetchall())
    else :
        print("ID invalido, não adm")





# Fazer o commit das mudanças no banco de dados
conexao.commit()

# Fechar o cursor e a conexão ao terminar
cursor.close()
conexao.close()