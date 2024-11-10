-- # criação do banco de dados e das tabelas em SQL

CREATE DATABASE IF NOT EXISTS webdriver;
USE webdriver;

CREATE TABLE IF NOT EXISTS plano(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(30) NOT NULL,
duracao TIME NOT NULL,
data_aquisicao DATE NOT NULL,
espaco_usuario VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS instituicao(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(30) NOT NULL,
endereco VARCHAR(100) NOT NULL,
causa_social VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS usuario(
id INT AUTO_INCREMENT PRIMARY KEY,
login VARCHAR(50) NOT NULL,
senha VARCHAR(30) NOT NULL,
email VARCHAR(50),
data_ingresso DATE NOT NULL,
id_instituicao INT,
FOREIGN KEY(id_instituicao) REFERENCES instituicao(id)
);

CREATE TABLE IF NOT EXISTS arquivo(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(30) NOT NULL,
tipo VARCHAR(30) NOT NULL,
permissao_acesso VARCHAR(5),
id_usuario INT,
URL VARCHAR(100),
FOREIGN KEY(id_usuario) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS historico_versionamento(
id INT AUTO_INCREMENT PRIMARY KEY,
id_usuario INT,
data_v DATE,
hora TIME,
id_arquivo INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

CREATE TABLE IF NOT EXISTS operacao(
id INT AUTO_INCREMENT PRIMARY KEY,
tipo VARCHAR(30) NOT NULL,
hora TIME,
data_o DATE
);

CREATE TABLE IF NOT EXISTS usuario_operacoes(
id_usuario INT,
id_operacao INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_operacao) REFERENCES operacao(id)
);

CREATE TABLE IF NOT EXISTS comentario(
id INT AUTO_INCREMENT PRIMARY KEY,
conteudo VARCHAR(150),
id_arquivo INT,
data_c DATE,
hora TIME,
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

CREATE TABLE IF NOT EXISTS usuario_comentario(
id_usuario INT,
id_comentario INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_comentario) REFERENCES comentario(id)
);

CREATE TABLE IF NOT EXISTS compartilhamento(
id INT AUTO_INCREMENT PRIMARY KEY,
id_dono INT,
id_compartilhado INT,
data_c DATE,
FOREIGN KEY(id_dono) REFERENCES usuario(id),
FOREIGN KEY(id_compartilhado) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS usuario_compartilhamento(
id_usuario INT,
id_compartilhamento INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_compartilhamento) REFERENCES compartilhamento(id)
);

CREATE TABLE  IF NOT EXISTS adm( 
-- #analisar isso aq pra ver se e necessario
id INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS usuario_adm(
id_usuario INT,
id_adm INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_adm) REFERENCES adm(id)
);

CREATE TABLE  IF NOT EXISTS suporte(
id INT AUTO_INCREMENT PRIMARY KEY,
dia DATE,
id_arquivo INT,
hora TIME, 
descricao VARCHAR(50),
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

CREATE TABLE IF NOT EXISTS usuario_suporte(
id_usuario INT,
id_suporte INT,
FOREIGN KEY(id_usuario) REFERENCES usuario(id),
FOREIGN KEY(id_suporte) REFERENCES suporte(id)
);

CREATE TABLE IF NOT EXISTS atividades_recentes(
id_arquivo INT PRIMARY KEY,
ultima_versao DATE,
acesso VARCHAR(20) NOT NULL,
FOREIGN KEY(id_arquivo) REFERENCES arquivo(id)
);

-- # TRIGGERS

DELIMITER //

CREATE TRIGGER insercao_drive
BEFORE INSERT ON arquivo
FOR EACH ROW
BEGIN
    IF NEW.tipo = '.exe' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Esse arquivo não pode ser salvo, pois é um arquivo executável.';
    END IF;
END;
//

CREATE TRIGGER Registrar_operacao
AFTER UPDATE ON arquivo
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM atividades_recentes WHERE id_arquivo = NEW.id) THEN
        UPDATE atividades_recentes 
        SET ultima_versao = CURDATE()
        WHERE id_arquivo = NEW.id;
    ELSE
        INSERT INTO atividades_recentes (id_arquivo, ultima_versao, acesso)
        VALUES (NEW.id, CURDATE(), 'default');
    END IF;
END;
//

CREATE TRIGGER atualizar_acesso
AFTER INSERT ON compartilhamento
FOR EACH ROW
BEGIN
    INSERT INTO historico_versionamento (id_usuario, id_arquivo, data_v, hora)
    VALUES (NEW.id_compartilhado, NEW.id_dono, CURDATE(), CURTIME());
END;
//

DELIMITER ;
