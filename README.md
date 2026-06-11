# Brio Lab - Desafio Tecnico de Automacao e IA

Este repositorio contem a entrega do desafio tecnico da Brio Lab para a vaga de Desenvolvedor(a) de Automacao & IA.

A solucao esta dividida em dois desafios independentes:

1. **Desafio 1 - Orquestracao com N8N**
2. **Desafio 2 - Backend com Python**

O objetivo da entrega e demonstrar uma automacao ponta a ponta com N8N e um fluxo backend em Python para validacao, tratamento, persistencia e integracao simulada.

## Contexto

A Brio Lab trabalha com operacoes que conectam ferramentas como ClickUp, Google Sheets, portais web, canais de notificacao e servicos de inteligencia artificial.

Neste desafio, os fluxos foram implementados com foco em:

- clareza da logica;
- facilidade de reproducao local;
- documentacao objetiva;
- transparencia sobre integracoes reais e simuladas;
- separacao entre orquestracao visual e backend.

## Visao geral da solucao

O projeto entrega dois fluxos complementares:

- **N8N**: recebe um evento simulado do ClickUp, processa apenas tarefas aprovadas, gera hashtags simuladas, salva o resultado no Google Sheets e envia uma notificacao externa.
- **Python**: recebe um JSON de diagnostico, valida e normaliza os dados, salva em SQLite, monta um payload realista para o ClickUp e simula a criacao da tarefa.

As integracoes que exigiriam tokens, contas externas ou chaves privadas foram simuladas quando necessario para manter a avaliacao reproduzivel.

## Estrutura do repositorio

```txt
.
|-- n8n/
|   |-- payloads/
|   |-- screenshots/
|   |-- workflow-brio-clickup-aprovado.json
|   `-- README.md
|
|-- python/
|   |-- app/
|   |-- examples/
|   |-- data/
|   |-- requirements.txt
|   |-- .env.example
|   `-- README.md
|
|-- .gitignore
`-- README.md
```

## Desafio 1 - N8N

O workflow implementado em N8N automatiza o processamento de tarefas de conteudo quando uma tarefa chega ao status `aprovado`.

O fluxo faz:

1. recebe um payload simulado do ClickUp via Webhook;
2. verifica se o status da tarefa e `aprovado`;
3. ignora tarefas com status diferente;
4. extrai dados da tarefa e custom fields:
   - `task_id`
   - `task_name`
   - `description`
   - `task_url`
   - `caption`
   - `post_date`
   - `content_type`
5. simula a geracao de hashtags por IA;
6. prepara o registro para persistencia;
7. salva o resultado no Google Sheets;
8. envia notificacao via Webhook.site;
9. retorna a resposta final do processamento.

Arquivos principais:

- workflow exportado: `n8n/workflow-brio-clickup-aprovado.json`
- payloads de teste: `n8n/payloads/`
- evidencias visuais: `n8n/screenshots/`
- documentacao detalhada: `n8n/README.md`

## Desafio 2 - Python

O script Python simula o processamento de um formulario de diagnostico recebido pelo site de uma cliente.

O fluxo faz:

1. carrega um JSON de diagnostico;
2. valida campos obrigatorios;
3. normaliza e-mail;
4. formata telefone;
5. salva os dados tratados em SQLite;
6. monta um payload realista para criacao de tarefa no ClickUp;
7. simula a criacao da tarefa no ClickUp;
8. atualiza o banco com status e `clickup_task_id`;
9. trata payload invalido sem salvar no banco.

Arquivos principais:

- codigo da aplicacao: `python/app/`
- payloads de exemplo: `python/examples/`
- banco SQLite local gerado em execucao: `python/data/leads.db`
- dependencias documentadas: `python/requirements.txt`
- variaveis de ambiente de exemplo: `python/.env.example`
- documentacao detalhada: `python/README.md`

O arquivo `python/data/leads.db` e gerado localmente e nao deve ser versionado.

## Como testar

### Testar o Desafio 2 - Python

A partir da raiz do repositorio:

```bash
cd python
python -m app.main
```

O comando acima usa `examples/valid_payload.json` por padrao.

Para testar o payload invalido:

```bash
python -m app.main --payload examples/invalid_payload.json
```

Para consultar os registros salvos no SQLite:

```bash
sqlite3 -header -column data/leads.db "SELECT id, nome, status, clickup_task_id, error_message, created_at FROM diagnostic_leads;"
```

### Testar o Desafio 1 - N8N

1. Importe ou abra o workflow exportado em `n8n/workflow-brio-clickup-aprovado.json`.
2. Configure as credenciais e destinos necessarios no ambiente N8N, como Google Sheets e Webhook.site.
3. Clique em `Execute workflow` no modo de teste para deixar o Webhook aguardando requisicao.
4. Substitua `URL_DO_WEBHOOK_TEST` pela URL de teste exibida pelo N8N.

Payload aprovado, a partir da raiz do repositorio:

```bash
curl -X POST "URL_DO_WEBHOOK_TEST" -H "Content-Type: application/json" --data-binary @n8n/payloads/clickup-task-approved.json
```

Resultado esperado:

- a tarefa passa pela condicao de status `aprovado`;
- os dados sao extraidos;
- as hashtags simuladas sao geradas;
- o registro e salvo no Google Sheets;
- a notificacao e enviada para Webhook.site;
- o Webhook retorna a resposta final.

Payload nao aprovado:

```bash
curl -X POST "URL_DO_WEBHOOK_TEST" -H "Content-Type: application/json" --data-binary @n8n/payloads/clickup-task-not-approved.json
```

Resultado esperado:

- a tarefa e ignorada;
- IA, persistencia e notificacao nao sao executadas;
- o Webhook retorna uma resposta informando que o item nao foi processado.

## Decisoes tecnicas

- SQLite foi usado no Desafio 2 para facilitar a execucao local pelo avaliador.
- ClickUp foi simulado no Python para evitar dependencia de token real.
- No N8N, ClickUp foi simulado via Webhook manual, conforme permitido no desafio.
- A IA foi simulada para evitar dependencia de chave externa, mantendo o fluxo reproduzivel.
- Google Sheets foi usado como persistencia no N8N por facilitar validacao visual.
- Webhook.site foi usado para simular notificacao externa.
- JavaScript foi usado nos nodes `Code` do N8N por ser natural nas expressoes e transformacoes da ferramenta.
- Python ficou concentrado no Desafio 2, onde o foco era backend, tratamento de dados, banco e integracao simulada.
- O script Python foi mantido como comando de terminal, sem API HTTP, para preservar o escopo do desafio.

## Simulacoes realizadas

- ClickUp real nao foi usado; foi simulado por payloads e Webhook.
- IA real nao foi chamada; as hashtags foram simuladas no N8N.
- No Python, a criacao de tarefa no ClickUp e simulada por padrao.
- Essas decisoes foram tomadas para manter a entrega reproduzivel, sem tokens ou contas pagas.
- Em producao, essas etapas seriam substituidas por integracoes reais com ClickUp, Gemini/GPT/Claude e Supabase/PostgreSQL.

## Evidencias da entrega

Principais artefatos da entrega:

- `n8n/workflow-brio-clickup-aprovado.json`
- `n8n/screenshots/`
- `n8n/payloads/`
- `python/app/`
- `python/examples/`
- `python/requirements.txt`
- `python/.env.example`
- `n8n/README.md`
- `python/README.md`

## Demonstracao em video

Uma demonstracao curta foi salva localmente junto das evidencias do N8N:

```txt
n8n/screenshots/demonstracao-fluxo-de-execucao-completo.mp4
```

Link externo: [demonstracao](https://youtu.be/QKyCosu-6nk)

## Melhorias futuras

- Integrar com ClickUp real.
- Usar Gemini, GPT ou Claude via API real.
- Trocar Google Sheets por Supabase/PostgreSQL.
- Criar tratamento de erro mais granular no N8N. (tratar falhas separadamente em cada etapa do workflow, em vez de considerar apenas sucesso ou erro geral)
- Adicionar alertas especificos para falha de persistencia ou notificacao.
- Transformar o script Python em endpoint HTTP com FastAPI.
- Adicionar testes automatizados no Python.
- Adicionar logs estruturados. (centralizar e padronizar mensagens de erro, warnings e informacoes de execucao de forma clara e padronizada.)
- Adicionar deduplicacao de leads no Python. (evitar que o mesmo lead seja salvo várias vezes no banco.)
- Separar ambientes de teste e producao.

## Observacoes finais

A entrega prioriza clareza, reproducibilidade e documentacao das decisoes tomadas. As simulacoes foram usadas de forma explicita para evitar dependencia de tokens, credenciais privadas, URLs pessoais ou contas pagas.

Os READMEs internos de `n8n/` e `python/` trazem detalhes operacionais de cada desafio e devem ser consultados para validacao mais aprofundada.
