-- Apaga o schema se ele já existir, para garantir um ambiente limpo
DROP SCHEMA IF EXISTS tf_db;

-- Cria o schema e o seleciona
CREATE SCHEMA tf_db;
USE tf_db;

-- Tabela de usuários base
CREATE TABLE usuario(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- Tabela de tatuadores, com referência ao usuário
CREATE TABLE tatuador(
    id_tatuador INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    descricao VARCHAR(255) NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

-- Tabela de clientes, com referência ao usuário
CREATE TABLE cliente(
    id_cliente INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

-- Tabela de telefones do cliente (permite múltiplos números)
CREATE TABLE telefone_cliente(
    id_cliente INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_cliente, numero),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
);

-- Tabela de telefones do tatuador (permite múltiplos números)
CREATE TABLE telefone_tatuador(
    id_tatuador INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_tatuador, numero),
    FOREIGN KEY (id_tatuador) REFERENCES tatuador(id_tatuador) ON DELETE CASCADE
);

-- Tabela de publicações feitas por tatuadores
CREATE TABLE publicacao(
    id_publicacao INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    data_publicacao DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    id_tatuador INT NOT NULL,
    FOREIGN KEY (id_tatuador) REFERENCES tatuador(id_tatuador) ON DELETE CASCADE
);

-- Tabela de tags criadas por tatuadores
CREATE TABLE tag(
    id_tag INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    id_tatuador INT NOT NULL,
    FOREIGN KEY (id_tatuador) REFERENCES tatuador(id_tatuador) ON DELETE CASCADE
);

-- Tabela de associação entre publicações e tags
CREATE TABLE publicacao_tag(
    id_publicacao INT NOT NULL,
    id_tag INT NOT NULL,
    q_publicacao INT NOT NULL, -- Mantendo a coluna como no original, embora o propósito não seja 100% claro
    PRIMARY KEY (id_publicacao, id_tag),
    FOREIGN KEY (id_publicacao) REFERENCES publicacao(id_publicacao) ON DELETE CASCADE,
    FOREIGN KEY (id_tag) REFERENCES tag(id_tag) ON DELETE CASCADE
);

-- Tabela de feedbacks de clientes para tatuadores
CREATE TABLE feedback(
    id_feedback INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    data_publicacao DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    nota_avaliativa INT NOT NULL,
    id_cliente INT NOT NULL,
    id_tatuador INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_tatuador) REFERENCES tatuador(id_tatuador) ON DELETE CASCADE
);

-- Tabela de mensagens (mantida conforme estrutura original, caso seja usada no futuro)
CREATE TABLE mensagem(
    id_mensagem INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    data_publicacao DATE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    id_cliente INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
);