
class Processo:

    # Essa linha possibilita gerar ids sequenciais automaticamente para cada processo criado
    proximo_id = 1

    # Construtor com os atributos de um processo
    def __init__(self, id=None, logica=None, tempo_chegada=None, prioridade=None, quantum=None, tempo_execucao=None):
        # self.pc = 0
        # self.acc = 0
        self.id = Processo.proximo_id
        self.logica = logica
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade
        self.quantum = quantum
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        Processo.proximo_id += 1
        # Incluir "estado"?

    def __repr__(self):
        return f"Processo {self.id} (prioridade: {self.prioridade}, quantum: {self.quantum}, tempo execução: {self.tempo_execucao}, tempo restante: {self.tempo_restante})"

    # Carrega as instruções que estão no arquivo.txt direto na logica do processo
    def carregar_instrucoes(self, nome_do_arquivo):
        with open(nome_do_arquivo, 'r') as instrucoes:
            self.logica = instrucoes.read()
