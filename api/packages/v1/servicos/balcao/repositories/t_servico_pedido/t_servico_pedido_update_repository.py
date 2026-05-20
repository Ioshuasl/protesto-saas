from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoUpdateSchema,
)


class TServicoPedidoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_update_schema: TServicoPedidoUpdateSchema):
        """
        Atualiza um registro existente na tabela T_SERVICO_PEDIDO.

        Args:
            t_servico_pedido_update_schema (TServicoPedidoUpdateSchema):
                Esquema contendo os dados a serem atualizados.

        Returns:
            O registro atualizado (via RETURNING *).

        Raises:
            HTTPException: Caso ocorra um erro na execução do SQL.
        """
        try:
            # ----------------------------------------------------
            # Prepara parâmetros e colunas de atualização dinâmicas
            # ----------------------------------------------------
            params, update_columns = prepare_update_data(
                t_servico_pedido_update_schema,
                exclude_fields=["servico_pedido_id", "itens", "operacao"],
                id_field="servico_pedido_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_SERVICO_PEDIDO
                SET {update_columns}
                WHERE SERVICO_PEDIDO_ID = :servico_pedido_id
                RETURNING *;
            """

            # ----------------------------------------------------
            # Execução e retorno do registro atualizado
            # ----------------------------------------------------
            response = self.run_and_return(sql, params)
            return response

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de exceção e retorno HTTP padronizado
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em T_SERVICO_PEDIDO: {str(e)}",
            )
