"""THE ONLY PLACE A HACKATHON TEAM SHOULD NEED TO EDIT FOR A NEW PROBLEM.

A Domain bundles: persona, intents (router labels), hard-limit validators,
safe fallback, suggested prompts, UI languages. Everything else (LLM client,
memory, orchestrator, API, UI) is domain-agnostic.

Copy `example.py` -> `<yourdomain>.py`, set DOMAIN=<yourdomain> in .env.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Callable

from app.core.config import get_settings
from app.guardrails.validators import Validator


@dataclass
class Intent:
    name: str
    description: str  # shown to the router LLM; also used for keyword fallback
    instructions: str  # extra system instructions when this intent is chosen
    keywords: list[str] = field(default_factory=list)


@dataclass
class Domain:
    name: str
    title: str
    tagline: str
    persona: str  # system prompt core
    intents: list[Intent]
    validators: list[Validator]
    safe_fallback: str
    suggested_prompts: list[str]
    languages: dict[str, str] = field(default_factory=lambda: {"en": "English"})
    # Optional tools: name -> callable(text:str)->str, run before the specialist
    tools: dict[str, Callable[[str], str]] = field(default_factory=dict)
    intent_tools: dict[str, list[str]] = field(default_factory=dict)  # intent -> tool names


def load_domain() -> Domain:
    mod = importlib.import_module(f"app.domain.{get_settings().domain}")
    return mod.DOMAIN
