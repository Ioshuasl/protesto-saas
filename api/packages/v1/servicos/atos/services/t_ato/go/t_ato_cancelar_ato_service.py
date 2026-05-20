from datetime import datetime

from fastapi import HTTPException, status

from packages.v1.servicos.atos.repositories.t_ato.t_ato_cancelar_ato_repository import (
    TAtoCancelarAtoRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)


class TAtoCancelarAtoService:
    """
    Define situação Cancelado (4) e data de cancelamento. Retorna o show atualizado.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        repo = TAtoCancelarAtoRepository()
        updated = repo.execute(t_ato_id_schema)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este ato ja esta cancelado ou nao pode ser atualizado.",
            )

        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_id_schema.usuario_id
        ato_id = t_ato_id_schema.ato_id

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO",
            campo="Cancelamento do ato",
            operacao="U",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_id,
            observacao=(
                f"Ato cancelado (situação 4) pelo usuário({usuario_id}), no dia {now_br}"
            ),
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        show_service = TAtoShowService()
        return show_service.execute(t_ato_id_schema)
