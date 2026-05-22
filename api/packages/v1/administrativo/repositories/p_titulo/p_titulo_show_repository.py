from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.repositories.p_titulo.p_titulo_orm_helpers import (
    _TITULO_SHOW_INCLUDES,
    attach_pessoa_vinculos,
)
from packages.v1.administrativo.repositories.p_titulo.p_titulo_selos_repository import (
    SelosRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    map_titulo_row,
)


class ShowRepository(BaseRepository):
    def execute(self, titulo_schema: PTituloIdSchema) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(titulo_schema)
        return self._execute_sql(titulo_schema)

    def _execute_orm(self, titulo_schema: PTituloIdSchema) -> Optional[dict[str, Any]]:
        row = get_p_titulo_model().findOne(
            {
                "where": {"TITULO_ID": titulo_schema.titulo_id},
                "include": _TITULO_SHOW_INCLUDES,
            }
        )
        mapped = map_titulo_row(row)
        if mapped is None:
            return None
        attach_pessoa_vinculos(mapped, [titulo_schema.titulo_id])
        mapped["andamentos"] = self._load_andamentos_with_ocorrencia(
            titulo_schema.titulo_id
        )
        mapped["vinculos_selos"] = SelosRepository().execute(titulo_schema)
        return mapped

    @staticmethod
    def _load_andamentos_with_ocorrencia(titulo_id: int) -> list[dict[str, Any]]:
        rows = get_p_andamento_model().findAll(
            {
                "where": {"TITULO_ID": titulo_id},
                "include": [
                    {
                        "association": "ocorrencia_andamento",
                        "required": False,
                        "attributes": [
                            "OCORRENCIA_ANDAMENTO_ID",
                            "CODIGO",
                            "DESCRICAO",
                        ],
                    }
                ],
                "order": [("ANDAMENTO_ID", "DESC")],
            }
        )
        from packages.v1.administrativo.schemas.p_titulo_schema import (
            _map_andamento_item,
        )

        return [_map_andamento_item(item) for item in rows if item is not None]

    def _execute_sql(self, titulo_schema: PTituloIdSchema) -> Optional[dict[str, Any]]:
        sql = """
        SELECT *
        FROM P_TITULO
        WHERE TITULO_ID = :titulo_id
        """
        row = self.fetch_one(sql, {"titulo_id": titulo_schema.titulo_id})
        mapped = map_titulo_row(row)
        if mapped is None:
            return None

        self._attach_nested_relations_sql(mapped, titulo_schema.titulo_id)
        attach_pessoa_vinculos(mapped, [titulo_schema.titulo_id])
        mapped["andamentos"] = self._load_andamentos_with_ocorrencia(
            titulo_schema.titulo_id
        )
        mapped["vinculos_selos"] = SelosRepository().execute(titulo_schema)
        return mapped

    def _attach_nested_relations_sql(
        self, mapped: dict[str, Any], titulo_id: int
    ) -> None:
        """FKs aninhadas no ramo SQL (paridade com includes do ORM)."""
        ocorrencia_id = mapped.get("ocorrencia_id")
        if ocorrencia_id is not None:
            row = self.fetch_one(
                """
                SELECT OCORRENCIAS_ID, CODIGO, DESCRICAO, TIPO
                FROM P_OCORRENCIAS
                WHERE OCORRENCIAS_ID = :ocorrencia_id
                """,
                {"ocorrencia_id": ocorrencia_id},
            )
            mapped["ocorrencia"] = self._normalize_nested_row(row, "ocorrencias_id")

        oa_id = mapped.get("ocorrencia_andamento_id")
        if oa_id is not None:
            row = self.fetch_one(
                """
                SELECT OCORRENCIA_ANDAMENTO_ID, CODIGO, DESCRICAO
                FROM P_OCORRENCIA_ANDAMENTO
                WHERE OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id
                """,
                {"ocorrencia_andamento_id": oa_id},
            )
            mapped["ocorrencia_andamento"] = self._normalize_nested_row(
                row, "ocorrencia_andamento_id"
            )

        especie_id = mapped.get("especie_id")
        if especie_id is not None:
            row = self.fetch_one(
                """
                SELECT ESPECIE_ID, ESPECIE, DESCRICAO
                FROM P_ESPECIE
                WHERE ESPECIE_ID = :especie_id
                """,
                {"especie_id": especie_id},
            )
            mapped["especie"] = self._normalize_nested_row(row, "especie_id")

        banco_id = mapped.get("banco_id")
        if banco_id is not None:
            row = self.fetch_one(
                """
                SELECT BANCO_ID, CODIGO_BANCO, DESCRICAO
                FROM P_BANCO
                WHERE BANCO_ID = :banco_id
                """,
                {"banco_id": banco_id},
            )
            mapped["banco"] = self._normalize_nested_row(row, "banco_id")

        motivo_apontamento_id = mapped.get("motivo_apontamento_id")
        if motivo_apontamento_id is not None:
            row = self.fetch_one(
                """
                SELECT MOTIVOS_ID, DESCRICAO
                FROM P_MOTIVOS
                WHERE MOTIVOS_ID = :motivos_id
                """,
                {"motivos_id": motivo_apontamento_id},
            )
            nested = self._normalize_nested_row(row, "motivos_id")
            if nested is not None:
                mapped["motivo_apontamento"] = nested

        motivo_cancelamento_id = mapped.get("motivo_cancelamento")
        if motivo_cancelamento_id is not None:
            row = self.fetch_one(
                """
                SELECT MOTIVOS_CANCELAMENTO_ID, DESCRICAO
                FROM P_MOTIVOS_CANCELAMENTO
                WHERE MOTIVOS_CANCELAMENTO_ID = :motivos_cancelamento_id
                """,
                {"motivos_cancelamento_id": motivo_cancelamento_id},
            )
            nested = self._normalize_nested_row(row, "motivos_cancelamento_id")
            if nested is not None:
                mapped["motivo_cancelamento"] = nested

    @staticmethod
    def _normalize_nested_row(
        row: Optional[Mapping[str, Any]], pk_key: str
    ) -> Optional[dict[str, Any]]:
        if row is None:
            return None
        nested = normalize_row_keys(row)
        if nested is None:
            return None
        pk_val = nested.get(pk_key)
        if isinstance(pk_val, Decimal):
            nested[pk_key] = int(pk_val)
        return nested
