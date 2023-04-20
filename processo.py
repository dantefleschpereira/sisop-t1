import re


class Processo:

    # Essa linha possibilita gerar ids sequenciais automaticamente para cada processo criado
    proximo_pid = 1
    escalanador = ''

    def setEscalanador(modo: str):
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
        # Seleciona propriedade a ser usada na comparação entre processos de acordo com o modo de escalonamento
        self.modo.append(self.prioridade if Processo.escalanador ==
                         '1' else self.tempo_execucao)
        print(self.modo[0])

        Processo.proximo_pid += 1

    def __repr__(self):
        # return f"Processo {self.pid} (prioridade: {self.prioridade}, quantum: {self.quantum}, tempo execução: {self.tempo_execucao}, tempo chegada: {self.tempo_chegada} , tempo restante: {self.tempo_restante})"
        return f"Processo {self.pid}. Prioridade: {self.prioridade} Chegada {self.tempo_chegada}"

    def __eq__(self, other) -> bool:
        return self.modo[0] == other.modo[0]

    def __lt__(self, other) -> bool:
        # print(f'Processo {self.pid} < Processo {other.pid}')
        if self == other:
            # print(f'Tempo Chegada {self.tempo_chegada} < {other.tempo_chegada} = {self.tempo_chegada < other.tempo_chegada}')
            return self.tempo_chegada < other.tempo_chegada
        # print(f'Prioridade {self.prioridade} < {other.prioridade} = {self.prioridade < other.prioridade}')
        return self.modo[0] < other.prioridade

    def __le__(self, other) -> bool:
        if self < other:
            return True
        if self == other:
            return True
        return False

    # Carrega as instruções que estão no arquivo.txt direto na logica do processo
    def carregar_instrucoes(self, nome_do_arquivo):
        with open(nome_do_arquivo, 'r') as instrucoes:
            self.logica = instrucoes.read()

    # Le o campo da Memoria
    def parseMem(self, memoria):
        print(memoria.pop(0))
        for n in range(len(memoria)):
            instrucao = memoria[0].strip()
            print(instrucao)
            if (instrucao == '.enddata'):
                memoria.pop(0)
                return
            variavel, valor = instrucao.split()
            self.memDados[variavel] = int(valor)
            print(len(memoria))
            print(memoria.pop(0))
            print(len(memoria))
            print()
        raise Exception(f'.enddata não foi encontrado')

    # Le o campo de instrucoes
    def parseIns(self, instrucoes):
        labelAux = {}
        noIdLabel = {}
        instrucoes.pop(0)
        # Itera lista de instrucoes
        for n in range(len(instrucoes)):
            # Pega primeiro item da lista, removendo-o
            instrucao = instrucoes[0].strip()
            # Se for um endcode termine
            if (instrucao == '.endcode'):
                if len(noIdLabel) > 0:
                    raise Exception(
                        f'Encontrado comando de salto com label inválido {noIdLabel}')
                self.memIns.append(instrucoes.pop(0))
                return
            # Verifica se instrucao possui uma label em um dos seguintes padroes
            # loop: add 1
            # ou
            # loop:
            # add 1
            aux = re.search(r"^(\w+):(\s(\w+\s\w+))?", instrucao)
            if (aux):
                # pega o trecho label:
                label = aux.group(1)
                # se label for duplicata Exception
                if label in labelAux:
                    raise Exception(
                        f'label {label} encontrado mais de uma vez\nLinha {labelAux.get(label)} e na linha {n}')
                labelAux[label] = n
                # se label ja tiver sido invocada por uma instrucao branch
                if label in noIdLabel.keys():
                    # para cada instrucao branch que invoca esta label
                    for i in noIdLabel.get(label):
                        # substitua a label na instrucao pelo numeral representante da linha em que a label foi encontrada
                        self.memIns[i - 1] = re.sub(label, f'{n}', self.memIns[i - 1])
                    # removo-a do dicionario noIdLabel (labels, [branches]) para labels ainda não identificadas
                    noIdLabel.pop(label)

                # Se label estiver sozinha em sua propria linha
                # ex. loop:
                # remova-a da lista e continue a iteracao
                if (aux.group(2) == None):
                    instrucoes.pop(0)
                    continue
                # caso contrario
                # loop: add 1
                # recupera a instrucao e adiciona a memoria de instrucao memIns
                instrucao = aux.group(3)
            # separa instrucao do operando
            op, valor = instrucao.split()
            # se for uma instrucao branch
            if (re.search(r"^br", op)):
                # verifique se a label ja foi encontrada
                if valor in labelAux:
                    # se sim, subsititua label com numeral representante da linha em que label se encontra
                    labelPos = labelAux.get(valor)
                    self.memIns.append(f'{op} {labelPos}')
                    instrucoes.pop(0)
                    continue
                # se nao, e label ainda nao estiver no dicionario (labels, [branches]) noIdLabel, adicione-a de maneira a mapear uma lista
                # de todas as instrucoes de branch que invocam esta mesma label
                elif valor not in noIdLabel.keys():
                    noIdLabel[valor] = [n]
                # se label ja estiver no dicionario noIdLabel, adicione instrucao a lista mapeada pela label
                else:
                    noIdLabel[valor].append(n)
            # adicione instrucao a memIns e a remova da lista de instrucoes
            self.memIns.append(instrucao)
            instrucoes.pop(0)
        raise Exception(f'.endcode não encontrado')

    def compile(self):
        programa = self.logica.splitlines()
        programa = list(filter(lambda ins: ins != '', programa))
        while (len(programa) > 0):
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

    def getStatistics(self):
        self.turnAround = self.waitingTime + self.processingTime + self.blockedTime
        print(f'PROCESSO {self.pid}\nTURN_AROUND: {self.turnAround}\nPROCESSING_TIME: {self.processingTime}\nBLOCKED_TIME: {self.blockedTime}\nWAITING_TIME: {self.waitingTime}\nFINALIZED_TIME: {self.finalizedTime}')
