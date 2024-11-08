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
    print("10 - Adicionar arquivo")
    print("0 - Sair")
    
def main():

    con = criar_conexao("localhost", "root", "", "webdriver")
    op = -1; 
    while op != 0:
        menu()
        op = int(input(("Escolha: ")))
        if op == 1: # insere usuário
            global login
            login = input(("Login: "))
            senha = input(("Senha: "))
            email = input(("Email: "))
            data_ingresso = input(("Data de ingresso: "))
            id_instituicao = input(("Id da instituição: "))
            insere_usuario(con, login, senha, email, data_ingresso, id_instituicao)
            resposta = int(input(("É administrador?\n1 - sim\n2- não\n")))
            if resposta == 1:
                inserir_adm(con, login)
        elif op == 2: # insere instituição
            nome = input(("Nome: "))
            endereco = input(("Endereço: "))
            causa_social = input(("Causa social: "))
            insere_instituicao(con, nome, endereco, causa_social)
        elif op == 3: # cria arquivo
            print("a fazer")
        elif op == 4: # fazer comentário
            id_arquivo = input(("Id do arquivo: "))
            conteudo = input(("Conteúdo do comentário: "))
            fazerComentario(con, id_arquivo, conteudo, login=login)
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
            data = input(("Data (AAAA-MM-DD): "))
            compartilhar(con, id_arquivo, id_dono, id_compartilhado, data)
        elif op == 7: # acessar arquivo específico
            id_arquivo = input(("Id do arquivo: "))
            acessar_arquivo(con, id_arquivo)
        elif op == 8: # criar role
            nomeRole = input(("Que role você deseja criar? "))
            criarRole(con, nomeRole)
            privilegios = []
            input = input(("Que privilégio deseja dar? [...,...] (escreva em caixa alta e separando por virgulas): "))
            privilegios = [priv.strip() for priv in input.split(',')]
            concederPrivilegios(con, nomeRole, privilegios)
        elif op == 9: # pedir suporte
            id_arquivo = input(("Sobre que arquivo você deseja pedir o supórte (id)?" ))
            mensagem = input(("Descrição do suporte: "))
            pedir_suporte(con, id_arquivo, mensagem, login=login)
        elif op == 10:  #adiciona arquivo
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
