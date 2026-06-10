"""Validadores para o payload de diagnostico."""

from __future__ import annotations

from collections.abc import Mapping

from app.normalizers import only_digits, remove_extra_spaces


REQUIRED_FIELDS = (
    "nome",
    "telefone",
    "email",
    "especialidade",
    "principal_desafio",
)

MIN_PHONE_DIGITS = 10


def validate_required_fields(payload: Mapping[str, object]) -> list[str]:
    """Valida se todos os campos esperados foram enviados."""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in payload:
            errors.append(f"Campo obrigatorio ausente: {field}.")

    return errors


def validate_nome(value: object) -> list[str]:
    if not remove_extra_spaces(value):
        return ["O campo nome nao pode ficar vazio."]

    return []


def validate_telefone(value: object) -> list[str]:
    digits = only_digits(value)

    if len(digits) < MIN_PHONE_DIGITS:
        return [
            f"O campo telefone deve ter pelo menos {MIN_PHONE_DIGITS} digitos."
        ]

    return []


def validate_email(value: object) -> list[str]:
    email = remove_extra_spaces(value)
    email_parts = email.split("@")

    if (
        len(email_parts) != 2
        or not email_parts[0]
        or not email_parts[1]
        or " " in email
        or "." not in email_parts[1]
        or email_parts[1].startswith(".")
        or email_parts[1].endswith(".")
    ):
        return ["O campo email deve ter um formato valido, como nome@dominio.com"]

    return []


def validate_especialidade(value: object) -> list[str]:
    if not remove_extra_spaces(value):
        return ["O campo especialidade nao pode ficar vazio."]

    return []


def validate_principal_desafio(value: object) -> list[str]:
    if not remove_extra_spaces(value):
        return ["O campo principal_desafio nao pode ficar vazio."]

    return []


def validate_payload(payload: object) -> list[str]:
    """Retorna todos os erros de validacao encontrados no payload."""
    if not isinstance(payload, Mapping):
        return ["O payload deve ser um objeto JSON."]

    errors = validate_required_fields(payload)

    if "nome" in payload:
        errors.extend(validate_nome(payload.get("nome")))

    if "telefone" in payload:
        errors.extend(validate_telefone(payload.get("telefone")))

    if "email" in payload:
        errors.extend(validate_email(payload.get("email")))

    if "especialidade" in payload:
        errors.extend(validate_especialidade(payload.get("especialidade")))

    if "principal_desafio" in payload:
        errors.extend(validate_principal_desafio(payload.get("principal_desafio")))

    return errors
