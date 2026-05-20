from fastapi import HTTPException, status

from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_update_action import (
    TTbSinalPublicoUpdateAction,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
    TTbSinalPublicoIdSchema,
    TTbSinalPublicoUpdateSchema,
)


class TTbSinalPublicoUpdateService:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_tb_sinal_publico")

    def execute(
        self,
        tb_sinalpublico_id: int,
        sinal_publico_schema: TTbSinalPublicoUpdateSchema,
    ):
        show_service = self.dynamic_import.service(
            "t_tb_sinal_publico_show_service",
            "TTbSinalPublicoShowService",
        )
        self.show_service = show_service()
        current_data = self.show_service.execute(
            TTbSinalPublicoIdSchema(tb_sinalpublico_id=tb_sinalpublico_id)
        )

        descricao_service = self.dynamic_import.service(
            "t_tb_sinal_publico_get_descricao_service",
            "TTbSinalPublicoGetByDescricaoService",
        )
        self.descricao_service = descricao_service()
        duplicated = self.descricao_service.execute(
            TTbSinalPublicoDescricaoSchema(descricao=sinal_publico_schema.descricao),
            False,
        )

        duplicated_id = None
        if duplicated:
            duplicated_id = getattr(duplicated, "tb_sinalpublico_id", None)
            if duplicated_id is None and isinstance(duplicated, dict):
                duplicated_id = duplicated.get("tb_sinalpublico_id") or duplicated.get(
                    "TB_SINALPUBLICO_ID"
                )

        if duplicated_id is not None and duplicated_id != tb_sinalpublico_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=[{"input": "descricao", "message": "a descricao informada ja esta sendo utilizada."}],
            )

        update_action = TTbSinalPublicoUpdateAction()
        response = update_action.execute(tb_sinalpublico_id, sinal_publico_schema)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel atualizar o registro de sinal publico",
            )

        return response or current_data
