from datetime import datetime

from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_delete_action import (
    TAtoVinculoImovelDeleteAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIdSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TAtoVinculoImovelDeleteService:

    def execute(
        self,
        t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema,
    ):

        # Instância da classe
        t_ato_vinculoimovel_delete_action = TAtoVinculoImovelDeleteAction()

        # Executa a ação da classe
        data = t_ato_vinculoimovel_delete_action.execute(t_ato_vinculoimovel_id_schema)

        # 3. Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()

            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_ato_vinculoimovel_id_schema.ato_vinculoimovel_id,
                tabela="T_ATO_VINCULOIMOVEL",
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)

            # ----------------------------------------------------
            # Grava histórico de exclusão do vínculo de imóvel
            # ----------------------------------------------------
            now = datetime.now()
            now_br = now.strftime("%d/%m/%Y %H:%M:%S")
            usuario_id = t_ato_vinculoimovel_id_schema.usuario_id
            ato_vinculoimovel_id = t_ato_vinculoimovel_id_schema.ato_vinculoimovel_id

            historico_schema = THistoricoSaveSchema(
                tabela="T_ATO_VINCULOIMOVEL",
                campo="Exclusão de vínculo de imóvel",
                operacao="E",
                new_value=None,
                usuario_id=usuario_id,
                data=now,
                id=ato_vinculoimovel_id,
                observacao=f"Vínculo de imóvel removido pelo usuário({usuario_id}), no dia {now_br}",
                data_registro=None,
                dados_complementares=None,
            )

            t_historico_save_service = THistoricoSaveService()
            t_historico_save_service.execute(historico_schema)

            return data

        # 4. Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível excluir o registro ou ele não existe.",
        )
