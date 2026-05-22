#!/usr/bin/env python3
"""
Sincroniza api/Orius.postman_collection.json com a coleção no Postman (nuvem).

Variáveis de ambiente (carregadas de api/.env):
  POSTMAN_API_KEY          — obrigatória (Settings → API keys no Postman)
  POSTMAN_COLLECTION_UID   — opcional; UID da coleção (ex.: 12345678-uuid-...)
  POSTMAN_COLLECTION_FILE  — opcional; caminho do JSON (padrão: Orius.postman_collection.json)

Uso (na pasta api, com venv ativo se preferir):
  python scripts/sync_postman_collection.py              # envia uma vez
  python scripts/sync_postman_collection.py --watch      # observa o arquivo e reenvia ao salvar
  python scripts/sync_postman_collection.py --list     # lista coleções da conta
  python scripts/sync_postman_collection.py --dry-run    # só valida o JSON local
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_DIR = Path(__file__).resolve().parent.parent
DEFAULT_COLLECTION_FILE = API_DIR / "Orius.postman_collection.json"
POSTMAN_API_BASE = "https://api.getpostman.com"
DEBOUNCE_SECONDS = 1.5
POLL_INTERVAL_SECONDS = 0.75


class PostmanSyncError(Exception):
    pass


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_env() -> None:
    load_env_file(API_DIR / ".env")


def api_request(
    method: str,
    path: str,
    api_key: str,
    body: dict[str, Any] | None = None,
    timeout: int = 300,
) -> dict[str, Any]:
    url = f"{POSTMAN_API_BASE}{path}"
    data = None
    headers = {"X-Api-Key": api_key}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise PostmanSyncError(f"HTTP {exc.code} em {path}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise PostmanSyncError(f"Erro de rede em {path}: {exc}") from exc
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def read_collection(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise PostmanSyncError(f"Arquivo não encontrado: {path}")
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise PostmanSyncError(f"JSON inválido em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise PostmanSyncError("A coleção deve ser um objeto JSON.")
    if "info" not in data:
        raise PostmanSyncError('Coleção sem campo "info".')
    return data


def collection_name(data: dict[str, Any]) -> str:
    info = data.get("info") or {}
    name = info.get("name")
    return name if isinstance(name, str) and name.strip() else "Orius"


def list_collections(api_key: str) -> list[dict[str, Any]]:
    payload = api_request("GET", "/collections", api_key, timeout=120)
    collections = payload.get("collections")
    if not isinstance(collections, list):
        raise PostmanSyncError("Resposta inesperada ao listar coleções.")
    return collections


def resolve_collection_uid(
    api_key: str,
    data: dict[str, Any],
    explicit_uid: str | None,
) -> str:
    if explicit_uid:
        return explicit_uid.strip()

    name = collection_name(data)
    postman_id = (data.get("info") or {}).get("_postman_id")
    all_collections = list_collections(api_key)

    matches: list[dict[str, Any]] = []
    for entry in all_collections:
        entry_name = entry.get("name")
        entry_uid = entry.get("uid") or entry.get("id")
        if not isinstance(entry_uid, str):
            continue
        if entry_name == name:
            matches.append(entry)

    if len(matches) == 1:
        uid = matches[0].get("uid") or matches[0].get("id")
        if isinstance(uid, str):
            print(f'Coleção "{name}" → UID {uid}')
            return uid

    if len(matches) > 1:
        uids = [m.get("uid") or m.get("id") for m in matches]
        raise PostmanSyncError(
            f'Várias coleções com o nome "{name}". Defina POSTMAN_COLLECTION_UID. UIDs: {uids}'
        )

    if isinstance(postman_id, str):
        for entry in all_collections:
            entry_uid = entry.get("uid") or entry.get("id")
            if isinstance(entry_uid, str) and postman_id in entry_uid:
                print(f'Coleção encontrada por _postman_id → UID {entry_uid}')
                return entry_uid

    names = sorted(
        {e.get("name") for e in all_collections if isinstance(e.get("name"), str)}
    )
    raise PostmanSyncError(
        f'Coleção "{name}" não encontrada na conta. '
        f"Importe o JSON no Postman uma vez ou defina POSTMAN_COLLECTION_UID. "
        f"Coleções disponíveis: {', '.join(names) if names else '(nenhuma)'}"
    )


def put_collection(api_key: str, collection_uid: str, data: dict[str, Any]) -> dict[str, Any]:
    return api_request(
        "PUT",
        f"/collections/{collection_uid}",
        api_key,
        body={"collection": data},
        timeout=300,
    )


def file_fingerprint(path: Path) -> str:
    stat = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"{stat.st_mtime_ns}:{digest.hexdigest()}"


def sync_once(
    api_key: str,
    collection_path: Path,
    collection_uid: str | None,
    dry_run: bool,
) -> None:
    data = read_collection(collection_path)
    name = collection_name(data)
    size_kb = collection_path.stat().st_size / 1024

    if dry_run:
        print(f'[dry-run] JSON válido: "{name}" ({size_kb:.1f} KB) em {collection_path}')
        return

    uid = resolve_collection_uid(api_key, data, collection_uid)
    print(f'Enviando "{name}" ({size_kb:.1f} KB) → {uid} ...')
    result = put_collection(api_key, uid, data)
    updated = (result.get("collection") or {}).get("name") or name
    print(f"OK — coleção atualizada: {updated}")


def print_collection_list(api_key: str) -> None:
    rows = list_collections(api_key)
    if not rows:
        print("Nenhuma coleção encontrada nesta API key.")
        return
    print(f"{'UID':<50} {'Nome'}")
    print("-" * 80)
    for entry in sorted(rows, key=lambda item: (item.get("name") or "").lower()):
        uid = entry.get("uid") or entry.get("id") or "?"
        name = entry.get("name") or "?"
        print(f"{uid:<50} {name}")


def watch_and_sync(
    api_key: str,
    collection_path: Path,
    collection_uid: str | None,
    dry_run: bool,
) -> None:
    print(f"Observando {collection_path} (debounce {DEBOUNCE_SECONDS}s). Ctrl+C para sair.")
    last_sent_fingerprint: str | None = None
    pending_change_at: float | None = None
    pending_fingerprint: str | None = None

    while True:
        try:
            fingerprint = file_fingerprint(collection_path)
        except FileNotFoundError:
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        if fingerprint != last_sent_fingerprint:
            if pending_fingerprint != fingerprint:
                pending_fingerprint = fingerprint
                pending_change_at = time.monotonic()

            if (
                pending_change_at is not None
                and (time.monotonic() - pending_change_at) >= DEBOUNCE_SECONDS
            ):
                try:
                    sync_once(api_key, collection_path, collection_uid, dry_run)
                    last_sent_fingerprint = fingerprint
                except PostmanSyncError as exc:
                    print(f"Erro: {exc}", file=sys.stderr)
                pending_change_at = None
        else:
            pending_change_at = None
            pending_fingerprint = None

        time.sleep(POLL_INTERVAL_SECONDS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sincroniza Orius.postman_collection.json com o Postman."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help="Caminho do JSON da coleção (padrão: Orius.postman_collection.json na pasta api)",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Fica observando o arquivo e reenvia após cada salvamento",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista coleções da conta e encerra",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas valida o JSON local, sem chamar a API",
    )
    return parser.parse_args()


def main() -> int:
    load_env()
    args = parse_args()

    api_key = os.getenv("POSTMAN_API_KEY", "").strip()
    if not args.dry_run and not api_key:
        print(
            "Defina POSTMAN_API_KEY em api/.env (Postman → Settings → API keys).",
            file=sys.stderr,
        )
        return 1

    collection_path = args.file or Path(
        os.getenv("POSTMAN_COLLECTION_FILE", str(DEFAULT_COLLECTION_FILE))
    )
    if not collection_path.is_absolute():
        collection_path = (API_DIR / collection_path).resolve()

    collection_uid = os.getenv("POSTMAN_COLLECTION_UID", "").strip() or None

    try:
        if args.list:
            if not api_key:
                print("POSTMAN_API_KEY é obrigatória para --list.", file=sys.stderr)
                return 1
            print_collection_list(api_key)
            return 0

        if args.watch:
            watch_and_sync(api_key, collection_path, collection_uid, args.dry_run)
            return 0

        sync_once(api_key, collection_path, collection_uid, args.dry_run)
        return 0
    except PostmanSyncError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nEncerrado.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
