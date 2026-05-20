from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_TB_DOCUMENTOTIPO.
    """

    def execute(self, tb_documentotipo_id: int, documentotipo_schema: GTbDocumentoTipoUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            tb_documentotipo_id (int): O ID do registro a ser atualizado.
            documentotipo_schema (GtbDocumentotipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if documentotipo_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = documentotipo_schema.descricao

            if documentotipo_schema.texto is not None:
                updates.append("TEXTO = :texto")
                params["texto"] = documentotipo_schema.texto

            if documentotipo_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = documentotipo_schema.situacao

            if documentotipo_schema.possui_numeracao is not None:
                updates.append("POSSUI_NUMERACAO = :possui_numeracao")
                params["possui_numeracao"] = documentotipo_schema.possui_numeracao
                
            if documentotipo_schema.orgao_padrao is not None:
                updates.append("ORGAO_PADRAO = :orgao_padrao")
                params["orgao_padrao"] = documentotipo_schema.orgao_padrao
                
            if documentotipo_schema.descricao_simplificada is not None:
                updates.append("DESCRICAO_SIMPLIFICADA = :descricao_simplificada")
                params["descricao_simplificada"] = documentotipo_schema.descricao_simplificada

            if documentotipo_schema.tipo is not None:
                updates.append("TIPO = :tipo")
                params["tipo"] = documentotipo_schema.tipo
                
            if documentotipo_schema.descricao_sinter is not None:
                updates.append("DESCRICAO_SINTER = :descricao_sinter")
                params["descricao_sinter"] = documentotipo_schema.descricao_sinter
            
            if not updates:
                return False

            params["tb_documentotipo_id"] = tb_documentotipo_id
            sql = f"UPDATE G_TB_DOCUMENTOTIPO SET {', '.join(updates)} WHERE TB_DOCUMENTOTIPO_ID = :tb_documentotipo_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum G_TB_DOCUMENTOTIPO localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o G_TB_DOCUMENTOTIPO: {e}"
            )