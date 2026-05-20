from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoSituacaoSchema,
)


class TServicoPedidoSaveSituacaoRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_SERVICO_ITEMPEDIDO.
    """

    def execute(self, data: TServicoPedidoSituacaoSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_servico_itempedido_save_schema (TServicoItemPedidoSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = """ UPDATE T_SERVICO_PEDIDO TSP
                        SET TSP.SITUACAO = :situacao
                      WHERE
                        TSP.SERVICO_PEDIDO_ID = :servico_pedido_id
                      RETURNING *"""

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = data.model_dump(
                exclude_unset=True,
            )

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de erros e lançamento de exceção HTTP
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_SERVICO_ITEMPEDIDO: {e}",
            )
