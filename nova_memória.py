class NovaMemoria:
    def __init__(self):
        self.valores = {}
        self.fila_prontos = []  # Alterar para queue?


    def armazenar(self, processo, variavel, valor):
        if processo not in self.valores:
            self.valores[processo] = {}
        self.valores[processo][variavel] = valor

    def consultar(self, processo, variavel):
        if processo in self.valores and variavel in self.valores[processo]:
            return self.valores[processo][variavel]
        else:
            return None
