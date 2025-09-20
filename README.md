# Tattoo Finder (TF)

- [Tattoo Finder (TF)](#tattoo-finder-tf)
  - [1. O projeto:](#1-o-projeto)
  - [2. Nossa equipe:](#2-nossa-equipe)
  - [3. Arquitetura e tecnologias utilizadas:](#3-arquitetura-e-tecnologias-utilizadas)
    - [3.1 Front-end:](#31-front-end)
    - [3.2 Back-end:](#32-back-end)
    - [3.3 Banco de dados:](#33-banco-de-dados)
  - [4. Banco de dados](#4-banco-de-dados)
    - [DER:](#der)
    - [MER:](#mer)
  - [5. Requisitos funcionais e não funcionais](#5-requisitos-funcionais-e-não-funcionais)
    - [5.1 Requisitos funcionais:](#51-requisitos-funcionais)
      - [Para clientes (RF-C):](#para-clientes-rf-c)
      - [Para Tatuadores (RF-T):](#para-tatuadores-rf-t)
    - [5.2 Requisitos Não Funcionais](#52-requisitos-não-funcionais)
      - [Para o Sistema (RN):](#para-o-sistema-rn)
      - [Segurança (RN-S):](#segurança-rn-s)
      - [Usabilidade (RN-U):](#usabilidade-rn-u)

Projeto de PA2 2025 - Unifor

## 1. O projeto:

**Tattoo Finder** é uma plataforma web inovadora desenvolvida para conectar clientes em busca de tatuagens com tatuadores talentosos. O sistema oferece uma experiência personalizada onde usuários podem encontrar profissionais que melhor se adequam ao seu estilo preferido, enquanto tatuadores têm a oportunidade de promover seus trabalhos e expandir seu portfólio.

## 2. Nossa equipe:

A equipe da TF é formada por:

- **Leonardo Lima** - SCRUM Master e desenvolvedor front-end
- **Rodrigo Cabezas** - Desenvolvedor back-end
- **Renê Rodrigues** - Designer e administrador do banco de dados
- **Mariana Gonçalves (Lou)** - Diretor criativo e assistente de front-end

## 3. Arquitetura e tecnologias utilizadas:

### 3.1 Front-end:

- **HTML5**: Esqueleto e fundação do site
- **CSS3 (com flexbox)**: Estilização do projeto

### 3.2 Back-end:

- **Python**: Linguagem de programação principal
- **Flask**: Framework leve para utilização do Python na web
- **SQLAlchemy**: ORM para manipulação do banco de dados

### 3.3 Banco de dados:

- **MySQL**: Sistema de gerenciamento de banco de dados relacional

## 4. Banco de dados

O banco de dados da TF foi formado após análise do nosso designer sobre as entidades do nosso sistema:

- usuario
- cliente
- tatuador
- mensagem
- feedback
- publicacao
- tag

### DER:

<img width="2042" height="1542" alt="DER - TattooFider" src="https://github.com/TattooFinder/TattooFinder/blob/main/docs/DER%20-%20TattooFider.png" />

### MER:

<img width="3182" height="2132" alt="MER - TattoFinder" src="https://github.com/TattooFinder/TattooFinder/blob/main/docs/MER%20-%20TattoFinder.png" />

## 5. Requisitos funcionais e não funcionais

### 5.1 Requisitos funcionais:

#### Para clientes (RF-C):

- RF-C01: Criar conta de usuário como cliente
- RF-C02: Editar perfil pessoal (nome, email, cidade)
- RF-C03: Adicionar e gerenciar telefones de contato
- RF-C04: Buscar tatuadores por filtros (estilo, localização, especialidade do momento)
- RF-C05: Visualizar perfis completos de tatuadores (portfólio, descrição, contatos)
- RF-C06: Enviar emails ou mensagem no whatsapp para tatuadores
- RF-C07: Publicar feedback e avaliações sobre tatuadores
- RF-C08: Gerenciar próprias avaliações publicadas

#### Para Tatuadores (RF-T):

- RF-T01: Criar conta de usuário como tatuador
- RF-T02: Editar perfil profissional (nome, email, cidade, descrição)
- RF-T03: Adicionar e gerenciar telefones de contato
- RF-T04: Publicar trabalhos no portfólio (imagens, título, descrição)
- RF-T05: Gerenciar publicações (criar, editar, excluir)
- RF-T06: Adicionar tags categorizadoras ao perfil
- RF-T07: Associar tags às publicações
- RF-T08: Visualizar feedbacks e avaliações recebidas

### 5.2 Requisitos Não Funcionais

#### Para o Sistema (RN):

- RN01: Tempo de resposta inferior a 2 segundos para todas as requisições
- RN02: Interface responsiva compatível com dispositivos móveis e desktop
- RN03: Sistema deve suportar até 100 usuários concorrentes
- RN04: Dados sensíveis como senhas, devem ser criptografados no banco de dados
- RN05: Backup automático diário do banco de dados
- RN06: Compatibilidade com principais navegadores (Chrome, Firefox, Safari, Edge)
- RN07: Documentação técnica da API e banco de dados

#### Segurança (RN-S):

- RN-S01: Autenticação obrigatória para acesso às funcionalidades
- RN-S02: Validação de dados em front-end e back-end
- RN-S03: Criptografia de senhas usando algoritmo bcrypt(?)
- RN-S04: Controle de acesso baseado em perfis de usuário

#### Usabilidade (RN-U):

- RN-U01: Interface intuitiva com curva de aprendizado inferior a 10 minutos
- RN-U02: Sistema de busca com filtros intuitivos e resultados relevantes
- RN-U03: Tempo de carregamento de páginas inferior a 3 segundos
- RN-U04: Navegação simplificada com no máximo 3 cliques para funcionalidades principais
