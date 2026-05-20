from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status

from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_delete_by_tabela_campo_repository import (
    CaixaItemDeleteByTabelaCampoRepository,
)
from packages.v1.administrativo.repositories.c_caixa_item.c_caixa_item_show_by_tabela_campo_repository import (
    CaixaItemShowByTabelaCampoRepository,
)
from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_update_action import (
    TLivroAndamentoUpdateAction,
)
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroUpdateSchema
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoUpdateSchema,
)
from packages.v1.administrativo.services.g_selo_livro.go.g_selo_livro_update_service import (
    GSeloLivroUpdateService,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)
from packages.v1.servicos.atos.repositories.t_ato.t_ato_is_last_lavrado_by_protocolo_folha_repository import (
    TAtoIsLastLavradoByProtocoloFolhaRepository,
)
from packages.v1.servicos.atos.repositories.t_ato.t_ato_retirar_lavratura_repository import (
    TAtoRetirarLavraturaRepository,
)
from packages.v1.servicos.atos.actions.t_ato.t_ato_update_action import TAtoUpdateAction
from packages.v1.servicos.atos.actions.t_ato_tipo.t_ato_tipo_show_action import TAtoTipoShowAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema, TAtoUpdateSchema
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import TAtoTipoIdSchema
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)


class TAtoRetirarLavraturaService:
    """
    Limpa dados de lavratura, volta o ato para Pre-lavrado (2),
    desfaz o avanco da folha atual no livro de andamento
    e retorna o selo para livre.
    """

    def execute(self, data: TAtoIdSchema):

        # Etapa 1: buscar o ato que tera a lavratura retirada
        response_ato_show = TAtoShowService().execute(data)

        if not response_ato_show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TR404] Ato nao encontrado. Verifique o codigo informado.",
            )

        # Etapa 2: validar se o ato possui dados de lavratura
        if str(getattr(response_ato_show, "situacao_ato", None)) != "3":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TR409] Este ato nao esta lavrado ou a lavratura ja foi retirada.",
            )

        if getattr(response_ato_show, "livro_andamento_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR422] Ato sem livro de andamento vinculado para retirada da lavratura.",
            )

        if getattr(response_ato_show, "folha_inicial", None) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR423] Ato sem folha inicial registrada para retirada da lavratura.",
            )

        if getattr(response_ato_show, "folha_final", None) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR424] Ato sem folha final registrada para retirada da lavratura.",
            )

        if getattr(response_ato_show, "folha_atual", None) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR425] Livro sem folha atual registrada para retirada da lavratura.",
            )

        if getattr(response_ato_show, "protocolo", None) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR426] Ato sem protocolo registrado para retirada da lavratura.",
            )

        if getattr(response_ato_show, "selo_livro_id", None) is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR427] Ato sem selo vinculado para retirada da lavratura.",
            )

        # Etapa 3: buscar o item do caixa gerado pela lavratura
        response_caixa_item = CaixaItemShowByTabelaCampoRepository().execute(
            CaixaItemSchema(
                tabela="T_ATO",
                campo_id=response_ato_show.ato_id,
            )
        )

        if not response_caixa_item:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR432] Item do caixa da lavratura nao encontrado para retirada.",
            )

        # Etapa 4: validar se este e o ultimo ato lavrado no livro
        response_is_last_lavrado = TAtoIsLastLavradoByProtocoloFolhaRepository().execute(
            ato_id=response_ato_show.ato_id,
            livro_andamento_id=response_ato_show.livro_andamento_id,
            protocolo=Decimal(response_ato_show.protocolo),
            folha_final=Decimal(response_ato_show.folha_final),
        )

        if not response_is_last_lavrado:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TR428] Somente o ultimo ato lavrado por protocolo e folha pode ter a lavratura retirada.",
            )

        # Etapa 5: calcular folha atual anterior a lavratura
        value_nova_folha_atual = Decimal(response_ato_show.folha_inicial) - Decimal(1)

        if value_nova_folha_atual < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR429] Nao foi possivel calcular a folha atual de retorno do livro.",
            )

        # Etapa 5.1: validar regra de ato anterior (somente verificacoes)
        deve_atualizar_ato_anterior = False

        response_ato_tipo = TAtoTipoShowAction().execute(
            TAtoTipoIdSchema(ato_tipo_id=response_ato_show.ato_tipo_id)
        )
        if not response_ato_tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TR434] Tipo de ato nao encontrado para retirada da lavratura.",
            )

        if str(getattr(response_ato_tipo, "possui_ato_anterior", "N") or "N") == "S":
            if (
                not getattr(response_ato_show, "ato_anterior_ato_id", None)
                or int(getattr(response_ato_show, "ato_anterior_ato_id", 0)) <= 0
            ):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TR435] Tipo de ato exige vinculo com ato anterior para retirada da lavratura.",
                )

            response_ato_anterior = TAtoShowService().execute(
                TAtoIdSchema(ato_id=getattr(response_ato_show, "ato_anterior_ato_id"))
            )
            if not response_ato_anterior:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TR436] Nao foi possivel localizar o ato anterior vinculado.",
                )

            if (
                str(getattr(response_ato_anterior, "situacao_ato", None))
                != response_ato_tipo.situacao_ato_anterior
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"[TR437] Retirada de lavratura exige ato anterior na situacao {response_ato_tipo.situacao_ato_anterior}.",
                )

            deve_atualizar_ato_anterior = True

        # Etapa 6: procedimentos (somente apos concluir as verificacoes)
        # Etapa 6.1: retirar lavratura do ato
        response_ato_retirar_lavratura = TAtoRetirarLavraturaRepository().execute(data)

        if not response_ato_retirar_lavratura:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TR409] Este ato nao esta lavrado ou a lavratura ja foi retirada.",
            )

        # Etapa 6.2: retirar revogacao do ato anterior (quando aplicavel)
        if deve_atualizar_ato_anterior:
            response_ato_anterior_update = TAtoUpdateAction().execute(
                TAtoUpdateSchema(
                    ato_id=response_ato_show.ato_anterior_ato_id,
                    situacao_ato="3",
                )
            )
            if not response_ato_anterior_update:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TR438] Nao foi possivel atualizar a situacao do ato anterior.",
                )

        # Etapa 7: atualizar folha atual do livro para o valor anterior
        response_livro_andamento_update = TLivroAndamentoUpdateAction().execute(
            TLivroAndamentoUpdateSchema(
                livro_andamento_id=response_ato_show.livro_andamento_id,
                folha_atual=value_nova_folha_atual,
            )
        )

        if not response_livro_andamento_update:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR430] Retirada concluida, mas andamento do livro nao foi atualizado.",
            )

        # Etapa 8: retornar o selo da lavratura para livre
        response_selo_update = GSeloLivroUpdateService().execute(
            GSeloLivroUpdateSchema(
                selo_livro_id=response_ato_show.selo_livro_id,
                selo_situacao_id=1,
                descricao=None,
                tabela=None,
                campo_id=None,
                usuario_id=data.usuario_id,
                data_informacao=None,
                data=None,
                apresentante=None,
                numero_agrupador=None,
                valor_iss=None,
                valor_emolumento=None,
                valor_fundesp=None,
                valor_taxa_judiciaria=None,
                valor_total=None,
                emolumento_item_id=None,
            )
        )

        if not response_selo_update:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR431] Retirada concluida, mas selo da lavratura nao voltou para livre.",
            )

        # Etapa 9: remover item do caixa gerado pela lavratura
        response_caixa_item_delete = CaixaItemDeleteByTabelaCampoRepository().execute(
            CaixaItemSchema(
                tabela="T_ATO",
                campo_id=response_ato_show.ato_id,
            )
        )

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if response_caixa_item_delete:

            # Corrije o G_Sequencia
            SequenciaDeleteService().execute(
                GSequenciaDeleteSchema(
                    sequencia=response_caixa_item_delete.caixa_item_id, tabela="C_CAIXA_ITEM"
                )
            )

        if not response_caixa_item_delete:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR433] Retirada concluida, mas item do caixa nao foi removido.",
            )

        # Etapa 10: registrar historico da retirada de lavratura
        response_ato_historico = THistoricoSaveService().execute(
            THistoricoSaveSchema(
                tabela="T_ATO",
                campo="Retirada de lavratura",
                operacao="U",
                new_value=None,
                usuario_id=data.usuario_id,
                data=datetime.now(),
                id=data.ato_id,
                observacao=(
                    f"Lavratura retirada e situacao retornada para 2 (Pre-lavrado) "
                    f"pelo usuario({data.usuario_id}), no dia {datetime.now()}"
                ),
                data_registro=None,
                dados_complementares=None,
            )
        )

        if not response_ato_historico:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TR418] Retirada concluida, mas historico do ato nao foi registrado.",
            )

        # Etapa 11: retornar ato atualizado
        return TAtoShowService().execute(data)
