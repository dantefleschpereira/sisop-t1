import re

class Processo:

    # Essa linha possibilita gerar ids sequenciais automaticamente para cada processo criado
    proximo_pid = 1
    escalanador = ''

    def setEscalanador(modo:str):
        Processo.escalanador = modo

    # Construtor com os atributos de um processo
    def __init__(self, logica=None, tempo_chegada=None, prioridade=None, quantum=None, tempo_execucao=None):

        self.pid = Processo.proximo_pid
        self.status_pc = 0
        self.status_acc = 0
        self.processingTime = 0
        self.turnAround = 0
        self.waitingTime = 0
        self.finalizedTime = 0
        self.blockedTime = 0
        self.estado = 'new'
        self.logica = logica
        self.memDados = {}
        self.memIns = []
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade
        self.quantum = quantum
        self.quantumRemainder = quantum
        self.tempo_execucao = tempo_execucao
        self.modo = []
        self.modo.append(self.prioridade if Processo.escalanador == '1' else self.tempo_execucao)
        print(self.modo[0])

        Processo.proximo_pid += 1

    def __repr__(self):
        #return f"Processo {self.pid} (prioridade: {self.prioridade}, quantum: {self.quantum}, tempo execução: {self.tempo_execucao}, tempo chegada: {self.tempo_chegada} , tempo restante: {self.tempo_restante})"
        return f"Processo {self.pid}. Prioridade: {self.prioridade} Chegada {self.tempo_chegada}"

    def __eq__(self, other) -> bool:
        return self.modo[0] == other.modo[0]
    
    def __lt__(self, other) -> bool:
        #print(f'Processo {self.pid} < Processo {other.pid}')
        if self == other:
            #print(f'Tempo Chegada {self.tempo_chegada} < {other.tempo_chegada} = {self.tempo_chegada < other.tempo_chegada}')
            return self.tempo_chegada < other.tempo_chegada
        #print(f'Prioridade {self.prioridade} < {other.prioridade} = {self.prioridade < other.prioridade}')
        return self.modo[0] < other.prioridade
    
    def __le__(self, other) -> bool:
        if self < other: return True
        if self == other: return True
        return False
        ...

    # Carrega as instruções que estão no arquivo.txt direto na logica do processo
    def carregar_instrucoes(self, nome_do_arquivo):
        with open(nome_do_arquivo, 'r') as instrucoes:
            self.logica = instrucoes.read()

    def parseMem(self, memoria):
        print(memoria.pop(0))
        for n in range(len(memoria)):
            instrucao = memoria[0].strip()
            print(instrucao)
            if(instrucao == '.enddata'):
                memoria.pop(0)
                return
            variavel, valor = instrucao.split()
            self.memDados[variavel] = int(valor)
            print(len(memoria))
            print(memoria.pop(0))
            print(len(memoria))
            print()
        raise Exception(f'.enddata not found')
        
    def parseIns(self, instrucoes):
        labelAux = {}
        noIdLabel = {}
        instrucoes.pop(0)
        for n in range(len(instrucoes)):
            instrucao = instrucoes[0].strip()
            if(instrucao == '.endcode'):
                if len(noIdLabel) > 0:
                    raise Exception(f'Found jump commands with invalid Labels {noIdLabel}')
                self.memIns.append(instrucoes.pop(0))
                return
            aux = re.search(r"^(\w+):(\s(\w+\s\w+))?", instrucao)
            if(aux):
                label = aux.group(1)
                if label in labelAux:
                    raise Exception(f'label {label} found in two instances\nLine {labelAux.get(label)} and in Line {n}')
                labelAux[label] = n
                if label in noIdLabel.keys():
                    for i in noIdLabel.get(label):
                        self.memIns[i] = re.sub(label, f'{n}', self.memIns[i])
                    noIdLabel.pop(label)
                if(aux.group(2) == None):
                    instrucoes.pop(0)
                    continue
                instrucao = aux.group(3)
            op, valor = instrucao.split()
            if(re.search(r"^br", op)):
                if valor in labelAux:
                    labelPos = labelAux.get(valor)
                    self.memIns.append(f'{op} {labelPos}')
                    instrucoes.pop(0)
                    continue
                elif valor not in noIdLabel.keys():
                    noIdLabel[valor] = [n]
                else:
                    noIdLabel[valor].append(n)
            self.memIns.append(instrucao)
            instrucoes.pop(0)
        raise Exception(f'.endcode not found')
            
    def compile(self):
        programa = self.logica.splitlines()
        programa = list(filter(lambda ins: ins != '', programa))
        while(len(programa) > 0):
            instrucao = programa[0].strip()
            if instrucao == '.data':
                self.parseMem(programa)
                print(programa)
                print(self.memDados)
            elif instrucao == '.code':
                self.parseIns(programa)
                print(programa)
                print(self.memIns)
        print(self.memDados)
        print(self.memIns)

#process = Processo(tempo_chegada=0, prioridade=1, quantum=1, tempo_execucao=1)
#process.carregar_instrucoes('programa04.txt')
#process.compile()
#
#processos = []
#for i in range(10):
#    processo = Processo(logica=random.choice([True, False]),
#                        tempo_chegada=random.randint(1, 10),
#                        prioridade=random.randint(1, 3),
#                        quantum=random.randint(1, 5),
#                        tempo_execucao=random.randint(5, 20))
#    processos.append(processo)
## put the processes into a priority queue based on their priority attribute
#lista = queue.PriorityQueue()
#for processo in processos:
#    lista.put((processo))
#
#while not lista.empty():
#    print(f'{lista.queue[0]} {lista.get()}')
