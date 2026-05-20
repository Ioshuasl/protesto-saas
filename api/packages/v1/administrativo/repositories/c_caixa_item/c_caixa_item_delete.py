from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.repository import BaseRepository


class Delete(BaseRepository):

    def execute(self, caixa_item: CaixaItemSchema):

        try:

            # Montagem do sql
            sql = """ DELETE FROM c_caixa_item cci 
                      WHERE cci.caixa_item_id = :caixaItemId 
                      RETURNING cci.caixa_item_id
                 """

            # Preenchimento de parâmetros
            params = {
                "caixaItemId": caixa_item.caixa_item_id
            }
            
            #Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:

            # Informa que houve  uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir C_CAIXA_ITEM: {e}",
            )            