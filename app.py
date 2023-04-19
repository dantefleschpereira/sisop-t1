from processo import Processo
from cpu import Cpu
import random

processos = []
cpu = Cpu(10)
#for i in range(5):
#    processo = Processo(logica=random.choice([True, False]),
#                        tempo_chegada=random.randint(0, 3),
#                        prioridade=random.randint(1, 3),
#                        quantum=random.randint(1, 5),
#                        tempo_execucao=random.randint(2, 3))
#    cpu.adicionar_processo(processo)

#for i in range(9):
#    print(f'{cpu.fila_bloqueados.queue[i]} range')
#
#print()
#while not cpu.fila_bloqueados.empty():
#    print(f'{cpu.fila_bloqueados.get()}')


#cpu.run()

# Solicita ao usuário qual escalonador ele quer usar
escalonador = "1" #input("Digite 1 para Round Robin ou 2 para Shortest-Job-First: ")

quantidade_programas = 1 #int(
       #input("Digite a quantidade de programas que deseja criar: "))
   # Cria uma instancia da CPU

cpu_ = Cpu(2)

# Executa o escalonador correspondente
if escalonador == "1":

   # Solicita ao usuário a quantidade de programas que deseja criar


   # Cria um loop para receber as informações de cada processo
   #for i in range(quantidade_programas):
       #arquivo = input(f"Qual o nome do arquivo {i+1}? ")
       #tempo_chegada = int(input("Qual o tempo de chegada? "))
       #prioridade = int(input("Qual a prioridade do processo? "))
       #quantum = int(input("Qual o quantum do processo? "))
       #tempo_execucao = int(input("Qual o tempo de execução do processo? "))
       #print()

       # Cria um processo
       #process = Processo(tempo_chegada=tempo_chegada,
       #                   prioridade=prioridade, quantum=quantum, tempo_execucao=tempo_execucao)

       # Carrega as instruções que estão no arquivo.txt na lógica do processo que foi criado
    process = Processo(tempo_chegada=0, prioridade=3, quantum=1, tempo_execucao=1)
    process.carregar_instrucoes('programa04.txt')
    process.compile()      
    cpu_.adicionar_processo(process)

    process2 = Processo(tempo_chegada=10, prioridade=2, quantum=1, tempo_execucao=1)
    process2.carregar_instrucoes('programa01.txt')
    process2.compile()      
    cpu_.adicionar_processo(process2)

    process3 = Processo(tempo_chegada=12, prioridade=1, quantum=1, tempo_execucao=1)
    process3.carregar_instrucoes('programa02.txt')
    process3.compile()      
    cpu_.adicionar_processo(process3)

    cpu_.run()

#    # Executa Round Robin
#elif escalonador == "2":
#
#    # Cria um loop para receber as informações de cada processo
#    for i in range(quantidade_programas):
#        arquivo = input(f"Qual o nome do arquivo {i+1}? ")
#        tempo_chegada = int(input("Qual o tempo de chegada? "))
#        tempo_execucao = int(input("Qual o tempo de execução do processo? "))
#
#        # Cria um processo
#        process = Processo(tempo_chegada=tempo_chegada,
#                           tempo_execucao=tempo_execucao)
#
#        # Carrega as instruções que estão no arquivo.txt na lógica do processo que foi criado
#        process.carregar_instrucoes(arquivo)
#
#        # Adiciona o processo na lista de processos prontos
#        cpu_.adicionar_processo(process)
#
#    # Executa Shortest-Job-First
#    cpu_.sjf()
#else:
#    print("Opção inválida")
#