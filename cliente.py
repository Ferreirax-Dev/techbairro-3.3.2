# CLIENTE (Aula 21)
# ============================================================
# Responsabilidade: representar os dados de um cliente.
# NOVO NA AULA 21: a classe Cliente saiu do techbairro.py
# e veio para este arquivo, sem nenhuma mudança por dentro.
# Este arquivo não sabe nada de janela nem de banco.
class Cliente:

    # Método construtor
    #
    # NOVO NA AULA 14: o parâmetro id.
    # Ele fica None enquanto o cliente ainda não foi gravado no banco.
    def __init__(self, nome, telefone, email, endereco, id=None):

        # Armazena os dados do cliente
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

    # Retorna os dados do cliente em uma única String
    def resumo(self):
        return f"{self.nome} | {self.telefone} | {self.email} | {self.endereco}"

    # Retorna as iniciais do nome
    #
    # Exemplo:
    # "João Victor Mendes" -> "JVM"
    def iniciais(self):

        # Divide o nome em partes
        partes = self.nome.split()

        # Pega a primeira letra de cada parte
        return "".join(
            parte[0].upper()
            for parte in partes
            if parte
        )