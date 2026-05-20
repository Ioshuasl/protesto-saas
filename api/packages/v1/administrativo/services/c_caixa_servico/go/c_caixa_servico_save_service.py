from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.c_caixa_servico_schema import (
    CCaixaServicoSaveSchema,
    CCaixaServicoDescricaoSchema,
)
from packages.v1.administrativo.actions.c_caixa_servico.c_caixa_servico_save_action import (
    SaveAction,
)
from fastapi import HTTPException, status


class CCaixaServicoSaveService:

    def __init__(self):
        # Action responsável por carregar as services de acodo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("c_caixa_servico")
        pass

    # Cadastra o novo caixa serviço
    def execute(self, caixa_servico_schema: CCaixaServicoSaveSchema):

        # Armazena possíveis erros
        errors = []

        # Verifica se o e-mail já esta sendo utilizado
        # Importação de service de email
        descricao_service = self.dynamic_import.service(
            "c_caixa_servico_get_descricao_service", "GetDescricaoService"
        )

        # Instânciamento da service
        self.descricao_service = descricao_service()

        # Verifica se o email já esta sendo utilizado
        self.response = self.descricao_service.execute(
            CCaixaServicoDescricaoSchema(descricao=caixa_servico_schema.descricao),
            False,
        )

        # Se houver retorno significa que a descrição já esta sendo utiizada
        if self.response:
            errors.append(
                {
                    "input": "descricao",
                    "message": "a descrição informada já esta sendo utilizada.",
                }
            )

        # Se houver erros, informo
        if errors:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errors)

        # Verifica se precisa gerar o id de sequencia
        if not caixa_servico_schema.caixa_servico_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "C_CAIXA_SERVICO"

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            caixa_servico_schema.caixa_servico_id = sequencia.sequencia

        # Instânciamento de ações
        saveAction = SaveAction()

        # Retorna todos produtos desejados
        return saveAction.execute(caixa_servico_schema)
