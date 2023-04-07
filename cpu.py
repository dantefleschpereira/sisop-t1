
class Cpu:

    # Construtor com os atributos de uma CPU
    def __init__(self):
        self.pc = 0
        self.acc = 0
        self.memoria = {}
        self.programa_em_execucao = str()
        self.quantum = None
        self.processo_atual = None
        self.fila_prontos = [] # Alterar para queue? 

    # Método para adicionar processos na fila de prontos
    def adicionar_processo(self, processo):
        self.fila_prontos.append(processo)

    # Escalonador Shortest-Job-First
    def sjf(self):
        
        # Interrupção - se tiver algum processo com tempo de execução menor na fila (o atual vai pro fim)
        # Interrupção - quando há uma chamada do sistema
        # Caso o pedido seja de uma impressão ou leitura a partir da chamada do sistema, este processo deverá assumir o estado de bloqueado e um intervalo de tempo de permanência neste estado deverá ser assumido (aleatório entre 8 e 10 unidades de tempo). Passado este tempo, o processo pode avançar para o estado de pronto
        # guardar os resultados obtidos do programa que foi interrompido.
        
        # Ordena a lista de processos prontos de acordo com o tempo de execuçãoão
        self.fila_prontos.sort(key=lambda x: x.tempo_execucao) #Importante ver a diferença com o tempo de chegada, pois mesmo que um programa seja menor, se ele chegou depois ele só vai entrar na execução quando chegar.
        
        # Obtém o próximo processo a ser executado
        proximo_processo = self.fila_prontos.pop(0)
        
        # Executa o processo
        self.processo_atual = proximo_processo
        self.quantum = self.processo_atual.quantum
        self.processo_atual.tempo_restante -= self.quantum
        print(f"Executando {self.processo_atual}...")
        
        # Se o processo ainda tiver tempo restante, coloca-o de volta na fila de processos prontos
        if self.processo_atual.tempo_restante > 0:
            self.fila_prontos.append(self.processo_atual)
        self.processo_atual = None
 
    # Escalonador RoudRobin
    # *Pendente: a cada intervalo de tempo, interromper o processador, reavaliar as prioridades
    def rr(self):

        while self.fila_prontos:
            # Ordena a lista de processos prontos de acordo com a prioridade
            self.fila_prontos.sort(key=lambda x: x.prioridade)

            # Obtém o próximo processo a ser executado
            proximo_processo = self.fila_prontos.pop(0)

            # Executa o processo
            self.processo_atual = proximo_processo
            self.quantum = self.processo_atual.quantum
            self.processo_atual.tempo_restante -= self.quantum # *Talvez alterar a lógica do cálculo de tempo_restante...
            print(f"Executando {self.processo_atual}...")
            
            programa = self.processo_atual.logica
            programa = programa.splitlines()
            secao = ''
            for instrucao in programa:
                instrucao = instrucao.strip()
                if instrucao.startswith('.'):
                    secao = instrucao
                    continue
                if secao == '.data':
                    variavel, valor = instrucao.split()
                    self.memoria[variavel] = int(valor)
                elif secao == '.code':
                    self.executar_instrucao(instrucao)
                elif secao == '.enddata':
                    continue
                else:
                    raise Exception(f'Seção Inválida: {secao}')

            # Se o processo ainda tiver tempo restante, coloca-o de volta na fila de processos prontos
            if self.processo_atual.tempo_restante > 0:
                self.fila_prontos.append(self.processo_atual)
            self.processo_atual = None

    def executar_instrucao(self, instr):
        operacao, op1 = instr.split()
        if operacao == 'add':
            self.acc += self.get_operando(op1)
        elif operacao == 'sub':
            self.acc -= self.get_operando(op1)
        elif operacao == 'mul':
            self.acc *= self.get_operando(op1)
        elif operacao == 'div':
            self.acc /= self.get_operando(op1)
        elif operacao == 'load':
            self.acc = self.get_operando(op1)
        elif operacao == 'store':
            self.memoria[op1] = self.acc
        elif operacao == 'brany':
            self.pc = self.get_label(op1)
        elif operacao == 'brpos':
            if self.acc > 0:
                self.pc = self.get_label(op1)
        elif operacao == 'brzero':
            if self.acc == 0:
                self.pc = self.get_label(op1)
        elif operacao == 'brneg':
            if self.acc < 0:
                self.pc = self.get_label(op1)
        elif operacao == 'syscall':
            self.operacoes_syscall(op1)
        else:
            raise Exception(f'Invalid instruction: {instr}')
        self.pc += 1

    def get_operando(self, operando):
        if operando.startswith('#'):
            return int(operando[1:])
        else:
            return self.memoria[operando]

    def get_label(self, label):
        return int(label[:-1])

    def operacoes_syscall(self, indice):
        if indice == '0':
            exit(0)
        elif indice == '1':
            print(self.acc)
        elif indice == '2':
            self.acc = int(input("Informe um valor inteiro: "))
        else:
            raise Exception(f'Comando inválido: {indice}')
