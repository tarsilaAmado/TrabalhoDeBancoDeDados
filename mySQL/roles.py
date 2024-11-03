import mysql.connector
from mysql.connector import Error
from conexao import criar_conexao


def criarRole(con, nomeRole):
    try:
        cursor = con.cursor
        cursor.execute(f"CREATE ROLE '{nomeRole}';")
        con.commit()
        print(f"Role {nomeRole} criado com sucesso.")

    except Error as e:
        print("Erro ao criar Role!!!")
    finally:
        cursor.close()
    
def concederPrivilegios(con, nomeRole, privilegios):
    #ATENÇÂO : tem que passar os privilegios como um array quando chamar a função
    #EX: privilegios = ['SELECT', 'INSERT', 'UPDATE']

    con = criar_conexao("localhost", "root", "", "webdriver")
    try:
        cursor = con.cursor()
        for privilege in privilegios:
            cursor.execute(f"GRANT {privilege} ON webdriver TO '{nomeRole}';")
        con.commit()
        print(f"Privilegios {privilegios} concedidos ao Role {nomeRole}")
    except Error as e:
        print(f"Error creating role or granting privileges: {e}")
    finally:
        cursor.close()


def papelUsuario(con):
    criarRole(con, "PapelUsuario")
    privilegiosUsuario = ['SELECT', 'INSERT', 'UPDATE']
    concederPrivilegios(con, "PapelUsuario", privilegiosUsuario)

def papelEmpresa(con):
    criarRole(con, "PapelEmpresa")
    privilegiosEmpresa = ['SELECT']
    concederPrivilegios(con, "PapelEmpresa", privilegiosEmpresa)

def papelADM(con):
    criarRole(con, "PapelADM")
    privilegiosADM = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
    concederPrivilegios(con, "PapelADM", privilegiosADM)
