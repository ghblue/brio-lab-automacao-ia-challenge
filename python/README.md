# Desafio 2 - Backend com Python

Este diretorio contem o entregavel Python do desafio tecnico da Brio Lab.

O objetivo do Desafio 2 e simular o recebimento de um JSON de diagnostico, validar e normalizar os dados, salvar as informacoes tratadas em banco SQLite e simular a criacao de uma tarefa no ClickUp para o time comercial.

Nesta etapa, o script carrega um payload JSON local, valida os campos obrigatorios, normaliza os dados aceitos, persiste o lead em SQLite, monta um payload realista para o ClickUp, imprime a simulacao da tarefa e atualiza o registro com o ID simulado.

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

O banco SQLite e criado automaticamente em:

```txt
python/data/leads.db
```

O arquivo `leads.db` e um artefato local de execucao e nao deve ser versionado.

## Variaveis de ambiente

O projeto nao carrega `.env` automaticamente para evitar dependencias externas nesta etapa. Caso queira alterar algum valor, exporte as variaveis no terminal antes de rodar o script ou use um gerenciador de ambiente da sua preferencia.

As variaveis documentadas em `.env.example` sao:

- `CLICKUP_SIMULATION_MODE`: controla o modo simulado. O padrao do codigo e `true` quando a variavel nao existe.
- `CLICKUP_API_TOKEN`: token que seria usado em uma chamada real futura para a API do ClickUp. Nao e usado no modo simulado.
- `CLICKUP_LIST_ID`: lista de destino que seria usada na API real. No modo simulado, aparece como informacao de destino quando configurada.
- `CLICKUP_ASSIGNEE_ID`: usuario responsavel pela tarefa. Quando informado, entra no payload em `assignees`.

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

## Fluxo atual

O fluxo completo executado hoje e:

```txt
JSON -> validacao -> normalizacao -> SQLite -> payload ClickUp simulado -> atualizacao do banco
```

Com payload valido, o lead e salvo com status inicial `saved`, a tarefa ClickUp e simulada, e o registro e atualizado para `clickup_created` com o ID retornado pela simulacao.

Com payload invalido, o script lista todos os erros encontrados, nao salva no banco e nao executa a simulacao do ClickUp.

## Exemplo de uso valido

Com o payload valido em `examples/valid_payload.json`, o script imprime o payload recebido, o payload normalizado, o registro salvo, o payload ClickUp simulado e o registro final:

```txt
Payload normalizado:
{
  "nome": "Ana Carvalho",
  "telefone": "+5511999998888",
  "email": "ana.carvalho@example.com",
  "especialidade": "Dermatologia",
  "principal_desafio": "Atrair pacientes qualificados para a agenda particular"
}

Registro salvo no SQLite:
{
  "id": 1,
  "nome": "Ana Carvalho",
  "telefone": "+5511999998888",
  "email": "ana.carvalho@example.com",
  "especialidade": "Dermatologia",
  "principal_desafio": "Atrair pacientes qualificados para a agenda particular",
  "status": "saved",
  "clickup_task_id": null,
  "error_message": null,
  "created_at": "2026-06-10T12:00:00+00:00"
}

Payload ClickUp simulado:
Lista ClickUp destino: nao configurada no ambiente
{
  "name": "Novo lead: Ana Carvalho",
  "description": "Nome: Ana Carvalho\nTelefone: +5511999998888\nE-mail: ana.carvalho@example.com\nEspecialidade: Dermatologia\nPrincipal desafio: Atrair pacientes qualificados para a agenda particular",
  "tags": [
    "diagnostico",
    "lead-site",
    "automacao"
  ],
  "status": "novo lead"
}

Registro final no SQLite:
{
  "id": 1,
  "nome": "Ana Carvalho",
  "telefone": "+5511999998888",
  "email": "ana.carvalho@example.com",
  "especialidade": "Dermatologia",
  "principal_desafio": "Atrair pacientes qualificados para a agenda particular",
  "status": "clickup_created",
  "clickup_task_id": "simulated-clickup-task-1",
  "error_message": null,
  "created_at": "2026-06-10T12:00:00+00:00"
}

Sucesso: fluxo concluido em .../python/data/leads.db.
```

Com o payload invalido, o script imprime todas as mensagens de erro e nao normaliza, salva ou envia os dados.

## Decisao sobre banco de dados

SQLite foi escolhido para facilitar a execucao local pelo avaliador, sem depender de contas externas, servidores ou configuracoes adicionais.

A tabela criada automaticamente se chama `diagnostic_leads` e guarda os dados tratados do diagnostico, o status local do registro, campos reservados para uma futura tarefa do ClickUp e a data de criacao (`created_at`).

As operacoes de banco ficam concentradas em `app/database.py`:

- abertura da conexao SQLite;
- criacao da tabela com `init_db()`;
- insercao com `insert_diagnostic_lead()`;
- busca do registro criado com `get_lead_by_id()`;
- atualizacao do resultado da etapa ClickUp com `update_lead_clickup_result()`.

## ClickUp

A criacao de tarefa no ClickUp esta em modo simulado por padrao. Essa decisao evita depender de uma conta real, token valido ou lista configurada no ClickUp, facilita a reproducao local pelo avaliador e ainda demonstra o payload e a logica de integracao que seriam usados em uma chamada real.

O modulo `app/clickup_client.py` separa a montagem do payload (`build_clickup_task_payload()`) da criacao da tarefa (`create_clickup_task()`). Hoje, `create_clickup_task()` imprime o payload e retorna um ID no formato `simulated-clickup-task-{lead_id}`. Uma melhoria futura seria implementar o ramo real usando a API do ClickUp, com `CLICKUP_API_TOKEN` e `CLICKUP_LIST_ID`, sem mudar o restante do fluxo.

## Proximas etapas

- Substituir o modo simulado por uma chamada real opcional para a API do ClickUp.
- Adicionar testes automatizados para validacao, normalizacao, persistencia e montagem do payload.
