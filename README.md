# TechBairro — Cadastro de Clientes

Sistema de cadastro de clientes desenvolvido em Python, com interface gráfica e banco de dados SQLite.

## Sobre o projeto

A TechBairro permite cadastrar, consultar, editar e excluir clientes. O sistema também possui validação de dados e mensagens de status que ajudam o usuário a identificar erros durante o preenchimento.

## Funcionalidades

- Cadastro de clientes.
- Consulta dos clientes cadastrados.
- Edição de informações.
- Exclusão de clientes com confirmação.
- Validação dos dados antes de salvar.
- Contador de clientes cadastrados.
- Mensagens de sucesso e erro.

## Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Tkinter:** criação da interface gráfica.
- **SQLite:** armazenamento dos dados.
- **Git e GitHub:** controle de versão e hospedagem do código.

## Organização dos arquivos

- `techbairro.py`: interface gráfica e funcionamento principal.
- `cliente.py`: módulo relacionado aos dados dos clientes.
- `banco.py`: gerenciamento do banco de dados.
- `validacao.py`: validação das informações.

## Requisitos

- Python 3 instalado.
- Bibliotecas padrão do Python utilizadas pelo projeto, incluindo Tkinter e SQLite.
- Os arquivos do projeto na mesma estrutura esperada pelos imports.

## Como executar

1. Baixe ou clone o repositório.
2. Abra um terminal na pasta do projeto.
3. Execute:

```bash
python techbairro.py
```

No Windows, se o comando anterior não funcionar, tente:

```bash
py techbairro.py
```

## Banco de dados

O sistema utiliza o SQLite para armazenar os cadastros localmente no arquivo `techbairro.db`, localizado na pasta do projeto.

O banco de dados não precisa ser enviado ao GitHub, pois pode conter informações cadastradas durante o uso. Ele deve ser criado ou gerenciado pelo próprio sistema.

## Testes

Os testes devem ser executados antes da entrega final para verificar o funcionamento das operações e das regras de validação.

