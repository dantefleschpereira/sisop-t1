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
        processo.estado = 'ready'
        self.memoria.fila_prontos.append(processo)

    # Escalonador Shortest-Job-First
    def sjf(self):

        self.memoria.fila_prontos.sort(key=lambda x: x.tempo_chegada)

        while self.memoria.fila_prontos:

            # Obtém o próximo processo a ser executado
            proximo_processo = self.memoria.fila_prontos.pop(0)

            # Executa o processo
            self.processo_atual = proximo_processo
            self.processo_atual.estado = 'running'
            self.pc = self.processo_atual.status_pc
            self.acc = self.processo_atual.status_acc
            self.secao = self.processo_atual.status_secao
            print(f"\nExecutando {self.processo_atual}...")

            programa = self.processo_atual.logica
            programa = programa.splitlines()

            # Caso diferente significa que o programa já foi executado algum vez então é preciso salvar as info
            if self.processo_atual.tempo_restante != self.processo_atual.tempo_execucao:
                self.secao = self.processo_atual.status_secao
                secao = self.secao #?
                self.pc = self.processo_atual.status_pc
                self.acc = self.processo_atual.status_acc
                self.processo_atual.estado = "ready"

                # Fatiar programa para continuar de onde parou
                programa = programa[self.processo_atual.status_pc:]

            for instrucao in programa:

                if self.processo_atual.tempo_restante == self.processo_atual.tempo_execucao:
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
                        for chave, valor in self.memoria.memoria_ram.items():
                            print(f'Valor de {chave} = {valor}')
                        self.pc += 1
                    elif secao == '.code':
                        self.executar_instrucao(instrucao)
                        self.pc += 1
                    elif secao == '.enddata':
                        self.pc += 1
                    elif secao == '.endcode':
                        break
                    else:
                        raise Exception(f'Seção Inválida: {secao}')
                else:
                    print('Verificando chegada de processos...')
                    if len(self.memoria.fila_prontos) > 0:
                        # precisa verificar se tem o menor tempo de exec na fila de processos a cada instrucao
                        menor_tempo_execucao = min(
                            self.memoria.fila_prontos, key=lambda x: x.tempo_execucao)
                        if self.processo_atual.tempo_restante > menor_tempo_execucao.tempo_restante:
                            # Guarda as informações de onde o processo parou
                            print(
                                'Fim do tempo de ocupação do processo no processador')

                            self.processo_atual.status_pc = self.pc
                            self.processo_atual.status_acc = self.acc
                            self.processo_atual.status_secao = self.secao
                            self.processo_atual.estado = "ready"

                            self.processo_atual.tempo_ja_ocupou_cpu = 0
                            self.pc = 0

                            # Se o processo atual ainda tiver tempo restante, coloca-o de volta na fila de processos prontos
                            self.memoria.fila_prontos.append(
                                self.processo_atual)
                            break
                        else:
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
                                for chave, valor in self.memoria.memoria_ram.items():
                                    print(f'Valor de {chave} = {valor}')
                                self.pc += 1
                            elif secao == '.code':
                                self.executar_instrucao(instrucao)
                                self.pc += 1
                            elif secao == '.enddata':
                                self.pc += 1
                            elif secao == '.endcode':
                                break
                            else:
                                raise Exception(f'Seção Inválida: {secao}')
                    else:
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
                            for chave, valor in self.memoria.memoria_ram.items():
                                print(f'Valor de {chave} = {valor}')
                            self.pc += 1
                        elif secao == '.code':
                            self.executar_instrucao(instrucao)
                            self.pc += 1
                        elif secao == '.enddata':
                            self.pc += 1
                        elif secao == '.endcode':
                            break
                        else:
                            raise Exception(f'Seção Inválida: {secao}')
        print('\nFim do Sistema de Execução Dinâmica de Processos\n')

    # Escalonador RoudRobin
    def rr(self):

        self.memoria.fila_prontos.sort(key=lambda x: x.tempo_chegada)
        # self.memoria.fila_prontos.sort(key=lambda x: x.prioridade)

        while self.memoria.fila_prontos:

            # Obtém o próximo processo a ser executado
            proximo_processo = self.memoria.fila_prontos.pop(0)

            # Executa o processo
            self.processo_atual = proximo_processo
            self.processo_atual.estado = 'running'
            self.pc = self.processo_atual.status_pc
            self.acc = self.processo_atual.status_acc
            self.secao = self.processo_atual.status_secao
            print(f"\nExecutando {self.processo_atual}...")

            programa = self.processo_atual.logica
            programa = programa.splitlines()

            # Caso diferente significa que o programa já foi executado algum vez então é preciso salvar as info
            if self.processo_atual.tempo_restante != self.processo_atual.tempo_execucao:
                self.secao = self.processo_atual.status_secao
                secao = self.secao #?
                self.pc = self.processo_atual.status_pc
                self.acc = self.processo_atual.status_acc
                self.processo_atual.estado = "ready"

                # Fatiar programa para continuar de onde parou
                programa = programa[self.processo_atual.status_pc:]

            for instrucao in programa:

                if self.processo_atual.tempo_restante == self.processo_atual.tempo_execucao:
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
                        for chave, valor in self.memoria.memoria_ram.items():
                            print(f'Valor de {chave} = {valor}')
                        self.pc += 1
                    elif secao == '.code':
                        self.executar_instrucao(instrucao)
                        self.pc += 1
                    elif secao == '.enddata':
                        self.pc += 1
                    elif secao == '.endcode':
                        break
                    else:
                        raise Exception(f'Seção Inválida: {secao}')
                else:
                    print('Verificando chegada de processos...')
                    if len(self.memoria.fila_prontos) > 0:
                        # precisa verificar se tem a prioridade de exec na fila de processos a cada instrucao
                        processo_prioritario = min(
                            self.memoria.fila_prontos, key=lambda x: x.prioridade)
                        if self.processo_atual.prioridade > processo_prioritario.prioridade:
                            # Guarda as informações de onde o processo parou
                            print(
                                'Fim do tempo de ocupação do processo no processador')

                            self.processo_atual.status_pc = self.pc
                            self.processo_atual.status_acc = self.acc
                            self.processo_atual.status_secao = self.secao
                            self.processo_atual.estado = "ready"

                            self.processo_atual.tempo_ja_ocupou_cpu = 0
                            self.pc = 0

                            # Se o processo atual ainda tiver tempo restante, coloca-o de volta na fila de processos prontos
                            self.memoria.fila_prontos.append(
                                self.processo_atual)
                            break
                        else:
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
                                for chave, valor in self.memoria.memoria_ram.items():
                                    print(f'Valor de {chave} = {valor}')
                                self.pc += 1
                            elif secao == '.code':
                                self.executar_instrucao(instrucao)
                                self.pc += 1
                            elif secao == '.enddata':
                                self.pc += 1
                            elif secao == '.endcode':
                                break
                            else:
                                raise Exception(f'Seção Inválida: {secao}')
                    else:
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
                            for chave, valor in self.memoria.memoria_ram.items():
                                print(f'Valor de {chave} = {valor}')
                            self.pc += 1
                        elif secao == '.code':
                            self.executar_instrucao(instrucao)
                            self.pc += 1
                        elif secao == '.enddata':
                            self.pc += 1
                        elif secao == '.endcode':
                            break
                        else:
                            raise Exception(f'Seção Inválida: {secao}')
        print('\nFim do Sistema de Execução Dinâmica de Processos\n')

 

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
            for chave, valor in self.memoria.memoria_ram.items():
                print(f'Valor de {chave} = {valor}')
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

    def get_operando(self, operando):
        if operando.startswith('#'):
            return int(operando[1:])
        else:
            return self.memoria.memoria_ram[operando]

    def get_label(self, label):
        return int(label[:-1])

    def operacoes_syscall(self, indice):
        if indice == '0':
            # exit(0)
            print('Esse processo foi encerrado por syscall')
            self.processo_atual.estado = "exit"
        elif indice == '1':
            print(self.acc)
        elif indice == '2':
            self.acc = int(input("Informe um valor inteiro: "))
        else:
            raise Exception(f'Comando inválido: {indice}')
