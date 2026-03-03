from classes import Cliente
from classes import Carrinho
from classes import Produto
import funcoes as fc
import datetime

funcionando = True
cliente_logado = None
itens = [
    Produto("Notebook", 5,2500.00, 10),
    Produto("Mouse",7, 150.00),
    Produto("Teclado",14, 300.00),
    Produto("Monitor",5, 990.00),
    Produto("Impressora",2, 800.00, 15),
    Produto("Memoria Ram 8gb", 5, 1000)
    ]

print("Bem-vindo à Loja de compras Onliner!")
while funcionando and not cliente_logado:
    print("1. Registrar nova conta | 2. logar conta existente | 3. Sair: ")
    escolha = fc.user_escolha()
    if not escolha:
        continue
    if escolha == 1:
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        cliente = fc.registro_json(nome, email, senha)
        if cliente:
            print(f"Registro bem-sucedido! bem-vindo, {cliente.nome}!")
            cliente_logado = cliente
        else:
            print("Registro falhou. Tente novamente.")
            continue

    if escolha == 2:
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        cliente = fc.autenticar(email, senha)
        if not cliente:
            print("Falha na autenticação. Tente novamente.")
            continue
        print(f"Bem-vindo, {cliente.nome}!")
        cliente_logado = cliente

    elif escolha == 3:
        funcionando = False

while funcionando and cliente_logado:
    print("\nMenu:")
    print("1. Ver carrinho.")
    print("2. Adicionar produto ao carrinho.")
    print("3. Remover produto do carrinho.")
    print("4. Total do carrinho.")
    print("5. finalizar compra. (NOTA FISCAL)")
    print("6. Sair. (Suas alterações serão salvas)")

    escolha = fc.user_escolha()
    if not escolha:
        continue

    #Vizualizar carrinho
    if escolha == 1:
        fc.ver_carrinho(cliente_logado)

    #Adicionar produto ao carrinho
    elif escolha == 2:
        print("\nProdutos disponíveis:")
        for index, item in enumerate(itens, 1):
            print(f"{index}. {item.nome} - R${item.preco:.2f} - Quantidade: {item.quantidade}", f" |Há Desconto: {item.desconto}%" if item.desconto > 0 else "")
        
        produto_index = int(input("Digite o número do produto que deseja adicionar: ")) - 1
        quantidade = int(input("Digite a quantidade que deseja adicionar: "))

        if 0 <= produto_index < len(itens) and quantidade > 0 and quantidade <= itens[produto_index].quantidade:
            fc.adicionar_produto(cliente_logado, itens[produto_index], quantidade)
            itens[produto_index].quantidade -= quantidade
        else:
            print("Produto inválido.")

    #Remover produto do carrinho
    elif escolha == 3:
        if not cliente_logado.carrinho.itens:
            print("\nSeu carrinho está vazio.")
        else:
            print("\nItens no carrinho:")
            for index, item in enumerate(cliente_logado.carrinho.itens, 1):
                print(f"{index}. {item.nome} - R${item.preco:.2f} - Quantidade: {item.quantidade}")
            
            produto_index = int(input("Digite o número do produto que deseja remover: ")) - 1
            if 0 <= produto_index < len(cliente_logado.carrinho.itens):                
                quantidade = int(input("Digite a quantidade que deseja remover: "))
                
                if 0 < quantidade <= cliente_logado.carrinho.itens[produto_index].quantidade:
                    fc.remover_produto(cliente_logado, cliente_logado.carrinho.itens[produto_index], quantidade)
                    itens[produto_index].quantidade += quantidade
                else:
                    print("Quantidade inválida.")
            else:
                print("Produto inválido.")

    #Calcular total
    elif escolha == 4:
        total = cliente_logado.carrinho.calcular_total()
        print(f"\nValor total do carrinho com descontos aplicados: R${total:.2f}")

    #Gerar nota fiscal e finalizar compra
    elif escolha == 5:
        total = cliente_logado.carrinho.calcular_total()
        if total == 0:
            print("\nSeu carrinho está vazio. Adicione produtos antes de finalizar a compra.")
            continue 

        print("\nNota Fiscal:")
        print(f"Cliente: {cliente_logado.nome}, Email: {cliente_logado.email}")
        print("Data: ",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
        for item in cliente_logado.carrinho.itens:
            if item.desconto == 0:
                print(f"{item.quantidade}x {item.nome} - R${item.preco:.2f} cada")
            else:
                    preco_final = item.preco * (1 - item.desconto / 100)
                    print(f"{item.quantidade}x {item.nome} - R${preco_final:.2f} cada (Desconto: {item.desconto}%)")
        print(f"Total a pagar: R${total:.2f}")
        print("Obrigado por comprar!")
        cliente_logado.carrinho.itens.clear()
        fc.atualizar_carrinho(cliente_logado)

    elif escolha == 6:
        funcionando = False

print("Aplicação Encerrada - Até logo!")