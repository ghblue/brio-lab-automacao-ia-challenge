# Desafio 2 - Backend com Python

Este diretorio contem o entregavel Python do desafio tecnico da Brio Lab.

O objetivo final do Desafio 2 sera simular o recebimento de um JSON de diagnostico, validar e normalizar os dados, salvar as informacoes tratadas em banco SQLite e criar ou simular a criacao de uma tarefa no ClickUp para o time comercial.

Nesta etapa, o script carrega um payload JSON local, valida os campos obrigatorios, normaliza os dados aceitos e imprime o resultado tratado. Ainda nao ha persistencia em banco nem chamada ao ClickUp.

## Estrutura

```txt
python/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── validators.py
│   ├── normalizers.py
│   ├── clickup_client.py
│   └── schemas.py
├── examples/
│   ├── valid_payload.json
│   └── invalid_payload.json
├── data/
│   └── .gitkeep
├── requirements.txt
├── .env.example
└── README.md
```

## Como rodar

A partir da pasta `python/`, execute:

```bash
python -m app.main
```

Para testar o payload invalido:

```bash
python -m app.main --payload examples/invalid_payload.json
```

Tambem e possivel passar outro arquivo JSON pelo argumento `--payload`.

## Validacoes implementadas

O script valida:

- presenca dos campos obrigatorios: `nome`, `telefone`, `email`, `especialidade` e `principal_desafio`;
- `nome` nao vazio;
- `telefone` com pelo menos 10 digitos;
- `email` com formato minimo, como `nome@dominio.com`;
- `especialidade` nao vazia;
- `principal_desafio` nao vazio.

Quando o payload tem mais de um problema, o script lista todos os erros encontrados antes de finalizar.

## Normalizacoes implementadas

O script normaliza:

- espacos extras em campos de texto;
- e-mail para letras minusculas;
- telefone para um padrao brasileiro simplificado, como `+5511999998888`.

Se o telefone ja vier com DDI `55`, o codigo do pais nao e duplicado.

## Exemplo de uso

Com o payload valido em `examples/valid_payload.json`, o script imprime o payload recebido e o payload normalizado:

```txt
Payload normalizado:
{
  "nome": "Ana Carvalho",
  "telefone": "+5511999998888",
  "email": "ana.carvalho@example.com",
  "especialidade": "Dermatologia",
  "principal_desafio": "Atrair pacientes qualificados para a agenda particular"
}
```

Com o payload invalido, o script imprime mensagens de erro e nao normaliza, salva ou envia os dados.

## Decisao sobre banco de dados

SQLite foi escolhido para facilitar a execucao local pelo avaliador, sem depender de contas externas, servidores ou configuracoes adicionais. A implementacao do banco sera adicionada em uma etapa futura.

## Proximas etapas

- Criar a camada SQLite em `app/database.py`.
- Persistir os dados tratados em `data/`.
- Implementar o modo simulado de criacao de tarefa no ClickUp.
- Documentar o payload enviado ao ClickUp e possiveis melhorias futuras.
