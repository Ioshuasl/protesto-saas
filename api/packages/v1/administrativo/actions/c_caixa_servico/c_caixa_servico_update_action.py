from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoUpdateSchema
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_update_repository import UpdateRepository


class UpdateAction:

    def execute(self, caixa_servico_id : int, c_caixa_servico_schema : CCaixaServicoUpdateSchema):

        save_repository = UpdateRepository()

        return save_repository.execute(caixa_servico_id, c_caixa_servico_schema)