from datetime import datetime
import json

from fastapi import HTTPException, status
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.servicos.atos.repositories.t_ato.t_ato_protocolar_lock_show_repository import (
    TAtoProtocolarLockShowRepository,
)
from packages.v1.servicos.atos.repositories.t_ato.t_ato_protocolar_update_repository import (
    TAtoProtocolarUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoIdSchema,
    TAtoProtocolarUpdateSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)


class TAtoProtocolarService:
    def execute(self, data: TAtoIdSchema):

        # Etapa 1: buscar o ato que sera protocolado
        response_ato_show = TAtoProtocolarLockShowRepository().execute(data)

        if not response_ato_show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TA404] Ato nao encontrado. Verifique o codigo informado.",
            )

        # Etapa 2: validar se o ato ja possui protocolo
        if response_ato_show.protocolo is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TA409] Este ato ja esta protocolado.",
            )

        # Etapa 3: gerar novo numero de protocolo pelo contador de sequencia
        response_sequencia = GenerateService().execute(
            GSequenciaSchema(
                contador=True,
                tabela="ATO_PROTOCOLO",
            )
        )

        # Etapa 4: aplicar protocolo no ato
        response_ato_updated = TAtoProtocolarUpdateRepository().execute(
            TAtoProtocolarUpdateSchema(
                ato_id=data.ato_id,
                protocolo=response_sequencia.sequencia,
            )
        )

        if not response_ato_updated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TA409] Este ato ja esta protocolado.",
            )

        # Etapa 6: registrar historico da protocolacao
        response_historico = THistoricoSaveService().execute(
            THistoricoSaveSchema(
                tabela="T_ATO",
                campo="Protocolacao",
                operacao="I",
                new_value=json.dumps(response_ato_show, default=str),
                usuario_id=data.usuario_id,
                data=datetime.now(),
                id=data.ato_id,
                observacao=(
                    f"Ato protocolado (n {response_ato_updated.protocolo}) pelo usuario({data.usuario_id}), "
                    f"no dia {datetime.now()}"
                ),
                data_registro=None,
                dados_complementares=None,
            )
        )

        if not response_historico:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA418] Protocolacao concluida, mas historico do ato nao foi registrado.",
            )

        return response_ato_updated
