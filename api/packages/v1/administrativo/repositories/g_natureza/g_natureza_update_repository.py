from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_NATUREZA.
    """

    def execute(self, natureza_id : int, natureza_schema: GNaturezaUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            natureza_id (int): O ID do registro a ser atualizado.
            natureza_schema (GNaturezaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if natureza_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = natureza_schema.descricao

            if natureza_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = natureza_schema.situacao
            
            if natureza_schema.sistema_id is not None:
                updates.append("SISTEMA_ID = :sistema_id")
                params["sistema_id"] = natureza_schema.sistema_id
            
            if natureza_schema.pedir_numero_imovel is not None:
                updates.append("PEDIR_NUMERO_IMOVEL = :pedir_numero_imovel")
                params["pedir_numero_imovel"] = natureza_schema.pedir_numero_imovel

            if natureza_schema.controle_frenteverso is not None:
                updates.append("CONTROLE_FRENTEVERSO = :controle_frenteverso")
                params["controle_frenteverso"] = natureza_schema.controle_frenteverso
            
            if not updates:
                return False

            params["natureza_id"] = natureza_id
            sql = f"UPDATE G_NATUREZA SET {', '.join(updates)} WHERE natureza_id = :natureza_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.natureza_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhuma NATUREZA localizada para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o NATUREZA: {e}"
            )