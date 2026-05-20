import logging

from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
)
from packages.v1.docx.services.docx_marker_to_sdt_converter_service import (
    DocxMarkerToSdtConverter,
)
from packages.v1.docx.services.docx_process_service import (
    DOCXProcess,
    DOCXProcessSchema,
)
from packages.v1.docx.services.docx_sdt_extractor_service import DocxSdtExtractor
from packages.v1.docx.services.docx_sdt_filler_service import DocxSdtFiller
from packages.v1.resolver.schemas.resolver_schema import (
    DOCXSdtConvertSchema,
    DOCXSdtExtractSchema,
    DOCXSdtFillerSchema,
    ResolverSchema,
)
from packages.v1.resolver.services.fixo.resolver_fixo_filler import ResolverFixoFiller
from packages.v1.resolver.services.lista.resolver_lista_filler import (
    ResolverListaFiller,
)
from packages.v1.resolver.services.resolver_buscar_marcacao_service import (
    ResolverBuscarMarcacaoService,
)
from packages.v1.resolver.services.texto.resolver_texto_filler_service import (
    ResolverTextoFillerService,
)

logger = logging.getLogger(__name__)


class ResolverMainService:

    def execute(self, data: ResolverSchema):

        # Executa o procedimento
        docx_process_response = DOCXProcess().execute(
            DOCXProcessSchema(
                id=str(data.id),
                content=data.texto,
                save_disk=True,
            )
        )

        # Classe para converter as marcações em SDT
        docx_maker_to_sdt_converter = DocxMarkerToSdtConverter(
            marker_regex=r"<!([A-Za-z0-9_]+)!>",
            keep_marker_text=True,
        )

        # Gera o arquivo final com SDTs no lugar das marcações
        response = docx_maker_to_sdt_converter.convert(
            DOCXSdtConvertSchema(
                input_docx="./storage/temp/" + docx_process_response,
                save_to_disk=False,
            ),
        )

        # Classe para extrair o sdt do documento
        docx_maker_extractor = DocxSdtExtractor()

        # Realiza o procedimento
        sdts = docx_maker_extractor.extract(
            DOCXSdtExtractSchema(input_content=response)
        )

        """
        Executa o processo de qualificação das marcações (SDTs).

        - Percorre as marcações encontradas no documento
        - Resolve cada marcação a partir da tag
        - Aplica o filler correto conforme o tipo da marcação
        - Retorna um dicionário com os valores já qualificados
        """

        # Serviço responsável por buscar a definição da marcação
        # (normalmente consulta banco ou cache de domínio)
        resolver_buscar_marcacao = ResolverBuscarMarcacaoService()

        # Instancia os fillers uma única vez
        # Evita custo de criação repetida dentro do loop
        fixo_filler = ResolverFixoFiller()
        lista_filler = ResolverListaFiller()
        texto_filler = ResolverTextoFillerService()

        # Cache simples por tag de marcação
        # Evita buscar a mesma marcação várias vezes no banco
        marcacao_cache = {}

        # Estrutura final de retorno
        # Dict é suficiente e mais simples que SimpleNamespace nesse caso
        marcacoes_qualificadas = {}

        # Mapeamento de tipo de valor para o método responsável
        # Evita múltiplos if/elif e facilita extensão futura
        fillers = {
            "F": fixo_filler.execute,  # Fixo
            "L": lista_filler.execute,  # Lista
            "T": texto_filler.execute,  # Texto
        }

        # Itera sobre todas as SDTs (marcações encontradas no documento)
        for sdt in sdts:

            # Extrai a tag identificadora da marcação
            tag = getattr(sdt, "tag", None)
            if not tag:
                # Sem tag não há como qualificar
                continue

            # Verifica se a marcação já foi resolvida anteriormente
            marcacao = marcacao_cache.get(tag)
            if marcacao is None:
                # Busca a definição da marcação no serviço
                marcacao = resolver_buscar_marcacao.execute(
                    GMarcacaoTipoNomeSchema(
                        nome=tag,
                        sistema_id=data.sitema_id,
                    )
                )
                # Armazena no cache para reutilização
                marcacao_cache[tag] = marcacao

            # Obtém o tipo da marcação (ex: lista, texto, etc.)
            marcacao_tipo_id = getattr(marcacao, "marcacao_tipo_id", None)
            if marcacao_tipo_id is None:
                # Marcações inválidas ou incompletas são ignoradas
                continue

            # Injeta o valor de referência (campo_id_valor)
            # Usado principalmente para textos que dependem de contexto
            if getattr(marcacao, "texto", None):
                marcacao.texto.campo_id_valor = data.campo_id_valor

            # Seleciona o handler correto com base no tipo de valor
            handler = fillers.get(getattr(marcacao, "tipo_valor", None))
            if not handler:
                # Tipo não suportado ou não implementado
                continue

            # Executa o filler responsável por gerar o valor final.
            # Em caso de erro em uma marcação específica, ignora apenas
            # aquela marcação e continua processando as demais.
            try:
                valor = handler(marcacao)
            except Exception as exc:
                logger.warning(
                    f"Marcacao ignorada por erro no resolver: {getattr(marcacao, "nome", None)}",
                    extra={
                        "tag": tag,
                        "nome": getattr(marcacao, "nome", None),
                        "tipo_valor": getattr(marcacao, "tipo_valor", None),
                        "erro": str(exc),
                    },
                )
                continue

            # Nome lógico da marcação (chave do resultado final)
            nome = getattr(marcacao, "nome", None)
            if not nome:
                # Sem nome não há como mapear o resultado
                continue

            # Armazena o valor qualificado no resultado final
            marcacoes_qualificadas[nome] = valor

        if marcacoes_qualificadas:

            sdt_filler = DocxSdtFiller(
                also_match_alias=False,  # recomendado: preencher por tag
                clear_if_missing=False,  # se não achar no dict, não mexe
            )

            sdt_filler.fill(
                DOCXSdtFillerSchema(
                    input_content=response,
                    values=marcacoes_qualificadas,
                    save_to_disk=True,
                    output_docx="./storage/temp/" + str(docx_process_response),
                )
            )

        # Retorna todas as marcações qualificadas
        return docx_process_response
