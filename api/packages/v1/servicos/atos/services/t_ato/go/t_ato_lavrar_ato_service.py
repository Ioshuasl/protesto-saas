from datetime import datetime
import json
from decimal import Decimal
from types import SimpleNamespace

from fastapi import HTTPException, status

from packages.v1.administrativo.repositories.g_selo_livro.g_selo_livro_show_by_tabela_campo_repository import (
    GSeloLivroShowByTabelaCampoRepository,
)
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_first_aberto_by_natureza_action import (
    TLivroAndamentoFirstAbertoByNaturezaAction,
)
from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_show_action import (
    TLivroNaturezaShowAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import (
    GSeloLivroLivreSchema,
    GSeloLivroSchema,
    GSeloLivroUpdateSchema,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoNaturezaIdSchema,
    TLivroAndamentoUpdateSchema,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import (
    TLivroNaturezaShowModeloSchema,
)
from packages.v1.administrativo.services.g_selo_livro.go.g_selo_livro_livre_show_service import (
    GSeloLivroLivreShowService,
)
from packages.v1.docx.actions.docx_convert_to_pdf_action import DOCXConvertToPDFAction
from packages.v1.docx.services.docx_page_usage_service import DOCXPageUsageService
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import TAtoShowAction
from packages.v1.servicos.atos.actions.t_ato.t_ato_lavrar_ato_uow_action import (
    TAtoLavrarAtoUowAction,
)
from packages.v1.servicos.atos.actions.t_ato_tipo.t_ato_tipo_show_action import TAtoTipoShowAction
from packages.v1.servicos.atos.actions.t_ato_parteimovel.t_ato_parteimovel_index_action import (
    TAtoParteImovelIndexAction,
)
from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_index_action import (
    TAtoVinculoParteIndexAction,
)
from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_index_action import (
    TAtoVinculoValorIndexAction,
)
from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_index_action import (
    TAtoVinculoImovelIndexAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoIdSchema,
    TAtoLavraturaSchema,
    TAtoTextoVisualizarSchema,
    TAtoUpdateSchema,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import TAtoTipoIdSchema
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import TAtoParteImovelIndexSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import TAtoVinculoParteIndexSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import TAtoVinculoValorIndexSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIndexSchema,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_lavrar_ato_uow_schema import (
    TAtoLavrarAtoUowSchema,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_display_texto_service import (
    TAtoDisplayTextoService,
)


class TAtoLavrarAtoService:
    """
    Marca o ato como lavrado (situacao 3), grava historico
    e retorna os dados atualizados do show.
    """

    def execute(self, data: TAtoLavraturaSchema):

        # Etapa 1: buscar o ato que sera lavrado
        response_ato_show = TAtoShowAction().execute(TAtoIdSchema(ato_id=data.ato_id))

        if not response_ato_show:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TA404] Ato nao encontrado. Verifique o codigo informado.",
            )

        # Etapa 2: validar se ja existe selo ou agrupador vinculado ao ato
        if getattr(response_ato_show, "selo_livro_id", None):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TA423] Ato ja possui selo ou agrupador vinculado. Lavratura bloqueada.",
            )

        response_selo_existente = GSeloLivroShowByTabelaCampoRepository().execute(
            GSeloLivroSchema(
                tabela="T_ATO",
                campo_id=response_ato_show.ato_id,
            )
        )

        if response_selo_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="[TA423] Ato ja possui selo ou agrupador vinculado. Lavratura bloqueada.",
            )

        # Etapa 3: buscar o tipo do ato
        response_ato_tipo = TAtoTipoShowAction().execute(
            TAtoTipoIdSchema(ato_tipo_id=response_ato_show.ato_tipo_id)
        )

        if not response_ato_tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TA405] Tipo de ato nao encontrado para o ato informado.",
            )

        # Etapa 4: validar imovel obrigatorio do ato
        if (
            getattr(response_ato_tipo, "possui_imovel", None) == "S"
            and getattr(response_ato_show, "ato_antigo", None) != "S"
        ):
            response_ato_vinculo_imovel = TAtoVinculoImovelIndexAction().execute(
                TAtoVinculoImovelIndexSchema(ato_id=response_ato_show.ato_id)
            )

            if not response_ato_vinculo_imovel:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA424] Tipo de ato exige imovel, mas nao existe imovel vinculado ao ato.",
                )

        # Etapa 5: buscar a natureza do livro do ato
        response_livro_natureza = TLivroNaturezaShowAction().execute(
            TLivroNaturezaShowModeloSchema(livro_natureza_id=response_ato_tipo.livro_natureza_id)
        )

        if not response_livro_natureza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TA406] Livro natureza nao encontrado para o tipo de ato.",
            )

        # Etapa 6: buscar livro de andamento aberto para lavratura
        response_livro_andamento = TLivroAndamentoFirstAbertoByNaturezaAction().execute(
            TLivroAndamentoNaturezaIdSchema(
                livro_natureza_id=response_livro_natureza.livro_natureza_id
            )
        )

        if not response_livro_andamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[TA407] Livro de andamento aberto nao encontrado para lavratura.",
            )

        if response_livro_andamento.folha_atual is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA421] Livro de andamento sem folha atual configurada para lavratura.",
            )

        # Etapa 7: montar o texto do ato para lavratura
        response_t_ato_display = TAtoDisplayTextoService().execute(
            TAtoTextoVisualizarSchema(ato_id=response_ato_show.ato_id, tipo_visualizacao=1)
        )

        if not response_t_ato_display:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA408] Texto do ato nao foi gerado para lavratura.",
            )

        # Etapa 8: converter o texto do ato para PDF
        response_t_ato_pdf = DOCXConvertToPDFAction.execute(
            input_docx_path=f"storage/temp/{response_t_ato_display.texto}",
            output="path",
        )

        if not response_t_ato_pdf:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA409] PDF do ato nao foi gerado para contagem de paginas.",
            )

        # Etapa 9: validar quantidade de paginas do ato
        total_paginas = int(response_t_ato_pdf.get("pages", 0))

        if total_paginas <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA410] Quantidade de paginas invalida para lavratura.",
            )

        # Etapa 10: calcular folhas usadas conforme regra de frente e verso
        page_usage = DOCXPageUsageService().execute(
            total_paginas=total_paginas,
            frente_verso=getattr(response_livro_natureza, "frente_verso", None),
        )

        if not page_usage:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA411] Nao foi possivel calcular as folhas utilizadas.",
            )

        # Etapa 11: buscar valores vinculados ao ato
        response_ato_vinculo_valor = TAtoVinculoValorIndexAction().execute(
            TAtoVinculoValorIndexSchema(ato_id=response_ato_show.ato_id)
        )

        if not response_ato_vinculo_valor:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA412] Valores vinculados ao ato nao encontrados.",
            )

        # Etapa 12: buscar partes vinculadas ao ato
        response_ato_vinculo_parte = TAtoVinculoParteIndexAction().execute(
            TAtoVinculoParteIndexSchema(ato_id=response_ato_show.ato_id)
        )

        if not response_ato_vinculo_parte:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA413] Partes vinculadas ao ato nao encontradas.",
            )

        # Etapa 13: validar vinculo entre parte e imovel quando DOI for obrigatoria
        if getattr(response_ato_tipo, "informar_doi", None) == "S":

            response_ato_parte_imovel = TAtoParteImovelIndexAction().execute(
                TAtoParteImovelIndexSchema(ato_id=response_ato_show.ato_id)
            )

            parte_imovel_valido = False

            for ato_parte_imovel in response_ato_parte_imovel or []:
                if getattr(ato_parte_imovel, "ato_vinculoparte_id", None) and getattr(
                    ato_parte_imovel, "ato_vinculoimovel_id", None
                ):
                    parte_imovel_valido = True

            if not parte_imovel_valido:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA425] DOI obrigatoria, mas nao existe vinculo valido entre parte e imovel.",
                )

        # Etapa 14: identificar a pessoa requerente para o selo
        selo_pessoa = None

        for ato_vinculo_parte in response_ato_vinculo_parte:
            if ato_vinculo_parte.requerente == "S":
                selo_pessoa = ato_vinculo_parte

        if not selo_pessoa or not getattr(selo_pessoa, "pessoa_nome", None):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA414] Requerente do ato nao encontrado para emissao do selo.",
            )

        # Etapa 15: validar selos livres antes de gravar a lavratura
        selos_livres = []

        for ato_vinculo_valor in response_ato_vinculo_valor:

            if not getattr(ato_vinculo_valor, "selo_grupo_id", None):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA419] Grupo de selo nao informado para um valor vinculado ao ato.",
                )

            response_selo_livre = GSeloLivroLivreShowService().execute(
                GSeloLivroLivreSchema(selo_grupo_id=ato_vinculo_valor.selo_grupo_id)
            )

            if not response_selo_livre:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA417] Selo livre nao encontrado para lavratura.",
                )

            if isinstance(response_selo_livre, dict):
                response_selo_livre = SimpleNamespace(**response_selo_livre)

            selos_livres.append(
                {
                    "ato_vinculo_valor": ato_vinculo_valor,
                    "selo_livre": response_selo_livre,
                }
            )

        # Etapa 16: preencher dados de lavratura no schema
        data.situacao_ato = 3
        data.folha_inicial = Decimal(response_livro_andamento.folha_atual) + Decimal(1)
        data.folha_total = Decimal(page_usage["folhas_utilizadas"])
        data.folha_final = data.folha_inicial + data.folha_total - Decimal(1)
        data.livro_andamento_id = response_livro_andamento.livro_andamento_id
        data.selo_livro_id = Decimal(selos_livres[0]["selo_livre"].selo_livro_id)

        # Verifica se possui ato anterior para lavrar
        ato_anterior_update = None

        if str(getattr(response_ato_tipo, "possui_ato_anterior", "N") or "N") == "S":
            if response_ato_show.ato_anterior_ato_id > 0:
                response_ato_anterior = TAtoShowAction().execute(
                    TAtoIdSchema(ato_id=response_ato_show.ato_anterior_ato_id)
                )
                if not response_ato_anterior:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="[TA415] Nao foi possivel localizar o ato para revogar.",
                    )
                ato_anterior_update = TAtoUpdateSchema(
                    ato_id=response_ato_anterior.ato_id,
                    situacao_ato=response_ato_tipo.situacao_ato_anterior,
                )

        livro_andamento_update = TLivroAndamentoUpdateSchema(
            livro_andamento_id=response_livro_andamento.livro_andamento_id,
            folha_atual=data.folha_final,
        )

        # Etapa 19: salvar valor total da lavratura no caixa
        total_emolumento = Decimal(0)
        total_taxa_judiciaria = Decimal(0)
        total_iss = Decimal(0)
        total_fundesp = Decimal(0)

        for ato_vinculo_valor in response_ato_vinculo_valor:
            total_emolumento += Decimal(ato_vinculo_valor.emolumento or 0)
            total_taxa_judiciaria += Decimal(ato_vinculo_valor.taxa_judiciaria or 0)
            total_iss += Decimal(ato_vinculo_valor.valor_iss or 0)
            total_fundesp += Decimal(ato_vinculo_valor.fundesp or 0)

        total_servico = total_emolumento + total_taxa_judiciaria + total_iss + total_fundesp

        now = datetime.now()
        caixa_descricao = (
            f"Prot.:{response_ato_show.protocolo} - "
            f"{response_ato_tipo.descricao} - "
            f"{selo_pessoa.pessoa_nome}"
        )

        caixa_item = CaixaItemSchema(
            especie_pagamento="D",
            caixa_servico_id=4,
            apresentante=selo_pessoa.pessoa_nome,
            usuario_servico_id=data.usuario_id,
            chave_servico=response_ato_show.ato_id,
            descricao=caixa_descricao,
            data_pagamento=now.date(),
            situacao=4,
            tipo_documento="C",
            tipo_transacao="C",
            hora_pagamento=now.strftime("%H:%M"),
            tipo_servico="1",
            registrado=1,
            emolumento=total_emolumento,
            taxa_judiciaria=total_taxa_judiciaria,
            fundesp=None,
            desconto=0,
            outra_taxa1=0,
            fundo_ri=total_fundesp,
            iss=total_iss,
            valor_servico=total_servico,
            valor_pago=total_servico,
            valor_taxa=Decimal(0),
            cpfcnpj_apresentante=getattr(selo_pessoa, "pessoa_cpf", None),
            nome_pagador=selo_pessoa.pessoa_nome,
            tabela="T_ATO",
            campo_id=response_ato_show.ato_id,
        )

        # Etapa 20: atualizar selos ja validados
        selos_update = []

        for selo_livre_item in selos_livres:

            ato_vinculo_valor = selo_livre_item["ato_vinculo_valor"]
            response_selo_livre = selo_livre_item["selo_livre"]

            selo_descricao = (
                f"Ato - Protocolo No. {response_ato_show.protocolo} - "
                f"Ped. {response_ato_show.ato_id}"
            )

            selo_update = GSeloLivroUpdateSchema(
                selo_livro_id=response_selo_livre.selo_livro_id,
                selo_situacao_id=2,
                descricao=selo_descricao,
                tabela="T_ATO",
                campo_id=ato_vinculo_valor.ato_id,
                usuario_id=data.usuario_id,
                data_informacao=datetime.now(),
                data=datetime.now(),
                apresentante=selo_pessoa.pessoa_nome,
                numero_agrupador=response_selo_livre.numero_selo,
                valor_iss=ato_vinculo_valor.valor_iss,
                valor_emolumento=ato_vinculo_valor.emolumento,
                valor_fundesp=ato_vinculo_valor.fundesp,
                valor_taxa_judiciaria=ato_vinculo_valor.taxa_judiciaria,
                valor_total=ato_vinculo_valor.emolumento
                + ato_vinculo_valor.taxa_judiciaria
                + ato_vinculo_valor.fundesp,
                emolumento_item_id=ato_vinculo_valor.emolumento_item_id,
            )

            selos_update.append(selo_update)
            response_selo_update = True

            if not response_selo_update:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="[TA420] Lavratura concluida, mas selo da lavratura nao foi atualizado.",
                )

        # Etapa 21: registrar historico da lavratura
        historico = THistoricoSaveSchema(
            tabela="T_ATO",
            campo="Lavratura do ato",
            operacao="U",
            new_value=json.dumps(response_ato_show, default=str),
            usuario_id=data.usuario_id,
            data=now,
            id=data.ato_id,
            observacao=(
                f"Ato lavrado (situacao 3) pelo usuario({data.usuario_id}), " f"no dia {now}"
            ),
            data_registro=None,
            dados_complementares=None,
        )

        response_ato_lavratura = TAtoLavrarAtoUowAction().execute(
            TAtoLavrarAtoUowSchema(
                lavratura=data,
                livro_andamento_update=livro_andamento_update,
                caixa_item=caixa_item,
                selos_update=selos_update,
                historico=historico,
                ato_anterior_update=ato_anterior_update,
            )
        )

        if not response_ato_lavratura:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="[TA415] Nao foi possivel concluir a lavratura do ato.",
            )

        return response_ato_lavratura
