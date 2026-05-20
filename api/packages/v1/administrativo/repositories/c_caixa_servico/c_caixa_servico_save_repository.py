
from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoSaveSchema

class SaveRepository(BaseRepository):

    def execute(self, caixa_servico_schema : CCaixaServicoSaveSchema):
            
        try:

            # Montagem do SQL
            sql = """ INSERT INTO C_CAIXA_SERVICO(
                        CAIXA_SERVICO_ID,
                        TIPO_TRANSACAO,
                        SISTEMA_ID,
                        SITUACAO,
                        INTERNO_SISTEMA,
                        DESCRICAO,
                        EMITIR_RELATORIO,
                        TIPO_CONTA_CARNELEAO,
                        CENTRO_DE_CUSTA_ID,
                        REPETIR_DESCRICAO
                        ) VALUES (
                        :caixa_servico_id,
                        :tipo_transacao,
                        :sistema_id,
                        :situacao,
                        :interno_sistema,
                        :descricao,
                        :emitir_relatorio,
                        :tipo_conta_carneleao,
                        :centro_de_custa_id,
                        :repetir_descricao
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'caixa_servico_id': caixa_servico_schema.caixa_servico_id,
                'tipo_transacao': caixa_servico_schema.tipo_transacao,
                'sistema_id': caixa_servico_schema.sistema_id,
                'situacao': caixa_servico_schema.situacao,
                'interno_sistema': caixa_servico_schema.interno_sistema,
                'descricao': caixa_servico_schema.descricao,
                'emitir_relatorio': caixa_servico_schema.emitir_relatorio,
                'tipo_conta_carneleao': caixa_servico_schema.tipo_conta_carneleao,
                'centro_de_custa_id': caixa_servico_schema.centro_de_custa_id,
                'repetir_descricao': caixa_servico_schema.repetir_descricao
            }

            # Excução do sql
            return self.run_and_return(sql, params)
    
        except Exception as e:
        
            # Informa que houve  uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar caixa serviço: {e}"
            )     