
import os
import time
import sys
from datetime import datetime

saldo   = 0
limit   = 500
extrato = ""
numero_saques         = 0
LIMITE_SAQUES_DIARIOS = 3

def menu():
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[q] Sair")

def esperar_tecla():
   print("Pressione qualquer tecla para continuar...")
   sys.stdin.read(1)     

def exibir_extrato():
   print(extrato)
   esperar_tecla()

def atualizar_saldo(valor):
   global saldo
   saldo += valor

def efetuar_deposito():   
   valor_deposito = int(input("Digite o valor para depósito:"));
   depositar(valor_deposito)
   
def depositar(valor_deposito):

   global saldo, extrato

   if valor_deposito > 0: 
         
     saldo_atual = saldo;
     
     atualizar_saldo(valor_deposito)
     
     extrato += f"""Deposito no valor de R$ {"{:.2f}".format(valor_deposito)} realizado em {datetime.now()}, saldo alterado de R$ {"{:.2f}".format(saldo_atual)} para R$ {"{:.2f}".format(saldo)}. \n"""
     print("Deposito realizado com sucesso")
     time.sleep(2)
   else:  
     print("Deposito não realizado, problemas com o valor")

def efetuar_saque():   
   valor_saque = int(input("Digite o valor para saque:"));
   sacar(valor_saque)

def pode_realizar_saque(valor_saque):

   global numero_saques, saldo

   if (numero_saques >= LIMITE_SAQUES_DIARIOS):
      print("Saque não realizado. Excedido o limite de saque.")      
      return False
   
   if (valor_saque > limit):
      print("Saque não realizado. Valor maior que o permitido.")    
      return False      

   if (valor_saque > saldo):
      print("Saque não realizado. Saldo insuficiente")    
      return False
   
   return True  

def sacar(valor_saque):

   global saldo, extrato, numero_saques
   
   if (pode_realizar_saque(valor_saque)):

      saldo_atual = saldo
      atualizar_saldo(valor_saque*-1)
    
      numero_saques += 1

      extrato += f"""Saque no valor de R$ {"{:.2f}".format(valor_saque)} realizado em {datetime.now()}, saldo alterado de R$ {"{:.2f}".format(saldo_atual)} para R$ {"{:.2f}".format(saldo)}. \n"""
      print("Saque realizado com sucesso")
      time.sleep(4)
   else:
      esperar_tecla()

while True:
   
   os.system('cls')
   menu()

   opcao = input()

   if   opcao == "d":
      os.system('cls')
      print("****Efetuar Deposito****")
      efetuar_deposito()
   elif opcao == "s":
      os.system('cls')
      print("****Efetuar Saque****")
      efetuar_saque()
   elif opcao == "e": 
      os.system('cls')
      print("****Extrato****")
      exibir_extrato();
   elif opcao == "q":
    print("Encerrando ...")
    time.sleep(2)
    os.system('cls')
    break