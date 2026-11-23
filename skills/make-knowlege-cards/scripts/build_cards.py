#!/usr/bin/env python3
"""Build a knowledge-card deck (HTML, optional Markdown) from a JSON file.

Usage:
    python build_cards.py cards.json -o cards.html [--md cards.md]

Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "deck-template.html"

REQUIRED = ("title", "knowledge")
OPTIONAL = ("introduction", "example")
SOFT_LIMITS = {"title": 60, "knowledge": 240, "introduction": 500, "example": 400}
MIN_CARDS, MAX_CARDS = 5, 8

LABELS = {
    "en": {"knowledge": "Main knowledge", "introduction": "Introduction", "example": "Example", "source": "Source"},
    "de": {"knowledge": "Kernwissen", "introduction": "Einführung", "example": "Beispiel", "source": "Quelle"},
    "zh": {"knowledge": "核心知识", "introduction": "介绍", "example": "示例", "source": "来源"},
}


def labels_for(deck):
    return LABELS.get(str(deck.get("lang", "en"))[:2].lower(), LABELS["en"])


def validate(deck):
    """Return (errors, warnings, notes) for a deck."""
    errors, warnings, notes = [], [], []

    if not isinstance(deck, dict):
        return ["The top level must be a JSON object."], warnings, notes
    if not isinstance(deck.get("title"), str) or not deck["title"].strip():
        errors.append("Deck needs a non-empty 'title'.")
    if "source" in deck and (not isinstance(deck["source"], str) or not deck["source"].strip()):
        errors.append("'source' must be a non-empty string; omit it if unknown.")
    cards = deck.get("cards")
    if not isinstance(cards, list) or not cards:
        errors.append("Deck needs a non-empty 'cards' list.")
        return errors, warnings, notes

    examples = {}
    for i, card in enumerate(cards, 1):
        where = f"Card {i}"
        if not isinstance(card, dict):
            errors.append(f"{where}: must be an object.")
            continue
        if isinstance(card.get("title"), str) and card["title"].strip():
            where = f"Card {i} ({card['title'][:30]})"

        for field in REQUIRED:
            if not isinstance(card.get(field), str) or not card[field].strip():
                errors.append(f"{where}: needs a non-empty '{field}'.")
        for field in OPTIONAL:
            if field in card and (not isinstance(card[field], str) or not card[field].strip()):
                errors.append(f"{where}: '{field}' is empty or not a string; omit the field instead.")
        unknown = sorted(set(card) - set(REQUIRED) - set(OPTIONAL))
        if unknown:
            warnings.append(f"{where}: unknown field(s) ignored: {', '.join(unknown)}.")

        for field, limit in SOFT_LIMITS.items():
            if isinstance(card.get(field), str) and len(card[field]) > limit:
                hint = " One piece of information per card." if field == "knowledge" else ""
                warnings.append(f"{where}: '{field}' is longer than {limit} characters.{hint}")

        example = card.get("example")
        if isinstance(example, str) and example.strip():
            key = " ".join(example.lower().split())
            if key in examples:
                warnings.append(f"{where}: same example as card {examples[key]}; do not reuse examples.")
            else:
                examples[key] = i

    if len(cards) > MAX_CARDS:
        warnings.append(f"{len(cards)} cards; the target is {MIN_CARDS}-{MAX_CARDS}. Keep the most important ones.")
    elif len(cards) < MIN_CARDS:
        notes.append(f"{len(cards)} card(s); fine if the article holds no more important information.")
    return errors, warnings, notes


def render_html(deck):
    template = TEMPLATE.read_text(encoding="utf-8")
    payload = dict(deck, labels=labels_for(deck))
    # Keep the JSON inert inside the <script> element.
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return (
        template.replace("__LANG__", html.escape(str(deck.get("lang", "en")), quote=True))
        .replace("__TITLE__", html.escape(deck["title"]))
        .replace("__DECK_JSON__", data)
    )


def render_markdown(deck):
    lab = labels_for(deck)
    out = [f"# {deck['title']}", ""]
    if deck.get("source"):
        out += [f"{lab['source']}: {deck['source']}", ""]
    for i, card in enumerate(deck["cards"], 1):
        out += [f"## {i}. {card['title']}", "", f"**{lab['knowledge']}:** {card['knowledge']}", ""]
        for field in OPTIONAL:
            if card.get(field):
                out += [f"**{lab[field]}:** {card[field]}", ""]
    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build a knowledge-card deck from JSON.")
    parser.add_argument("deck", help="Path to the deck JSON file")
    parser.add_argument("-o", "--output", default="cards.html", help="HTML output path (default: cards.html)")
    parser.add_argument("--md", help="Also write the deck as Markdown to this path")
    args = parser.parse_args(argv)

    try:
        deck = json.loads(Path(args.deck).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {args.deck}: {exc}", file=sys.stderr)
        return 1

    errors, warnings, notes = validate(deck)
    for n in notes:
        print(f"Note: {n}", file=sys.stderr)
    for w in warnings:
        print(f"Warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    Path(args.output).write_text(render_html(deck), encoding="utf-8")
    written = [args.output]
    if args.md:
        Path(args.md).write_text(render_markdown(deck), encoding="utf-8")
        written.append(args.md)

    print(f"{len(deck['cards'])} cards -> {', '.join(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
