-- ============================================================
-- MODELAGEM DO BANCO DA TECHBAIRRO (Aula 13)
-- ============================================================

-- Tabela usada pela TechBairro desde a v3.0 (Aula 14)
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    endereco TEXT
);

-- Tabela projetada para o requisito de pedidos (ainda não usada pelo programa)
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido TEXT,
    valor_total REAL,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

-- Por que a chave estrangeira importa: sem ela, nada impediria cadastrar
-- um pedido com um cliente_id que não existe na tabela clientes (pedido órfão).
-- A chave estrangeira garante a integridade referencial.
