from data import Repository
from model import Venda
from exceptions import ProdutoNaoEncontradoException


class VendaService:

    def __init__(self):
        self.repository = Repository()
        self.lista_produtos = self.repository.carregar_produtos()
        self.venda_atual = None

    def iniciar_venda(self):
        self.venda_atual = Venda()
        return self.venda_atual

    def processar_codigo(self, codigo, quantidade=1):
        for produto in self.lista_produtos:
            if codigo == produto.codigo:
                self.venda_atual.adicionar_itens(produto, quantidade)
                return
        raise ProdutoNaoEncontradoException("Produto não encontrado.")

    def finaliza_venda(self):
        total = self.venda_atual.calcula_total()

        for item in self.venda_atual.itens:
            item.produto.quantidade_estoque -= item.quantidade

        self.repository.salvar_produtos(self.lista_produtos)

        self.venda_atual = None

        return total

    def buscar_produto(self, codigo):
        for produto in self.lista_produtos:
            if codigo == produto.codigo:
                return produto
        raise ProdutoNaoEncontradoException("Produto não encontrado.")
