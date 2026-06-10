"""Normalizadores para os dados recebidos do formulario."""

from __future__ import annotations

from collections.abc import Mapping

from app.schemas import Diagnostico


def remove_extra_spaces(value: object) -> str:
    """Remove espacos nas pontas e reduz espacos internos repetidos."""
    if value is None:
        return ""

    return " ".join(str(value).strip().split())


def only_digits(value: object) -> str:
    """Retorna apenas os digitos de um valor."""
    return "".join(char for char in remove_extra_spaces(value) if char.isdigit())


def normalize_email(value: object) -> str:
    """Normaliza e-mail para minusculas e sem espacos extras."""
    return remove_extra_spaces(value).lower()


def format_brazilian_phone(value: object) -> str:
    """Formata telefone para um padrao brasileiro simplificado."""
    digits = only_digits(value)

    if digits.startswith("00"):
        digits = digits[2:]

    if digits.startswith("55") and len(digits) > 11:
        return f"+{digits}"

    return f"+55{digits}"


def normalize_payload(payload: Mapping[str, object]) -> Diagnostico:
    """Converte o payload recebido para a estrutura normalizada."""
    return Diagnostico(
        nome=remove_extra_spaces(payload.get("nome")),
        telefone=format_brazilian_phone(payload.get("telefone")),
        email=normalize_email(payload.get("email")),
        especialidade=remove_extra_spaces(payload.get("especialidade")),
        principal_desafio=remove_extra_spaces(payload.get("principal_desafio")),
    )
