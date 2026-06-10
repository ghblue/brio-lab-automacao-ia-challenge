# Desafio 2 - Backend com Python

Este diretorio contem a estrutura inicial do entregavel Python do desafio tecnico da Brio Lab.

O objetivo final do Desafio 2 sera simular o recebimento de um JSON de diagnostico, validar e normalizar os dados, salvar as informacoes tratadas em banco SQLite e criar ou simular a criacao de uma tarefa no ClickUp para o time comercial.

Nesta etapa, apenas a base do projeto foi criada. Ainda nao ha persistencia em banco, chamada ao ClickUp ou validacao completa.

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
python app/main.py
```

O script carrega `examples/valid_payload.json`, imprime o conteudo no terminal e exibe uma mensagem confirmando que a estrutura inicial foi criada com sucesso.

## Decisao sobre banco de dados

SQLite foi escolhido para facilitar a execucao local pelo avaliador, sem depender de contas externas, servidores ou configuracoes adicionais. A implementacao do banco sera adicionada em uma etapa futura.

## Proximas etapas

- Implementar validacao dos campos obrigatorios.
- Normalizar e-mail e formatar telefone.
- Criar a camada SQLite em `app/database.py`.
- Persistir os dados tratados em `data/`.
- Implementar o modo simulado de criacao de tarefa no ClickUp.
- Documentar o payload enviado ao ClickUp e possiveis melhorias futuras.
