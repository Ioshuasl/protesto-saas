from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeUpdateSchema
from fastapi import HTTPException, status


class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização de um registro na tabela G_CIDADE.
    """

    def execute(self, cidade_id: int, g_cidade_schema: GCidadeUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            cidade_id (int): O ID (CIDADE_ID) do registro a ser atualizado.
            g_cidade_schema (GCidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = """ UPDATE G_CIDADE SET
                        UF = :uf,
                        CIDADE_NOME = :cidade_nome,
                        CODIGO_IBGE = :codigo_ibge,
                        CODIGO_GYN = :codigo_gyn
                      WHERE CIDADE_ID = :cidade_id
                      RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'cidade_id': cidade_id,
                'uf': g_cidade_schema.uf,
                'cidade_nome': g_cidade_schema.cidade_nome,
                'codigo_ibge': g_cidade_schema.codigo_ibge,
                'codigo_gyn': g_cidade_schema.codigo_gyn
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar G_CIDADE: {e}"
            )