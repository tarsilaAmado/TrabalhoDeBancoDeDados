import tkinter as tk
from tkinter import messagebox
from conexao import criar_conexao, fechar_conexao
from CRUD import check_login

def login():
    usuario = entry_usuario.get()
    email = entry_email.get()
    senha = entry_senha.get()
    
    if not usuario or not email or not senha:
        messagebox.showerror("Por favor, preencha TODOS os campos.")
        return
    
    conexao = criar_conexao("localhost", usuario, senha, "webdriver")
    
    if conexao:
        # faz vaidacao com check_login do CRUD
        if check_login(conexao, usuario, senha):
            messagebox.showinfo(f"Login realizado com sucesso! Bem-vindo(a), {usuario}.")
            abrir_menu(conexao, usuario)  #mostra o menu
        else:
            messagebox.showerror("Credenciais incorretas. Verifique o usuário, email ou senha.")
            fechar_conexao(conexao)
    else:
        messagebox.showerror("Não foi possível te conectar ao banco de dados. Verifique as suas credenciais.")

def abrir_menu(conexao, usuario):
    menu_janela = tk.Toplevel(root)
    menu_janela.title(f"Bem-vindo(a), {usuario}")
    
    tk.Label(menu_janela, text=f"Bem-vindo(a), {usuario}! Escolha uma opção:").pack(pady=10)
    
    btn_ver_arquivos = tk.Button(menu_janela, text="Criar usuário", command=lambda: Criar_usuario(conexao))
    btn_ver_arquivos.pack(pady=5)
    btn_ver_arquivos = tk.Button(menu_janela, text="Inserir Instituição", command=lambda: inserir_instituicao(conexao))
    btn_ver_arquivos.pack(pady=5)
    btn_pedir_suporte = tk.Button(menu_janela, text="Criar Arquivo", command=lambda: Criar_arquivo(conexao))
    btn_pedir_suporte.pack(pady=5)
    btn_pedir_suporte = tk.Button(menu_janela, text="Fazer Comentário", command=lambda: fazer_comentario(conexao))
    btn_pedir_suporte.pack(pady=5)
    btn_pedir_suporte = tk.Button(menu_janela, text="Criar Plano", command=lambda: Criar_plano(conexao))
    btn_pedir_suporte.pack(pady=5)
    btn_sair = tk.Button(menu_janela, text="sair", command=lambda: fechar_conexao(conexao) or menu_janela.destroy())
    btn_sair.pack(pady=5)

#BOTOES FEITOS
#Criar usuário") 
#print("2 - Inserir instituição")
#print("3 - Criar arquivo")
#print("4 - Fazer comentário")
#print("5 - Criar plano")

root = tk.Tk()
root.title("Login WebDrive")
tk.Label(root, text="Usuário:").pack(pady=5)
entry_usuario = tk.Entry(root, width=30)
entry_usuario.pack(pady=5)
tk.Label(root, text="Email:").pack(pady=5)
entry_email = tk.Entry(root, width=30)
entry_email.pack(pady=5)
tk.Label(root, text="Senha:").pack(pady=5)
entry_senha = tk.Entry(root, width=30, show="*")
entry_senha.pack(pady=5)
btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=10)
root.mainloop()
