import json
from pathlib import Path

from sistema_biblioteca.models import Emprestimo, Livro, Usuario


class BibliotecaRepository:
    def __init__(self, caminho_arquivo: Path):
        self.caminho_arquivo = caminho_arquivo

    def carregar(self) -> dict:
        if not self.caminho_arquivo.exists():
            return self._dados_iniciais()

        with self.caminho_arquivo.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar(
        self,
        livros: dict[int, Livro],
        usuarios: dict[int, Usuario],
        emprestimos: list[Emprestimo],
        proximo_codigo_livro: int,
        proximo_codigo_usuario: int,
    ) -> None:
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        dados = {
            "livros": [livro.to_dict() for livro in livros.values()],
            "usuarios": [usuario.to_dict() for usuario in usuarios.values()],
            "emprestimos": [emprestimo.to_dict() for emprestimo in emprestimos],
            "proximo_codigo_livro": proximo_codigo_livro,
            "proximo_codigo_usuario": proximo_codigo_usuario,
        }

        with self.caminho_arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    @staticmethod
    def _dados_iniciais() -> dict:
        return {
            "livros": [],
            "usuarios": [],
            "emprestimos": [],
            "proximo_codigo_livro": 1,
            "proximo_codigo_usuario": 1,
        }
