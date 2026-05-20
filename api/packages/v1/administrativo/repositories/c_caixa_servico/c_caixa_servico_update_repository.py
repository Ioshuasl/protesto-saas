from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):

    def execute(self, caixa_servico_id : int, c_caixa_servico_schema: CCaixaServicoUpdateSchema):

        try:
            updates = []
            params = {}       

            if c_caixa_servico_schema.tipo_transacao is not None:
                updates.append("TIPO_TRANSACAO = :tipo_transacao")
                params["tipo_transacao"] = c_caixa_servico_schema.tipo_transacao

            if c_caixa_servico_schema.sistema_id is not None:
                updates.append("SISTEMA_ID = :sistema_id")
                params["sistema_id"] = c_caixa_servico_schema.sistema_id

            if c_caixa_servico_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = c_caixa_servico_schema.situacao

            if c_caixa_servico_schema.interno_sistema is not None:
                updates.append("INTERNO_SISTEMA = :interno_sistema")
                params["interno_sistema"] = c_caixa_servico_schema.interno_sistema

            if c_caixa_servico_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = c_caixa_servico_schema.descricao

            if c_caixa_servico_schema.emitir_relatorio is not None:
                updates.append("EMITIR_RELATORIO = :emitir_relatorio")
                params["emitir_relatorio"] = c_caixa_servico_schema.emitir_relatorio

            if c_caixa_servico_schema.tipo_conta_carneleao is not None:
                updates.append("TIPO_CONTA_CARNELEAO = :tipo_conta_carneleao")
                params["tipo_conta_carneleao"] = c_caixa_servico_schema.tipo_conta_carneleao

            if c_caixa_servico_schema.centro_de_custa_id is not None:
                updates.append("CENTRO_DE_CUSTA_ID = :centro_de_custa_id")
                params["centro_de_custa_id"] = c_caixa_servico_schema.centro_de_custa_id


            if c_caixa_servico_schema.repetir_descricao is not None:
                updates.append("REPETIR_DESCRICAO = :repetir_descricao")
                params["repetir_descricao"] = c_caixa_servico_schema.repetir_descricao                

            if not updates:
                return False

            params["caixa_servico_id"] = caixa_servico_id
            sql = f"UPDATE C_CAIXA_SERVICO SET {', '.join(updates)} WHERE caixa_servico_id = :caixa_servico_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.caixa_servico_id:

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