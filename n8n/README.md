# Desafio 1 - Orquestracao com N8N

Esta pasta concentra os entregaveis do Desafio 1, referente a um workflow N8N para automatizar o processamento de tarefas de conteudo da Brio Lab quando uma tarefa do ClickUp chega ao status `aprovado`.

O workflow foi montado, testado e exportado em:

```txt
n8n/workflow-brio-clickup-aprovado.json
```

## 1. Objetivo

O objetivo do Desafio 1 e demonstrar uma automacao ponta a ponta que:

1. Detecta uma tarefa aprovada.
2. Le dados da tarefa, incluindo nome, descricao e campos personalizados.
3. Gera sugestoes de hashtags com IA ou com retorno simulado.
4. Persiste o resultado em uma ferramenta aceita pelo desafio.
5. Envia uma notificacao externa.

Nesta implementacao, o ClickUp foi simulado por um Webhook manual do N8N, a IA foi simulada em um node `Code`, o resultado foi salvo no Google Sheets e a notificacao foi enviada para o Webhook.site.

## 2. Visao geral do workflow

O workflow recebe um payload JSON simulando um evento do ClickUp e verifica se a tarefa esta com status `aprovado`.

Se o status nao for `aprovado`, o fluxo retorna uma resposta informando que a tarefa foi ignorada.

Se o status for `aprovado`, o fluxo:

1. Extrai os dados principais da tarefa.
2. Simula a geracao de hashtags para Instagram.
3. Prepara um objeto estruturado para persistencia.
4. Salva o registro no Google Sheets.
5. Envia uma notificacao via Webhook.site.
6. Retorna a resposta final do processamento pelo Webhook.

## 3. Arquitetura do fluxo

Ordem dos nodes implementados:

1. `Webhook`
   - Recebe payloads `POST` simulando o evento do ClickUp.
   - Usa resposta via node `Respond to Webhook`.

2. `Verificar status aprovado`
   - Confere se o status recebido e igual a `aprovado`.
   - Aceita estruturas como `task.status.status`, `status.status` ou `status`.

3. `Responder tarefa ignorada`
   - Caminho negativo do `IF`.
   - Retorna `processed: false` quando a tarefa nao esta aprovada.

4. `Extrair dados da tarefa`
   - Usa JavaScript em um node `Code`.
   - Normaliza o payload recebido e extrai os campos relevantes.

5. `Gerar hashtags com IA simulada`
   - Usa JavaScript em um node `Code`.
   - Simula o prompt e o retorno de uma IA para sugestoes de hashtags.

6. `Preparar registro para salvar`
   - Monta um objeto de persistencia com os campos que serao enviados ao Google Sheets.

7. `Salvar no Google Sheets`
   - Faz append de uma nova linha na planilha configurada no N8N.

8. `Enviar notificacao`
   - Envia um `POST` para Webhook.site com o resumo do processamento.

9. `Responder tarefa aprovada`
   - Retorna a resposta final do processamento para a chamada original do Webhook.

## 4. Payloads de teste

Os payloads de teste ficam em:

```txt
n8n/payloads/
```

Arquivos disponiveis:

- `clickup-task-approved.json`: payload com status `aprovado`; deve seguir o fluxo completo.
- `clickup-task-not-approved.json`: payload com status `em revisao`; deve ser ignorado na validacao inicial.

Os payloads sao ficticios e nao contem tokens, credenciais ou dados reais de clientes.

## 5. Etapas implementadas

O workflow implementado faz:

1. Recebe um payload simulado do ClickUp via Webhook.
2. Verifica se o status da tarefa e `aprovado`.
3. Se nao for aprovado, retorna uma resposta informando que a tarefa foi ignorada.
4. Se for aprovado, extrai:
   - `task_id`
   - `task_name`
   - `description`
   - `task_url`
   - `caption`
   - `post_date`
   - `content_type`
5. Simula a geracao de hashtags por IA.
6. Prepara um objeto de persistencia.
7. Salva o resultado no Google Sheets.
8. Envia uma notificacao via Webhook.site.
9. Retorna a resposta final do processamento.

## 6. Simulacoes realizadas

### ClickUp

O ClickUp foi simulado com um Webhook manual porque o desafio permite usar payload simulado quando nao houver uma conta real ou integracao real disponivel.

Essa decisao evita depender de credenciais externas, protege dados reais e facilita a validacao pelo avaliador com payloads versionados no repositorio.

Em producao, o Webhook manual seria substituido por uma integracao real com ClickUp, usando um webhook do ClickUp ou um trigger equivalente para eventos de mudanca de status.

### IA

A IA foi simulada em um node `Code`, retornando hashtags organizadas em categorias:

- `amplas`
- `nichadas`
- `operacionais`

O desafio permite simular o retorno de IA com node `Set` ou `Code`. A simulacao foi escolhida para evitar dependencia de chaves externas, limites de API e configuracoes privadas no N8N.

Em producao, esse node seria substituido por uma chamada real para Gemini, GPT ou Claude via `HTTP Request` ou por um node oficial da ferramenta escolhida.

### Linguagem dos nodes Code

Os nodes `Code` usam JavaScript porque essa e a linguagem natural das expressoes e transformacoes dentro do N8N. Isso facilita acessar o payload, normalizar campos, buscar custom fields e montar objetos intermediarios.

## 7. Persistencia no Google Sheets

O Google Sheets foi escolhido como camada de persistencia porque e uma das opcoes aceitas pelo desafio e facilita a validacao visual pelo avaliador.

O node `Salvar no Google Sheets` insere uma nova linha com campos como:

- `task_id`
- `task_name`
- `task_url`
- `caption`
- `post_date`
- `content_type`
- `ai_provider`
- `hashtags`
- `hashtags_amplas`
- `hashtags_nichadas`
- `hashtags_operacionais`
- `processed_status`
- `created_at`

O README nao inclui link privado da planilha. Para executar o workflow em outro ambiente, e necessario configurar uma credencial de Google Sheets no N8N e apontar o node para uma planilha valida.

Em producao, a persistencia poderia ser migrada para Supabase ou PostgreSQL, especialmente se fosse necessario historico mais estruturado, consultas, auditoria e controle transacional.

## 8. Notificacao via Webhook.site

A notificacao externa foi simulada com Webhook.site.

Essa escolha facilita comprovar que o workflow enviou uma chamada externa depois da persistencia, sem exigir conta de e-mail, Telegram, WhatsApp ou outro provedor.

O README nao inclui URL real do Webhook.site. Para testar em outro ambiente, gere uma URL temporaria no Webhook.site e configure essa URL no node `Enviar notificacao`.

Em producao, essa etapa poderia ser substituida por:

- e-mail;
- Telegram;
- WhatsApp;
- webhook interno;
- sistema de alertas operacional.

## 9. Como testar

Antes de disparar os comandos abaixo no modo de teste do N8N, clique em `Execute workflow` para deixar o Webhook aguardando uma requisicao.

Substitua `URL_DO_WEBHOOK_TEST` pela URL de teste exibida pelo N8N para o node `Webhook`.

Payload aprovado:

```bash
curl -X POST "URL_DO_WEBHOOK_TEST" -H "Content-Type: application/json" --data-binary @n8n/payloads/clickup-task-approved.json
```

Resultado esperado:

- o status e reconhecido como `aprovado`;
- os dados da tarefa sao extraidos;
- as hashtags simuladas sao geradas;
- o registro e salvo no Google Sheets;
- a notificacao e enviada para Webhook.site;
- o Webhook retorna a resposta final do processamento.

Payload nao aprovado:

```bash
curl -X POST "URL_DO_WEBHOOK_TEST" -H "Content-Type: application/json" --data-binary @n8n/payloads/clickup-task-not-approved.json
```

Resultado esperado:

- o status nao passa pela condicao de aprovado;
- nenhuma etapa de IA, persistencia ou notificacao e executada;
- o Webhook retorna uma resposta indicando que a tarefa foi ignorada.

## 10. Screenshots

Os arquivos encontrados em `n8n/screenshots/` sao:

- `workflow-completo.png`
- `workflow-completo-em-caso-de-aprovado.png`
- `execucao-payload-aprovado-hashtags-pt1.png`
- `execucao-payload-aprovado-hashtags-pt2.png`
- `google-sheets-registro-salvo.png`
- `webhook-site-notificacao.png`
- `workflow-completo-payload-nao-aprovado.png`
- `execucao-payload-nao-aprovado-pt1.png`

Tambem foi salvo um video de demonstracao:

- `demonstracao-fluxo-de-execucao-completo.mp4`

Os nomes acima refletem os arquivos reais existentes na pasta. Eles documentam a visao geral do workflow, o caminho aprovado, a geracao simulada de hashtags, o registro no Google Sheets, a notificacao externa e o caminho de payload nao aprovado.

## 11. Arquivos entregues

Arquivos principais do Desafio 1:

- `n8n/workflow-brio-clickup-aprovado.json`
- `n8n/payloads/clickup-task-approved.json`
- `n8n/payloads/clickup-task-not-approved.json`
- `n8n/screenshots/`
- `n8n/README.md`

## 12. Melhorias futuras

Possiveis evolucoes do workflow:

- Substituir o Webhook manual por um trigger real do ClickUp.
- Buscar detalhes completos da tarefa diretamente na API do ClickUp.
- Usar API real de IA, como Gemini, GPT ou Claude.
- Persistir em Supabase ou PostgreSQL em vez de Google Sheets.
- Adicionar tratamento de erro por etapa.
- Adicionar alerta especifico para falha na persistencia ou notificacao.
- Adicionar logs estruturados para facilitar auditoria e reprocessamento.
- Criar versionamento de payloads de teste.
- Adicionar ambientes separados para teste e producao.
- Validar campos obrigatorios antes de chamar IA, persistencia ou notificacao.

## 13. Limitacoes conhecidas

- O evento do ClickUp esta simulado por Webhook manual.
- A etapa de IA esta simulada e retorna hashtags fixas para demonstracao.
- A persistencia depende de credencial e planilha configuradas no ambiente N8N.
- A notificacao usa Webhook.site, que e adequado para teste, mas nao para operacao final.
- O fluxo atual cobre o caminho feliz e o caminho de tarefa nao aprovada, mas ainda nao possui tratamento detalhado para falhas em cada integracao.
- Os payloads simulados cobrem dois cenarios principais, mas podem ser expandidos para casos de campos ausentes, status com letras maiusculas, custom fields incompletos e payloads fora do formato esperado.
