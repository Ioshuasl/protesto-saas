from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, status

from actions.env.env_config_loader import EnvConfigLoader
from actions.file.file import File
from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_save_action import (
    TAtoVinculoParteSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteSaveSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)

from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)
from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_show_action import (
    GMarcacaoTipoShowAction,
)

from packages.v1.resolver.services.resolver_main_service import (
    ResolverMainService,
)
from packages.v1.resolver.schemas.resolver_schema import (
    ResolverSchema,
)

from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService

class TAtoVinculoParteSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, data: TAtoVinculoParteSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            data (TAtoVinculoParteSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not data.ato_vinculoparte_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_ATO_VINCULOPARTE"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            data.ato_vinculoparte_id = sequencia.sequencia

        # ----------------------------------------------------
        # Busca o texto para o tipo de assinatura
        # ----------------------------------------------------
        response_gmarcacao_tipo_show_service = GMarcacaoTipoShowAction().execute(GMarcacaoTipoIdSchema(marcacao_tipo_id=data.marcacao_tipo_id))
        if not response_gmarcacao_tipo_show_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o texto para o tipo de assinatura",
            )

        texto = ResolverMainService().execute(
            ResolverSchema(
                id=data.pessoa_id,
                campo_id_valor=data.pessoa_id,
                sitema_id=2,
                texto=response_gmarcacao_tipo_show_service.texto,
            )
        )

        # Carrega o conteúdo do arquivo DOCX gerado em disco (mesmo diretório do resolver).
        temp_dir = Path(EnvConfigLoader(".env").ORIUS_TEMP_DIR)
        docx_path = temp_dir / str(texto)
        data.texto_qualificacao = File().read(docx_path)

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_ato_vinculoparte_save_action = TAtoVinculoParteSaveAction()
        ato_vinculoparte_response = t_ato_vinculoparte_save_action.execute(
            data
        )

        # ----------------------------------------------------
        # Grava histórico de inclusão do vínculo de parte
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = data.usuario_id
        ato_vinculoparte_id = getattr(
            ato_vinculoparte_response,
            "ato_vinculoparte_id",
            data.ato_vinculoparte_id,
        )

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO_VINCULOPARTE",
            campo="Cadastro de vínculo de parte",
            operacao="I",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_vinculoparte_id,
            observacao=f"Vínculo de parte cadastrado pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        return ato_vinculoparte_response

