#!/usr/bin/env python3
"""
Executa findAll e count para models do pacote administrativo.

Uso (na pasta api/, com USE_ORM_FIREBIRD=true no .env):
  python3 scripts/research_administrativo_models_findall_count.py
  python3 scripts/research_administrativo_models_findall_count.py --model g_emolumento --model g_selo_livro
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ModelLoader = Callable[[], Any]

MODEL_NAMES = (
    "g_emolumento",
    "g_emolumento_item",
    "g_sistema",
    "g_selo_grupo",
    "g_selo_livro",
    "g_selo_lote",
)
FIND_ALL_LIMIT = 20


def _as_int(value: Any) -> int:
    if isinstance(value, dict):
        for key in ("count", "COUNT", "total", "TOTAL"):
            if key in value:
                return _as_int(value[key])
        return 0
    if isinstance(value, Decimal):
        return int(value)
    return int(value or 0)


def _build_model_loaders() -> dict[str, ModelLoader]:
    from packages.v1.administrativo.model.g_emolumento import get_g_emolumento_model
    from packages.v1.administrativo.model.g_emolumento_item import (
        get_g_emolumento_item_model,
    )
    from packages.v1.administrativo.model.g_selo_grupo import get_g_selo_grupo_model
    from packages.v1.administrativo.model.g_selo_livro import get_g_selo_livro_model
    from packages.v1.administrativo.model.g_selo_lote import get_g_selo_lote_model
    from packages.v1.administrativo.model.g_sistema import get_g_sistema_model

    return {
        "g_emolumento": get_g_emolumento_model,
        "g_emolumento_item": get_g_emolumento_item_model,
        "g_sistema": get_g_sistema_model,
        "g_selo_grupo": get_g_selo_grupo_model,
        "g_selo_livro": get_g_selo_livro_model,
        "g_selo_lote": get_g_selo_lote_model,
    }


def _run_model(model_name: str, model_loaders: dict[str, ModelLoader]) -> None:
    loader = model_loaders[model_name]
    model = loader()

    table_name = getattr(model, "tableName", model_name.upper())
    primary_key = getattr(model, "primaryKey", None)

    find_options: dict[str, Any] = {"limit": FIND_ALL_LIMIT}
    if primary_key:
        find_options["order"] = [(primary_key, "DESC")]

    rows = model.findAll(find_options)
    total = _as_int(model.count({}))

    print(f"\n=== {model_name} ({table_name}) ===")
    print(f"count: {total}")
    print(f"findAll últimos {FIND_ALL_LIMIT}: {len(rows)} row(s)")

    for index, row in enumerate(rows, start=1):
        print(f"  row[{index}]: {json.dumps(row, default=str, ensure_ascii=False)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa count/findAll nos models administrativo selecionados."
    )
    parser.add_argument(
        "--model",
        action="append",
        choices=sorted(MODEL_NAMES),
        help="Model específico para executar (repetível).",
    )
    args = parser.parse_args()

    try:
        from database.orm_firebird_settings import use_orm_firebird

        model_loaders = _build_model_loaders()
    except ModuleNotFoundError as exc:
        print(f"Dependência ausente para executar o script: {exc}")
        print("Instale as dependências da API (ex.: python-dotenv) e tente novamente.")
        return 3

    if not use_orm_firebird():
        print("USE_ORM_FIREBIRD=false — ative no .env para consultar via ORM.")
        return 1

    selected_models = args.model or list(model_loaders.keys())
    print("Models alvo:", ", ".join(selected_models))

    for model_name in selected_models:
        _run_model(model_name, model_loaders)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
