import sqlite3


# Conectar ao banco de dados SQLite
conexao = sqlite3.connect('Banco_de_Dados.db')  # Certifique-se de usar '.db' na extensão
cursor = conexao.cursor()




# Fazer o commit das mudanças no banco de dados
conexao.commit()

# Fechar o cursor e a conexão ao terminar
cursor.close()
conexao.close()