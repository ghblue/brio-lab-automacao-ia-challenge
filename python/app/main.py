"""Ponto de entrada inicial do Desafio 2."""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
EXAMPLE_PAYLOAD_PATH = BASE_DIR / "examples" / "valid_payload.json"


def load_example_payload() -> dict:
    """Carrega o payload valido usado nesta etapa inicial."""
    with EXAMPLE_PAYLOAD_PATH.open(encoding="utf-8") as payload_file:
        return json.load(payload_file)


def main() -> None:
    payload = load_example_payload()

    print("Payload carregado:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("\nEstrutura inicial do Desafio 2 criada com sucesso.")


if __name__ == "__main__":
    main()
