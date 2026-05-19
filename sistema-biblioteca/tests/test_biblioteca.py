import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sistema_biblioteca.repository import BibliotecaRepository
from sistema_biblioteca.services import Biblioteca


class BibliotecaTestCase(unittest.TestCase):
    def criar_biblioteca(self) -> Biblioteca:
        pasta_temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(pasta_temporaria.cleanup)

        caminho_arquivo = Path(pasta_temporaria.name) / "biblioteca.json"
        repository = BibliotecaRepository(caminho_arquivo)
        return Biblioteca(repository)

    def test_cadastra_livro(self):
        biblioteca = self.criar_biblioteca()

        livro = biblioteca.cadastrar_livro(
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            ano=1899,
        )

        self.assertEqual(livro.codigo, 1)
        self.assertEqual(livro.titulo, "Dom Casmurro")
        self.assertTrue(livro.disponivel)

    def test_empresta_e_devolve_livro(self):
        biblioteca = self.criar_biblioteca()
        livro = biblioteca.cadastrar_livro("Clean Code", "Robert C. Martin", 2008)
        usuario = biblioteca.cadastrar_usuario("Ana Silva", "ana@email.com")

        biblioteca.emprestar_livro(livro.codigo, usuario.codigo)
        self.assertFalse(biblioteca.obter_livro(livro.codigo).disponivel)
        self.assertEqual(len(biblioteca.listar_emprestimos()), 1)

        biblioteca.devolver_livro(livro.codigo)
        self.assertTrue(biblioteca.obter_livro(livro.codigo).disponivel)
        self.assertEqual(len(biblioteca.listar_emprestimos()), 0)

    def test_busca_livro_por_autor(self):
        biblioteca = self.criar_biblioteca()
        biblioteca.cadastrar_livro("O Cortico", "Aluisio Azevedo", 1890)

        resultados = biblioteca.buscar_livros("azevedo")

        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].titulo, "O Cortico")


if __name__ == "__main__":
    unittest.main()
