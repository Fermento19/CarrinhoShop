import json

jdata = 'databse/data.json'

def carregar_dados():
    with open(jdata, 'r') as file:
        data = json.load(file)
    return data

def salvar_dados(data):
    with open(jdata, 'w') as file:
        json.dump(data, file, indent=4)

def registro_json(name, email, senha):
    data = carregar_dados()
    
    if any(cliente['email'] == email for cliente in data['clientes']):
        print("Email já registrado.")
        return False
    novo_cliente = {"name": name, "email": email, "senha": senha, "carrinho": []}
    data['clientes'].append(novo_cliente)

    salvar_dados(data)
    
    return criar_Cliente(novo_cliente)


def autenticar(email, senha):
    data = carregar_dados()
    
    for cliente in data['clientes']:
        if cliente['email'] == email and cliente['senha'] == senha:
            return criar_Cliente(cliente)
    print("Email ou senha incorretos.")
    return None

def criar_Cliente(cliente_json):
    from classes import Cliente
    return Cliente(cliente_json['name'], cliente_json['email'], cliente_json['senha'], cliente_json.get('carrinho', []))


def ver_carrinho(cliente):
    atualizar_carrinho(cliente)
    if not cliente.carrinho.itens:
        print("\nSeu carrinho está vazio.")
    else:
        print("\nItens no carrinho:")
        for item in cliente.carrinho.itens:
            print(f"{item.quantidade}x {item.nome}: R${item.preco:.2f}")

def adicionar_produto(cliente, produto, quantidade=1):
    cliente.carrinho.adicionar_produto(produto, quantidade)
    print(f"{produto.nome} adicionado ao carrinho.")
    atualizar_carrinho(cliente)

def remover_produto(cliente, produto, quantidade=1):
    cliente.carrinho.remover_produto(produto, quantidade)
    print(f"{produto.nome} removido do carrinho.")
    atualizar_carrinho(cliente)

def atualizar_carrinho(cliente):
    data = carregar_dados()
    
    for cliente_json in data['clientes']:
        if cliente_json['email'] == cliente.email:

            cliente_json['carrinho'] = [
                {
                    'nome': item.nome,
                    'quantidade': item.quantidade,
                    'preco': item.preco,
                    'desconto': item.desconto
                }
                for item in cliente.carrinho.itens
                if item.quantidade > 0
            ]

            break

    salvar_dados(data)

def user_escolha():
    try:
        esc= int(input("Escolha uma opção (Número): "))
    except ValueError:
        print("digite um número válido com as opções...")
        return None
    return esc