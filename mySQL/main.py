from conexao import criar_conexao, fechar_conexao
from roles import *
from views import *
from CRUD import *
from procedures import *

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
    print("13 - Visualisar arquivos")
    print("14 - Atualizar atividades recentes com a data atual")
    print("15 - Total de usuários com acesso a um arquivo")
    print("16 - Trocar acesso não prioritário para prioritário de um arquivo")
    print("17 - Remover acessos de arquivo")
    print("18 -alterar url de um arquivo")
    print("0 - Sair")
    
def main():

    print("Entrar:\n1 - Com login\n2 - Como root")
    resposta = input("Escolha: ")

    

    if resposta == "1":
        global login
        login = None

        login = input(("Login: "))
        senha = input(("Senha: "))
        
        con = criar_conexao("localhost", "root", "", "webdriver")
        if con is None:
            print("Falha na conexão com o banco de dados.")
            return
        
        # checa se o login existe
        # checa se a senha bate com o login
        
        if check_login(con, login, senha):
            print(f"Login realizado, seja bem vindo(a) {login}\n")
        else:
            print("Não foi possivel realizar login, login ou senha invalidos.\n")
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
            role = role_check(con, login)
            if login == "root" or any('papelADM' in i[0] for i in role):
                login = input(("Login: "))
                #checa se o login existe
                senha = input(("Senha: "))
                #checa se a senha está correta
                email = input(("Email: "))
                data_ingresso = input(("Data de ingresso: "))
                id_instituicao = input(("Id da instituição: "))
                insere_usuario(con, login, senha, email, data_ingresso, id_instituicao)
                
            else:
                #se ele não for root nem adm 
                print("Permissão negada para criar usuário.\n")
                break
                
        elif op == 2: # insere instituição
            role = role_check(con, login)
            if login == "root" or any('papelADM' in i[0] for i in role):
                nome = input(("Nome: "))
                endereco = input(("Endereço: "))
                causa_social = input(("Causa social: "))
                plano = input("Id do plano: ")
                insere_instituicao(con, nome, endereco, causa_social,plano)
                print("Instituição adicionada com sucesso!\n")
            else:
                #se ele não for root nem adm 
                print("Permissão negada para criar instituição.\n")
                break
    
        elif op == 3: # cria arquivo
            role = role_check(con, login)
            if login == "root" or any('papelADM' in i[0] for i in role) or any('papelUsuario' in i[0] for i in role):
                nome = input("Nome do arquivo: ")
                tipo = input("Tipo (.exe não pode): ")
                permissao_acesso = input("Permissão de acesso (publi/priv): ")
                id_usuario = input("Id do usuário: ")
                url = input("URL: ")
                adicionar_arquivo(con, nome, tipo, permissao_acesso, id_usuario, url)
            else:
                # se não for root nem adm
                print("Permissão negada para criar instituição.\n")
                break
        
        elif op == 4: # fazer comentário
            role = role_check(con, login)
            if login == "root" or any('papelADM' in i[0] for i in role) or any('papelUsuario' in i[0] for i in role):
                id_arquivo = input(("Id do arquivo: "))
                conteudo = input(("Conteúdo do comentário: "))
                id_usuario = input(("Id do usuário que está comentando: "))
                fazerComentario(con, id_arquivo, conteudo, id_usuario)
            else:
                #se ele não for adm, nem root, nem usuário
                print("Permissão negada para fazer comentário.\n")
                break
        
        elif op == 5: # criar plano
            nome = input(("Nome: "))
            duracao = input(("Duração (HH:MM:SS): "))
            data_aquisicao = input(("Data de aquisição (AAAA-MM-DD): ")) 
            espaco_usuario = input(("Espaço do usuário: "))
            insere_plano(con, nome, duracao, data_aquisicao, espaco_usuario)

        elif op == 6: # compartilhar arquivo
            id_arquivo = input("Id do arquivo: ")
            # id_dono = input(("Id do dono: "))
            #vai pegar o ID do dono por função
            id_dono = get_id(con, login)
            #vai pegar o id do compartilhado
            login_compartilhado = input(("Login do compartilhado: "))
            id_compartilhado = get_id(con, login_compartilhado)
            compartilhar(con, id_arquivo, id_dono, id_compartilhado,login)

        elif op == 7: # acessar arquivo específico
            nome_arquivo = input(("Nome do arquivo: "))
            acessar_arquivo(con, nome_arquivo)
        elif op == 8: # pedir suporte
            id_arquivo = input(("Sobre que arquivo você deseja pedir o supórte (id)? " ))
            mensagem = input(("Descrição do suporte: "))
            pedir_suporte(con, id_arquivo, mensagem, login)

        elif op == 9:  # remover arquivo
            id_arquivo = input("Id do arquivo a ser deletado: ")
            remover_arquivo(con, id_arquivo,login)

        elif op == 10: # verificar 100 dias

            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                id_arquivo = input("Id do arquivo a ser checado: ")
                if verificacaoDe100Dias(con,id_arquivo):
                    print("Arquivo modificado há mais de 100 dias.\n")
                else:
                    print("Arquivo modificado há menos de 100 dias.\n")

        elif op == 11: # visualizar atividades recentes
            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                visualizar_atividades_R (con,login)

        elif op == 12: # visualizar histórico de versionamento
            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                acessar_historico_operacoes(con)
            #terminar a logica ainda

        elif op == 13:
            #veifica qual o role do usuario atual
            role = role_check(con,login)
            #exibe os arquivos baseado no role
            if login == "root":
                #acessar tudo se for root
                acessar_arquivos_root(con, login)
            elif any('papelADM' in i[0] for i in role):
                #views adm
                id = get_id(con, login)
                acessar_arquivos_ADM(con, id)
            elif any('papelEmpresa' in i[0] for i in role):
                #views empresa
                id = get_id(con, login)
                acessar_arquivos_instituicao(con, id)
            elif any('papelUsuario' in i[0] for i in role):
                #views usuario
                id = get_id(con, login)
                acessar_arquivos_usuario(con,id)

        elif op == 14: # Atualizar atividades recentes com a data atual
            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                verificar_atividades(con)

        elif op == 15: # Total de usuários com acesso a um arquivo
            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                id_arquivo = input(("Id do arquivo: "))
                conta_usuarios(con, id_arquivo)

        elif op == 16: # Trocar acesso não prioritário para prioritário de um arquivo
            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                id_arquivo = input(("Id do arquivo: "))
                chavear(con, id_arquivo)

        elif op == 17: # Remover acessos de arquivo
            id_arquivo = input(("Id do arquivo: "))
            remover_acessos(con, id_arquivo)


        elif op ==18: # alterar arquivo
            role = role_check(con,login)
            if any('papelEmpresa' in i[0] for i in role):
                print("Empresa com permissão negada para compartilhamento.\n")
            else:
                escolha = input(("\n1 - Alterar tipo\n2 - Alterar URL\nEscolha: "))
                if escolha == 1:
                    id_arquivo=input(("Id arquivo: "))
                    novo_tipo = input(("Novo tipo (não pode ser .exe): "))
                    while novo_tipo == ".exe":
                        novo_tipo = input(("Não pode ser .exe. Novo tipo: "))
                    alterar_tipo_arquivo(con,id_arquivo,novo_tipo)
                elif escolha == 2:
                    id_arquivo=input(("Id arquivo: "))
                    nova_url=input(("Qual a nova url: "))
                    alterar_url_arquivo(con,id_arquivo,nova_url)

    print("Saindo do programa...")
    fechar_conexao(con)


if __name__ == "__main__":
    main()
