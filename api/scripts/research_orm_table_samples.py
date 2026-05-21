#!/usr/bin/env python3
"""
Amostras e contagens via orm-firebird-py para validar cardinalidades de associações.

Uso (na pasta api/, USE_ORM_FIREBIRD=true no .env):
  python3 scripts/research_orm_table_samples.py
  python3 scripts/research_orm_table_samples.py --table G_CIDADE --limit 10
  python3 scripts/research_orm_table_samples.py --fk P_PESSOA ESTADO_CIVIL_ID G_TB_ESTADOCIVIL
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from abstracts.repository import BaseRepository
from database.orm_firebird import describe_table_schema, get_orm
from database.orm_firebird_settings import use_orm_firebird


class _SqlCounter(BaseRepository):
    def count_where(self, table: str, column: str, value) -> int:
        sql = f"""
        SELECT COUNT(*) AS TOTAL
        FROM {table}
        WHERE {column} = :value
        """
        row = self.fetch_one(sql, {"value": value})
        if not row:
            return 0
        total = row.get("TOTAL") or row.get("total") or 0
        return int(total)


DEFAULT_TABLES = (
    "G_TB_ESTADOCIVIL",
    "G_TB_PROFISSAO",
    "G_CIDADE",
)


def sample_table(table: str, limit: int) -> None:
    orm = get_orm()
    model = orm.models.get(table)
    if model is None:
        print(f"[{table}] model não definido — chame get_*_model() antes ou registre no ORM.")
        return

    pk = getattr(model, "primaryKey", None) or table
    rows = model.findAll({"limit": limit, "order": [(pk, "ASC")]})
    print(f"\n=== {table} (limit={limit}, rows={len(rows)}) ===")
    for row in rows:
        print(json.dumps(row, default=str, ensure_ascii=False))


def count_fk_usage(
    child_table: str,
    child_fk: str,
    parent_table: str,
    parent_pk: str,
    sample_parents: int = 5,
) -> None:
    orm = get_orm()
    child = orm.models.get(child_table)
    parent = orm.models.get(parent_table)
    if child is None or parent is None:
        print("Models não encontrados:", child_table, parent_table)
        return

    parents = parent.findAll(
        {"limit": sample_parents, "order": [(parent_pk, "ASC")]}
    )
    print(
        f"\n=== FK {child_table}.{child_fk} -> {parent_table}.{parent_pk} "
        f"(amostra {sample_parents} pais) ==="
    )
    for parent_row in parents:
        parent_id = parent_row.get(parent_pk)
        if parent_id is None:
            continue
        total = _SqlCounter().count_where(child_table, child_fk, parent_id)
        print(
            f"  {parent_table}.{parent_pk}={parent_id} "
            f"desc={parent_row.get('DESCRICAO') or parent_row.get('CIDADE_NOME')} "
            f"-> {child_table} count={total}"
        )


def print_schema(table: str) -> None:
    schema = describe_table_schema(table)
    print(f"\n=== schema {table} ({len(schema.get('columns', []))} cols) ===")
    for col in schema.get("columns", []):
        print(
            f"  {col['column_name']}: {col['data_type']}({col.get('length')}) "
            f"nullable={col['nullable']}"
        )
    fks = [
        fk
        for fk in schema.get("foreign_keys", [])
        if fk.get("child_table") == table or fk.get("parent_table") == table
    ]
    if fks:
        print("  FKs relevantes:")
        for fk in fks[:15]:
            print(
                f"    {fk.get('child_table')}.{fk.get('child_field')} -> "
                f"{fk.get('parent_table')}.{fk.get('parent_field')}"
            )


def main() -> int:
    if not use_orm_firebird():
        print("USE_ORM_FIREBIRD=false — ative no .env.")
        return 1

    parser = argparse.ArgumentParser(description="Pesquisa ORM com limites")
    parser.add_argument("--table", action="append", help="Tabela para amostra")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--schema", action="append", help="Só imprimir describe_table")
    parser.add_argument(
        "--fk",
        nargs=4,
        metavar=("CHILD", "CHILD_FK", "PARENT", "PARENT_PK"),
        action="append",
        help="Contar filhos por FK (ex.: P_PESSOA ESTADO_CIVIL_ID G_TB_ESTADOCIVIL TB_ESTADOCIVIL_ID)",
    )
    args = parser.parse_args()

    # Garante models + associações carregados
    from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
    from packages.v1.administrativo.model.g_tb_estadocivil import (
        get_g_tb_estadocivil_model,
    )
    from packages.v1.administrativo.model.g_tb_profissao import get_g_tb_profissao_model
    from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model

    get_g_tb_estadocivil_model()
    get_g_tb_profissao_model()
    get_g_cidade_model()
    get_p_pessoa_model()

    for table in args.schema or []:
        print_schema(table.upper())

    tables = args.table or list(DEFAULT_TABLES)
    for table in tables:
        print_schema(table.upper())
        sample_table(table.upper(), args.limit)

    fk_checks = args.fk or [
        ["P_PESSOA", "ESTADO_CIVIL_ID", "G_TB_ESTADOCIVIL", "TB_ESTADOCIVIL_ID"],
        ["P_PESSOA", "PROFISSAO_ID", "G_TB_PROFISSAO", "TB_PROFISSAO_ID"],
        ["P_PESSOA", "CIDADE_ID", "G_CIDADE", "CIDADE_ID"],
    ]
    for child, child_fk, parent, parent_pk in fk_checks:
        count_fk_usage(child, child_fk, parent, parent_pk, sample_parents=args.limit)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
