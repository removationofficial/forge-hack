"""Deterministic guardrails. The LLM proposes, plain code disposes.

(Pattern from Demeter: `validate_hard_limits` + reject-with-critique loop.)
A validator takes the draft answer text and returns a list of violation strings.
Empty list == OK. Violations are fed back to the agent once as a critique; if it
still fails, the orchestrator returns the domain's safe fallback instead.
"""
from __future__ import annotations

import re
from typing import Callable

Validator = Callable[[str], list[str]]


def forbid_patterns(rules: dict[str, str]) -> Validator:
    """rules: {regex: message}. Flags any regex that matches (case-insensitive)."""
    compiled = [(re.compile(p, re.I), m) for p, m in rules.items()]

    def check(text: str) -> list[str]:
        return [m for rx, m in compiled if rx.search(text)]

    return check


def numeric_limit(label: str, pattern: str, lo: float | None = None, hi: float | None = None, unit: str = "") -> Validator:
    """Extract a number via regex group 1 and enforce a hard range.

    numeric_limit("pH", r"pH\\s*(?:of|to|=)?\\s*([\\d.]+)", 5.0, 7.5)
    """
    rx = re.compile(pattern, re.I)

    def check(text: str) -> list[str]:
        out = []
        for m in rx.finditer(text):
            try:
                v = float(m.group(1))
            except ValueError:
                continue
            if lo is not None and v < lo:
                out.append(f"{label}={v}{unit} is below the safe minimum {lo}{unit}.")
            if hi is not None and v > hi:
                out.append(f"{label}={v}{unit} is above the safe maximum {hi}{unit}.")
        return out

    return check


def max_words(n: int) -> Validator:
    def check(text: str) -> list[str]:
        w = len(text.split())
        return [f"Answer is {w} words; limit is {n}. Shorten it."] if w > n else []

    return check


def run_all(validators: list[Validator], text: str) -> list[str]:
    out: list[str] = []
    for v in validators:
        out.extend(v(text))
    return out
