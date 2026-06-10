"""Cliente futuro para criacao ou simulacao de tarefas no ClickUp."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from app.config import (
    CLICKUP_ASSIGNEE_ID,
    CLICKUP_LIST_ID,
    CLICKUP_SIMULATION_MODE,
)


CLICKUP_TAGS = ["diagnostico", "lead-site", "automacao"]
CLICKUP_DEFAULT_STATUS = "novo lead"


def _format_assignee_id(assignee_id: str) -> int | str:
    if assignee_id.isdigit():
        return int(assignee_id)

    return assignee_id


def build_clickup_task_payload(lead: Mapping[str, Any]) -> dict[str, Any]:
    """Monta o corpo que seria enviado para a criacao da tarefa no ClickUp."""
    description = "\n".join(
        [
            f"Nome: {lead['nome']}",
            f"Telefone: {lead['telefone']}",
            f"E-mail: {lead['email']}",
            f"Especialidade: {lead['especialidade']}",
            f"Principal desafio: {lead['principal_desafio']}",
        ]
    )

    payload: dict[str, Any] = {
        "name": f"Novo lead: {lead['nome']}",
        "description": description,
        "tags": CLICKUP_TAGS,
        "status": CLICKUP_DEFAULT_STATUS,
    }

    if CLICKUP_ASSIGNEE_ID:
        payload["assignees"] = [_format_assignee_id(CLICKUP_ASSIGNEE_ID)]

    return payload


def create_clickup_task(lead: Mapping[str, Any]) -> str:
    """Cria uma tarefa no ClickUp ou simula a chamada, conforme configuracao."""
    payload = build_clickup_task_payload(lead)

    if CLICKUP_SIMULATION_MODE:
        print("\nPayload ClickUp simulado:")
        if CLICKUP_LIST_ID:
            print(f"Lista ClickUp destino: {CLICKUP_LIST_ID}")
        else:
            print("Lista ClickUp destino: nao configurada no ambiente")

        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return f"simulated-clickup-task-{lead['id']}"

    raise RuntimeError(
        "modo real do ClickUp ainda nao foi implementado; "
        "use CLICKUP_SIMULATION_MODE=true para executar localmente"
    )
