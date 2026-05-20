from packages.v1.administrativo.actions.t_ato_partetipo.t_ato_partetipo_save_action import (
    TAtoParteTipoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TAtoParteTipoSaveService:

    # Cadastra o novo CENSEC_QUALIDADE
    def execute(self, t_ato_partetipo_save_schema: TAtoParteTipoSaveSchema):

        # Verifica se precisa gerar o ID de sequência
        # Coluna primária ajustadaA
        if not t_ato_partetipo_save_schema.ato_partetipo_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_ATO_PARTETIPO"

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            t_ato_partetipo_save_schema.ato_partetipo_id = sequencia.sequencia

        # Instanciamento de ações
        # Ação já é importada como SaveAction
        t_ato_partetipo_save_action = TAtoParteTipoSaveAction()

        # Retorna o resultado da operação
        return t_ato_partetipo_save_action.execute(
            t_ato_partetipo_save_schema
        )  # Nome do parâmetro ajustado
