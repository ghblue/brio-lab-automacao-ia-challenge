"""Schemas simples para os dados do diagnostico."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Diagnostico:
    """Representa um diagnostico ja validado e normalizado."""

    nome: str
    telefone: str
    email: str
    especialidade: str
    principal_desafio: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
