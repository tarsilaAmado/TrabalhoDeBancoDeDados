import mysql.connector
from mysql.connector import Error
from conexao import *


def atribuir_role(con, login, escolha):
    cursor = con.cursor()
    
    try:
        if escolha == "1":
            cursor.execute("GRANT papelUsuario TO %s@'localhost'", (login,))
            cursor.execute("FLUSH PRIVILEGES;")
        elif escolha == "2":
            cursor.execute("GRANT papelEmpresa TO %s@'localhost'", (login,))
            cursor.execute("FLUSH PRIVILEGES;")
        elif escolha == "3":
            cursor.execute("GRANT papelADM TO %s@'localhost'", (login,))
            cursor.execute("FLUSH PRIVILEGES;")
        else:
            print("Opção de role inválida.")
            return
        
        con.commit()  # Commitando a alteração
        print("Role atribuída com sucesso.\n")

    except mysql.connector.Error as e:
        print(f"Erro ao atribuir role : {e}")
        
    finally:
        con.commit()
        cursor.close()
