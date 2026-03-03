class Produto:
    def __init__(self, nome, quantidade=1, preco=0, desconto=0):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.desconto = desconto


class Cliente:
    def __init__(self, nome, email, senha, itens=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.carrinho = Carrinho()

        if itens:
            for item in itens:
                self.carrinho.adicionar_produto(
                    Produto(item['nome'], item['quantidade'], item['preco'], item.get('desconto', 0)),
                    item['quantidade']
                )


class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto, quantidade=1):
        for item in self.itens:
            if item.nome == produto.nome:
                item.quantidade += quantidade
                return
        
        produto_copiado = Produto(
            produto.nome,
            quantidade,
            produto.preco,
            produto.desconto
        )

        self.itens.append(produto_copiado)

    def remover_produto(self, produto, quantidade=1):
        for item in self.itens:
            if item.nome == produto.nome:
                if item.quantidade > quantidade:
                    item.quantidade -= quantidade
                else:
                    self.itens.remove(item)
                break

    def calcular_total(self):
        total = 0
        for item in self.itens:
            preco_final = item.preco * (1 - item.desconto / 100)
            total += preco_final * item.quantidade
        return total