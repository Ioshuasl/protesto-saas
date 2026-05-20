from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoCertidaoSaveSchema,
)


class TServicoItemPedidoCertidaoSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_SERVICO_ITEMPEDIDO.
    """

    def execute(self, data: TServicoItemPedidoCertidaoSaveSchema):
        try:
            params = data.model_dump(exclude_unset=True)
            sql = "UPDATE T_SERVICO_ITEMPEDIDO TSI SET TSI.CERTIDAO_TEXTO = :certidao_texto WHERE TSI.SERVICO_ITEMPEDIDO_ID = :servico_itempedido_id RETURNING *"
            # Execução do SQL e retorno do registro
            return self.run_and_return(sql, params)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_SERVICO_ITEMPEDIDO: {e}",
            )
