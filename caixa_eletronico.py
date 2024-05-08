import os
import time
import sys
import re
from datetime import datetime


LIMITE_SAQUES_DIARIOS = 3
LIMITE_VALOR_SAQUE = 500
AGENCIA = '0001'
sequencia_numero_conta = 0

clientes = []
contas = []

def menu():

    print("[u] Criar Cliente")
    print("[c] Criar Conta Corrente")
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[l] Listar Contas")
    print("[q] Sair")

def exibir_titulo(texto):

    os.system('cls')

    linha = '*'*len(texto)

    print(linha)
    print(texto)
    print(linha)

    print()    

def esperar_tecla():
   print("Pressione qualquer tecla para continuar...")
   sys.stdin.read(1)

def exibir_extrato(extrato, saldo):
   print(extrato)
   print()
   print(f"Saldo atual: {"{:.2f}".format(saldo)}")
   esperar_tecla()   

def criar_cliente():

   global clientes

   cpf = input("Informe o CPF (somente números):")

   cliente = buscar_cliente(cpf, clientes)

   if cliente:
      print('cliente já cadastrado')
      esperar_tecla()
      return 
      
   nome     = input("Informe o nome do cliente:")
   data_nascimento = input("Informe data nascimento:")
   endereco = input("Informe o  endereco:")

   clientes.append({"nome":nome, "data_nascimento": data_nascimento, "cpf": re.sub('[^0-9]', '', cpf), "endereco":endereco})
   
   print('Cliente cadastrado com sucesso.')
   esperar_tecla();

def criar_conta():

   global contas, clientes,sequencia_numero_conta, AGENCIA

   cpf = input("Informe o cpf do usuário:")

   cliente =  buscar_cliente(cpf, clientes)

   if not cliente:
      print('cliente não localizado.')
      esperar_tecla();
      return
   
   sequencia_numero_conta += 1
   
   contas.append({"agencia":AGENCIA,"numero_conta":sequencia_numero_conta,"cliente":cliente})

   print(f'Conta cadastrado com sucesso para o cpf {cpf}')
   esperar_tecla();

def listar_contas():
   global contas
   
   for conta in contas:
       
       print("Dados Cliente: \n")
       print(f"""Titular: {conta["cliente"]["nome"]} CPF: {conta["cliente"]["cpf"]} Endereco: {conta["cliente"]["endereco"]}""")

       print("Dados Conta:\n")
       print(f"""Titular: {conta["agencia"]} numero conta: {conta["numero_conta"]}""")

   esperar_tecla();
   
def buscar_cliente(cpf, clientes):

   cliente  = [cliente for cliente in clientes if cliente["cpf"] == cpf]
   
   return cliente[0] if cliente else None

def atualizar_saldo(valor,saldo):
     
   saldo += valor
   return saldo

def registrar_extrato(mensagem,/,*, data ,saldo_anterior, saldo):
   return f"""{mensagem} realizado em {data}, saldo alterado de R$ {"{:.2f}".format(saldo_anterior)} para R$ {"{:.2f}".format(saldo)}. \n"""
   

def efetuar_deposito(saldo,extrato):

   valor_deposito = int(input("Digite o valor para depósito:"));
   saldo,extrato = depositar(valor_deposito,saldo,extrato)
   
   return [saldo,extrato]
   
def depositar(valor_deposito,saldo,extrato,/):  

   if valor_deposito > 0: 
         
     saldo_atual = saldo;
     
     saldo = atualizar_saldo(valor_deposito,saldo)
     
     extrato += registrar_extrato(f"""Deposito no valor de R$ {"{:.2f}".format(valor_deposito)}.""",saldo_anterior=saldo_atual,data=datetime.now(),saldo=saldo)
     
     print("Deposito realizado com sucesso")
     
   else:  
     print("Deposito não realizado, problemas com o valor")
   
   esperar_tecla()
   return [saldo,extrato]

def efetuar_saque(saldo,extrato,numero_saques):

   valor_saque = int(input("Digite o valor para saque:"));

   saldo,extrato,numero_saques = sacar(valor_saque=valor_saque,saldo=saldo,extrato=extrato,numero_saques=numero_saques)

   return [saldo,extrato,numero_saques]

def pode_realizar_saque(valor_saque, numero_saques, saldo):  

   if (verificar_excedeu_numero_saque(numero_saques)):
      print("Saque não realizado. Excedido o limite de saque.")      
      return False
   
   if (verificar_excedeu_valor_saque(valor_saque)):
      print("Saque não realizado. Valor maior que o permitido.")    
      return False      

   if (verificar_saldo_maior_valor_saque(valor_saque, saldo)):
      print("Saque não realizado. Saldo insuficiente")    
      return False
   
   return True

def verificar_excedeu_numero_saque(numero_saques):
    return numero_saques >= LIMITE_SAQUES_DIARIOS

def verificar_excedeu_valor_saque(valor_saque):
    return valor_saque > LIMITE_VALOR_SAQUE

def verificar_saldo_maior_valor_saque(valor_saque, saldo):
    return valor_saque > saldo

def sacar(*,valor_saque,saldo,extrato,numero_saques):   
   
   if (pode_realizar_saque(valor_saque, numero_saques, saldo)):

      saldo_atual = saldo
      saldo = atualizar_saldo(valor_saque*-1,saldo)
    
      numero_saques += 1
      
      extrato +=registrar_extrato(f"""Saque no valor de R$ {"{:.2f}".format(valor_saque)}.""",saldo_anterior=saldo_atual,data=datetime.now(),saldo=saldo)
      
      print("Saque realizado com sucesso")      
   
   esperar_tecla()

   return [saldo,extrato,numero_saques]

def exibir_opcoes():
    
    saldo   = 0
    extrato = ""
    numero_saques = 0

    while True:
   
        os.system('cls')
        menu()

        opcao = input()

        if opcao == "c":      
            
            os.system('cls')
            exibir_titulo("Cadastrar Conta Corrente")
            criar_conta()
        
        elif opcao == "d":      
            
            os.system('cls')
            exibir_titulo("Efetuar Deposito")
            saldo,extrato = efetuar_deposito(saldo,extrato)

        elif opcao == "s":
      
            os.system('cls')
            exibir_titulo("Efetuar Saque")
            saldo,extrato,numero_saques = efetuar_saque(saldo,extrato,numero_saques)
        elif opcao == "e": 
      
            os.system('cls')
            exibir_titulo("Exibir extrato")
            exibir_extrato(extrato, saldo)            
   
        elif opcao == "u": 
            
            os.system('cls')
            exibir_titulo("Cadastrar cliente")
            criar_cliente()

        elif opcao == "l": 
            
            os.system('cls')
            exibir_titulo("Listar Contas")
            listar_contas()            
      
        elif opcao == "q":
            
            print("Encerrando ...")
            time.sleep(2)
            os.system('cls')
            break

def main(): 

    os.system('cls');    
    exibir_opcoes()    

if __name__ == '__main__':
    main();
