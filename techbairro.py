# ============================================================
# TECHBAIRRO - CADASTRO DE CLIENTES
# Versão 3.3.2
# ============================================================

# Importa as bibliotecas necessárias para o sistema.
import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Importa as classes separadas nos arquivos do projeto.
from cliente import Cliente
from banco import GerenciadorClientes
from validacao import ValidadorCliente

# ============================================================
# CONFIGURAÇÕES DO SISTEMA
# ============================================================

# A versão fica em um único lugar para facilitar a atualização.
VERSAO = "3.3.2"

# Cores utilizadas na interface.
AZUL_ESCURO = "#24527A"
AZUL_CLARO = "#EAF5FF"
AZUL_MEDIO = "#B8DDF5"
BRANCO = "#FFFFFF"
TEXTO = "#243746"
CINZA = "#64748B"
VERDE = "#16803C"
VERMELHO = "#C62828"


# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================

# Descobre a pasta onde este arquivo está salvo.
PASTA_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))

# Define o caminho completo do banco de dados.
CAMINHO_BANCO = os.path.join(PASTA_DO_PROJETO, "techbairro.db")

# Mostra no terminal qual banco está sendo utilizado.
print(f"Banco em uso: {CAMINHO_BANCO}")

# Cria os objetos responsáveis pelo banco e pela validação.
gerenciador = GerenciadorClientes(CAMINHO_BANCO)
validador = ValidadorCliente()

# Guarda o ID do cliente que está sendo editado.
# None significa que estamos cadastrando um novo cliente.
id_em_edicao = None


# ============================================================
# FUNÇÃO PARA PADRONIZAR OS BOTÕES
# ============================================================


def estilizar_botao(botao, principal=False):
    """Aplica o padrão visual aos botões da aplicação."""

    # O botão principal utiliza azul-escuro.
    if principal:
        cor_fundo = AZUL_ESCURO
        cor_texto = BRANCO
    else:
        cor_fundo = BRANCO
        cor_texto = AZUL_ESCURO

    botao.configure(
        bg=cor_fundo,
        fg=cor_texto,
        activebackground=AZUL_MEDIO,
        activeforeground=AZUL_ESCURO,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Arial", 9, "bold"),
        padx=5,
        pady=4,
    )


# ============================================================
# JANELA PRINCIPAL
# ============================================================

# Cria a janela principal do sistema.
janela = tk.Tk()

# Define o título, o tamanho e as cores da janela.
janela.title("TechBairro - Cadastro de Cliente")
janela.geometry("500x490")
janela.resizable(False, False)
janela.configure(bg=AZUL_CLARO)


# ============================================================
# CABEÇALHO DA INTERFACE
# ============================================================

# Cria uma faixa azul-escura no topo da janela.
cabecalho = tk.Frame(janela, bg=AZUL_ESCURO)
cabecalho.pack(side="top", fill="x")

# Exibe o título do sistema.
tk.Label(
    cabecalho,
    text="Cadastro de Cliente",
    fg=BRANCO,
    bg=AZUL_ESCURO,
    font=("Arial", 14, "bold"),
    pady=12,
).pack()


# ============================================================
# FORMULÁRIO
# ============================================================

# Cria um espaço para organizar os campos.
form = tk.Frame(janela, bg=AZUL_CLARO)
form.pack(pady=20)

# Define os campos que serão preenchidos pelo usuário.
campos = ["Nome", "Telefone", "E-mail", "Endereço"]

# Dicionário que guarda os campos de entrada.
entradas = {}

# Cria um rótulo e um campo de entrada para cada informação.
for i, campo in enumerate(campos):

    tk.Label(form, text=f"{campo}:", bg=AZUL_CLARO, fg=TEXTO, font=("Arial", 10)).grid(
        row=i, column=0, sticky="e", padx=5, pady=6
    )

    entrada = tk.Entry(
        form,
        width=30,
        bg=BRANCO,
        fg=TEXTO,
        relief="solid",
        bd=1,
        insertbackground=AZUL_ESCURO,
        font=("Arial", 10),
    )

    entrada.grid(row=i, column=1, padx=5, pady=6)

    # Guarda o campo para acessar seu conteúdo posteriormente.
    entradas[campo] = entrada


# ============================================================
# MENSAGENS DE STATUS E CONTADOR
# ============================================================

# Exibe mensagens de sucesso, erro e orientação.
status = tk.Label(
    janela,
    text="Nenhum cliente cadastrado ainda",
    fg=CINZA,
    bg=AZUL_CLARO,
    wraplength=460,
    justify="left",
    font=("Arial", 9),
)
status.pack(pady=(0, 5))

# Mostra a quantidade atual de clientes cadastrados.
contador = tk.Label(
    janela,
    text=f"Clientes cadastrados: {gerenciador.total()}",
    bg=AZUL_CLARO,
    fg=AZUL_ESCURO,
    font=("Arial", 10, "bold"),
)
contador.pack()


# ============================================================
# LIMPAR CAMPOS
# ============================================================


def limpar_campos():
    """Limpa o formulário e encerra o modo de edição."""

    global id_em_edicao

    # Apaga o conteúdo de todos os campos.
    for entrada in entradas.values():
        entrada.delete(0, tk.END)

    # Volta ao modo de cadastro de um novo cliente.
    id_em_edicao = None

    # Restaura o botão para a função de salvar.
    botao_salvar.config(text="Salvar", command=salvar)


# ============================================================
# SALVAR CLIENTE
# ============================================================


def salvar():
    """Valida os dados e cadastra ou atualiza um cliente."""

    global id_em_edicao

    # Obtém os valores digitados, removendo espaços extras.
    valores = {campo: entradas[campo].get().strip() for campo in campos}

    # Cria um objeto Cliente com os dados do formulário.
    cliente = Cliente(
        valores["Nome"], valores["Telefone"], valores["E-mail"], valores["Endereço"]
    )

    # Verifica se os dados atendem às regras de validação.
    erro = validador.validar(cliente)

    if erro is not None:
        status.config(text=erro, fg=VERMELHO)
        return

    try:
        # Sem um ID, o sistema cadastra um novo cliente.
        if id_em_edicao is None:
            gerenciador.adicionar(cliente)

            status.config(text=f"Cliente '{cliente.nome}' salvo com sucesso!", fg=VERDE)

        # Com um ID, o sistema atualiza o cliente existente.
        else:
            alterou = gerenciador.atualizar(id_em_edicao, cliente)

            # Verifica se o cliente ainda existe no banco.
            if not alterou:
                status.config(
                    text="Cliente não encontrado. Nada foi alterado.", fg=VERMELHO
                )
                limpar_campos()
                return

            status.config(
                text=f"Cliente '{cliente.nome}' atualizado com sucesso!", fg=VERDE
            )

    except sqlite3.Error as erro:
        # Informa quando ocorre um erro relacionado ao banco.
        status.config(text=f"Erro ao salvar no banco: {erro}", fg=VERMELHO)
        return

    # Atualiza o contador depois de uma operação bem-sucedida.
    contador.config(text=f"Clientes cadastrados: {gerenciador.total()}")

    # Limpa o formulário após salvar ou atualizar.
    limpar_campos()


# ============================================================
# CANCELAR OU LIMPAR FORMULÁRIO
# ============================================================


def cancelar():
    """Limpa os campos e informa se uma edição foi cancelada."""

    # Verifica se o formulário estava editando um cliente.
    estava_editando = id_em_edicao is not None

    # Limpa o formulário e encerra a edição.
    limpar_campos()

    # Exibe uma mensagem de acordo com a operação realizada.
    if estava_editando:
        status.config(text="Edição cancelada", fg=CINZA)
    else:
        status.config(text="Formulário limpo", fg=CINZA)


# ============================================================
# CONSULTA DE CLIENTES
# ============================================================


def abrir_consulta():
    """Abre uma janela com a lista de clientes cadastrados."""

    # Cria uma segunda janela vinculada à janela principal.
    consulta = tk.Toplevel(janela)
    consulta.title("Consulta de Clientes")
    consulta.geometry("500x380")
    consulta.resizable(False, False)
    consulta.configure(bg=AZUL_CLARO)

    # Organiza a lista e a barra de rolagem.
    frame_lista = tk.Frame(consulta, bg=AZUL_CLARO)
    frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

    # Cria a barra de rolagem vertical.
    scrollbar = tk.Scrollbar(frame_lista, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Cria a lista que mostrará os clientes.
    lista = tk.Listbox(
        frame_lista,
        width=65,
        height=12,
        bg=BRANCO,
        fg=TEXTO,
        selectbackground=AZUL_ESCURO,
        selectforeground=BRANCO,
        activestyle="none",
        relief="solid",
        bd=1,
        font=("Arial", 9),
    )
    lista.pack(side="left", fill="both", expand=True)

    # Liga a barra de rolagem à lista.
    lista.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista.yview)

    # Guarda os objetos Cliente na mesma ordem da lista.
    # Isso evita confundir a posição do cliente com seu ID.
    clientes_na_tela = []

    # ========================================================
    # ATUALIZAR LISTA
    # ========================================================

    def atualizar_lista():
        """Atualiza os clientes exibidos na janela de consulta."""

        # Remove os itens antigos da interface.
        lista.delete(0, tk.END)
        clientes_na_tela.clear()

        try:
            # Busca os clientes no banco de dados.
            clientes_cadastrados = gerenciador.listar()

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no banco",
                f"Não foi possível consultar os clientes.\n{erro}",
                parent=consulta,
            )
            return

        # Informa quando não existem clientes cadastrados.
        if not clientes_cadastrados:
            lista.insert(tk.END, "Nenhum cliente cadastrado")
            return

        # Exibe o resumo de cada cliente e guarda seu objeto.
        for cliente in clientes_cadastrados:
            lista.insert(tk.END, cliente.resumo())
            clientes_na_tela.append(cliente)

    # ========================================================
    # IDENTIFICAR CLIENTE SELECIONADO
    # ========================================================

    def cliente_selecionado(acao):
        """Retorna o cliente selecionado ou None."""

        # Obtém a posição selecionada na lista.
        selecionado = lista.curselection()

        # Impede operações quando não há um cliente válido.
        if not selecionado or selecionado[0] >= len(clientes_na_tela):
            messagebox.showwarning(
                "Atenção", f"Selecione um cliente antes de {acao}.", parent=consulta
            )
            return None

        return clientes_na_tela[selecionado[0]]

    # ========================================================
    # EDITAR CLIENTE
    # ========================================================

    def editar_cliente():
        """Carrega os dados do cliente no formulário principal."""

        global id_em_edicao

        cliente = cliente_selecionado("editar")

        if cliente is None:
            return

        # Guarda o ID fixo do cliente que será atualizado.
        id_em_edicao = cliente.id

        # Preenche os campos com os dados do cliente.
        entradas["Nome"].delete(0, tk.END)
        entradas["Nome"].insert(0, cliente.nome)

        entradas["Telefone"].delete(0, tk.END)
        entradas["Telefone"].insert(0, cliente.telefone)

        entradas["E-mail"].delete(0, tk.END)
        entradas["E-mail"].insert(0, cliente.email)

        entradas["Endereço"].delete(0, tk.END)
        entradas["Endereço"].insert(0, cliente.endereco)

        # Informa que o usuário está editando um cadastro.
        status.config(text=f"Editando cliente: {cliente.nome}", fg=AZUL_ESCURO)

        # Altera o texto do botão principal.
        botao_salvar.config(text="Salvar edição", command=salvar)

        # Fecha a consulta após carregar os dados.
        consulta.destroy()

    # ========================================================
    # EXCLUIR CLIENTE
    # ========================================================

    def excluir_cliente():
        """Solicita confirmação e remove um cliente do banco."""

        cliente = cliente_selecionado("excluir")

        if cliente is None:
            return

        # Confirma a exclusão antes de alterar o banco.
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir o cadastro de "
            f"{cliente.nome}?\n\n"
            f"Essa ação não pode ser desfeita.",
            parent=consulta,
        )

        if not confirmar:
            return

        try:
            # Remove o cliente usando seu ID.
            foi_removido = gerenciador.remover(cliente.id)

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no banco",
                f"Não foi possível excluir o cliente.\n{erro}",
                parent=consulta,
            )
            return

        # Trata o caso em que o cliente já não existe no banco.
        if not foi_removido:
            messagebox.showwarning(
                "Cliente não encontrado",
                f"{cliente.nome} não está mais no banco.",
                parent=consulta,
            )
            atualizar_lista()
            return

        # Atualiza a lista e o contador após a exclusão.
        atualizar_lista()

        contador.config(text=f"Clientes cadastrados: {gerenciador.total()}")

        # Informa que a exclusão foi realizada.
        status.config(text=f"Cliente '{cliente.nome}' excluído com sucesso!", fg=VERDE)

    # ========================================================
    # BOTÕES DA JANELA DE CONSULTA
    # ========================================================

    botoes_consulta = tk.Frame(consulta, bg=AZUL_CLARO)
    botoes_consulta.pack(pady=10)

    # Botão para editar o cliente selecionado.
    botao_editar = tk.Button(
        botoes_consulta, text="Editar selecionado", width=18, command=editar_cliente
    )
    estilizar_botao(botao_editar, principal=True)
    botao_editar.grid(row=0, column=0, padx=5)

    # Botão para excluir o cliente selecionado.
    botao_excluir = tk.Button(
        botoes_consulta, text="Excluir selecionado", width=18, command=excluir_cliente
    )
    estilizar_botao(botao_excluir)
    botao_excluir.grid(row=0, column=1, padx=5)

    # O duplo clique também permite iniciar a edição.
    lista.bind("<Double-1>", lambda evento: editar_cliente())

    # Carrega os clientes assim que a janela é aberta.
    atualizar_lista()


# ============================================================
# BOTÕES DA JANELA PRINCIPAL
# ============================================================

# Cria o espaço que organiza os botões lado a lado.
botoes = tk.Frame(janela, bg=AZUL_CLARO)
botoes.pack(pady=10)

# Botão para salvar um novo cliente ou atualizar um existente.
botao_salvar = tk.Button(botoes, text="Salvar", width=13, command=salvar)
estilizar_botao(botao_salvar, principal=True)
botao_salvar.grid(row=0, column=0, padx=5)

# Botão para limpar o formulário ou cancelar uma edição.
botao_cancelar = tk.Button(botoes, text="Cancelar", width=12, command=cancelar)
estilizar_botao(botao_cancelar)
botao_cancelar.grid(row=0, column=1, padx=5)

# Botão para abrir a consulta de clientes.
botao_consultar = tk.Button(botoes, text="Consultar", width=12, command=abrir_consulta)
estilizar_botao(botao_consultar)
botao_consultar.grid(row=0, column=2, padx=5)


# ============================================================
# VERSÃO DO SISTEMA
# ============================================================

# Exibe a versão no canto inferior direito da janela.
tk.Label(janela, text=f"v{VERSAO}", fg=CINZA, bg=AZUL_CLARO, font=("Arial", 8)).place(
    relx=0.97, rely=0.97, anchor="se"
)


# ============================================================
# ATALHO DE TECLADO
# ============================================================

# Pressionar Enter na janela principal executa a função salvar.
janela.bind("<Return>", lambda evento: salvar())


# ============================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ============================================================

# Mantém a janela aberta até o usuário fechá-la.
janela.mainloop()
