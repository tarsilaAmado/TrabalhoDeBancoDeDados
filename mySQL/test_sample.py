import pytest
from CRUD import *
from conexao import *

class TestLogin:
    login = 'joao'
    senha = 'joao123'
    con =  criar_conexao("localhost", login, senha, "webdriver")
    
    def test_usuario_existente(self):
        resultado =  check_login(self.con, self.login, self.senha)
        assert resultado == True

    def test_senha_errada(self):
        senha = 'errado1234'
        resultado =  check_login(self.con, self.login, senha)
        assert resultado == False
    
    def test_usuario_inexistente(self):
        login = 'Adamocles'
        senha = 'adamocles123'
        resultado =  check_login(self.con, login, senha)
        assert resultado == False

class TestRoles:
    login = 'joao'
    senha = 'joao123'
    con =  criar_conexao("localhost", login, senha, "webdriver")
    
    def test_atribuir_role_usuario_usuario(self):
        #usuario tentando atribuir role a alguem
        resultado = atribuir_role(self.con, self.login, "1")
        print(resultado)
        #resultado esperado é que ele falhe
        assert resultado == None
    
    def test_atribuir_role_papelEmpresa_usuario(self):
        resultado = atribuir_role(self.con, self.login, "2")
        print(resultado)
        #resultado esperado é que ele falhe
        assert resultado == None
    
    def test_atribuir_role_papelADM_usuario(self):
        resultado = atribuir_role(self.con, self.login, "3")
        print(resultado)
        #resultado esperado é que ele falhe
        assert resultado == None


    def test_atribuir_role_usuario_Empresa(self):
        #empresa tentando atribuir role a alguem
        login = 'UNICAP'
        resultado = atribuir_role(self.con, login, "1")
        print(resultado)
        #resultado esperado é que ele falhe
        assert resultado == None

    def test_atribuir_role_papelEmpresa_empresa(self):
        login = 'UNICAP'
        resultado = atribuir_role(self.con, login, "2")
        print(resultado)
        #resultado esperado é que ele falhe
        assert resultado == None
    
    def test_atribuir_role_papelADM_empresa(self):
        login = 'UNICAP'
        resultado = atribuir_role(self.con, login, "3")
        print(resultado)
        #resultado esperado é que ele falhe
        assert resultado == None
    

    def test_atribuir_role_usuario_root(self):
        con = criar_conexao("localhost", "root", "", "webdriver")
        resultado = atribuir_role(con, "root", "1")
        print(resultado)
        assert any('papelUsuario' in grant[0] for grant in resultado)

    
    
    def test_atribuir_role_papelEmpresa_root(self):
        con = criar_conexao("localhost", "root", "", "webdriver")
        resultado = atribuir_role(con, "root", "2")
        print(resultado)
        assert any('papelEmpresa' in grant[0] for grant in resultado)

    def test_atribuir_role_papelADM_root(self):
        con = criar_conexao("localhost", "root", "", "webdriver")
        resultado = atribuir_role(con, "root", "3")
        print(resultado)
        assert any('papelADM' in grant[0] for grant in resultado)

    
    
    
class TestInserts:
    login = 'augusto'
    senha= 'novo'
    con =  criar_conexao("localhost", "root", "", "webdriver")
    cursor = con.cursor()

    # def test_insere_usuario(self):
    #     insere_usuario(self.con,self.login,self.login, "usuarionovo", "2024-12-12", "1")
    #     self.cursor.execute(f'''SELECT id, login, senha, email FROM usuario WHERE login = '{self.login}'''')

    #     resultado = self.cursor.fetchall() 
    #     print(resultado)
    #     assert resultado != None
        

    def test_insere_plano(self):
        nome = "plano Teste"
        insere_plano(self.con, nome, "01:59:59", "2024-12-12", "usuario")
        self.cursor.execute(f"SELECT id, nome, duracao, data_aquisicao, espaco_usuario FROM plano WHERE nome = '{nome}'")
        resultado = self.cursor.fetchall()
        assert resultado != None
    
    #def test_inserir_adm(self):
        #inserir_adm(self.con, self.login)
        #self.cursor.execute(f"SELECT FROM  WHERE ")
        

class TestGetsEChecks:
    login = 'joao'
    senha = 'joao123'
    con =  criar_conexao("localhost", login, senha, "webdriver")
    
    def test_get_id(self):
        resultado = get_id(self.con, self.login)
        print(resultado)
        assert resultado == 13

class TestFuncoes:
    login = 'joao'
    senha = 'joao123'
    con =  criar_conexao("localhost", login, senha, "webdriver")

class TestViews:
    
    
    def test_acessar_arquivos_usuario(self):
        login = 'joao'
        senha = 'joao123'
        con =  criar_conexao("localhost", login, senha, "webdriver")
        id = get_id(con, login)
        resultado = acessar_arquivos_usuario(con, id)
        print(resultado)
        assert resultado != None

        
    
    
