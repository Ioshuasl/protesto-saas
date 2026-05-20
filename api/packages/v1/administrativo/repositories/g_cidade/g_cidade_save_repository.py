from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela G_CIDADE.
    """

    def execute(self, g_cidade_schema: GCidadeSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            g_cidade_schema (GCidadeSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_CIDADE(
                        CIDADE_ID,
                        UF,
                        CIDADE_NOME,
                        CODIGO_IBGE,
                        CODIGO_GYN
                        ) VALUES (
                        :cidade_id,
                        :uf,
                        :cidade_nome,
                        :codigo_ibge,
                        :codigo_gyn
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'cidade_id': g_cidade_schema.cidade_id,
                'uf': g_cidade_schema.uf,
                'cidade_nome': g_cidade_schema.cidade_nome,
                'codigo_ibge': g_cidade_schema.codigo_ibge,
                'codigo_gyn': g_cidade_schema.codigo_gyn
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar G_CIDADE: {e}"
            )