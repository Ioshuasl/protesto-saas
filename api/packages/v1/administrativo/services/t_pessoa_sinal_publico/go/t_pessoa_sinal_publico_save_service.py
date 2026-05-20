from packages.v1.administrativo.actions.t_pessoa_sinal_publico.t_pessoa_sinal_publico_save_action import (
    TPessoaSinalPublicoSaveAction,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TPessoaSinalPublicoSaveService:
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoSaveSchema):
        if not pessoa_sinal_publico_schema.pessoa_sinalpublico_id:
            sequencia_schema = GSequenciaSchema(tabela="T_PESSOA_SINALPUBLICO")
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)
            pessoa_sinal_publico_schema.pessoa_sinalpublico_id = sequencia.sequencia

        action = TPessoaSinalPublicoSaveAction()
        return action.execute(pessoa_sinal_publico_schema)
