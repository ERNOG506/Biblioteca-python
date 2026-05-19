from dataclasses import asdict, dataclass


@dataclass
class Livro:
    codigo: int
    titulo: str
    autor: str
    ano: int | None = None
    disponivel: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Usuario:
    codigo: int
    nome: str
    email: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Emprestimo:
    codigo_livro: int
    codigo_usuario: int
    data_emprestimo: str

    def to_dict(self) -> dict:
        return asdict(self)
