
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

    def readMem(self, instrucoes):
        print(instrucoes.pop(0))
        for n in range(len(instrucoes)):
            instrucao = instrucoes[0].strip()
            print(instrucao)
            if(instrucao == '.enddata'):
                instrucoes.pop(0)
                return instrucoes
            variavel, valor = instrucao.split()
            self.memoria[variavel] = int(valor)
            print(len(instrucoes))
            print(instrucoes.pop(0))
            print(len(instrucoes))
            print()
        raise Exception(f'.enddata not found')
        ...    
    
    def compile(self):
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
            secao = ''
            
            programa = self.processo_atual.logica
            programa = programa.splitlines()
            for instrucao in programa:
                instrucao = instrucao.strip()
                print(instrucao)
                if instrucao == '.data':
                    self.readMem(programa)
                    print(programa)
                    print(self.memoria)
                elif instrucao == '.code':
                    secao = '.code'
                    print(f'secao eh {secao}')
                elif secao == '.code':
                    if instrucao == '.endcode':
                        break
                    print(f'rodando instrucao: {instrucao}')
                    self.executar_instrucao(instrucao)
                else:
                    raise Exception(f'Seção Inválida: {instrucao}')

            # Se o processo ainda tiver tempo restante, coloca-o de volta na fila de processos prontos
            if self.processo_atual.tempo_restante > 0:
                self.fila_prontos.append(self.processo_atual)
            self.processo_atual = None
    
    # Escalonador Shortest-Job-First
    def sjf(self):
        ...

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
            print(self.memoria)
            exit(0)
        elif indice == '1':
            print(self.acc)
        elif indice == '2':
            self.acc = int(input("Informe um valor inteiro: "))
        else:
            raise Exception(f'Comando inválido: {indice}')
