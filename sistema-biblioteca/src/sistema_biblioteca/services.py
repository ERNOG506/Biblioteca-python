from datetime import date

from sistema_biblioteca.models import Emprestimo, Livro, Usuario
from sistema_biblioteca.repository import BibliotecaRepository


class Biblioteca:
    def __init__(self, repository: BibliotecaRepository):
        self.repository = repository
        dados = repository.carregar()

        self.livros = {
            livro["codigo"]: Livro(**livro)
            for livro in dados.get("livros", [])
        }
        self.usuarios = {
            usuario["codigo"]: Usuario(**usuario)
            for usuario in dados.get("usuarios", [])
        }
        self.emprestimos = [
            Emprestimo(**emprestimo)
            for emprestimo in dados.get("emprestimos", [])
        ]
        self.proximo_codigo_livro = dados.get("proximo_codigo_livro", 1)
        self.proximo_codigo_usuario = dados.get("proximo_codigo_usuario", 1)

    def cadastrar_livro(
        self,
        titulo: str,
        autor: str,
        ano: int | None = None,
    ) -> Livro:
        if not titulo.strip() or not autor.strip():
            raise ValueError("Titulo e autor sao obrigatorios.")

        livro = Livro(
            codigo=self.proximo_codigo_livro,
            titulo=titulo.strip(),
            autor=autor.strip(),
            ano=ano,
        )

        self.livros[livro.codigo] = livro
        self.proximo_codigo_livro += 1
        self._salvar()
        return livro

    def cadastrar_usuario(self, nome: str, email: str = "") -> Usuario:
        if not nome.strip():
            raise ValueError("Nome e obrigatorio.")

        usuario = Usuario(
            codigo=self.proximo_codigo_usuario,
            nome=nome.strip(),
            email=email.strip(),
        )

        self.usuarios[usuario.codigo] = usuario
        self.proximo_codigo_usuario += 1
        self._salvar()
        return usuario

    def listar_livros(self) -> list[Livro]:
        return list(self.livros.values())

    def listar_usuarios(self) -> list[Usuario]:
        return list(self.usuarios.values())

    def listar_emprestimos(self) -> list[Emprestimo]:
        return list(self.emprestimos)

    def buscar_livros(self, termo: str) -> list[Livro]:
        termo_normalizado = termo.strip().lower()
        if not termo_normalizado:
            return []

        return [
            livro
            for livro in self.livros.values()
            if termo_normalizado in livro.titulo.lower()
            or termo_normalizado in livro.autor.lower()
        ]

    def emprestar_livro(self, codigo_livro: int, codigo_usuario: int) -> Emprestimo:
        livro = self._obter_livro(codigo_livro)
        self._obter_usuario(codigo_usuario)

        if not livro.disponivel:
            raise ValueError("Este livro ja esta emprestado.")

        emprestimo = Emprestimo(
            codigo_livro=codigo_livro,
            codigo_usuario=codigo_usuario,
            data_emprestimo=date.today().isoformat(),
        )

        livro.disponivel = False
        self.emprestimos.append(emprestimo)
        self._salvar()
        return emprestimo

    def devolver_livro(self, codigo_livro: int) -> None:
        livro = self._obter_livro(codigo_livro)

        if livro.disponivel:
            raise ValueError("Este livro nao esta emprestado.")

        self.emprestimos = [
            emprestimo
            for emprestimo in self.emprestimos
            if emprestimo.codigo_livro != codigo_livro
        ]
        livro.disponivel = True
        self._salvar()

    def obter_livro(self, codigo_livro: int) -> Livro:
        return self._obter_livro(codigo_livro)

    def obter_usuario(self, codigo_usuario: int) -> Usuario:
        return self._obter_usuario(codigo_usuario)

    def _obter_livro(self, codigo_livro: int) -> Livro:
        if codigo_livro not in self.livros:
            raise ValueError("Livro nao encontrado.")
        return self.livros[codigo_livro]

    def _obter_usuario(self, codigo_usuario: int) -> Usuario:
        if codigo_usuario not in self.usuarios:
            raise ValueError("Usuario nao encontrado.")
        return self.usuarios[codigo_usuario]

    def _salvar(self) -> None:
        self.repository.salvar(
            livros=self.livros,
            usuarios=self.usuarios,
            emprestimos=self.emprestimos,
            proximo_codigo_livro=self.proximo_codigo_livro,
            proximo_codigo_usuario=self.proximo_codigo_usuario,
        )
