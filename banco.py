# ============================================================
# BANCO (Aula 21)
# ============================================================
#
# Responsabilidade: toda a comunicação com o banco SQLite.
# Este arquivo não sabe nada de janela.
# Importa o módulo do SQLite (já vem com o Python)
import sqlite3
# O banco devolve linhas; o GerenciadorClientes transforma cada linha
# num objeto Cliente, por isso precisa conhecer a classe
from cliente import Cliente

class GerenciadorClientes:

    def __init__(self, caminho_banco="techbairro.db"):

        # Guarda o nome do arquivo do banco
        self.caminho_banco = caminho_banco

        # Cria a tabela (se ela ainda não existir)
        self.criar_tabela()


    # Abre uma conexão com o banco
    def conectar(self):

        return sqlite3.connect(self.caminho_banco)


    # Cria a tabela clientes projetada na Aula 13.
    #
    # IF NOT EXISTS: na primeira vez cria a tabela,
    # nas próximas não faz nada e não apaga os dados.
    def criar_tabela(self):

        conexao = self.conectar()

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            )
        """)

        conexao.commit()
        conexao.close()


    # ========================================================
    # CREATE
    # ========================================================

    # Grava um novo cliente no banco
    def adicionar(self, cliente):

        conexao = self.conectar()

        # Cada ? é trocado, na ordem, por um valor da tupla.
        # Nunca monte o SQL juntando textos com f-string!
        cursor = conexao.execute(
            "INSERT INTO clientes (nome, telefone, email, endereco) VALUES (?, ?, ?, ?)",
            (cliente.nome, cliente.telefone, cliente.email, cliente.endereco)
        )

        # Sem o commit, o cliente não fica salvo no arquivo
        conexao.commit()

        # Guarda o id que o banco gerou para este cliente
        cliente.id = cursor.lastrowid

        conexao.close()


    # ========================================================
    # READ
    # ========================================================

    # Retorna todos os clientes cadastrados no banco
    def listar(self):

        conexao = self.conectar()

        # fetchall() devolve uma lista de tuplas, uma por linha
        linhas = conexao.execute(
            "SELECT id, nome, telefone, email, endereco FROM clientes ORDER BY nome"  # CORRIGIDO (BUG 3): antes era ORDER BY id
        ).fetchall()

        conexao.close()

        # Transforma cada linha do banco num objeto Cliente
        return [
            Cliente(nome, telefone, email, endereco, id)
            for (id, nome, telefone, email, endereco) in linhas
        ]


    # ========================================================
    # UPDATE
    # ========================================================

    # Atualiza um cliente existente.
    #
    # MUDOU NA AULA 14: recebe o id do cliente, e não mais o índice da lista.
    def atualizar(self, id_cliente, novo_cliente):

        conexao = self.conectar()

        cursor = conexao.execute(
            "UPDATE clientes SET nome = ?, telefone = ?, email = ?, endereco = ? WHERE id = ?",
            (novo_cliente.nome, novo_cliente.telefone, novo_cliente.email,
             novo_cliente.endereco, id_cliente)
        )

        conexao.commit()   # CORRIGIDO (BUG 4): sem commit, o close() descartava a alteração
        conexao.close()

        # rowcount diz quantas linhas foram alteradas
        return cursor.rowcount == 1


    # ========================================================
    # DELETE
    # ========================================================

    # Remove um cliente existente.
    #
    # MUDOU NA AULA 14: recebe o id do cliente, e não mais o índice da lista.
    def remover(self, id_cliente):

        conexao = self.conectar()

        # Atenção à vírgula: (id_cliente,) é uma tupla de um elemento
        cursor = conexao.execute(
            "DELETE FROM clientes WHERE id = ?",
            (id_cliente,)
        )

        conexao.commit()
        conexao.close()

        return cursor.rowcount == 1


    # Retorna a quantidade de clientes cadastrados
    def total(self):

        conexao = self.conectar()

        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM clientes"
        ).fetchone()[0]

        conexao.close()

        return quantidade