from processo import Processo
from cpu import Cpu
import random

processos = []

# Solicita ao usuário qual escalonador ele quer usar
escalonador = input("Digite 1 para Round Robin ou 2 para Shortest-Job-First: ")
if escalonador != '1' and escalonador != '2':
    raise Exception(f'Modo de Escalanador {escalonador} invalido') 
Processo.setEscalanador(escalonador)

quantidade_programas = int(
    input("Digite a quantidade de programas que deseja criar: "))
   # Cria uma instancia da CPU

cpu_ = Cpu(quantidade_programas, escalonador)

# Solicita ao usuário a quantidade de programas que deseja criar
# Cria um loop para receber as informações de cada processo
for i in range(quantidade_programas):
    arquivo = input(f"Qual o nome do arquivo {i+1}? ")
    tempo_chegada = int(input("Qual o tempo de chegada? "))
    prioridade = int(input("Qual a prioridade do processo? "))
    quantum = int(input("Qual o quantum do processo? "))
    tempo_execucao = int(input("Qual o tempo de execução do processo? "))
    print()
    #Cria um processo
    process = Processo(tempo_chegada=tempo_chegada,
                      prioridade=prioridade, quantum=quantum, tempo_execucao=tempo_execucao)
    process.carregar_instrucoes(arquivo)
    process.compile()
    cpu_.adicionar_processo(process)
    #Carrega as instruções que estão no arquivo.txt na lógica do processo que foi criado

# process = Processo(tempo_chegada=0, prioridade=0, quantum=25, tempo_execucao=80)
# process.carregar_instrucoes('programa04.txt')
# process.compile()      
# cpu_.adicionar_processo(process)
# process2 = Processo(tempo_chegada=10, prioridade=1, quantum=1, tempo_execucao=4)
# process2.carregar_instrucoes('programa01.txt')
# process2.compile()      
# cpu_.adicionar_processo(process2)
# process3 = Processo(tempo_chegada=12, prioridade=0, quantum=25, tempo_execucao=5)
# process3.carregar_instrucoes('programa04.txt')
# process3.compile()      
# cpu_.adicionar_processo(process3)
cpu_.run()