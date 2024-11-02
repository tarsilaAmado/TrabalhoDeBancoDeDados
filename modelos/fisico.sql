# criação do banco de dados e das tabelas em SQL

CREATE DATABASE webdriver;
USE webdriver;

CREATE TABLE plano(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(30) NOT NULL,
duracao TIME NOT NULL,
data_aquisicao DATE NOT NULL,
espaco_usuario VARCHAR(50)
);

CREATE TABLE instituicao(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(30) NOT NULL,
endereco VARCHAR(100) NOT NULL,
causa_social VARCHAR(50)
);

CREATE TABLE usuario(
id INT AUTO_INCREMENT PRIMARY KEY,
login VARCHAR(50) NOT NULL,
senha VARCHAR(30) NOT NULL,
email VARCHAR(50),
data_ingresso DATE NOT NULL,
id_instituicao INT,
FOREIGN KEY(id_instituicao) REFERENCES instituicao(id)
);

CREATE TABLE arquivo(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(30) NOT NULL,
tipo VARCHAR(30) NOT NULL,
permissao_acesso VARCHAR(5),
id_usuario INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id)
);

CREATE TABLE historico_versionamento(
id INT AUTO_INCREMENT PRIMARY KEY,
id_usuario INT,
data_v DATE,
hora TIME,
id_arquivo INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

CREATE TABLE operacao(
id INT AUTO_INCREMENT PRIMARY KEY,
tipo VARCHAR(30) NOT NULL,
hora TIME,
data_o DATE
);

CREATE TABLE usuario_operacoes(
id_usuario INT,
id_operacao INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_operacao) REFERENCES operacao(id)
);

CREATE TABLE comentario(
id INT AUTO_INCREMENT PRIMARY KEY,
conteudo VARCHAR(150),
id_arquivo INT,
data_c DATE,
hora TIME,
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

CREATE TABLE usuario_comentario(
id_usuario INT,
id_comentario INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_comentario) REFERENCES comentario(id)
);

CREATE TABLE compartilhamento(
id INT AUTO_INCREMENT PRIMARY KEY,
id_dono INT,
id_compartilhado INT,
data_c DATE,
FOREIGN KEY(id_dono) REFERENCES usuario(id),
FOREIGN KEY(id_compartilhado) REFERENCES usuario(id)
);

CREATE TABLE usuario_compartilhamento(
id_usuario INT,
id_compartilhamento INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_compartilhamento) REFERENCES compartilhamento(id)
);

CREATE TABLE adm(#analisar isso aq pra ver se e necessari o
id INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE usuario_adm(
id_usuario INT,
id_adm INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_adm) REFERENCES adm(id)
);

CREATE TABLE suporte(
id INT AUTO_INCREMENT PRIMARY KEY,
dia DATE,
id_arquivo INT,
hora TIME, 
descricao VARCHAR(50),
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

CREATE TABLE usuario_suporte(
id_usuario INT,
id_suporte INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_suporte) REFERENCES suporte(id)
);
