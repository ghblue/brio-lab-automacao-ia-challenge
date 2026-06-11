# Desafio 2 - Backend com Python

Este diretorio contem o entregavel Python do desafio tecnico da Brio Lab.

O objetivo do Desafio 2 e simular o fluxo de um formulario de diagnostico do site de uma cliente:

```txt
JSON -> validacao -> normalizacao -> SQLite -> payload ClickUp simulado -> atualizacao do banco
```

O projeto foi mantido como um script executavel pelo terminal. Nao ha API HTTP, FastAPI, Flask ou chamada real ao ClickUp nesta etapa.

## O que o script faz

- Le um payload JSON local com dados de diagnostico.
- Valida campos obrigatorios e formatos minimos.
- Normaliza campos de texto, e-mail e telefone.
- Cria o banco local em `data/leads.db`, se necessario.
- Insere o lead normalizado na tabela `diagnostic_leads`.
- Monta e imprime o payload que seria enviado ao ClickUp.
- Atualiza o registro com status `clickup_created` ou `clickup_failed`.

## Estrutura de pastas

```txt
python/
├── app/
│   ├── __init__.py
│   ├── main.py              # entrada do script
│   ├── config.py            # caminhos e variaveis de ambiente
│   ├── database.py          # persistencia SQLite
│   ├── validators.py        # validacao do payload
│   ├── normalizers.py       # normalizacao dos dados
│   ├── clickup_client.py    # payload e simulacao ClickUp
│   └── schemas.py           # dataclass do diagnostico normalizado
├── examples/
│   ├── valid_payload.json
│   └── invalid_payload.json
├── data/
│   └── .gitkeep
├── requirements.txt
├── .env.example
└── README.md
```

## Instalacao

Use Python 3.10+.

Nao ha dependencias externas obrigatorias nesta etapa. O arquivo `requirements.txt` foi mantido apenas para documentar isso.

```bash
cd python
python -m app.main
```

Caso queira usar um ambiente virtual:

```bash
cd python
python -m venv .venv
source .venv/bin/activate
python -m app.main
```

## Como testar payload valido

A partir da pasta `python/`:

```bash
python -m app.main
```

Esse comando usa `examples/valid_payload.json` por padrao. O exemplo contem dados realistas com pequenas sujeiras intencionais:

- espacos extras em campos de texto;
- e-mail em uppercase;
- telefone com mascara.

## Como testar payload invalido

A partir da pasta `python/`:

```bash
python -m app.main --payload examples/invalid_payload.json
```

O exemplo invalido demonstra multiplos erros de validacao:

- nome vazio;
- telefone curto;
- e-mail sem formato valido;
- campo obrigatorio ausente;
- desafio principal vazio.

Payloads invalidos encerram o fluxo de forma controlada, com codigo de saida `1`, sem salvar no banco e sem simular envio ao ClickUp.

## Fluxo da aplicacao

1. `app/main.py` resolve o caminho do arquivo JSON.
2. O JSON e lido com tratamento para arquivo inexistente, caminho invalido, erro de permissao, encoding invalido e JSON malformado.
3. `app/validators.py` valida os campos obrigatorios.
4. `app/normalizers.py` remove espacos extras, normaliza e-mail e formata telefone.
5. `app/database.py` cria a tabela e salva o lead em SQLite.
6. `app/clickup_client.py` monta o payload ClickUp e simula a criacao da tarefa.
7. O banco e atualizado com o resultado da etapa ClickUp.

## Validacoes implementadas

Campos esperados:

- `nome`
- `telefone`
- `email`
- `especialidade`
- `principal_desafio`

Regras aplicadas:

- todos os campos acima sao obrigatorios;
- campos de texto nao podem ficar vazios depois da remocao de espacos;
- telefone deve ter pelo menos 10 digitos;
- e-mail deve ter um formato minimo, como `nome@dominio.com`.

Quando mais de um problema e encontrado, todos os erros sao listados antes do encerramento.

## Normalizacoes implementadas

- Reducao de espacos extras em campos de texto.
- E-mail convertido para minusculas.
- Telefone convertido para digitos e formatado em padrao brasileiro simplificado, como `+5511999998888`.
- DDI `55` nao e duplicado quando ja vem no payload.

## Banco de dados

O banco SQLite e criado automaticamente em:

```txt
python/data/leads.db
```

A tabela criada se chama `diagnostic_leads` e possui os campos:

- `id`
- `nome`
- `telefone`
- `email`
- `especialidade`
- `principal_desafio`
- `status`
- `clickup_task_id`
- `error_message`
- `created_at`

O arquivo `data/leads.db` e um banco local gerado pela execucao e nao deve ser versionado. A pasta `data/` mantem apenas `data/.gitkeep` no Git.

Para inspecionar os registros criados localmente, a partir da pasta `python/`:

```bash
sqlite3 -header -column data/leads.db "SELECT id, nome, status, clickup_task_id, error_message, created_at FROM diagnostic_leads;"
```

## Variaveis de ambiente

O projeto nao carrega `.env` automaticamente para evitar dependencias externas. Nao e necessario criar arquivo `.env` para rodar localmente.

O modo simulado do ClickUp e o comportamento padrao e recomendado para avaliacao local. Se `CLICKUP_SIMULATION_MODE` nao existir, estiver vazia ou vier com um valor nao reconhecido, o script usa modo simulado.

Valores aceitos como verdadeiro:

- `true`
- `1`
- `yes`
- `y`
- `sim`

Valores aceitos como falso:

- `false`
- `0`
- `no`
- `n`
- `nao`
- `não`

Use `CLICKUP_SIMULATION_MODE=false` apenas para demonstrar o caminho de erro controlado do modo real. A chamada real ao ClickUp ainda nao foi implementada; nesse caso, o lead e salvo e depois atualizado com `status` igual a `clickup_failed`.

Essa decisao evita depender de token real, conta ClickUp ou lista configurada, facilitando a reproducao pelo avaliador.

Variaveis documentadas em `.env.example`:

- `CLICKUP_SIMULATION_MODE`: controla o modo simulado. O padrao do codigo e `true`.
- `CLICKUP_API_TOKEN`: token que seria usado em uma integracao real futura com ClickUp. Nao e usado no modo simulado.
- `CLICKUP_LIST_ID`: lista de destino que seria usada na API real. No modo simulado, aparece apenas na saida.
- `CLICKUP_ASSIGNEE_ID`: usuario responsavel pela tarefa. Quando informado, entra no payload em `assignees`.

Exemplos:

```bash
# Linux/macOS: execucao padrao em modo simulado
unset CLICKUP_SIMULATION_MODE
python -m app.main

# Linux/macOS: forcar caminho real ainda nao implementado
CLICKUP_SIMULATION_MODE=false python -m app.main
```

```powershell
# PowerShell: execucao padrao em modo simulado
Remove-Item Env:CLICKUP_SIMULATION_MODE
python -m app.main

# PowerShell: forcar caminho real ainda nao implementado
$env:CLICKUP_SIMULATION_MODE="false"; python -m app.main
```

## Exemplo resumido de saida valida

```txt
=== Payload recebido ===
Arquivo: .../python/examples/valid_payload.json
{ ... }

=== Validacao ===
Resultado: payload valido.

=== Normalizacao ===
{
  "nome": "Ana Carvalho",
  "telefone": "+5511999998888",
  "email": "ana.carvalho@example.com",
  "especialidade": "Dermatologia",
  "principal_desafio": "Atrair pacientes qualificados para a agenda particular"
}

=== Persistencia SQLite ===
Banco: .../python/data/leads.db
Lead salvo com ID: 1
{ "status": "saved", ... }

=== ClickUp ===
Modo: simulado
Lista ClickUp destino: nao configurada no ambiente
Payload ClickUp simulado:
{ "name": "Novo lead: Ana Carvalho", ... }
Resultado: tarefa simulada criada com ID simulated-clickup-task-1.

=== Resultado final ===
{ "status": "clickup_created", "clickup_task_id": "simulated-clickup-task-1", ... }
Sucesso: fluxo concluido em .../python/data/leads.db.
```

## Exemplo resumido de saida invalida

```txt
=== Payload recebido ===
Arquivo: .../python/examples/invalid_payload.json
{ ... }

=== Validacao ===
Resultado: payload invalido.
Erros encontrados:
- Campo obrigatorio ausente: especialidade.
- O campo nome nao pode ficar vazio.
- O campo telefone deve ter pelo menos 10 digitos.
- O campo email deve ter um formato valido, como nome@dominio.com
- O campo principal_desafio nao pode ficar vazio.

=== Resultado final ===
Falha: nenhum dado foi salvo no SQLite e nenhuma tarefa ClickUp foi simulada.
```

## Decisoes tecnicas

- SQLite foi escolhido para facilitar a reproducao local por qualquer avaliador, sem conta externa, servidor ou credenciais.
- O ClickUp esta simulado por padrao para evitar dependencia de token real e ainda demonstrar o payload que seria enviado.
- A solucao foi separada em modulos pequenos para validacao, normalizacao, banco de dados, configuracao, schema e cliente ClickUp.
- A biblioteca padrao do Python foi priorizada sempre que possivel para reduzir instalacao e pontos de falha.
- O script foi mantido como comando de terminal porque o desafio pede backend e integracao, nao uma API HTTP.
- Nao foram criadas migrations complexas porque a estrutura local tem uma unica tabela simples e reproduzivel.

## Tratamento de erros

- Arquivo inexistente, diretorio no lugar de arquivo, erro de permissao, encoding invalido e JSON malformado geram mensagens claras.
- Payload invalido lista todos os erros encontrados e encerra antes da normalizacao, banco e ClickUp.
- Erro na etapa ClickUp, quando o lead ja foi salvo, atualiza o registro com status `clickup_failed` e grava a mensagem em `error_message`.
- Excecoes inesperadas nao sao escondidas silenciosamente.

## Limitacoes conhecidas

- A validacao de e-mail e propositalmente simples.
- A formatacao de telefone cobre um padrao brasileiro basico, mas nao substitui uma biblioteca especializada.
- A integracao real com ClickUp ainda nao foi implementada.
- Nao ha testes automatizados nesta entrega.
- Nao ha deduplicacao de leads por e-mail ou telefone.
- O `.env` nao e carregado automaticamente para evitar dependencia externa.

## Melhorias futuras

- Trocar SQLite por Supabase ou PostgreSQL em ambiente real.
- Integrar chamada real com a API do ClickUp.
- Transformar o script em endpoint HTTP com FastAPI.
- Adicionar testes automatizados para validacao, normalizacao, banco e payload ClickUp.
- Adicionar logs estruturados.
- Validar telefone com biblioteca especializada.
- Adicionar deduplicacao por e-mail e telefone.
