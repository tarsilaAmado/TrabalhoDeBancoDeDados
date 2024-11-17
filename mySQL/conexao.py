# fazendo a conexão com o banco de dados previamente criado em SQL

import mysql.connector
from mysql.connector import Error

def criar_conexao (host, usuario, senha, banco):
    try:
        return mysql.connector.connect(host = host, user = usuario, password = senha, database = banco)
    except mysql.connector.Error as e:
        print(f"Erro ao atribuir role : {e}")
        return None

def fechar_conexao (con):
    return con.close()
