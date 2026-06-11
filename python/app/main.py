"""Ponto de entrada do script de diagnostico."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path

from app.clickup_client import create_clickup_task
from app.config import BASE_DIR, DATABASE_PATH
from app.database import (
    get_lead_by_id,
    init_db,
    insert_diagnostic_lead,
    update_lead_clickup_result,
)
from app.normalizers import normalize_payload
from app.validators import validate_payload


DEFAULT_PAYLOAD_PATH = BASE_DIR / "examples" / "valid_payload.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida, normaliza e salva um payload de diagnostico."
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


def print_section(title: str, *, first: bool = False) -> None:
    if not first:
        print()

    print(f"=== {title} ===")


def print_json(content: object) -> None:
    print(json.dumps(content, indent=2, ensure_ascii=False))


def main() -> int:
    args = parse_args()
    payload_path = resolve_payload_path(args.payload)

    try:
        payload = load_payload(payload_path)
    except FileNotFoundError:
        print(f"Falha: arquivo de payload nao encontrado: {payload_path}")
        return 1
    except IsADirectoryError:
        print(
            "Falha: o caminho informado e um diretorio, "
            f"nao um arquivo JSON: {payload_path}"
        )
        return 1
    except PermissionError:
        print(f"Falha: sem permissao para ler o arquivo de payload: {payload_path}")
        return 1
    except UnicodeDecodeError as error:
        print(f"Falha: nao foi possivel ler {payload_path} como UTF-8: {error}")
        return 1
    except json.JSONDecodeError as error:
        print(f"Falha: JSON invalido em {payload_path}: {error}")
        return 1
    except OSError as error:
        print(
            f"Falha: nao foi possivel ler o arquivo de payload {payload_path}: "
            f"{error}"
        )
        return 1

    print_section("Payload recebido", first=True)
    print(f"Arquivo: {payload_path}")
    print_json(payload)

    print_section("Validacao")
    errors = validate_payload(payload)
    if errors:
        print("Resultado: payload invalido.")
        print("Erros encontrados:")
        for error in errors:
            print(f"- {error}")

        print_section("Resultado final")
        print(
            "Falha: nenhum dado foi salvo no SQLite e nenhuma tarefa ClickUp "
            "foi simulada."
        )
        return 1

    if not isinstance(payload, Mapping):
        print("Falha: payload validado deveria ser um objeto JSON.")
        return 1

    normalized_payload = normalize_payload(payload)

    print("Resultado: payload valido.")

    print_section("Normalizacao")
    print_json(normalized_payload.to_dict())

    try:
        print_section("Persistencia SQLite")
        print(f"Banco: {DATABASE_PATH}")
        init_db()
        lead_id = insert_diagnostic_lead(normalized_payload)
        saved_lead = get_lead_by_id(lead_id)
    except RuntimeError as error:
        print(f"Falha de banco de dados: {error}")
        return 1

    if saved_lead is None:
        print(f"Falha: lead {lead_id} nao encontrado apos a insercao.")
        return 1

    print(f"Lead salvo com ID: {lead_id}")
    print_json(saved_lead)

    clickup_failed = False

    print_section("ClickUp")
    try:
        clickup_task_id = create_clickup_task(saved_lead)
        update_lead_clickup_result(
            lead_id,
            status="clickup_created",
            clickup_task_id=clickup_task_id,
            error_message=None,
        )
        print(f"Resultado: tarefa simulada criada com ID {clickup_task_id}.")
    except RuntimeError as error:
        clickup_failed = True
        error_message = str(error)
        print(f"Falha na etapa ClickUp: {error_message}")

        try:
            update_lead_clickup_result(
                lead_id,
                status="clickup_failed",
                clickup_task_id=None,
                error_message=error_message,
            )
        except RuntimeError as database_error:
            print(f"Falha adicional ao registrar erro no banco: {database_error}")
            return 1
        print("Resultado: falha registrada no SQLite com status clickup_failed.")

    try:
        final_lead = get_lead_by_id(lead_id)
    except RuntimeError as error:
        print(f"Falha de banco de dados: {error}")
        return 1

    if final_lead is None:
        print(f"Falha: lead {lead_id} nao encontrado apos a etapa ClickUp.")
        return 1

    print_section("Resultado final")
    print_json(final_lead)

    if clickup_failed:
        print(f"Fluxo concluido com falha registrada no ClickUp em {DATABASE_PATH}.")
        return 1

    print(f"Sucesso: fluxo concluido em {DATABASE_PATH}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
