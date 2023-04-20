import queue
import processo
import random

class Cpu:

    # Construtor com os atributos de uma CPU
    def __init__(self, n, escalanador):
        #self.memoria_ram = {}
        self.fila_bloqueados = []
        self.fila_prontos = queue.PriorityQueue(n)
        self.listaProcessos = []
        self.pc = 0
        self.acc = 0
        self.memDados = {}
        self.memIns = []
        self.programa_em_execucao = str()
        self.quantum = None
        self.processo_atual = None
        self.tempo = 0
        self.escalanador = escalanador

    # Método para adicionar processos na fila de prontos
    def adicionar_processo(self, processo):
        processo.estado = 'waiting'
        self.fila_bloqueados.append(processo)
        self.listaProcessos.append(processo)
        
    def getNextProcesso(self) -> processo:
        #Desbloqueia/Inicializa Processos
        while self.fila_bloqueados:
            aux = self.fila_bloqueados[0]
            if aux.tempo_chegada <= self.tempo:
                aux.estado = 'ready'
                print(f'    {aux} Pronto')
                self.fila_prontos.put(self.fila_bloqueados.pop(0))
            else:
                break
        
        #Se fila de pronts, bloqueados estiverem vazias e o processo atual for None, encerre o programa
        if self.fila_prontos.empty():
            if self.processo_atual is None and not self.fila_bloqueados:
                print('Todos os Processos foram encerrados')
                for processo in self.listaProcessos:
                    processo.getStatistics()
                    print()
                exit(0)
            return self.processo_atual
        else:
            #Pega o proximo processo da fila e verifica se este tem prioridade sobre o processo atual
            nextProcess = self.fila_prontos.queue[0]
            if self.processo_atual is None:
                self.processo_atual = self.fila_prontos.get()
            else:
                if self.processo_atual <= nextProcess: 
                    return self.processo_atual
                else:
                    #Salva contexto
                    print(f'    {self.processo_atual} DESALOCADO')
                    self.fila_prontos.get()
                    self.processo_atual.estado = 'waiting'
                    self.processo_atual.status_acc = self.acc
                    self.processo_atual.status_pc = self.pc
                    self.fila_prontos.put(self.processo_atual)

            #Troca de contexto 
            print(f'    ALOCANDO {nextProcess}')
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
            print(f'TEMPO: {self.tempo}')
            self.getNextProcesso()
            self.tempo += 1
            if self.processo_atual is None:
                continue
            
            if(self.escalanador == '1'):
                #Verifica se Quantum estourou
                if self.processo_atual.quantumRemainder:
                    self.processo_atual.quantumRemainder -= 1
                else:
                    #Se, sim salva o contexto e para de executar processo, colocando o novamente na fila de processos prontos
                    print(f'\n      Quantum PROCESSO {self.processo_atual.pid} estourado. DESALOCANDO\n')
                    self.processo_atual.quantumRemainder = self.processo_atual.quantum
                    self.processo_atual.tempo_chegada = self.tempo
                    self.processo_atual.estado = 'waiting'
                    self.processo_atual.status_acc = self.acc
                    self.processo_atual.status_pc = self.pc

                    self.fila_prontos.put_nowait(self.processo_atual)
                    self.processo_atual = None
                    continue
            
            # Executa o processo
            instrucao = self.memIns[self.pc]
            print(f'    PROCESSO {self.processo_atual.pid}\n         {instrucao}')
            if(instrucao == '.endcode'): 
                print(f"    PROCESSO {self.processo_atual.pid} encerrado")
                self.processo_atual.estado = 'exit'
                print(self.memDados)
                self.processo_atual.getStatistics()
                self.processo_atual = None
                continue

            for processo in self.listaProcessos:
                match processo.estado:
                    case 'waiting':
                        processo.waitingTime += 1
                    case 'running':
                        processo.processingTime += 1
                    case 'exit':
                        processo.finalizedTime += 1
                    case 'blocked':
                        processo.blockedTime += 1
                    case 'new':
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
                return
            
            case 'IO':
                print(f'OPERACAO IO {op1} PROCESSO {self.processo_atual.pid}')
                self.processo_atual.memIns[self.pc] = f'syscall {op1}'
                match op1:
                    case '1':
                        print(self.acc)
                    case '2':
                        self.acc = int(input("Informe um valor inteiro: "))
            case _:
                raise Exception(f'Intrução inválida: {instr}')
            
        self.pc += 1

    def get_operando(self, operando):
        if operando.startswith('#'):
            return int(operando[1:])
        else:
            return self.memDados[operando]

    def operacoes_syscall(self, indice):
        tempo_espera = random.randint(8, 10)
        if indice == '0':
            print('     Esse processo foi encerrado por syscall')
            self.processo_atual.estado = "exit"
            print(f"    PROCESSO {self.processo_atual.pid} encerrado")
            print(self.memDados)
            self.processo_atual.getStatistics()
            self.processo_atual = None
            return
        elif indice == '1' or indice == '2':
            print(f'     OP IO: BLOQUEANDO Processo{self.processo_atual.pid} POR {tempo_espera} UT')
            self.processo_atual.estado = 'blocked'
            self.processo_atual.status_acc = self.acc
            self.processo_atual.status_pc = self.pc
            self.processo_atual.memIns[self.pc] = f'IO {indice}'
            self.processo_atual.tempo_chegada = tempo_espera + self.tempo
            self.fila_bloqueados.append(self.processo_atual)
            self.fila_bloqueados.sort(key=lambda x: x.tempo_chegada)
            self.processo_atual = None
            return

        raise Exception(f'Comando inválido: {indice}')
        
        
    

