from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.actions.t_pessoa_representante.t_pessoa_representante_save_action import (
    TPessoaRepresentanteSaveAction,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TPessoaRepresentanteSaveService:

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_pessoa_representante")
        pass

    # Cadastra o novo regime de bens
    def execute(
        self, t_pessoa_representante_save_schema: TPessoaRepresentanteSaveSchema
    ):

        # Verifica se precisa gerar o ID de sequência
        if not t_pessoa_representante_save_schema.pessoa_representante_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_PESSOA_REPRESENTANTE"

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            t_pessoa_representante_save_schema.pessoa_representante_id = (
                sequencia.sequencia
            )

        # Instanciamento de ações
        t_pessoa_representante_save_action = TPessoaRepresentanteSaveAction()

        # Retorna o resultado da operação
        return t_pessoa_representante_save_action.execute(
            t_pessoa_representante_save_schema
        )
