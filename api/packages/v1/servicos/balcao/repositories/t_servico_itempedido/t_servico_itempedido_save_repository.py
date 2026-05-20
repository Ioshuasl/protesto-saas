from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSchema,
)


class TServicoItemPedidoSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_SERVICO_ITEMPEDIDO.
    """

    def execute(self, data: TServicoItemPedidoSaveSchema):
        try:
            params = data.model_dump(
                exclude_unset=True,
                exclude=["usuario_id", "cartao_data", "cartao_numero"],
            )
            sql = generate_insert_sql("T_SERVICO_ITEMPEDIDO", params)
            # Execução do SQL e retorno do registro
            return self.run_and_return(sql, params)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_SERVICO_ITEMPEDIDO: {e}",
            )
