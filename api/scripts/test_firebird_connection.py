#!/usr/bin/env python3
"""
Testa conectividade com o Firebird usando as variáveis do api/.env.

Uso (na pasta api/):
  source venv/bin/activate
  python3 scripts/test_firebird_connection.py

  # ou sem ativar o venv:
  ./venv/bin/python3 scripts/test_firebird_connection.py
"""

from __future__ import annotations

import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_PYTHON = ROOT / "venv" / "bin" / "python3"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from sqlalchemy import text
except ModuleNotFoundError as exc:
    print("Erro: dependências do projeto não estão disponíveis neste Python.")
    print(f"  Python em uso: {sys.executable}")
    print(f"  Detalhe: {exc}")
    print()
    print("As bibliotecas (sqlalchemy, orm-py, etc.) estão instaladas apenas no venv.")
    print("Opções:")
    print("  cd api && source venv/bin/activate && python3 scripts/test_firebird_connection.py")
    if VENV_PYTHON.exists():
        print("  cd api && ./venv/bin/python3 scripts/test_firebird_connection.py")
    else:
        print("  cd api && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt")
    raise SystemExit(1) from exc

from actions.env.env_config_loader import EnvConfigLoader
from database.firebird import Firebird
from database.firebird_host import collect_local_ipv4_addresses, resolve_firebird_host
from database.orm_firebird import _build_connection_config
from database.orm_firebird_settings import use_orm_firebird


def _mask_password(value: str | None) -> str:
    if not value:
        return "(vazio)"
    if len(value) <= 2:
        return "***"
    return f"{value[0]}***{value[-1]}"


def _print_env_summary() -> None:
    env = EnvConfigLoader(".env")
    configured_host = getattr(env, "ORIUS_API_FDB_HOST", "")
    resolved_host = resolve_firebird_host(configured_host)

    print("=== Configuração (api/.env) ===")
    print(f"  ORIUS_API_FDB_HOST          : {configured_host}")
    if resolved_host != (configured_host or "").strip():
        print(f"  host resolvido (local)      : {resolved_host}")
    print(f"  ORIUS_API_FDB_PORT          : {getattr(env, 'ORIUS_API_FDB_PORT', '')}")
    print(f"  ORIUS_API_FDB_NAME          : {getattr(env, 'ORIUS_API_FDB_NAME', '')}")
    print(f"  ORIUS_API_FDB_USER          : {getattr(env, 'ORIUS_API_FDB_USER', '')}")
    print(
        f"  ORIUS_API_FDB_PASSWORD      : {_mask_password(getattr(env, 'ORIUS_API_FDB_PASSWORD', None))}"
    )
    print(f"  ORIUS_API_FDB_CHARSET       : {getattr(env, 'ORIUS_API_FDB_CHARSET', '')}")
    print(f"  USE_ORM_FIREBIRD            : {use_orm_firebird()}")
    print(f"  IPs locais detectados       : {', '.join(sorted(collect_local_ipv4_addresses()))}")
    print()


def _test_tcp(host: str, port: int, timeout: float = 3.0) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True, f"TCP OK em {host}:{port}"
    except OSError as exc:
        return False, f"TCP falhou em {host}:{port} — {exc}"


def _test_sqlalchemy() -> tuple[bool, str]:
    try:
        engine = Firebird.get_engine()
        with engine.connect() as conn:
            row = conn.execute(text("SELECT 1 AS OK FROM RDB$DATABASE")).scalar_one()
        Firebird.dispose()
        return True, f"SQLAlchemy (Firebird.get_engine) OK — SELECT 1 = {row}"
    except Exception as exc:
        Firebird.dispose()
        return False, f"SQLAlchemy falhou — {type(exc).__name__}: {exc}"


def _test_orm() -> tuple[bool, str]:
    from database.orm_firebird import _dispose_orm_singleton, get_orm

    try:
        _dispose_orm_singleton()
        orm = get_orm()
        conn = orm.get_connection()
        rows = conn.execute("SELECT 1 AS OK FROM RDB$DATABASE")
        first = rows[0] if rows else {}
        value = first.get("OK", first.get("ok"))
        _dispose_orm_singleton()
        return True, f"ORM (orm-firebird-py) OK — SELECT 1 = {value}"
    except Exception as exc:
        _dispose_orm_singleton()
        return False, f"ORM falhou — {type(exc).__name__}: {exc}"


def main() -> int:
    _print_env_summary()

    cfg = _build_connection_config()
    host = str(cfg["host"])
    port = int(cfg["port"])

    results: list[tuple[str, bool, str]] = []

    ok_tcp, msg_tcp = _test_tcp(host, port)
    results.append(("Porta Firebird", ok_tcp, msg_tcp))
    print(f"[{'OK' if ok_tcp else 'ERRO'}] {msg_tcp}")

    ok_sql, msg_sql = _test_sqlalchemy()
    results.append(("SQLAlchemy", ok_sql, msg_sql))
    print(f"[{'OK' if ok_sql else 'ERRO'}] {msg_sql}")

    if use_orm_firebird():
        ok_orm, msg_orm = _test_orm()
        results.append(("ORM Firebird", ok_orm, msg_orm))
        print(f"[{'OK' if ok_orm else 'ERRO'}] {msg_orm}")
    else:
        print("[SKIP] USE_ORM_FIREBIRD=false — teste ORM não executado")

    print()
    failures = [name for name, ok, _ in results if not ok]
    if failures:
        print(f"Resultado: FALHA ({len(failures)} de {len(results)} teste(s) com erro)")
        return 1

    print(f"Resultado: SUCESSO ({len(results)} teste(s) passaram)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
