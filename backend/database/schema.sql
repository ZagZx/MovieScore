CREATE DATABASE moviescore;
USE moviescore;

CREATE TABLE usuario(
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    foto_perfil_url VARCHAR(255),
    data_criacao DATETIME NOT NULL
);

CREATE TABLE conteudo(
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	id_externo BIGINT NOT NULL,
    api_fonte VARCHAR(255) NOT NULL,
    tipo ENUM("Anime", "Filme", "Série") NOT NULL,
	data_adicao DATETIME NOT NULL,
    UNIQUE (id_externo, api_fonte) # não permite ser inserido mais de uma vez um id externo da mesma api
);

CREATE TABLE avaliacao(
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT NOT NULL,
    conteudo_id BIGINT NOT NULL,
    estrelas DECIMAL(2,1) NOT NULL,
    comentario TEXT,
	data_criacao DATETIME NOT NULL,
    data_atualizacao DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (conteudo_id) REFERENCES conteudo(id)
);

CREATE TABLE favorito(
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	usuario_id BIGINT NOT NULL,
    conteudo_id BIGINT NOT NULL,
	data_adicao DATETIME NOT NULL,
	FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (conteudo_id) REFERENCES conteudo(id)
);

CREATE TABLE assistido(
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	usuario_id BIGINT NOT NULL,
    conteudo_id BIGINT NOT NULL,
	data_adicao DATETIME NOT NULL,
	FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (conteudo_id) REFERENCES conteudo(id)
);