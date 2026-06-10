"""Configuracoes simples da aplicacao."""

from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "leads.db"

_TRUE_VALUES = {"1", "true", "yes", "y", "sim", "s", "on"}
_FALSE_VALUES = {"0", "false", "no", "n", "nao", "off"}


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.environ.get(name)

    if value is None:
        return default

    normalized_value = value.strip().lower()

    if normalized_value in _TRUE_VALUES:
        return True

    if normalized_value in _FALSE_VALUES:
        return False

    return default


CLICKUP_SIMULATION_MODE = _get_bool_env("CLICKUP_SIMULATION_MODE", True)
CLICKUP_API_TOKEN = os.environ.get("CLICKUP_API_TOKEN", "").strip()
CLICKUP_LIST_ID = os.environ.get("CLICKUP_LIST_ID", "").strip()
CLICKUP_ASSIGNEE_ID = os.environ.get("CLICKUP_ASSIGNEE_ID", "").strip()
