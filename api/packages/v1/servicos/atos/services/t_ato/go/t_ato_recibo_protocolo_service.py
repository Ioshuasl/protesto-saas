from datetime import datetime

from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import TAtoShowAction
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)


class TAtoReciboProtocoloService:
    """
    Dados de T_ATO (e livro vinculado via show) para montagem do PDF de recibo
    de protocolo. Somente leitura; não usa G_SEQUENCIA.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        action = TAtoShowAction()
        data = action.execute(t_ato_id_schema)

        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_id_schema.usuario_id
        ato_id = t_ato_id_schema.ato_id

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO",
            campo="Recibo de protocolo (PDF)",
            operacao="C",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_id,
            observacao=(
                f"Consulta de dados para recibo de protocolo pelo usuário({usuario_id}), "
                f"no dia {now_br}"
            ),
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        return data
