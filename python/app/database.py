"""Camada de persistencia em SQLite para leads de diagnostico."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import DATABASE_PATH
from app.schemas import Diagnostico


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS diagnostic_leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL,
    especialidade TEXT NOT NULL,
    principal_desafio TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'saved',
    clickup_task_id TEXT,
    error_message TEXT,
    created_at TEXT NOT NULL
)
"""

INSERT_DIAGNOSTIC_LEAD_SQL = """
INSERT INTO diagnostic_leads (
    nome,
    telefone,
    email,
    especialidade,
    principal_desafio,
    created_at
) VALUES (?, ?, ?, ?, ?, ?)
"""

GET_LEAD_BY_ID_SQL = """
SELECT
    id,
    nome,
    telefone,
    email,
    especialidade,
    principal_desafio,
    status,
    clickup_task_id,
    error_message,
    created_at
FROM diagnostic_leads
WHERE id = ?
"""


def open_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Abre uma conexao SQLite e garante que a pasta de dados exista."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Cria a tabela de leads de diagnostico se ela ainda nao existir."""
    try:
        with closing(open_connection()) as connection:
            connection.execute(CREATE_TABLE_SQL)
            connection.commit()
    except sqlite3.Error as error:
        raise RuntimeError(
            f"nao foi possivel inicializar o banco SQLite: {error}"
        ) from error


def insert_diagnostic_lead(diagnostic: Diagnostico) -> int:
    """Insere um diagnostico normalizado e retorna o id criado."""
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    try:
        with closing(open_connection()) as connection:
            cursor = connection.execute(
                INSERT_DIAGNOSTIC_LEAD_SQL,
                (
                    diagnostic.nome,
                    diagnostic.telefone,
                    diagnostic.email,
                    diagnostic.especialidade,
                    diagnostic.principal_desafio,
                    created_at,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
    except sqlite3.Error as error:
        raise RuntimeError(
            f"nao foi possivel inserir o lead no banco SQLite: {error}"
        ) from error


def get_lead_by_id(lead_id: int) -> dict[str, Any] | None:
    """Busca um lead pelo id e retorna um dicionario pronto para impressao."""
    try:
        with closing(open_connection()) as connection:
            row = connection.execute(GET_LEAD_BY_ID_SQL, (lead_id,)).fetchone()
    except sqlite3.Error as error:
        raise RuntimeError(
            f"nao foi possivel buscar o lead {lead_id} no banco SQLite: {error}"
        ) from error

    if row is None:
        return None

    return dict(row)
