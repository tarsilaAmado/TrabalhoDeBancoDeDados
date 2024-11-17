import mysql.connector
from mysql.connector import Error
from conexao import *

def inserir_adm(con, login):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT id FROM usuario WHERE login = %s", (login,))  # busca o id do usuário com base no login
        resultado = cursor.fetchone()
        
        if resultado:
            id_usuario = resultado[0]
            cursor.execute("INSERT INTO adm (id) VALUES (%s)", (id_usuario,))  # insere o id do usuário na tabela adm
            con.commit()

            # Obtém o id do novo administrador inserido
            cursor.execute("SELECT id FROM adm WHERE id = %s", (id_usuario,))
            id_adm = cursor.fetchone()[0]

            # Insere na tabela usuario_adm
            cursor.execute(
                "INSERT INTO usuario_adm (id_usuario, id_adm) VALUES (%s, %s)",
                (id_usuario, id_adm)
            )
            con.commit()
            print("Administrador inserido com sucesso e vinculado ao usuário.")
        else:
            print("Erro: usuário com o login especificado não encontrado.")
            
    except mysql.connector.Error as e:
        print(f"Erro ao inserir administrador: {e}")
    finally:
        cursor.close()


def atribuir_role(con, login, escolha):
    cursor = con.cursor()
    
    try:

        if escolha == "1":
            try:
                cursor.execute(f"GRANT papelUsuario TO '{login}'@'localhost'")
                cursor.execute(f"FLUSH PRIVILEGES;")
                con.commit()
            except mysql.connector.Error as e:
                print(f"Erro ao garantir role: {e}")

        elif escolha == "2":
            try:
                cursor.execute(f"GRANT papelEmpresa TO '{login}'@'localhost'")
                cursor.execute(f"FLUSH PRIVILEGES;")
                con.commit()
            except mysql.connector.Error as e:
                print(f"Erro ao garantir role: {e}")

        elif escolha == "3":
            try:
                cursor.execute(f"GRANT papelADM TO '{login}'@'localhost'")
                cursor.execute(f"FLUSH PRIVILEGES;")
                con.commit()
                inserir_adm(con, login)
            except mysql.connector.Error as e:
                print(f"Erro ao garantir role: {e}")

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
