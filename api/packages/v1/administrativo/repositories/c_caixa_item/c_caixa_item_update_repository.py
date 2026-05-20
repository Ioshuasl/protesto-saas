# Importação de bibliotecas
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class UpdateRepository(BaseRepository):

    def execute(self, caixa_item_id : int, caixa_item_schema : CaixaItemSchema):

        try:
            updates = []
            params = {}       

            if caixa_item_schema.especie_pagamento is not None:
                updates.append("ESPECIE_PAGAMENTO = :especie_pagamento")
                params["especie_pagamento"] = caixa_item_schema.especie_pagamento

            if caixa_item_schema.caixa_item_id is not None:
                updates.append("CAIXA_ITEM_ID = :caixa_item_id")
                params["caixa_item_id"] = caixa_item_schema.caixa_item_id

            if caixa_item_schema.caixa_servico_id is not None:
                updates.append("CAIXA_SERVICO_ID = :caixa_servico_id")
                params["caixa_servico_id"] = caixa_item_schema.caixa_servico_id

            if caixa_item_schema.usuario_servico_id is not None:
                updates.append("USUARIO_SERVICO_ID = :usuario_servico_id")
                params["usuario_servico_id"] = caixa_item_schema.usuario_servico_id

            if caixa_item_schema.usuario_caixa_id is not None:
                updates.append("USUARIO_CAIXA_ID = :usuario_caixa_id")
                params["usuario_caixa_id"] = caixa_item_schema.usuario_caixa_id

            if caixa_item_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = caixa_item_schema.descricao

            if caixa_item_schema.data_pagamento is not None:
                updates.append("DATA_PAGAMENTO = :data_pagamento")
                params["data_pagamento"] = caixa_item_schema.data_pagamento

            if caixa_item_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = caixa_item_schema.situacao

            if caixa_item_schema.tipo_documento is not None:
                updates.append("TIPO_DOCUMENTO = :tipo_documento")
                params["tipo_documento"] = caixa_item_schema.tipo_documento   

            if caixa_item_schema.tipo_transacao is not None:
                updates.append("TIPO_TRANSACAO = :tipo_transacao")
                params["tipo_transacao"] = caixa_item_schema.tipo_transacao

            if caixa_item_schema.valor_servico is not None:
                updates.append("VALOR_SERVICO = :valor_servico")
                params["valor_servico"] = caixa_item_schema.valor_servico     

            if caixa_item_schema.valor_pago is not None:
                updates.append("VALOR_PAGO = :valor_pago")
                params["valor_pago"] = caixa_item_schema.valor_pago    

            if caixa_item_schema.observacao is not None:
                updates.append("OBSERVACAO = :observacao")
                params["observacao"] = caixa_item_schema.observacao    

            if caixa_item_schema.hora_pagamento is not None:
                updates.append("HORA_PAGAMENTO = :hora_pagamento")
                params["hora_pagamento"] = caixa_item_schema.hora_pagamento    

            if caixa_item_schema.tipo_servico is not None:
                updates.append("TIPO_SERVICO = :tipo_servico")
                params["tipo_servico"] = caixa_item_schema.tipo_servico  

            if caixa_item_schema.registrado is not None:
                updates.append("REGISTRADO = :registrado")
                params["registrado"] = caixa_item_schema.registrado                                                                                                     


            if not updates:
                return False

            params["caixa_item_id"] = caixa_item_id
            sql = f"UPDATE C_CAIXA_ITEM SET {', '.join(updates)} WHERE caixa_item_id = :caixa_item_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.caixa_item_id:

                # Informa que não existe usuário a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum caixa serviço localizado para esta solicitação'
                )                
            
            # Verifica o resultado da execução
            if result:
                # Se houver um resultado, a atualização foi bem-sucedida
                return result


        except Exception as e:
        
            # Informa que houve  uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar caixa serviço: {e}"
            )         