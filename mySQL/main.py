from conexao import criar_conexao, fechar_conexao
from roles import *
from views import *
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


def select_todos_usuarios(con): # irá mostrar todos os usuários já inseridos
    cursor = con.cursor()
    sql = "SELECT login, email, data_ingresso, id_instituicao FROM usuario" # não vai exibir a senha. escolha não inteligente.
    cursor.execute(sql)

    for (login, email, data_ingresso, id_instituicao) in cursor:
        print(login, email, data_ingresso, id_instituicao)

    cursor.close()
    # não precisa dar commit porque não fez nenhuma alteração no banco de dados

def fazerComentario(con, id_arquivo, conteudo):
    cursor = con.cursor()
    try:
        #obter data e hora
        data = datetime.now().date()
        hora = datetime.now().time()
        #inserir no comentario
        cursor.execute(''' 
            INSERT INTO comentario(conteudo, id_arquivo, data_c, hora)
            VALUES (%s, %s, %s, %s)
        ''', (conteudo, id_arquivo, data, hora)) 
    except mysql.connector.Error as e:
        print(f"Erro ao inserir comentario : {e}")
    finally:
        cursor.close()
        #confirmar a insercao
        con.commit()
    
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
        
def pedir_suporte(con, id_usuario, mensagem):
    cursor = con.cursor()
    try:
        data_pedido = datetime.datetime.now().date() #pede data e hora atual
        hora_pedido = datetime.datetime.now().time()
        
        sql = """
            INSERT INTO suporte (id_usuario, mensagem, data_pedido, hora_pedido)
            VALUES (%s, %s, %s, %s)
        """ #faz um pedido de suporte enviando uma mensagem, exemplo: não consigo acessar meu arquivo
        valores = (id_usuario, mensagem, data_pedido, hora_pedido)
        cursor.execute(sql, valores)
        

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
    
def main():
    con = criar_conexao("localhost", "root", "", "webdriver")
    
    insere_instituicao(con, "UNICAP", "R. do Príncipe, 526", "socialização")

    insere_usuario(con, "juliasvilar", "julia123", "juliasvilar@gmail.com", "2024-11-02", 1)

    acessar_arquivos_usuario(con, )
    # select_todos_usuarios(con)
    update_arquivo(con, id_arquivo, id_usuario, novo_conteudo)

    fechar_conexao(con)

if __name__ == "__main__":
    main()
