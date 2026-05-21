#!/usr/bin/env python3
"""describe_table G_TB_PROFISSAO — orm-firebird-py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database.orm_firebird import describe_table_schema
from database.orm_firebird_settings import use_orm_firebird


def main() -> int:
    if not use_orm_firebird():
        print("USE_ORM_FIREBIRD=false")
        return 1
    print(json.dumps(describe_table_schema("G_TB_PROFISSAO"), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
