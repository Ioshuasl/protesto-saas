from packages.v1.administrativo.schemas.c_caixa_servico_schema import (
    CCaixaServicoSaveSchema,
)
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_save_repository import (
    SaveRepository,
)


class SaveAction:

    def execute(self, usuario_schema: CCaixaServicoSaveSchema):

        save_repository = SaveRepository()

        return save_repository.execute(usuario_schema)
