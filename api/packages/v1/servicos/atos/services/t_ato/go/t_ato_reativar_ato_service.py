from datetime import datetime

from fastapi import HTTPException, status

from packages.v1.servicos.atos.repositories.t_ato.t_ato_reativar_ato_repository import (
    TAtoReativarAtoRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)


class TAtoReativarAtoService:
    """
    Volta a situação para Montagem (1) e remove data de cancelamento.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        repo = TAtoReativarAtoRepository()
        updated = repo.execute(t_ato_id_schema)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este ato nao esta cancelado ou nao pode ser reativado.",
            )

        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_id_schema.usuario_id
        ato_id = t_ato_id_schema.ato_id

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO",
            campo="Reativação do ato",
            operacao="U",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_id,
            observacao=(
                # Firebird pode falhar na conversão de alguns caracteres Unicode
                # (ex.: traço "—"), então normalizamos para ASCII antes de gravar.
                (
                    f"Ato reativado (situação 1 — Montagem) pelo usuário({usuario_id}), "
                    f"no dia {now_br}"
                )
                .replace("—", "-")
                .replace("–", "-")
            )[:260],
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        show_service = TAtoShowService()
        return show_service.execute(t_ato_id_schema)
