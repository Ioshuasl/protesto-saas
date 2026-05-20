from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela G_TB_DOCUMENTOTIPO.
    """

    def execute(self, documentotipo_schema: GTbDocumentoTipoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            documentotipo_schema (GtbDocumentotipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_TB_DOCUMENTOTIPO(
                        TB_DOCUMENTOTIPO_ID,
                        DESCRICAO,
                        TEXTO,
                        SITUACAO,
                        POSSUI_NUMERACAO,
                        ORGAO_PADRAO,
                        DESCRICAO_SIMPLIFICADA,
                        TIPO,
                        DESCRICAO_SINTER
                        ) VALUES (
                        :tb_documentotipo_id,
                        :descricao,
                        :texto,
                        :situacao,
                        :possui_numeracao,
                        :orgao_padrao,
                        :descricao_simplificada,
                        :tipo,
                        :descricao_sinter
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_documentotipo_id': documentotipo_schema.tb_documentotipo_id,
                'descricao': documentotipo_schema.descricao,
                'texto': documentotipo_schema.texto,
                'situacao': documentotipo_schema.situacao,
                'possui_numeracao': documentotipo_schema.possui_numeracao,
                'orgao_padrao': documentotipo_schema.orgao_padrao,
                'descricao_simplificada': documentotipo_schema.descricao_simplificada,
                'tipo': documentotipo_schema.tipo,
                'descricao_sinter': documentotipo_schema.descricao_sinter
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar G_TB_DOCUMENTOTIPO: {e}"
            )