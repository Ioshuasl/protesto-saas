from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.actions.t_imovel_unidade.t_imovel_unidade_save_action import (
    TImovelUnidadeSaveAction,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TImovelUnidadeSaveService:

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_imovel_unidade")
        pass

    # Cadastra o novo CENSEC_QUALIDADE
    def execute(self, t_imovel_unidade_save_schema: TImovelUnidadeSaveSchema):

        # Verifica se precisa gerar o ID de sequência
        if not t_imovel_unidade_save_schema.imovel_unidade_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_IMOVEL_UNIDADE"

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            t_imovel_unidade_save_schema.imovel_unidade_id = sequencia.sequencia

        # Instanciamento de ações
        t_imovel_unidade_save_action = TImovelUnidadeSaveAction()

        # Retorna o resultado da operação
        return t_imovel_unidade_save_action.execute(t_imovel_unidade_save_schema)
