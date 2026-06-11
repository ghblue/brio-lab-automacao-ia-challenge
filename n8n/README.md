# Desafio 1 - Orquestracao com N8N

Esta pasta concentra os entregaveis do Desafio 1, que simula um fluxo de automacao para tarefas de conteudo da Brio Lab gerenciadas no ClickUp.

O objetivo do workflow sera detectar quando uma tarefa de postagem mudar para o status `aprovado`, ler seus dados principais, gerar ou simular sugestoes de hashtags com IA, persistir o resultado e enviar uma notificacao.

## Por que usar Webhook manual

O desafio permite simular o ClickUp caso nao exista uma conta real disponivel. Por isso, a primeira versao do fluxo usara um Webhook manual no N8N recebendo payloads JSON simulados.

Essa abordagem facilita a avaliacao porque:

- nao depende de credenciais reais do ClickUp;
- evita uso de dados reais de clientes;
- permite testar rapidamente o status `aprovado`;
- deixa claro quais dados o workflow espera receber.

## Etapas previstas do workflow

1. Receber o payload da tarefa via Webhook manual.
2. Verificar se `task.status.status` e igual a `aprovado`.
3. Ler `name`, `description`, `url`, responsavel/criador e `custom_fields`.
4. Extrair os campos `legenda`, `data_postagem` e `tipo_conteudo`.
5. Enviar a legenda para uma IA ou simular a resposta com um node `Set`.
6. Persistir o resultado em banco ou planilha.
7. Enviar uma notificacao informando que a tarefa aprovada foi processada.

## Payloads simulados

Os payloads ficam em `n8n/payloads/`.

- `clickup-task-approved.json`: representa uma tarefa com status `aprovado`. Deve seguir pelo fluxo completo.
- `clickup-task-not-approved.json`: representa uma tarefa com status `em revisao`. Deve ser barrada na condicao inicial do workflow.

Os dados sao ficticios e nao contem credenciais, tokens ou informacoes reais de clientes.

## Workflow exportado

O arquivo `workflow-brio-clickup-aprovado.json` sera usado para armazenar o JSON exportado do N8N depois que o fluxo for montado.

Neste momento ele contem apenas um placeholder valido para manter a estrutura do projeto preparada sem inventar uma estrutura completa de exportacao do N8N antes da montagem real.

## Screenshots

Os screenshots do fluxo montado ficarao em `n8n/screenshots/`.

A pasta ja possui um `.gitkeep` para ser versionada mesmo antes da captura das imagens.

## O que sera simulado

Nesta etapa inicial, serao simulados:

- evento de mudanca de status do ClickUp;
- payload recebido pelo Webhook;
- dados de tarefa, responsavel e campos personalizados;
- possivel retorno de IA, caso nao seja usada uma chave real;
- notificacao final, se necessario.

## Como seria em producao

Em um ambiente real, o workflow poderia usar:

- Webhook real do ClickUp para receber eventos de tarefas;
- chamada na API do ClickUp para buscar dados completos da tarefa;
- API de IA com credenciais protegidas no N8N;
- banco ou planilha de producao para registrar os resultados;
- canal oficial de notificacao, como e-mail, Telegram, WhatsApp ou webhook interno;
- tratamento de erros, logs e reprocessamento para falhas temporarias.

## Proximos passos

1. Criar o Webhook manual no N8N.
2. Enviar `clickup-task-approved.json` para validar o caminho positivo.
3. Criar uma condicao para continuar apenas quando o status for `aprovado`.
4. Extrair os custom fields necessarios.
5. Simular ou integrar a etapa de IA para gerar hashtags.
6. Simular ou configurar a persistencia.
7. Simular ou configurar a notificacao.
8. Exportar o workflow real e substituir `workflow-brio-clickup-aprovado.json`.
9. Capturar screenshots do fluxo e salvar em `n8n/screenshots/`.
