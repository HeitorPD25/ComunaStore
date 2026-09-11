class Produto:
    def __init__(self, codigo, categoria, nome, preco, quantidade_estoque):
        self.codigo = codigo
        self.categoria = categoria
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

    def __str__(self):
        return f"{self.codigo} -> {self.nome} -> {self.categoria} -> R${self.preco:.2f} -> {self.quantidade_estoque}"


class Livro(Produto):

    def __init__(self, codigo, categoria, nome, preco, quantidade_estoque, autor, editora, paginas):
        super().__init__(codigo, categoria, nome, preco, quantidade_estoque)
        self.autor = autor
        self.editora = editora
        self.paginas = paginas

    def __str__(self):
        return super().__str__() + f" -> {self.autor} -> {self.editora} -> {self.paginas}"


class Roupa(Produto):

    def __init__(self, codigo, categoria, nome, preco, quantidade_estoque, modelo, tamanho, cor):
        super().__init__(codigo, categoria, nome, preco, quantidade_estoque)
        self.modelo = modelo
        self.tamanho = tamanho
        self.cor = cor

    def __str__(self):
        return super().__str__() + f" -> {self.modelo} -> {self.tamanho} -> {self.cor}"


class ItemVenda:

    def __init__(self, produto, quantidade=1):
        self.produto = produto
        self.quantidade = quantidade

    def calcula_subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.produto.nome} - Quant: {self.quantidade} == R${self.calcula_subtotal():.2f}"


class Venda:

    def __init__(self):
        self.itens = []

    def adicionar_itens(self, produto, quantidade=1):
        for item in self.itens:
            if item.produto.codigo == produto.codigo:
                item.quantidade += quantidade
                return
        item = ItemVenda(produto, quantidade)
        self.itens.append(item)

    def calcula_total(self):
        total = 0
        for item in self.itens:
            total += item.calcula_subtotal()
        return total
