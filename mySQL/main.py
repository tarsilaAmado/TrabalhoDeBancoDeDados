from conexao import criar_conexao, fechar_conexao
from roles import *
from views import *
from CRUD import *

def menu():
    print("Opções: ")
    print("1 -Fazer Login")
    print("2 - Inserir usuário")
    print("3 - Inserir instituição")
    print("4 - Criar arquivo")
    print("5 - Fazer comentário")
    print("6 - Criar plano")
    print("7 - Compartilhar arquivo")
    print("8 - Acessar arquivo")
    print("9 - Criar role e atribuir privilégios")
    print("10 - Pedir suporte")
    print("11 - Adicionar arquivo")
    print("0 - Sair")
    
def main():

    con = criar_conexao("localhost", "root", "", "webdriver")
    op = -1; 
    global login
    while op != 0:
        menu()
        op = int(input(("Escolha: ")))
        if op == 1:#fazer login
            login_input = input(("Login: "))
            senha = input(("Senha: "))
            #checa se o login existe
            #checa se a senha bate com o login
            check_login(login, senha, con)
            #

            #
        elif op == 2: # insere usuário
            
            login = input(("Login: "))
            #checa se o login existe
            senha = input(("Senha: "))
            #checa se a senha está correta
            email = input(("Email: "))
            data_ingresso = input(("Data de ingresso: "))
            id_instituicao = input(("Id da instituição: "))
            insere_usuario(con, login, senha, email, data_ingresso, id_instituicao)
            resposta = int(input(("É administrador?\n1 - sim\n2- não\n")))
            if resposta == 1:
                inserir_adm(con, login)
        elif op == 3: # insere instituição
            nome = input(("Nome: "))
            endereco = input(("Endereço: "))
            causa_social = input(("Causa social: "))
            insere_instituicao(con, nome, endereco, causa_social)
        elif op == 4: # cria arquivo
            print("a fazer")
        elif op == 5: # fazer comentário
            id_arquivo = input(("Id do arquivo: "))
            conteudo = input(("Conteúdo do comentário: "))
            fazerComentario(con, id_arquivo, conteudo, login=login)
        elif op == 6: # criar plano
            nome = input(("Nome: "))
            duracao = input(("Duração (HH:MM:SS): "))
            data_aquisicao = input(("Data de aquisição (AAAA-MM-DD): "))
            espaco_usuario = input(("Espaço do usuário: "))
            insere_plano(con, nome, duracao, data_aquisicao, espaco_usuario)
        elif op == 7: # compartilhar arquivo
            id_arquivo = input("Id do arquivo: ")
            id_dono = input(("Id do dono: "))
            id_compartilhado = input(("Id do compartilhado: "))
            data = input(("Data (AAAA-MM-DD): "))
            compartilhar(con, id_arquivo, id_dono, id_compartilhado, data)
        elif op == 8: # acessar arquivo específico
            nome_arquivo = input(("Nome do arquivo: "))
            acessar_arquivo(con, nome_arquivo, login=login)
        elif op == 9: # criar role
            nomeRole = input(("Que role você deseja criar? "))
            criarRole(con, nomeRole)
            privilegios = []
            input = input(("Que privilégio deseja dar? [...,...] (escreva em caixa alta e separando por virgulas): "))
            privilegios = [priv.strip() for priv in input.split(',')]
            concederPrivilegios(con, nomeRole, privilegios)
        elif op == 10: # pedir suporte
            id_arquivo = input(("Sobre que arquivo você deseja pedir o supórte (id)?" ))
            mensagem = input(("Descrição do suporte: "))
            pedir_suporte(con, id_arquivo, mensagem, login=login)
        elif op == 11:  #adiciona arquivo
            nome = input("Nome do arquivo: ")
            tipo = input("Tipo do arquivo: ")
            permissao_acesso = input("Permissão de acesso (Ex.: 'r' para leitura, 'rw' para leitura e escrita): ")
            id_usuario = int(input("ID do usuário: "))
            url = input("URL do arquivo: ")
            adicionar_arquivo(con, nome, tipo, permissao_acesso, id_usuario, url)
    
    print("Saindo do programa...")
    fechar_conexao(con)


if __name__ == "__main__":
    main()
