from conexao import criar_conexao, fechar_conexao
from roles import *
from views import *
from CRUD import *

def menu():
    print("Opções: ")
    print("1 - Criar usuário")
    print("2 - Inserir instituição")
    print("3 - Criar arquivo")
    print("4 - Fazer comentário")
    print("5 - Criar plano")
    print("6 - Compartilhar arquivo")
    print("7 - Acessar arquivo")
    print("8 - Pedir suporte")
    print("9 - Remover arquivo")
    print("10 - Checar tempo de modificação de arquivo")
    print("11 - Acessar atividades recentes")
    print("12 - Visualizar histórico de operações")
    print("13 - visualisar arquivos de usuários da empresa/")
    print("0 - Sair")
    
def main():

    print("Entrar:\n1 - Com login\n2 - Como root")
    resposta = input("Escolha: ")

    

    if resposta == "1":
        global login
        login = None

        login_input = input(("Login: "))
        senha = input(("Senha: "))
        
        con = criar_conexao("localhost", login_input, senha, "webdriver")
        if con is None:
            print("Falha na conexão com o banco de dados.")
            return
        
        # checa se o login existe
        # checa se a senha bate com o login
        
        if check_login(con, login_input, senha):
            login = login_input
            print(f"Login realizado, seja bem vindo(a) {login}\n")
        else:
            print("Não foi possivel realizar login, login ou senha invalidos")
            fechar_conexao(con)
            return
    elif resposta == "2":
        login = "root"
        print("Seja bem vindo(a) root\n")
        con = criar_conexao("localhost", "root", "", "webdriver")
    else:
        print("Opção inválida.")
        return

    op = -1; 
    while op != 0:

        menu()

        try:
            op = int(input("Escolha: "))
        except ValueError:
            print("Entrada inválida, por favor, insira um número.")
            continue

        if op == 1: # insere usuário
            #checa se é root ou usuario
            if user_check(login) == False :
                #False = user, True = root
                #checa se é adm
                
                role = role_check(con, login)
                
                if any('papelADM' in i[0] for i in role):
                    login = input(("Login: "))
                    #checa se o login existe
                    senha = input(("Senha: "))
                    #checa se a senha está correta
                    email = input(("Email: "))
                    data_ingresso = input(("Data de ingresso: "))
                    id_instituicao = input(("Id da instituição: "))
                    insere_usuario(con, login, senha, email, data_ingresso, id_instituicao)
                else:
                    #se ele nao for adm 
                    break
            else:
                login = input(("Login: "))
                #checa se o login existe
                senha = input(("Senha: "))
                #checa se a senha está correta
                email = input(("Email: "))
                data_ingresso = input(("Data de ingresso: "))
                id_instituicao = input(("Id da instituição: "))
                insere_usuario(con, login, senha, email, data_ingresso, id_instituicao)
                
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
            acessar_arquivo(con, nome_arquivo
                            )
        elif op == 8: # pedir suporte
            id_arquivo = input(("Sobre que arquivo você deseja pedir o supórte (id)? " ))
            mensagem = input(("Descrição do suporte: "))
            pedir_suporte(con, id_arquivo, mensagem, login)

        elif op == 9:  # remover arquivo
            id_arquivo = input("Id do arquivo a ser deletado: ")
            remover_arquivo(con, id_arquivo)

        elif op == 10: # verificar 100 dias
            if login == "root" :
                id_arquivo = input("Id do arquivo a ser checado: ")
                if verificacaoDe100Dias(con,id_arquivo):
                    print("Arquivo modificado há mais de 100 dias.\n")
                else:
                    print("Arquivo modificado há menos de 100 dias.\n")
            else:
                role = role_check(con, login)
                
                if any('papelADM' in i[0] for i in role):
                    id_arquivo = input("Id do arquivo a ser checado: ")
                    if verificacaoDe100Dias(con,id_arquivo):
                        print("Arquivo modificado há mais de 100 dias.\n")
                    else:
                        print("Arquivo modificado há menos de 100 dias.\n")
                else:
                    print("Erro: acesso negado!\n")

        elif op == 11: # visualizar atividades recentes
            visualizar_atividades_R (con,login)

        elif op == 12: # visualizar histórico de versionamento
            print("fazer")
            # visualizar_historico_v(con,login)
            #terminar a logica ainda

    print("Saindo do programa...")
    fechar_conexao(con)


if __name__ == "__main__":
    main()


