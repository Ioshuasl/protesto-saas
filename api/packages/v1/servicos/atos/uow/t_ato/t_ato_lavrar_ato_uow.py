from abstracts.repository import BaseRepository
from database.firebird import Firebird
from fastapi import HTTPException, status
from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_save import (
    Save as CaixaItemSaveRepository,
)
from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_update_repository import (
    GSeloLivroUpdateRepository,
)
from packages.v1.administrativo.repositories.t_livro_andamento.t_livro_andamento_update_repository import (
    TLivroAndamentoUpdateRepository,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.servicos.atos.repositories.t_ato.t_ato_update_repository import (
    TAtoUpdateRepository,
)
from packages.v1.servicos.atos.repositories.t_ato.t_ato_lavrar_ato_repository import (
    TAtoLavrarAtoRepository,
)
from packages.v1.servicos.atos.repositories.t_historico.t_historico_save_repository import (
    THistoricoSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_lavrar_ato_uow_schema import (
    TAtoLavrarAtoUowSchema,
)


class TAtoLavrarAtoUow(BaseRepository):
    """
    Orquestra a unidade de trabalho da lavratura.
    """

    def execute(self, data: TAtoLavrarAtoUowSchema):
        engine = Firebird.get_engine()

        with engine.begin() as connection:
            if data.ato_anterior_update:
                response_ato_anterior_update = TAtoUpdateRepository().execute(
                    data.ato_anterior_update,
                    connection=connection,
                )

                if not response_ato_anterior_update:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="[TA415] Nao foi possivel revogar o ato",
                    )

            response_ato_lavratura = TAtoLavrarAtoRepository().execute(
                data.lavratura,
                connection=connection,
            )

            if not response_ato_lavratura:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA415] Nao foi possivel concluir a lavratura do ato.",
                )

            response_livro_andamento_update = TLivroAndamentoUpdateRepository().execute(
                data.livro_andamento_update,
                connection=connection,
            )

            if not response_livro_andamento_update:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA416] Lavratura concluida, mas andamento do livro nao foi atualizado.",
                )

            if not data.caixa_item.caixa_item_id:
                sequencia = GenerateService().execute(
                    GSequenciaSchema(tabela="C_CAIXA_ITEM"),
                )
                data.caixa_item.caixa_item_id = sequencia.sequencia

            response_caixa_item = CaixaItemSaveRepository().execute(
                data.caixa_item,
                connection=connection,
            )

            if not response_caixa_item:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA422] Lavratura concluida, mas valor da lavratura nao foi salvo no caixa.",
                )

            for selo_update in data.selos_update:
                response_selo_update = GSeloLivroUpdateRepository().execute(
                    selo_update,
                    connection=connection,
                )

                if not response_selo_update:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="[TA420] Lavratura concluida, mas selo da lavratura nao foi atualizado.",
                    )

            if not data.historico.historico_id:
                sequencia = GenerateService().execute(
                    GSequenciaSchema(tabela="T_HISTORICO"),
                )
                data.historico.historico_id = sequencia.sequencia

            response_historico = THistoricoSaveRepository().execute(
                data.historico,
                connection=connection,
            )

            if not response_historico:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA418] Lavratura concluida, mas historico do ato nao foi registrado.",
                )

            return response_ato_lavratura
