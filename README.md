# Sistema de Biblioteca

Sistema de gerenciamento de biblioteca feito em Python, com cadastro de livros,
cadastro de usuarios, emprestimos, devolucoes, busca e persistencia de dados em
JSON.

Este projeto foi criado para portfolio, com foco em organizacao de codigo,
clareza, boas praticas e facilidade de execucao.

## Funcionalidades

- Cadastro de livros
- Cadastro de usuarios
- Listagem de livros e usuarios
- Emprestimo de livros
- Devolucao de livros
- Listagem de emprestimos ativos
- Busca de livros por titulo ou autor
- Salvamento automatico dos dados em arquivo JSON

## Tecnologias

- Python 3.10+
- JSON
- Programacao orientada a objetos
- Testes com `unittest`

## Estrutura do projeto

```txt
sistema-biblioteca/
├── main.py
├── README.md
├── .gitignore
├── src/
│   └── sistema_biblioteca/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── repository.py
│       └── services.py
└── tests/
    └── test_biblioteca.py
```

## Como executar

Entre na pasta do projeto:

```powershell
cd "C:\sistema-biblioteca"
```

Execute o sistema:

```powershell
py main.py
```

## Como usar

Ao iniciar, o sistema mostra um menu:

```txt
1. Cadastrar livro
2. Cadastrar usuario
3. Listar livros
4. Listar usuarios
5. Emprestar livro
6. Devolver livro
7. Listar emprestimos
8. Buscar livro
0. Sair
```

Os dados cadastrados ficam salvos automaticamente no arquivo:

```txt
data/biblioteca.json
```

## Como rodar os testes

```powershell
py -m unittest discover -s tests
```

## Objetivo do projeto

Este projeto demonstra conhecimentos importantes para quem esta entrando na
area de tecnologia:

- organizacao de projeto Python;
- separacao de responsabilidades;
- manipulacao de arquivos JSON;
- criacao de classes;
- validacao de dados;
- testes automatizados;
- documentacao para GitHub.

