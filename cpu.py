import queue
import processo

class Cpu:

    # Construtor com os atributos de uma CPU
    def __init__(self, n):
        #self.memoria_ram = {}
        self.fila_bloqueados = []
        self.fila_prontos = queue.PriorityQueue(n)
        self.pc = 0
        self.acc = 0
        self.memDados = {}
        self.memIns = []
        self.programa_em_execucao = str()
        self.quantum = None
        self.processo_atual = None
        self.tempo = 0

    # Método para adicionar processos na fila de prontos
    def adicionar_processo(self, processo):
        processo.estado = 'waiting'
        self.fila_bloqueados.append(processo)
        
    def getNextProcesso(self) -> processo:
        #Desbloqueia Processos
        while self.fila_bloqueados:
            aux = self.fila_bloqueados[0]
            if aux.tempo_chegada <= self.tempo:
                aux.estado = 'ready'
                print(f'Tempo: {self.tempo} {aux} Pronto')
                self.fila_prontos.put(self.fila_bloqueados.pop(0))
            else:
                break
        
        if self.fila_prontos.empty():
            if self.processo_atual is None and not self.fila_bloqueados:
                exit(0)
            return self.processo_atual
        else:
            nextProcess = self.fila_prontos.queue[0]
            if self.processo_atual is None:
                self.processo_atual = self.fila_prontos.get()
            else:
                if self.processo_atual <= nextProcess: 
                    return self.processo_atual
                else:
                    print(f'{self.processo_atual} DESALOCADO\nALOCANDO {nextProcess}')
                    self.fila_prontos.get()
                    self.processo_atual.estado = 'waiting'
                    self.processo_atual.status_acc = self.acc
                    self.processo_atual.status_pc = self.pc
                    self.fila_prontos.put(self.processo_atual)
            
            self.processo_atual = nextProcess
            self.processo_atual.estado = 'running'
            self.pc = self.processo_atual.status_pc
            self.acc = self.processo_atual.status_acc
            self.memDados = self.processo_atual.memDados
            self.memIns = self.processo_atual.memIns
            return self.processo_atual
        
    def run(self):
        self.fila_bloqueados.sort(key=lambda x: x.tempo_chegada)
        while True:
            self.getNextProcesso()
            print(f'Tempo: {self.tempo} {self.processo_atual} Exec')
            if self.processo_atual is None:
                continue
            #self.processo_atual.tempo_execucao -= 1
            #if self.processo_atual.tempo_execucao <= 0:
            #    print(f"Tempo: {self.tempo} {self.processo_atual} encerrado")
            #    for processo in self.fila_prontos.queue:
            #        print(processo)
            #    print()
            #    self.processo_atual = None
            
            self.tempo += 1
            # Executa o processo
            instrucao = self.memIns[self.pc]
            if(instrucao == '.endcode'): 
                print(f"Tempo: {self.tempo} {self.processo_atual} encerrado")
                for processo in self.fila_prontos.queue:
                    print(processo)
                    print()
                self.processo_atual = None
                continue
            self.executar_instrucao(instrucao)
            
        print('\nFim do Sistema de Execução Dinâmica de Processos\n')
        print(self.memDados)


    def executar_instrucao(self, instr):
        operacao, op1 = instr.split()
        match(operacao):
            case 'add':
                self.acc += self.get_operando(op1)
            
            case 'sub':
                self.acc -= self.get_operando(op1)
            
            case 'mul':
                self.acc *= self.get_operando(op1)
            
            case 'div':
                self.acc /= self.get_operando(op1)
            
            case 'load':
                self.acc = self.get_operando(op1)
            
            case 'store':
                self.memDados[op1] = self.acc
                #for chave, valor in self.memDados.items():
                    #print(f'Valor de {chave} = {valor}')
            
            case 'brany':
                self.pc = int(op1)
                return
            
            case 'brpos':
                if self.acc > 0:
                    self.pc = int(op1)
                    return
            
            case 'brzero':
                if self.acc == 0:
                    self.pc = int(op1)
                    return
            
            case 'brneg':
                if self.acc < 0:
                    self.pc = int(op1)
                    return
            
            case 'syscall':
                self.operacoes_syscall(op1)
            
            case _:
                raise Exception(f'Intrução inválida: {instr}')
            
        self.pc += 1

    def get_operando(self, operando):
        if operando.startswith('#'):
            return int(operando[1:])
        else:
            return self.memDados[operando]

    def operacoes_syscall(self, indice):
        if indice == '0':
            # exit(0)
            print('Esse processo foi encerrado por syscall')
            self.processo_atual.estado = "exit"
            print(f"Tempo: {self.tempo} {self.processo_atual} encerrado")
            for processo in self.fila_prontos.queue:
                print(processo)
            print(self.memDados)
            self.processo_atual = None
        elif indice == '1':
            print(self.acc)
        elif indice == '2':
            self.acc = int(input("Informe um valor inteiro: "))
        else:
            raise Exception(f'Comando inválido: {indice}')
        
    

