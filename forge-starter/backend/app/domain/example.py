"""EXAMPLE domain (farm advisor) -- exists to show every extension point.
Replace with your own problem statement on hackathon day.
"""
from __future__ import annotations

from app.domain import Domain, Intent
from app.guardrails.validators import forbid_patterns, max_words, numeric_limit


def weather_stub(text: str) -> str:
    # Replace with a real API call (Open-Meteo is free, no key). Tools must never raise.
    return "Weather (stub): 31C, humidity 70%, 40% chance of rain tomorrow."


DOMAIN = Domain(
    name="example",
    title="KrishiMitra (example domain)",
    tagline="Practical farm advice, grounded in a knowledge base.",
    persona=(
        "You are an expert agricultural advisor for small Indian farmers. "
        "Be practical, specific and brief (max 5 short points). "
        "Use ONLY the provided CONTEXT for facts and numbers; if the context does not "
        "cover it, say you are not sure and suggest asking the local KVK / agriculture officer. "
        "Never invent scheme names, prices or dosages."
    ),
    intents=[
        Intent(
            "crop_advice",
            "questions about crops, soil, pests, diseases, irrigation, fertilizer",
            "Give step-by-step practical advice. Mention a low-cost organic option first.",
            ["crop", "soil", "pest", "disease", "leaf", "irrigat", "fertili", "seed"],
        ),
        Intent(
            "scheme_info",
            "government schemes, subsidies, loans, insurance eligibility",
            "State eligibility, benefit and how to apply. Cite the source file name.",
            ["scheme", "subsidy", "loan", "insurance", "pm-kisan", "kcc"],
        ),
        Intent(
            "weather_plan",
            "what to do given weather, rain, heat, sowing or harvest timing",
            "Use the WEATHER tool output to recommend actions for the next 2-3 days.",
            ["weather", "rain", "forecast", "heat", "monsoon", "when to sow"],
        ),
        Intent("general", "anything else / greetings / small talk", "Answer briefly and steer back to farming."),
    ],
    validators=[
        # Hard limits live in code, not in the prompt (see docs/ARCHITECTURE.md > Guardrails)
        numeric_limit("pesticide dose", r"([\d.]+)\s*(?:ml|g)\s*(?:per|/)\s*(?:litre|liter|l)\b", hi=5, unit=" per litre"),
        forbid_patterns({r"\b(banned|endosulfan|monocrotophos)\b.*\b(use|apply|spray)\b": "Recommends a banned pesticide."}),
        max_words(160),
    ],
    safe_fallback=(
        "I want to be careful here. Please confirm with your local Krishi Vigyan Kendra (KVK) or "
        "agriculture officer before applying anything. I can share general guidance if you tell me more."
    ),
    suggested_prompts=[
        "My tomato leaves have brown spots. What should I do?",
        "Am I eligible for PM-KISAN?",
        "Will rain tomorrow affect my wheat sowing?",
    ],
    languages={"en": "English", "hi": "हिन्दी", "mr": "मराठी", "ta": "தமிழ்", "te": "తెలుగు", "bn": "বাংলা"},
    tools={"weather": weather_stub},
    intent_tools={"weather_plan": ["weather"]},
)
