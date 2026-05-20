from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_TB_ESTADOCIVIL.
    """

    def execute(self, tb_estadocivil_id: int, estado_civil_schema: GTbEstadoCivilUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            tb_estadocivil_id (int): O ID do registro a ser atualizado.
            estado_civil_schema (GTBEstadoCivilUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if estado_civil_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = estado_civil_schema.descricao

            if estado_civil_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = estado_civil_schema.situacao

            if estado_civil_schema.sistema_id is not None:
                updates.append("SISTEMA_ID = :sistema_id")
                params["sistema_id"] = estado_civil_schema.sistema_id
            
            if estado_civil_schema.tipo is not None:
                updates.append("TIPO = :tipo")
                params["tipo"] = estado_civil_schema.tipo

            if not updates:
                return False

            params["tb_estadocivil_id"] = tb_estadocivil_id
            sql = f"UPDATE G_TB_ESTADOCIVIL SET {', '.join(updates)} WHERE TB_ESTADOCIVIL_ID = :tb_estadocivil_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.tb_estadocivil_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum Estado Civil localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o Estado Civil: {e}"
            )