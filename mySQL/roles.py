import mysql.connector
from mysql.connector import Error
from conexao import *


def atribuir_role(con, login, escolha):
    cursor = con.cursor()
    
    try:
        if escolha == "1":
            
            cursor.execute(f"GRANT 'papelUsuario' TO '{login}'@'localhost'")
            con.commit()

        elif escolha == "2":
            
            cursor.execute(f"GRANT 'papelEmpresa' TO '{login}'@'localhost'")
            con.commit()
        elif escolha == "3":
            
            cursor.execute(f"GRANT 'papelADM' TO '{login}'@'localhost'")
            con.commit()
        else:
            print("Opção de role inválida.")
            return None
        #debug
        cursor.execute(f"SHOW GRANTS FOR '{login}'@'localhost';")
        grants = cursor.fetchall()
        
        
        print("Role atribuída com sucesso.\n")
        #pra testes
        return grants

    except mysql.connector.Error as e:
        print(f"Erro ao atribuir role : {e}")
        return None
        
    finally:
        
        cursor.close()
