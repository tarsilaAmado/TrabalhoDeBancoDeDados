import sqlite3

# Conectar ao banco de dados SQLite
conexao = sqlite3.connect('Banco_de_Dados.db')  # Certifique-se de usar '.db' na extensão
cursor = conexao.cursor()

# Criar as tabelas no SQLite
#perguntar para jhey como fazer os 3 tipos de operacoes 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Operacao (
        ID INTEGER PRIMARY KEY,
        tipo TEXT,
        hora TEXT,
        data TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Instituicoes (
        ID_inst INTEGER PRIMARY KEY,
        end TEXT,
        nome TEXT,
        Causa_soc TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ADM (
        ID_adm INTEGER PRIMARY KEY
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Plano (
        ID_plano INTEGER PRIMARY KEY,
        nome TEXT,
        duracao TEXT,
        espaco_usuario TEXT,
        data_aqui TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        ID_us INTEGER PRIMARY KEY,
        login TEXT,
        senha TEXT,
        email TEXT,
        data_ingresso TEXT,
        ID_inst INTEGER,
        FOREIGN KEY (ID_inst) REFERENCES Instituicoes(ID_inst)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Arquivo (
        ID_arq INTEGER PRIMARY KEY,
        nome TEXT,
        tipo TEXT,
        PA TEXT,
        ID_us INTEGER,
        FOREIGN KEY (ID_us) REFERENCES Usuario(ID_us)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comentario (
        ID INTEGER PRIMARY KEY,
        conteudo TEXT,
        data TEXT,
        hora TEXT,
        ID_arq INTEGER,
        FOREIGN KEY (ID_arq) REFERENCES Arquivo(ID_arq)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Compartilhamento (
        ID_compart INTEGER PRIMARY KEY,
        data TEXT,
        ID_us INTEGER,
        ID_arq INTEGER,
        FOREIGN KEY (ID_us) REFERENCES Usuario(ID_us),
        FOREIGN KEY (ID_arq) REFERENCES Arquivo(ID_arq)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Historico_Versionamento (
        ID_hist INTEGER PRIMARY KEY,
        data TEXT,
        hora TEXT,
        ID_us INTEGER,
        ID_arq INTEGER,
        FOREIGN KEY (ID_us) REFERENCES Usuario(ID_us),
        FOREIGN KEY (ID_arq) REFERENCES Arquivo(ID_arq)
    )
''')

cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS Controle_Arquivos (
        ID_arq INTEGER PRIMARY KEY,           
        Ultima_versao DATE,
        Acesso TEXT,
               
        FOREIGN KEY (ID_arq) REFERENCES Arquivo(ID_arq)
    )
    
''')

# Fazer o commit das mudanças no banco de dados
conexao.commit()

# Fechar o cursor e a conexão ao terminar
cursor.close()
conexao.close()
