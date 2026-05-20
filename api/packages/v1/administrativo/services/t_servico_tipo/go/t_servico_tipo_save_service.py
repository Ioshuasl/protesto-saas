from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService

# Ajuste das importações para o novo schema
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoSaveSchema,
    TServicoTipoDescricaoSchema,
)

# Ajuste da importação para a nova action
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_save_action import (
    SaveAction,
)
from fastapi import HTTPException, status


class SaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_SERVICO_TIPO.
    """

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_servico_tipo")  # Tabela ajustada
        pass

    # Cadastra o novo T_SERVICO_TIPO
    def execute(
        self, servico_tipo_schema: TServicoTipoSaveSchema
    ):  # Nome do parâmetro e tipo ajustados

        # Armazena possíveis erros
        errors = []

        # Verifica se a descrição já está sendo utilizada
        # Importação de service ajustada
        descricao_service = self.dynamic_import.service(
            "t_servico_tipo_get_by_descricao_service", "GetByDescricaoService"
        )

        # Instanciamento da service
        self.descricao_service = descricao_service()

        # Verifica se a descrição já está sendo utilizada
        # Uso do novo schema e parâmetro
        self.response = self.descricao_service.execute(
            TServicoTipoDescricaoSchema(descricao=servico_tipo_schema.descricao), False
        )

        # Se houver retorno significa que a descrição já está sendo utilizada
        if self.response:
            errors.append(
                {
                    "input": "descricao",
                    "message": "a descrição informada já está sendo utilizada.",
                }
            )

        # Se houver erros, lança a exceção
        if errors:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errors)

        # Verifica se precisa gerar o ID de sequência
        # Coluna primária ajustada
        if not servico_tipo_schema.servico_tipo_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_SERVICO_TIPO"  # Nome da tabela ajustado

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            servico_tipo_schema.servico_tipo_id = (
                sequencia.sequencia
            )  # Coluna primária ajustada

        # Instanciamento de ações
        # Ação já é importada como SaveAction
        save_action = SaveAction()

        # Retorna o resultado da operação
        return save_action.execute(servico_tipo_schema)  # Nome do parâmetro ajustado
