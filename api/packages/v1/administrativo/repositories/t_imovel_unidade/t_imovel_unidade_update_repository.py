from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeUpdateSchema,
)
from fastapi import HTTPException, status


class TImovelUnidadeUpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_CENSEC_QUALIDADE.
    """

    def execute(self, t_imovel_unidade_update_schema: TImovelUnidadeUpdateSchema):
        """
        Executa a atualização de um registro na tabela.

        Args:
            t_imovel_unidade_id (int): O ID do registro a ser atualizado.
            t_imovel_unidade_schema (TImovelUnidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.

        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:

            params, update_columns = prepare_update_data(
                t_imovel_unidade_update_schema,
                exclude_fields=["imovel_unidade_id"],
                id_field="imovel_unidade_id",
            )

            sql = f"""
                    UPDATE T_IMOVEL_UNIDADE
                    SET {update_columns}
                    WHERE IMOVEL_UNIDADE_ID = :imovel_unidade_id
                    RETURNING IMOVEL_UNIDADE_ID
                """

            # Executa o update
            response = self.run_and_return(sql, params)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o imóvel unidade: {str(e)}",
            )
