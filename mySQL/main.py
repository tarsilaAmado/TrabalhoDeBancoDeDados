from conexao import criar_conexao, fechar_conexao
from roles import *
from views import *
from CRUD import *

def menu():
    print("Opções: ")
    print("1 - Inserir usuário")
    print("2 - Inserir instituição")
    print("3 - Criar arquivo")
    print("4 - Fazer comentário")
    print("5 - Criar plano")
    print("6 - Compartilhar arquivo")
    print("7 - Acessar arquivo")
    print("8 - Criar role e atribuir privilégios")
    print("9 - Pedir suporte")
    print("10 - Remover arquivo")
    print("0 - Sair")
    
def main():

    con = criar_conexao("localhost", "root", "", "webdriver")
    op = -1; 
    global login
    login = None

    login_input = input(("Login: "))
    senha = input(("Senha: "))
    #checa se o login existe
    #checa se a senha bate com o login
    status = check_login(con, login_input, senha)
    #
    if status == True:
        login = login_input
        print(f"Login realizado, seja bem vindo(a) {login}\n")
    else:
        print("Não foi possivel realizar login, login ou senha invalidos")


    while op != 0:

        menu()

        try:
            op = int(input("Escolha: "))
        except ValueError:
            print("Entrada inválida, por favor, insira um número.")
            continue

        if op == 1: # insere usuário
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
            print("Usuário adicionado com sucesso!\n")
        elif op == 2: # insere instituição
            nome = input(("Nome: "))
            endereco = input(("Endereço: "))
            causa_social = input(("Causa social: "))
            insere_instituicao(con, nome, endereco, causa_social)
            print("Instituição adicionada com sucesso!\n")
        elif op == 3: # cria arquivo
            nome = input("Nome do arquivo: ")
            tipo = input("Tipo (exemplo: .exe): ")
            permissao_acesso = input("Permissão de acesso (público/privado): ")
            id_usuario = input("Id do usuário: ")
            url = input("URL: ")
            adicionar_arquivo(con, nome, tipo, permissao_acesso, id_usuario, url)
        elif op == 4: # fazer comentário
            id_arquivo = input(("Id do arquivo: "))
            conteudo = input(("Conteúdo do comentário: "))
            fazerComentario(con, id_arquivo, conteudo, login)
        elif op == 5: # criar plano
            nome = input(("Nome: "))
            duracao = input(("Duração (HH:MM:SS): "))
            data_aquisicao = input(("Data de aquisição (AAAA-MM-DD): "))
            espaco_usuario = input(("Espaço do usuário: "))
            insere_plano(con, nome, duracao, data_aquisicao, espaco_usuario)
        elif op == 6: # compartilhar arquivo
            id_arquivo = input("Id do arquivo: ")
            id_dono = input(("Id do dono: "))
            id_compartilhado = input(("Id do compartilhado: "))
            compartilhar(con, id_arquivo, id_dono, id_compartilhado)
        elif op == 7: # acessar arquivo específico
            nome_arquivo = input(("Nome do arquivo: "))
            acessar_arquivo(con, nome_arquivo, login=login)
        elif op == 8: # criar role
            nomeRole = input(("Que role você deseja criar? "))
            criarRole(con, nomeRole)
            privilegios = []
            privilegios = input(("Que privilégio deseja dar? [...,...] (escreva em caixa alta e separando por virgulas): "))
            privilegios = [priv.strip() for priv in input.split(',')]
            concederPrivilegios(con, nomeRole, privilegios)
        elif op == 9: # pedir suporte
            id_arquivo = input(("Sobre que arquivo você deseja pedir o supórte (id)?" ))
            mensagem = input(("Descrição do suporte: "))
            pedir_suporte(con, id_arquivo, mensagem, login=login)
        elif op == 10:  # remover arquivo
            id_arquivo = input("Id do arquivo a ser deletado: ")
            remover_arquivo(con, id_arquivo)
    
    print("Saindo do programa...")
    fechar_conexao(con)


if _name_ == "_main_":
    main()
