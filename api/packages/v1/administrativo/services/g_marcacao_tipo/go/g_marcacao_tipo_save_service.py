from actions.data.base64 import Base64
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService

# Ajuste das importações para o novo schema
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoSaveSchema,
)

# Ajuste da importação para a nova action
from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_save_action import (
    GMarcacaoTipoSaveAction,
)


class GMarcacaoTipoSaveService:

    # Cadastra o novo G_MARCACAO_TIPO
    def execute(
        self, data: GMarcacaoTipoSaveSchema
    ):  # Nome do parâmetro e tipo ajustados

        # Verifica se precisa gerar o ID de sequência
        # Coluna primária ajustada (MARCACAO_TIPO_ID)
        if not data.marcacao_tipo_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = "G_MARCACAO_TIPO"  # Nome da tabela ajustado

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            data.marcacao_tipo_id = sequencia.sequencia  # Coluna primária ajustada

        if getattr(data, "texto", None):

            texto = data.texto
            if isinstance(texto, str):
                if ".docx" in texto.lower():
                    if hasattr(data, "texto"):
                        delattr(data, "texto")
                else:
                    data.texto = Base64().decode(texto)
            else:
                data.texto = Base64().decode(texto)

        # Instanciamento de ações
        # Ação já é importada como SaveAction
        save_action = GMarcacaoTipoSaveAction()

        # Retorna o resultado da ação
        return save_action.execute(data)
