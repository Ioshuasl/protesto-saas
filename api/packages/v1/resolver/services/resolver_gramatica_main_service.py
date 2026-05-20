from pathlib import Path

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
from packages.v1.resolver.services.gramatica.resolver_gramatica_qualifier_service import (
    ResolverGramaticaQualifierService,
)
from packages.v1.resolver.services.gramatica.resolver_gramatica_tag_parser_service import (
    parse_gram_tag,
)


class ResolverGramaticaMainService:
    def execute(self, data: ResolverSchema):
        docx_process_response = DOCXProcess().execute(
            DOCXProcessSchema(
                id=str(data.id),
                content=data.texto,
                save_disk=True,
            )
        )

        docx_maker_to_sdt_converter = DocxMarkerToSdtConverter(
            marker_regex=r"<!([^!]+)!>",
            keep_marker_text=True,
        )

        response = docx_maker_to_sdt_converter.convert(
            DOCXSdtConvertSchema(
                input_docx="./storage/temp/" + docx_process_response,
                save_to_disk=False,
            ),
        )

        sdts = DocxSdtExtractor().extract(DOCXSdtExtractSchema(input_content=response))

        qualifier = ResolverGramaticaQualifierService()
        contexto_gramatical = data.gramatica or {}
        marcacoes_qualificadas = {}

        for sdt in sdts:
            tag = getattr(sdt, "tag", None)
            if not tag:
                continue

            if not parse_gram_tag(tag):
                continue

            valor = qualifier.execute(tag, contexto_gramatical)
            marcacoes_qualificadas[tag] = valor if valor is not None else tag

        output_docx = Path("./storage/temp") / str(docx_process_response)

        if marcacoes_qualificadas:
            sdt_filler = DocxSdtFiller(
                also_match_alias=False,
                clear_if_missing=False,
            )
            sdt_filler.fill(
                DOCXSdtFillerSchema(
                    input_content=response,
                    values=marcacoes_qualificadas,
                    save_to_disk=True,
                    output_docx=str(output_docx),
                )
            )
        else:
            output_docx.write_bytes(response)

        return docx_process_response
