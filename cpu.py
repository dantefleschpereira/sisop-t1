from memoria import Memoria


class Cpu:

    # Construtor com os atributos de uma CPU
    def __init__(self):
        self.pc = 0
        self.acc = 0
        self.secao = ''
        self.processo_atual = None
        self.memoria = Memoria()

    # Método para adicionar processos na fila de prontos
    def adicionar_processo(self, processo):
        # self.fila_prontos.append(processo)
        self.memoria.fila_prontos.append(processo)
        # Ordena a lista de processos prontos de acordo com a prioridade
        self.memoria.fila_prontos.sort(key=lambda x: x.prioridade)

    # Escalonador Shortest-Job-First
    def sjf(self):
        menor_processo = min(self.memoria.fila_prontos, key=lambda x: x.tempo_execucao)
        print(menor_processo)
    # Escalonador RoudRobin
    def rr(self):

        while self.memoria.fila_prontos:

            # Obtém o próximo processo a ser executado
            proximo_processo = self.memoria.fila_prontos.pop(0)

            # Executa o processo
            self.processo_atual = proximo_processo
            print(f"Executando {self.processo_atual}...")

            programa = self.processo_atual.logica
            programa = programa.splitlines()
            # secao = ''
            if self.processo_atual.estado == "bloqueado":
                self.secao = self.processo_atual.status_secao
                self.pc = self.processo_atual.status_pc
                self.acc = self.processo_atual.status_acc
                self.processo_atual.estado = "pronto"

                # Fatiar programa para continuar de onde parou
                programa = programa[self.processo_atual.status_pc:]

            for instrucao in programa:

                if self.processo_atual.tempo_ja_ocupou_cpu < self.processo_atual.quantum:
                    self.processo_atual.tempo_ja_ocupou_cpu += 1
                    self.processo_atual.tempo_restante -= 1
                    instrucao = instrucao.strip()
                    if instrucao.startswith('.'):
                        secao = instrucao
                        self.secao = secao
                        self.processo_atual.status_secao = self.secao
                        self.pc += 1
                        continue
                    if secao == '.data':
                        variavel, valor = instrucao.split()
                        self.memoria.memoria_ram[variavel] = int(valor)
                        self.pc += 1
                    elif secao == '.code':
                        self.executar_instrucao(instrucao)
                        self.pc += 1
                    elif secao == '.enddata':
                        self.pc += 1
                    else:
                        raise Exception(f'Seção Inválida: {secao}')
                else:
                    print('Fim do tempo de ocupação do processo no processador')
                    print('Processo atual voltará para fila de prontos...')

                    # Guarda as informações de onde o processo parou
                    self.processo_atual.status_pc = self.pc
                    self.processo_atual.status_acc = self.acc
                    self.processo_atual.status_secao = self.secao
                    self.processo_atual.estado = "bloqueado"

                    self.processo_atual.tempo_ja_ocupou_cpu = 0

                    # Se o processo atual ainda tiver tempo restante, coloca-o de volta na fila de processos prontos
                    self.memoria.fila_prontos.append(self.processo_atual)
                    break

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
            self.memoria.memoria_ram[op1] = self.acc
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
            raise Exception(f'Intrução inválida: {instr}')
        # self.pc += 1

    def get_operando(self, operando):
        if operando.startswith('#'):
            return int(operando[1:])
        else:
            return self.memoria.memoria_ram[operando]

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
