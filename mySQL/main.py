from conexao import criar_conexao, fechar_conexao
from roles import *
from views import *


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

def fazerComentario(con):
    


def main():
    con = criar_conexao("localhost", "root", "", "webdriver")
    
    insere_instituicao(con, "UNICAP", "R. do Príncipe, 526", "socialização")

    insere_usuario(con, "juliasvilar", "julia123", "juliasvilar@gmail.com", "2024-11-02", 1)

    # select_todos_usuarios(con)

    fechar_conexao(con)

if __name__ == "__main__":
    main()
