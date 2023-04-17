from processo import Processo
from cpu import Cpu


# Cria uma instancia da CPU
cpu_ = Cpu()

# Solicita ao usuário qual escalonador ele quer usar
escalonador = "1" #input("Digite 1 para Round Robin ou 2 para Shortest-Job-First: ")

# Executa o escalonador correspondente
if escalonador == "1":

    # Solicita ao usuário a quantidade de programas que deseja criar
    quantidade_programas = 1 #int(
        #input("Digite a quantidade de programas que deseja criar: "))

    # Cria um loop para receber as informações de cada processo
    for i in range(quantidade_programas):
        #arquivo = input(f"Qual o nome do arquivo {i+1}? ")
        #tempo_chegada = int(input("Qual o instante da carga? "))
        #prioridade = int(input("Qual a prioridade do processo? "))
        #quantum = int(input("Qual o quantum do processo? "))
        #tempo_execucao = int(input("Qual o tempo de execução do processo? "))
        print()

        # Cria um processo
        #process = Processo(tempo_chegada=tempo_chegada,
        #                   prioridade=prioridade, quantum=quantum, tempo_execucao=tempo_execucao)

        # Carrega as instruções que estão no arquivo.txt na lógica do processo que foi criado
        process = Processo(tempo_chegada=0, prioridade=1, quantum=1, tempo_execucao=1)
        process.carregar_instrucoes('programa01.txt')

        # Adiciona o processo na lista de processos prontos
        cpu_.adicionar_processo(process)

    # Executa Round Robin
elif escalonador == "2":

    # Solicita ao usuário a quantidade de programas que deseja criar
    quantidade_programas = int(
        input("Digite a quantidade de programas que deseja criar: "))

    # Cria um loop para receber as informações de cada processo
    for i in range(quantidade_programas):
        arquivo = input(f"Qual o nome do arquivo {i+1}? ")
        tempo_chegada = int(input("Qual o instante da carga? "))
        tempo_execucao = int(input("Qual o tempo de execução do processo? "))

        # Cria um processo
        process = Processo(tempo_chegada=tempo_chegada,
                           tempo_execucao=tempo_execucao)

        # Carrega as instruções que estão no arquivo.txt na lógica do processo que foi criado
        process.carregar_instrucoes(arquivo)

        # Adiciona o processo na lista de processos prontos
        cpu_.adicionar_processo(process)

    # Executa Shortest-Job-First
    cpu_.sjf()
else:
    print("Opção inválida")
