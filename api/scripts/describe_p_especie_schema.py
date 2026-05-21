#!/usr/bin/env python3
"""
Debug da tabela P_ESPECIE via QueryInterface (orm-firebird-py).

Uso (na pasta api/, com USE_ORM_FIREBIRD=true no .env):
  python3 scripts/describe_p_especie_schema.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.orm_firebird import describe_table_schema, get_query_interface
from database.orm_firebird_settings import use_orm_firebird


def main() -> int:
    if not use_orm_firebird():
        print("USE_ORM_FIREBIRD=false — ative no .env para introspectar via ORM.")
        return 1

    qi = get_query_interface()
    print("table_exists P_ESPECIE:", qi.table_exists("P_ESPECIE"))
    print(json.dumps(describe_table_schema("P_ESPECIE"), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
