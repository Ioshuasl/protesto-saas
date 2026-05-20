from actions.dynamic_import.dynamic_import import DynamicImport
from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa_sinal_publico.t_pessoa_sinal_publico_update_action import (
    TPessoaSinalPublicoUpdateAction,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
    TPessoaSinalPublicoUpdateSchema,
)


class TPessoaSinalPublicoUpdateService:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_pessoa_sinal_publico")

    def execute(
        self,
        pessoa_sinalpublico_id: int,
        pessoa_sinal_publico_schema: TPessoaSinalPublicoUpdateSchema,
    ):
        show_service = self.dynamic_import.service(
            "t_pessoa_sinal_publico_show_service",
            "TPessoaSinalPublicoShowService",
        )
        self.show_service = show_service()
        self.show_service.execute(
            TPessoaSinalPublicoIdSchema(pessoa_sinalpublico_id=pessoa_sinalpublico_id)
        )

        action = TPessoaSinalPublicoUpdateAction()
        response = action.execute(pessoa_sinalpublico_id, pessoa_sinal_publico_schema)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel atualizar o registro de pessoa sinal publico",
            )

        return response
