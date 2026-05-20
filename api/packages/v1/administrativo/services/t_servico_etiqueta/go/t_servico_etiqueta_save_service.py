from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService

# Ajuste das importações para o novo schema
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaSaveSchema,
)

# Ajuste da importação para a nova action
from packages.v1.administrativo.actions.t_servico_etiqueta.t_servico_etiqueta_save_action import (
    SaveAction,
)
from fastapi import HTTPException, status


class SaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_SERVICO_ETIQUETA.
    """

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_servico_etiqueta")  # Tabela ajustada
        pass

    # Cadastra o novo T_SERVICO_ETIQUETA
    def execute(
        self, servico_etiqueta_schema: TServicoEtiquetaSaveSchema
    ):  # Nome do parâmetro e tipo ajustados

        # Armazena possíveis erros
        errors = []

        # A verificação de unicidade por "descricao" foi removida, pois a tabela
        # T_SERVICO_ETIQUETA não possui esse campo. Se a unicidade for necessária,
        # deve ser implementada uma lógica de checagem pela combinação de ETIQUETA_MODELO_ID e SERVICO_TIPO_ID.

        # Se houver erros, lança a exceção
        if errors:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errors)

        # Verifica se precisa gerar o ID de sequência
        # Coluna primária ajustada
        if not servico_etiqueta_schema.servico_etiqueta_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "T_SERVICO_ETIQUETA"  # Nome da tabela ajustado

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            servico_etiqueta_schema.servico_etiqueta_id = (
                sequencia.sequencia
            )  # Coluna primária ajustada

        # Instanciamento de ações
        # Ação já é importada como SaveAction (nome ajustado acima)
        save_action = SaveAction()

        # Retorna o resultado da operação
        return save_action.execute(
            servico_etiqueta_schema
        )  # Nome do parâmetro ajustado
