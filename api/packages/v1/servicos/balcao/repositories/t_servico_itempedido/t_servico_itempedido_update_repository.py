from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoUpdateSchema,
)


class TServicoItemPedidoUpdateRepository(BaseRepository):

    def execute(self, data: TServicoItemPedidoUpdateSchema):
        try:
            params, update_columns = prepare_update_data(
                data,
                exclude_fields=["servico_itempedido_id"],
                id_field="servico_itempedido_id",
            )
            sql = f"""
                    UPDATE T_SERVICO_ITEMPEDIDO
                    SET {update_columns}
                    WHERE SERVICO_ITEMPEDIDO_ID = :servico_itempedido_id
                    RETURNING *;
                """
            # Execução e retorno do registro atualizado
            return self.run_and_return(sql, params)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em T_SERVICO_ITEMPEDIDO: {str(e)}",
            )
