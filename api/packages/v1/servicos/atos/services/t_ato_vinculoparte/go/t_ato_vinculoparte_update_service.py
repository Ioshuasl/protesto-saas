from pathlib import Path

from fastapi import HTTPException, status

from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_update_action import (
    TAtoVinculoParteUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteUpdateSchema,
)

from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_show_action import (
    GMarcacaoTipoShowAction,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)
from packages.v1.resolver.services.resolver_main_service import (
    ResolverMainService,
)
from packages.v1.resolver.schemas.resolver_schema import (
    ResolverSchema,
)

from actions.env.env_config_loader import EnvConfigLoader
from actions.file.file import File

class TAtoVinculoParteUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, data: TAtoVinculoParteUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            data (TAtoVinculoParteUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculoparte_update_action = TAtoVinculoParteUpdateAction()

        # Regenera TEXTO_QUALIFICACAO somente quando marcacao_tipo_id veio no PUT.
        # Campo omitido (edição sem alterar qualificação) não deve disparar o resolver.
        marcacao_tipo_informado = (
            "marcacao_tipo_id" in data.model_fields_set
            and data.marcacao_tipo_id is not None
        )
        if marcacao_tipo_informado:
            response_gmarcacao_tipo_show_service = GMarcacaoTipoShowAction().execute(
                GMarcacaoTipoIdSchema(marcacao_tipo_id=data.marcacao_tipo_id)
            )
            if not response_gmarcacao_tipo_show_service:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foi possível localizar o texto para o tipo de assinatura",
                )

            response_resolver = ResolverMainService().execute(
                ResolverSchema(
                    id=data.pessoa_id,
                    campo_id_valor=data.pessoa_id,
                    sitema_id=2,
                    texto=response_gmarcacao_tipo_show_service.texto,
                )
            )

            temp_dir = Path(EnvConfigLoader(".env").ORIUS_TEMP_DIR)
            docx_path = temp_dir / str(response_resolver)
            data.texto_qualificacao = File().read(docx_path)

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_vinculoparte_update_action.execute(data)
