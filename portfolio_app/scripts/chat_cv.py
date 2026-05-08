from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI

from portfolio_app.services.content import FRONTEND_CONTENT_PATH, GENERATED_DIR


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")


def _load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing context file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_context_bundle(
    *,
    ai_context_path: Path = GENERATED_DIR / "ai_context.json",
    resume_path: Path = GENERATED_DIR / "resume_snapshot.json",
    portfolio_path: Path = FRONTEND_CONTENT_PATH,
) -> dict[str, Any]:
    return {
        "ai_context": _load_json(ai_context_path),
        "resume_snapshot": _load_json(resume_path),
        "portfolio_content": _load_json(portfolio_path),
    }


def ask_cv_assistant(
    *,
    question: str,
    model: str,
    context_bundle: dict[str, Any],
    client: OpenAI | None = None,
) -> str:
    client = client or OpenAI()
    system_prompt = context_bundle["ai_context"].get(
        "system_prompt",
        "You are Mauricio's CV assistant. Answer from the provided context only.",
    )
    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=(
            f"Context bundle JSON:\n{json.dumps(context_bundle, indent=2)}\n\nQuestion: {question}"
        ),
    )
    return response.output_text.strip()


def _interactive_loop(model: str, context_bundle: dict[str, Any]) -> None:
    print("Mauricio CV assistant (CLI mode). Type 'exit' to stop.")
    while True:
        question = input("\nquestion> ").strip()
        if not question or question.lower() in {"exit", "quit"}:
            break
        answer = ask_cv_assistant(question=question, model=model, context_bundle=context_bundle)
        print(f"\n{answer}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask Mauricio's CV assistant locally using the OpenAI Responses API."
    )
    parser.add_argument("--question", help="Single question to answer. Omit for interactive mode.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name to use.")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required for portfolio_app.scripts.chat_cv")

    context_bundle = load_context_bundle()
    if args.question:
        print(
            ask_cv_assistant(
                question=args.question, model=args.model, context_bundle=context_bundle
            )
        )
        return

    _interactive_loop(model=args.model, context_bundle=context_bundle)


if __name__ == "__main__":
    main()
