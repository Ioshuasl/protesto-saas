from __future__ import annotations

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencia_andamento import (
    get_p_ocorrencia_andamento_model,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)


class DeleteRepository(BaseRepository):
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(ocorrencia_andamento_schema)
        return self._execute_sql(ocorrencia_andamento_schema)

    @staticmethod
    def _execute_orm(
        ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema,
    ) -> dict[str, int]:
        get_p_ocorrencia_andamento_model().destroy(
            {
                "where": {
                    "OCORRENCIA_ANDAMENTO_ID": ocorrencia_andamento_schema.ocorrencia_andamento_id
                }
            }
        )
        return {
            "ocorrencia_andamento_id": ocorrencia_andamento_schema.ocorrencia_andamento_id
        }

    def _execute_sql(
        self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema
    ) -> dict[str, int]:
        sql = """
        DELETE FROM P_OCORRENCIA_ANDAMENTO
        WHERE OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id
        """
        self.run(
            sql,
            {
                "ocorrencia_andamento_id": ocorrencia_andamento_schema.ocorrencia_andamento_id
            },
        )
        return {
            "ocorrencia_andamento_id": ocorrencia_andamento_schema.ocorrencia_andamento_id
        }
