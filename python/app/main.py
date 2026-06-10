"""Ponto de entrada do script de diagnostico."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.normalizers import normalize_payload
from app.validators import validate_payload


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PAYLOAD_PATH = BASE_DIR / "examples" / "valid_payload.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida e normaliza um payload de diagnostico."
    )
    parser.add_argument(
        "--payload",
        default=str(DEFAULT_PAYLOAD_PATH),
        help="Caminho para o arquivo JSON de entrada.",
    )

    return parser.parse_args()


def resolve_payload_path(payload_path: str) -> Path:
    path = Path(payload_path)

    if path.is_absolute():
        return path

    cwd_path = Path.cwd() / path
    if cwd_path.exists():
        return cwd_path

    return BASE_DIR / path


def load_payload(payload_path: Path) -> object:
    """Carrega um arquivo JSON de payload."""
    with payload_path.open(encoding="utf-8") as payload_file:
        return json.load(payload_file)


def print_json(title: str, content: object) -> None:
    print(title)
    print(json.dumps(content, indent=2, ensure_ascii=False))


def main() -> int:
    args = parse_args()
    payload_path = resolve_payload_path(args.payload)

    try:
        payload = load_payload(payload_path)
    except FileNotFoundError:
        print(f"Falha: arquivo de payload nao encontrado: {payload_path}")
        return 1
    except json.JSONDecodeError as error:
        print(f"Falha: JSON invalido em {payload_path}: {error}")
        return 1

    print_json("Payload recebido:", payload)

    errors = validate_payload(payload)
    if errors:
        print("\nErros de validacao:")
        for error in errors:
            print(f"- {error}")

        print("\nFalha: payload invalido. Nenhum dado foi salvo ou enviado.")
        return 0

    normalized_payload = normalize_payload(payload)

    print_json("\nPayload normalizado:", normalized_payload.to_dict())
    print("\nSucesso: payload validado e normalizado.")
    print("Banco de dados e ClickUp ainda nao foram acionados nesta etapa.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
