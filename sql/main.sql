create schema tf_db;
use tf_db;

create table usuario(
id_usuario int not null auto_increment primary key,
email varchar(20) not null
senha varchar(20) not null,
);

create table cliente(
id_cliente int not null auto_increment primary key,
nome varchar(20) not null,
cidade varchar(20) not null,
id_usuario int not null,
foreign key (id_usuario) references usuario(id_usuario)
);

create table telefone_cliente(
id_cliente int not null primary key,
numero varchar(20) not null,
foreign key (id_cliente) references cliente(id_cliente)
);

create table mensagem(
id_mensagem int not null auto_increment primary key,
titulo varchar(20) not null,
data_publicacao date not null,
descricao varchar(100) not null,
id_cliente int not null,
foreign key (id_cliente) references cliente(id_cliente)
);

create table feedabck(
id_feedback int not null auto_increment primary key,
titulo varchar(20) not null,
data_publicacao date not null,
descricao varchar(100) not null,
nota_avaliativa int not null,
id_cliente int not null,
foreign key (id_cliente) references cliente(id_cliente)
);

create table tatuador(
id_tatuador int not null auto_increment primary key,
descricao varchar(100) null,
nome varchar(20) not null,
cidade varchar(20) not null,
id_usuario int not null,
foreign key (id_usuario) references usuario(id_usuario)
);

create table telefone_tatuador(
id_tatuador int not null primary key,
numero varchar(20) not null,
foreign key (id_tatuador) references tatuador(id_tatuador)
);

create table publicacao(
id_publicacao int not null auto_increment primary key,
titulo varchar(20) not null,
data_publicacao date not null,
descricao varchar(100) not null,
id_tatuador int not null,
foreign key (id_tatuador) references tatuador(id_tatuador)
);

create table tag(
id_tag int not null auto_increment primary key,
nome varchar(20) not null,
descricao varchar(100) not null,
id_tatuador int not null,
foreign key (id_tatuador) references tatuador(id_tatuador)
);

create table publicacao_tag(
id_publicacao int not null,
id_tag int not null,
q_publicacao int not null,
primary key (id_publicacao,id_tag),
foreign key (id_publicacao) references publicacao(id_publicacao),
foreign key (id_tag) references tag(id_tag)
)
