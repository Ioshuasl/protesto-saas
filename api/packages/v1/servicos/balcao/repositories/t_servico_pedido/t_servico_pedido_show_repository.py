from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)


class TServicoPedidoShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        """
        Busca um registro específico de T_SERVICO_PEDIDO pelo ID.

        Args:
            t_servico_pedido_id_schema (TServicoPedidoIdSchema):
                Esquema contendo o ID do registro a ser buscado.

        Returns:
            O registro encontrado ou levanta exceção HTTP 404 se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                SELECT
                TSP.*,
                GU.lOGIN,
                GU.FUNCAO
                FROM T_SERVICO_PEDIDO TSP
                left JOIN G_USUARIO GU ON TSP.USUARIO_ID = GU.USUARIO_iD
                WHERE TSP.SERVICO_PEDIDO_ID = :servico_pedido_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_servico_pedido_id_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Execução do SQL
            # ----------------------------------------------------
            result = self.fetch_one(sql, params)

            # ----------------------------------------------------
            # Validação de retorno
            # ----------------------------------------------------
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de T_SERVICO_PEDIDO não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_SERVICO_PEDIDO: {e}",
            )
