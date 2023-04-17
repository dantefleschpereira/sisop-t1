def calcular_waiting_time_sjf(fila_processos):
    n = len(fila_processos) # Quantidade de processos na fila

    # Criar uma lista vazia para armazenar o tempo de espera de cada processo
    waiting_time = [0] * n  # Lista que contém n elementos iguais a zero

    # Inicializar o tempo de término do processo anterior como 0
    tempo_termino_anterior = 0

    # Ordenar os processos pelo tempo de execução
    processos_ordenados = sorted(
        fila_processos, key=lambda x: x['tempo_execucao'])

    # Tempo de espera de cada processo
    for i in range(n):
        # Tempo de início do processo
        # Calcula o tempo de início do processo i como o máximo entre o tempo de término do processo anterior e o tempo de chegada do processo atual.
        tempo_inicio = max(
            tempo_termino_anterior, processos_ordenados[i]['tempo_chegada'])

        # Tempo de término do processo
        tempo_fim = tempo_inicio + processos_ordenados[i]['tempo_execucao']

        # Tempo de espera do processo
        atual_waiting_time = tempo_inicio - \
            processos_ordenados[i]['tempo_chegada']

        # Incluir o tempo de espera do processo à lista de tempo de espera
        waiting_time[processos_ordenados[i]['pid'] - 1] = atual_waiting_time

        # Atualizar o tempo de término do processo anterior
        tempo_termino_anterior = tempo_fim

    return waiting_time


if __name__ == '__main__':

    # Exemplo de uso
    lista_processos = [
        {'pid': 1, 'tempo_chegada': 3, 'tempo_execucao': 8},
        {'pid': 2, 'tempo_chegada': 2, 'tempo_execucao': 9},
        {'pid': 3, 'tempo_chegada': 1, 'tempo_execucao': 11},
    ]

    waiting_time = calcular_waiting_time_sjf(lista_processos)

    # Imprime o tempo de espera de cada processo
    for i in range(len(waiting_time)):
        print("Tempo de espera do processo", i+1, "=", waiting_time[i])
