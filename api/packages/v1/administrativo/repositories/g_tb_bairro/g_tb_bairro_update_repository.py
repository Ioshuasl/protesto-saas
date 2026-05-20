from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroUpdateSchema


class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização de um registro na tabela
    g_tb_bairro.
    """

    def execute(self, tb_bairro_id: int, bairro_schema: GTbBairroUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            tb_bairro_id (int): O ID do registro a ser atualizado.
            bairro_schema (GTbBairroUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        try:
            # Montagem do SQL
            sql = """ UPDATE G_TB_BAIRRO SET
                        DESCRICAO = :descricao,
                        SITUACAO = :situacao,
                        SISTEMA_ID = :sistema_id
                    WHERE
                        TB_BAIRRO_ID = :tb_bairro_id
                    RETURNING * """

            # Preenchimento de parâmetros
            params = {
                'tb_bairro_id': tb_bairro_id,
                'descricao': bairro_schema.descricao,
                'situacao': bairro_schema.situacao,
                'sistema_id': bairro_schema.sistema_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:

            # Informa que houve uma falha na atualização do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o Bairro: {e}"
            )