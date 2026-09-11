import pandas as pd
from model import Produto, Livro, Roupa


class Repository:

    def carregar_produtos(self):

        dados = pd.read_excel("estoque.xlsx", dtype={"Codigo": str})
        produtos = []

        for i, linha in dados.iterrows():

            if linha["Categoria"] == "Livro":
                livro = Livro(linha["Codigo"], linha["Categoria"], linha["Nome"], linha["Preco"], linha["QuantidadeEstoque"], linha["Autor"], linha["Editora"], linha["Paginas"])
                produtos.append(livro)
            elif linha["Categoria"] == "Roupa":
                roupa = Roupa(linha["Codigo"], linha["Categoria"], linha["Nome"], linha["Preco"], linha["QuantidadeEstoque"], linha["Modelo"], linha["Tamanho"], linha["Cor"])
                produtos.append(roupa)
            else:
                produto = Produto(linha["Codigo"], linha["Categoria"], linha["Nome"], linha["Preco"], linha["QuantidadeEstoque"])
                produtos.append(produto)

        return produtos

    def converter_para_linhas(self, produtos):
        lines = []
        for produto in produtos:
            if isinstance(produto, Livro):
                line = {
                    "Codigo": produto.codigo,
                    "Categoria": produto.categoria,
                    "Nome": produto.nome,
                    "Preco": produto.preco,
                    "QuantidadeEstoque": produto.quantidade_estoque,
                    "Autor": produto.autor,
                    "Editora": produto.editora,
                    "Paginas": produto.paginas
                }
                lines.append(line)
            elif isinstance(produto, Roupa):
                line = {
                    "Codigo": produto.codigo,
                    "Categoria": produto.categoria,
                    "Nome": produto.nome,
                    "Preco": produto.preco,
                    "QuantidadeEstoque": produto.quantidade_estoque,
                    "Modelo": produto.modelo,
                    "Tamanho": produto.tamanho,
                    "Cor": produto.cor
                }
                lines.append(line)
            else:
                line = {
                    "Codigo": produto.codigo,
                    "Categoria": produto.categoria,
                    "Nome": produto.nome,
                    "Preco": produto.preco,
                    "QuantidadeEstoque": produto.quantidade_estoque
                }
                lines.append(line)

        return lines

    def salvar_produtos(self, produtos):
        linhas = self.converter_para_linhas(produtos)
        novo_df = pd.DataFrame(linhas)
        novo_df.to_excel("estoque.xlsx", index=False)
