from pathlib import Path

from sistema_biblioteca.repository import BibliotecaRepository
from sistema_biblioteca.services import Biblioteca


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT_DIR / "data" / "biblioteca.json"


def main() -> None:
    repository = BibliotecaRepository(DATA_FILE)
    biblioteca = Biblioteca(repository)

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip()

        try:
            if opcao == "1":
                cadastrar_livro(biblioteca)
            elif opcao == "2":
                cadastrar_usuario(biblioteca)
            elif opcao == "3":
                listar_livros(biblioteca)
            elif opcao == "4":
                listar_usuarios(biblioteca)
            elif opcao == "5":
                emprestar_livro(biblioteca)
            elif opcao == "6":
                devolver_livro(biblioteca)
            elif opcao == "7":
                listar_emprestimos(biblioteca)
            elif opcao == "8":
                buscar_livro(biblioteca)
            elif opcao == "0":
                print("Sistema encerrado. Ate logo!")
                break
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError as erro:
            print(f"Erro: {erro}")


def mostrar_menu() -> None:
    print("\n===== Sistema de Biblioteca =====")
    print("1. Cadastrar livro")
    print("2. Cadastrar usuario")
    print("3. Listar livros")
    print("4. Listar usuarios")
    print("5. Emprestar livro")
    print("6. Devolver livro")
    print("7. Listar emprestimos")
    print("8. Buscar livro")
    print("0. Sair")


def cadastrar_livro(biblioteca: Biblioteca) -> None:
    titulo = input("Titulo do livro: ")
    autor = input("Autor do livro: ")
    ano = ler_ano_opcional()

    livro = biblioteca.cadastrar_livro(titulo=titulo, autor=autor, ano=ano)
    print(f"Livro cadastrado com sucesso! Codigo: {livro.codigo}")


def cadastrar_usuario(biblioteca: Biblioteca) -> None:
    nome = input("Nome do usuario: ")
    email = input("Email do usuario (opcional): ")

    usuario = biblioteca.cadastrar_usuario(nome=nome, email=email)
    print(f"Usuario cadastrado com sucesso! Codigo: {usuario.codigo}")


def listar_livros(biblioteca: Biblioteca) -> None:
    livros = biblioteca.listar_livros()

    if not livros:
        print("Nenhum livro cadastrado.")
        return

    print("\nLivros cadastrados:")
    for livro in livros:
        ano = livro.ano if livro.ano else "Ano nao informado"
        status = "Disponivel" if livro.disponivel else "Emprestado"
        print(f"{livro.codigo} - {livro.titulo} | {livro.autor} | {ano} | {status}")


def listar_usuarios(biblioteca: Biblioteca) -> None:
    usuarios = biblioteca.listar_usuarios()

    if not usuarios:
        print("Nenhum usuario cadastrado.")
        return

    print("\nUsuarios cadastrados:")
    for usuario in usuarios:
        email = usuario.email if usuario.email else "Email nao informado"
        print(f"{usuario.codigo} - {usuario.nome} | {email}")


def emprestar_livro(biblioteca: Biblioteca) -> None:
    codigo_livro = ler_codigo("Codigo do livro: ")
    codigo_usuario = ler_codigo("Codigo do usuario: ")

    biblioteca.emprestar_livro(codigo_livro, codigo_usuario)
    print("Emprestimo realizado com sucesso!")


def devolver_livro(biblioteca: Biblioteca) -> None:
    codigo_livro = ler_codigo("Codigo do livro para devolucao: ")

    biblioteca.devolver_livro(codigo_livro)
    print("Devolucao realizada com sucesso!")


def listar_emprestimos(biblioteca: Biblioteca) -> None:
    emprestimos = biblioteca.listar_emprestimos()

    if not emprestimos:
        print("Nenhum emprestimo ativo.")
        return

    print("\nEmprestimos ativos:")
    for emprestimo in emprestimos:
        livro = biblioteca.obter_livro(emprestimo.codigo_livro)
        usuario = biblioteca.obter_usuario(emprestimo.codigo_usuario)
        print(
            f"Livro: {livro.titulo} | Usuario: {usuario.nome} | "
            f"Data: {emprestimo.data_emprestimo}"
        )


def buscar_livro(biblioteca: Biblioteca) -> None:
    termo = input("Digite parte do titulo ou autor: ")
    livros = biblioteca.buscar_livros(termo)

    if not livros:
        print("Nenhum livro encontrado.")
        return

    print("\nLivros encontrados:")
    for livro in livros:
        status = "Disponivel" if livro.disponivel else "Emprestado"
        print(f"{livro.codigo} - {livro.titulo} | {livro.autor} | {status}")


def ler_codigo(mensagem: str) -> int:
    valor = input(mensagem).strip()

    if not valor.isdigit():
        raise ValueError("Digite um codigo numerico valido.")

    return int(valor)


def ler_ano_opcional() -> int | None:
    valor = input("Ano de publicacao (opcional): ").strip()

    if not valor:
        return None

    if not valor.isdigit():
        raise ValueError("Digite um ano numerico valido.")

    return int(valor)
