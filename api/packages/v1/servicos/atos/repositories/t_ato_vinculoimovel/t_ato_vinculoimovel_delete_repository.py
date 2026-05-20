from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIdSchema,
)


class TAtoVinculoImovelDeleteRepository(BaseRepository):

    def execute(self, t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema):

        try:
            # ----------------------------------------------------
            # Busca ATO_ID via T_ATO_VINCULOIMOVEL
            # ----------------------------------------------------
            sql_get_ato_id = """
                SELECT FIRST 1 TA.ATO_ID
                FROM T_ATO_VINCULOIMOVEL TA
                WHERE TA.ATO_VINCULOIMOVEL_ID = :ato_vinculoimovel_id
            """

            params = {
                "ato_vinculoimovel_id": t_ato_vinculoimovel_id_schema.ato_vinculoimovel_id
            }

            result_ato_id = self.fetch_one(sql_get_ato_id, params)
            # O driver pode retornar chaves em minúsculo ou maiúsculo.
            # Por isso, tentamos ambas as variações.
            _ato_id = (
                result_ato_id.get("ATO_ID")
                if result_ato_id and "ATO_ID" in result_ato_id
                else result_ato_id.get("ato_id") if result_ato_id else None
            )

            if _ato_id is None or _ato_id == 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Não é possível excluir o imóvel, nenhum ato localizado para esta solicitação.",
                )

            # ----------------------------------------------------
            # Checa dependência em T_ATO_VINCULOVALOR
            # ----------------------------------------------------
            sql_check_vinculovalor = """
                SELECT FIRST 1 1 AS EXISTE
                FROM T_ATO_VINCULOVALOR TAV
                WHERE TAV.ATO_VINCULOIMOVEL_ID = :ato_vinculoimovel_id
                  AND TAV.ATO_ID = :ato_id
            """

            params_check = {
                "ato_vinculoimovel_id": t_ato_vinculoimovel_id_schema.ato_vinculoimovel_id,
                "ato_id": _ato_id,
            }

            result_check = self.fetch_one(sql_check_vinculovalor, params_check)
            if result_check:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Não é possível excluir o imóvel, primeiro exclua o emolumento correspondente ao mesmo.",
                )

            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO_VINCULOIMOVEL TA
                WHERE TA.ATO_VINCULOIMOVEL_ID = :ato_vinculoimovel_id
                RETURNING ato_vinculoimovel_id
            """

            # Preenchimento dos parâmetros
            # (reaproveita `params` já preenchido acima)

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except HTTPException:
            # Não mascarar validações/erros HTTP
            raise
        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_ATO_VINCULOIMOVEL: {e}",
            )
