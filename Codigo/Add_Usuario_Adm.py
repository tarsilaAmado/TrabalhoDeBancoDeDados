# Cria usuario
def criar_usuario(id_usuario, login, senha, email, data_ingresso, id_inst):
    try:
        cursor.execute('''
            INSERT INTO Usuario (ID_us, login, senha, email, data_ingresso, ID_inst)
            VALUES (?, ?, ?, ?, ?, ?)#tupla
        ''', (id_usuario, login, senha, email, data_ingresso, id_inst))
        
        conexao.commit()
        print(f"ID inserido com sucesso.")
    
    except sqlite3.IntegrityError:#funcao especifica do sqlite3, levantada quando o BD viola alguma restricao de integridade
        print(f"Erro: O ID  já existe.")
    
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao inserir o usuário")


def criar_adm(id_adm, login, senha, email, data_ingresso, id_inst):
    # Primeiro, cria o usuário
    criar_usuario(id_adm, login, senha, email, data_ingresso, id_inst)
    
    try:
        cursor.execute('''
            INSERT INTO ADM (ID_adm, ID_us)
            VALUES (?, ?)
        ''', (id_adm, id_adm))  # transforma um usuario(que foi criado com essa funcao) em um adm
        
        conexao.commit()
        print(f"ID inserido com sucesso.")
    
    except sqlite3.IntegrityError:#funcao especifica do sqlite3, levantada quando o BD viola alguma restricao de integridade
        print(f"Erro: O ID  já existe na tabela.")
    
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao inserir o administrador")
