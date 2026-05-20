from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_natureza.
    """

    def execute(self, natureza_schema: GNaturezaSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            natureza_schema (GNaturezaSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_NATUREZA(
                        NATUREZA_ID,
                        DESCRICAO,
                        SITUACAO,
                        SISTEMA_ID,
                        PEDIR_NUMERO_IMOVEL,
                        CONTROLE_FRENTEVERSO
                        ) VALUES (
                        :natureza_id,
                        :descricao,
                        :situacao,
                        :sistema_id,
                        :pedir_numero_imovel,
                        :controle_frenteverso
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'natureza_id': natureza_schema.natureza_id,
                'descricao': natureza_schema.descricao,
                'situacao': natureza_schema.situacao,
                'sistema_id': natureza_schema.sistema_id,
                'pedir_numero_imovel': natureza_schema.pedir_numero_imovel,
                'controle_frenteverso': natureza_schema.controle_frenteverso
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar NATUREZA: {e}"
            )