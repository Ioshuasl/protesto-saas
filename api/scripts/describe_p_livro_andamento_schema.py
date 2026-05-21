#!/usr/bin/env python3
"""
Debug P_LIVRO_ANDAMENTO via QueryInterface (orm-firebird-py).

Uso (na pasta api/, com USE_ORM_FIREBIRD=true no .env):
  python3 scripts/describe_p_livro_andamento_schema.py
  python3 scripts/describe_p_livro_andamento_schema.py --limit 10
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.orm_firebird import describe_table_schema, get_orm
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.index import register_administrativo_associations
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model


def _print_schema(table: str) -> None:
    from database.orm_firebird import get_query_interface

    qi = get_query_interface()
    print(f"\n=== {table} (exists={qi.table_exists(table)}) ===")
    if not qi.table_exists(table):
        return
    schema = describe_table_schema(table)
    print(json.dumps(schema, indent=2, default=str))


def _sample(model, pk: str, limit: int) -> list[dict]:
    return model.findAll({"limit": limit, "order": [(pk, "DESC")]})


def _counter(rows: list[dict], field: str) -> Counter:
    return Counter(
        (None if row.get(field) is None else str(row.get(field)).strip())
        for row in rows
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if not use_orm_firebird():
        print("USE_ORM_FIREBIRD=false — ative no .env para introspectar via ORM.")
        return 1

    _print_schema("P_LIVRO_ANDAMENTO")

    get_p_livro_andamento_model()
    register_administrativo_associations()

    orm = get_orm()
    andamento = orm.models["P_LIVRO_ANDAMENTO"]
    rows = _sample(andamento, "DATA_ABERTURA", args.limit)

    print(f"\n=== P_LIVRO_ANDAMENTO amostra (limit={args.limit}, rows={len(rows)}) ===")
    for row in rows:
        print(json.dumps(row, default=str, ensure_ascii=False))

    abertos = sum(1 for r in rows if r.get("DATA_FECHAMENTO") is None)
    print(f"  abertos na amostra (DATA_FECHAMENTO null): {abertos}/{len(rows)}")
    print(
        "  distinct LIVRO_NATUREZA_ID:",
        dict(_counter(rows, "LIVRO_NATUREZA_ID")),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
