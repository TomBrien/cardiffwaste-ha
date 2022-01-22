"""Helpers for the cardiffwaste integration."""
from __future__ import annotations


def redact_uprn(uprn: str | int) -> str:
    """Redact all but the last 4 digits of a UPRN."""
    if isinstance(uprn, int):
        uprn = str(uprn)
    if len(uprn) == 1:
        return uprn
    if len(uprn) < 5:
        return "x" + uprn[1:]
    return "x" * len(uprn[:-4]) + uprn[-4:]
