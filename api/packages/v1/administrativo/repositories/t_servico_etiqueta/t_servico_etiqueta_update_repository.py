from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import TServicoEtiquetaUpdateSchema # Schema ajustado para TServicoEtiqueta
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_SERVICO_ETIQUETA.
    """

    def execute(self, servico_etiqueta_id : int, servico_etiqueta_schema: TServicoEtiquetaUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            servico_etiqueta_id (int): O ID do registro a ser atualizado (SERVICO_ETIQUETA_ID).
            servico_etiqueta_schema (TServicoEtiquetaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            # --- Campos da T_SERVICO_ETIQUETA que podem ser atualizados (com base na DDL) ---
            
            # ETIQUETA_MODELO_ID NUMERIC(10,2)
            if servico_etiqueta_schema.etiqueta_modelo_id is not None:
                updates.append("ETIQUETA_MODELO_ID = :etiqueta_modelo_id")
                params["etiqueta_modelo_id"] = servico_etiqueta_schema.etiqueta_modelo_id

            # SERVICO_TIPO_ID NUMERIC(10,2)
            if servico_etiqueta_schema.servico_tipo_id is not None:
                updates.append("SERVICO_TIPO_ID = :servico_tipo_id")
                params["servico_tipo_id"] = servico_etiqueta_schema.servico_tipo_id

            # -------------------------------------------------------------------------
            
            if not updates:
                # Se não houver campos para atualizar, retorna False (ou um comportamento de sucesso sem alteração)
                return False

            # Parâmetro da chave primária para a cláusula WHERE
            params["servico_etiqueta_id"] = servico_etiqueta_id
            
            # Montagem e execução do SQL
            sql = f"UPDATE T_SERVICO_ETIQUETA SET {', '.join(updates)} WHERE SERVICO_ETIQUETA_ID = :servico_etiqueta_id RETURNING *;"

            # Executa a query e retorna o registro atualizado
            result = self.run_and_return(sql, params)
            
            # O result é uma tupla/objeto com os campos do registro, 
            # verificamos a existência do campo chave para confirmação
            if not result or not getattr(result, 'servico_etiqueta_id', None):
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhuma ETIQUETA DE SERVIÇO localizada para esta solicitação'
                )
            
            # Se houver um resultado e ele tiver o ID, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar a ETIQUETA DE SERVIÇO: {e}"
            )