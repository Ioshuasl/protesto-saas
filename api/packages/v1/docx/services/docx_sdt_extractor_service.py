import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from lxml import etree

from packages.v1.resolver.schemas.resolver_schema import DOCXSdtExtractSchema

# Namespace do WordprocessingML (DOCX / Word XML)
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": WORD_NS}


def w(tag: str) -> str:
    """Helper para montar tags com namespace do Word."""
    return f"{{{WORD_NS}}}{tag}"


@dataclass(frozen=True)
class SdtInfo:
    """
    Representa um SDT encontrado no DOCX.

    Campos:
    - part: qual parte do DOCX (document.xml, headerX.xml, footerX.xml)
    - tag: chave técnica (w:tag/@w:val) -> recomendado para identificação
    - alias: nome “visual” (w:alias/@w:val) -> opcional
    - sdt_id: id interno (w:id/@w:val) -> opcional
    - is_block: True se o SDT contém parágrafos (block-level), False se for inline
    - has_nested_sdt: True se existe SDT dentro do conteúdo deste SDT
    - text: texto extraído do conteúdo (human-readable, com quebras de linha)
    """

    part: str
    tag: Optional[str]
    alias: Optional[str]
    sdt_id: Optional[str]
    is_block: bool
    has_nested_sdt: bool
    text: str


class DocxSdtExtractor:
    """
    Extrator de SDT (Content Controls) em DOCX.

    Estratégia:
    1) Abre o .docx como ZIP.
    2) Lê apenas: word/document.xml, word/header*.xml, word/footer*.xml
    3) Em cada XML, encontra todos os w:sdt e extrai metadados (tag/alias/id) e texto.
    """

    def extract(self, data: DOCXSdtExtractSchema) -> list[SdtInfo]:
        """
        Extrai SDTs a partir de:
        - data.input_docx: caminho do arquivo .docx em disco
        - data.input_content: bytes do .docx em memória

        Regras:
        - Você deve informar exatamente um: data.input_docx OU data.input_content.
        """
        if (data.input_docx is None and data.input_content is None) or (
            data.input_docx is not None and data.input_content is not None
        ):
            raise ValueError("Informe apenas data.input_docx OU data.input_content.")

        found: list[SdtInfo] = []

        # ------------------------------------------------------
        # Caso 1: lê de disco
        # ------------------------------------------------------
        if data.input_docx is not None:
            data.input_docx = Path(data.input_docx)

            with zipfile.ZipFile(data.input_docx, "r") as zin:
                for item in zin.infolist():
                    if not self._is_word_xml_part(item.filename):
                        continue

                    xml_bytes = zin.read(item.filename)
                    found.extend(self._extract_from_xml_part(item.filename, xml_bytes))

            return found

        # ------------------------------------------------------
        # Caso 2: lê de memória (bytes do DOCX)
        # ------------------------------------------------------
        from io import BytesIO

        with zipfile.ZipFile(BytesIO(data.input_content), "r") as zin:
            for item in zin.infolist():
                if not self._is_word_xml_part(item.filename):
                    continue

                xml_bytes = zin.read(item.filename)
                found.extend(self._extract_from_xml_part(item.filename, xml_bytes))

        return found

    def _is_word_xml_part(self, filename: str) -> bool:
        """Define quais XMLs do DOCX serão processados (conteúdo editável)."""
        if filename == "word/document.xml":
            return True
        if filename.startswith("word/header") and filename.endswith(".xml"):
            return True
        if filename.startswith("word/footer") and filename.endswith(".xml"):
            return True
        return False

    def _extract_from_xml_part(self, part_name: str, xml_bytes: bytes) -> list[SdtInfo]:
        root = etree.fromstring(xml_bytes)
        sdts = root.xpath(".//w:sdt", namespaces=NS)

        infos: list[SdtInfo] = []
        for sdt in sdts:
            tag_val, alias_val, id_val = self._read_sdt_pr(sdt)
            sdt_content = sdt.find(w("sdtContent"))

            is_block = bool(
                sdt_content is not None and sdt_content.find(w("p")) is not None
            )
            has_nested = bool(
                sdt_content is not None
                and len(sdt_content.xpath(".//w:sdt", namespaces=NS)) > 0
            )

            text = self._extract_sdt_text(sdt_content)

            infos.append(
                SdtInfo(
                    part=part_name,
                    tag=tag_val,
                    alias=alias_val,
                    sdt_id=id_val,
                    is_block=is_block,
                    has_nested_sdt=has_nested,
                    text=text,
                )
            )

        return infos

    def _read_sdt_pr(
        self, sdt: etree._Element
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Lê propriedades do SDT:
        - w:tag/@w:val
        - w:alias/@w:val
        - w:id/@w:val
        """
        sdtPr = sdt.find(w("sdtPr"))
        if sdtPr is None:
            return None, None, None

        def _get_val(el_name: str) -> Optional[str]:
            el = sdtPr.find(w(el_name))
            if el is None:
                return None
            return el.get(w("val"))

        return _get_val("tag"), _get_val("alias"), _get_val("id")

    def _extract_sdt_text(self, sdt_content: Optional[etree._Element]) -> str:
        """
        Extrai texto “legível” do SDT.

        Regras:
        - Se houver parágrafos (block-level): junta textos dos parágrafos com "\n"
        - Caso contrário (inline): extrai em ordem, respeitando w:br como quebra de linha
        """
        if sdt_content is None:
            return ""

        # Se o SDT tem parágrafos, tratamos como bloco (um parágrafo por linha)
        paragraphs = sdt_content.xpath("./w:p | .//w:p", namespaces=NS)
        if paragraphs:
            lines = [self._extract_paragraph_text(p) for p in paragraphs]
            # Remove excesso de vazios “puros”, mas preserva quebras relevantes
            return "\n".join(lines).strip("\n")

        # Inline: percorre runs e respeita w:br
        parts: list[str] = []
        for r in sdt_content.xpath(".//w:r", namespaces=NS):
            parts.append(self._extract_run_text(r))
        return "".join(parts)

    def _extract_paragraph_text(self, p: etree._Element) -> str:
        """Extrai texto de um parágrafo, respeitando runs e w:br."""
        parts: list[str] = []
        for r in p.xpath(".//w:r", namespaces=NS):
            parts.append(self._extract_run_text(r))
        return "".join(parts)

    def _extract_run_text(self, r: etree._Element) -> str:
        """
        Extrai texto de um run em ordem:
        - w:t -> texto
        - w:br -> "\n"
        Observação: mantemos a ordem dos nós dentro do run.
        """
        out: list[str] = []
        for node in list(r):
            if node.tag == w("t"):
                out.append(node.text or "")
            elif node.tag == w("br"):
                out.append("\n")
        # Alguns casos têm w:t em níveis mais profundos; fallback seguro:
        if not out:
            ts = r.xpath(".//w:t", namespaces=NS)
            out.append("".join((t.text or "") for t in ts))
        return "".join(out)
