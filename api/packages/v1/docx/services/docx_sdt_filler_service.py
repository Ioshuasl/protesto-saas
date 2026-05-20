import zipfile
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from uuid import uuid4

from lxml import etree

from packages.v1.resolver.schemas.resolver_schema import DOCXSdtFillerSchema

# Namespace do WordprocessingML (DOCX / Word XML)
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
# Namespace XML padrão (usado para xml:space="preserve")
XML_NS = "http://www.w3.org/XML/1998/namespace"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

# Mapa de namespaces para usar em XPath
NS = {"w": WORD_NS}


def w(tag: str) -> str:
    """
    Helper para montar tags/atributos com namespace do Word.
    Ex.: w("p") -> "{.../wordprocessingml/2006/main}p"
    """
    return f"{{{WORD_NS}}}{tag}"


def qn(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


@dataclass(frozen=True)
class DocxSdtFiller:
    """
    Preenche SDTs (Content Controls) dentro de um .docx, procurando principalmente por w:tag.

    Estratégia (mesma linha da classe que cria SDT):
    1) Abre o .docx como ZIP.
    2) Processa somente XMLs de conteúdo: document.xml, header*.xml, footer*.xml
    3) Em cada XML:
       - Localiza todos os w:sdt
       - Lê o identificador pelo w:sdtPr/w:tag/@w:val (recomendado)
       - (opcional) fallback para w:alias/@w:val
       - Se existir valor para aquela chave, substitui o conteúdo de w:sdtContent
    4) Regrava o ZIP de saída preservando os demais arquivos.

    O preenchimento troca o conteúdo do SDT por texto simples:
    - Se o SDT for "inline" (normalmente contém runs w:r), coloca o texto em um único run.
      Se houver quebras de linha, vira w:br dentro do run.
    - Se o SDT for "block" (normalmente contém parágrafos w:p), cria um w:p por linha.

    Observação:
    - Preserva o máximo possível de estilo copiando rPr (estilo do run) e pPr (estilo do parágrafo)
      de um elemento já existente dentro do SDT (quando disponível).
    """

    # Se True, aceita também preencher por alias quando não encontrar tag
    also_match_alias: bool = False
    # Se True, quando a chave não existir no dict, limpa o conteúdo do SDT (em vez de ignorar)
    clear_if_missing: bool = False

    def fill(self, data: DOCXSdtFillerSchema) -> dict | tuple[bytes, dict]:
        """
        Preenche os SDTs do DOCX.

        Fontes de entrada:
        - data.input_docx: caminho do .docx em disco
        - data.input_content: bytes do .docx em memória

        Saída:
        - data.save_to_disk=True:
            - data.output_docx é obrigatório
            - salva em disco e retorna apenas o resumo
        - data.save_to_disk=False:
            - NÃO salva em disco e retorna (bytes_docx_resultante, resumo)

        data.values: dict { "chave": "valor" }
          - Recomendado que a chave seja a mesma usada no w:tag/@w:val do SDT (ex.: "escrevente_nome").
          - Valores são convertidos para string.

        Retorna um resumo: { "filled": N, "cleared": M, "skipped": K }
        """
        if data.values is None:
            data.values = {}

        # ------------------------------------------------------
        # Validações de entrada/saída (disco vs memória)
        # ------------------------------------------------------
        if (data.input_docx is None and data.input_content is None) or (
            data.input_docx is not None and data.input_content is not None
        ):
            raise ValueError("Informe apenas data.input_docx OU data.input_content.")

        if data.save_to_disk and data.output_docx is None:
            raise ValueError(
                "data.output_docx é obrigatório quando data.save_to_disk=True"
            )

        data.input_docx = Path(data.input_docx) if data.input_docx is not None else None
        data.output_docx = (
            Path(data.output_docx) if data.output_docx is not None else None
        )

        # Converte valores para str por segurança/consistência, exceto payloads de imagem.
        values_norm: dict[str, object] = {}
        for key, value in data.values.items():
            if self._is_image_payload(value):
                values_norm[key] = value
            else:
                values_norm[key] = "" if value is None else str(value)

        summary = {"filled": 0, "cleared": 0, "skipped": 0}

        # ------------------------------------------------------
        # Abre o ZIP de entrada (disco ou memória)
        # ------------------------------------------------------
        if data.input_docx is not None:
            zin_ctx = zipfile.ZipFile(data.input_docx, "r")
        else:
            from io import BytesIO

            zin_ctx = zipfile.ZipFile(BytesIO(data.input_content), "r")

        with zin_ctx as zin:

            # ------------------------------------------------------
            # Saída em disco (comportamento original)
            # ------------------------------------------------------
            if data.save_to_disk:
                with zipfile.ZipFile(data.output_docx, "w") as zout:
                    files = {item.filename: zin.read(item.filename) for item in zin.infolist()}
                    files = self._process_parts_with_values(files, values_norm, summary)

                    for filename, file_content in files.items():
                        zout.writestr(filename, file_content)

                return summary

            # ------------------------------------------------------
            # Saída em memória (retorna bytes do DOCX final)
            # ------------------------------------------------------
            else:
                from io import BytesIO

                buffer = BytesIO()
                with zipfile.ZipFile(buffer, "w") as zout:
                    files = {item.filename: zin.read(item.filename) for item in zin.infolist()}
                    files = self._process_parts_with_values(files, values_norm, summary)

                    for filename, file_content in files.items():
                        zout.writestr(filename, file_content)

                return buffer.getvalue(), summary

    def _is_image_payload(self, value) -> bool:
        if not isinstance(value, dict):
            return False
        if value.get("__type__") != "image":
            return False
        image_bytes = value.get("bytes")
        return isinstance(image_bytes, (bytes, bytearray))

    def _rels_part_name(self, part_name: str) -> str:
        p = Path(part_name)
        return str(p.parent / "_rels" / f"{p.name}.rels").replace("\\", "/")

    def _empty_rels_xml(self) -> bytes:
        rels = etree.Element(qn(REL_NS, "Relationships"), nsmap={None: REL_NS})
        return etree.tostring(rels, xml_declaration=True, encoding="UTF-8", standalone="yes")

    def _next_rid(self, rels_root: etree._Element) -> str:
        max_id = 0
        for rel in rels_root.findall(qn(REL_NS, "Relationship")):
            rel_id = rel.get("Id", "")
            if rel_id.startswith("rId"):
                try:
                    max_id = max(max_id, int(rel_id[3:]))
                except ValueError:
                    continue
        return f"rId{max_id + 1}"

    def _next_docpr_id(self, xml_root: etree._Element) -> int:
        docpr_ids = []
        for docpr in xml_root.xpath(".//wp:docPr", namespaces={"wp": WP_NS}):
            try:
                docpr_ids.append(int(docpr.get("id", "0")))
            except ValueError:
                pass
        return (max(docpr_ids) + 1) if docpr_ids else 1

    def _content_type_for_ext(self, ext: str) -> str:
        ext = ext.lower()
        if ext == "png":
            return "image/png"
        if ext in ("jpg", "jpeg"):
            return "image/jpeg"
        if ext == "gif":
            return "image/gif"
        return "application/octet-stream"

    def _ensure_content_type(self, files: dict[str, bytes], ext: str) -> None:
        ct_name = "[Content_Types].xml"
        if ct_name not in files:
            return

        root = etree.fromstring(files[ct_name])
        exists = root.xpath(
            "./ct:Default[translate(@Extension,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')=$ext]",
            namespaces={"ct": CONTENT_TYPES_NS},
            ext=ext.lower(),
        )
        if exists:
            return

        default_el = etree.SubElement(root, qn(CONTENT_TYPES_NS, "Default"))
        default_el.set("Extension", ext.lower())
        default_el.set("ContentType", self._content_type_for_ext(ext))
        files[ct_name] = etree.tostring(
            root, xml_declaration=True, encoding="UTF-8", standalone="yes"
        )

    def _build_inline_drawing(self, rel_id: str, docpr_id: int) -> etree._Element:
        drawing = etree.Element(w("drawing"))
        inline = etree.SubElement(
            drawing,
            qn(WP_NS, "inline"),
            nsmap={"wp": WP_NS, "a": A_NS, "pic": PIC_NS, "r": R_NS},
        )
        inline.set("distT", "0")
        inline.set("distB", "0")
        inline.set("distL", "0")
        inline.set("distR", "0")

        # 120x120 px em EMU (aprox)
        etree.SubElement(inline, qn(WP_NS, "extent"), cx="1143000", cy="1143000")
        etree.SubElement(
            inline,
            qn(WP_NS, "effectExtent"),
            l="0",
            t="0",
            r="0",
            b="0",
        )
        etree.SubElement(
            inline,
            qn(WP_NS, "docPr"),
            id=str(docpr_id),
            name=f"QRCode {docpr_id}",
        )
        c_nv = etree.SubElement(inline, qn(WP_NS, "cNvGraphicFramePr"))
        etree.SubElement(c_nv, qn(A_NS, "graphicFrameLocks"), noChangeAspect="1")

        graphic = etree.SubElement(inline, qn(A_NS, "graphic"))
        graphic_data = etree.SubElement(
            graphic,
            qn(A_NS, "graphicData"),
            uri="http://schemas.openxmlformats.org/drawingml/2006/picture",
        )
        pic = etree.SubElement(graphic_data, qn(PIC_NS, "pic"))

        nv_pic_pr = etree.SubElement(pic, qn(PIC_NS, "nvPicPr"))
        etree.SubElement(
            nv_pic_pr, qn(PIC_NS, "cNvPr"), id="0", name=f"QRCode {docpr_id}"
        )
        etree.SubElement(nv_pic_pr, qn(PIC_NS, "cNvPicPr"))

        blip_fill = etree.SubElement(pic, qn(PIC_NS, "blipFill"))
        etree.SubElement(blip_fill, qn(A_NS, "blip"), {qn(R_NS, "embed"): rel_id})
        stretch = etree.SubElement(blip_fill, qn(A_NS, "stretch"))
        etree.SubElement(stretch, qn(A_NS, "fillRect"))

        sp_pr = etree.SubElement(pic, qn(PIC_NS, "spPr"))
        xfrm = etree.SubElement(sp_pr, qn(A_NS, "xfrm"))
        etree.SubElement(xfrm, qn(A_NS, "off"), x="0", y="0")
        etree.SubElement(xfrm, qn(A_NS, "ext"), cx="1143000", cy="1143000")
        prst_geom = etree.SubElement(sp_pr, qn(A_NS, "prstGeom"), prst="rect")
        etree.SubElement(prst_geom, qn(A_NS, "avLst"))

        return drawing

    def _process_parts_with_values(
        self, files: dict[str, bytes], values: dict[str, object], summary: dict
    ) -> dict[str, bytes]:
        media_to_add = {}

        for part_name in list(files.keys()):
            if not self._is_word_xml_part(part_name):
                continue

            rels_name = self._rels_part_name(part_name)
            rels_bytes = files.get(rels_name, self._empty_rels_xml())
            xml_bytes = files[part_name]

            xml_out, rels_out, part_summary, media_part = self._fill_xml_part(
                xml_bytes=xml_bytes,
                rels_bytes=rels_bytes,
                values=values,
            )

            files[part_name] = xml_out
            files[rels_name] = rels_out
            media_to_add.update(media_part)

            summary["filled"] += part_summary["filled"]
            summary["cleared"] += part_summary["cleared"]
            summary["skipped"] += part_summary["skipped"]

        for media_name, media_bytes in media_to_add.items():
            files[media_name] = media_bytes
            ext = Path(media_name).suffix.lstrip(".")
            if ext:
                self._ensure_content_type(files, ext)

        return files

    def _is_word_xml_part(self, filename: str) -> bool:
        """Define quais XMLs do DOCX serão processados."""
        if filename == "word/document.xml":
            return True
        if filename.startswith("word/header") and filename.endswith(".xml"):
            return True
        if filename.startswith("word/footer") and filename.endswith(".xml"):
            return True
        return False

    def _fill_xml_part(
        self, xml_bytes: bytes, rels_bytes: bytes, values: dict[str, object]
    ) -> tuple[bytes, bytes, dict, dict[str, bytes]]:
        """
        Preenche SDTs dentro de um XML do Word (document/header/footer).
        Retorna (xml_atualizado, resumo_local).
        """
        root = etree.fromstring(xml_bytes)
        rels_root = etree.fromstring(rels_bytes)
        changed = False
        rels_changed = False
        media_part: dict[str, bytes] = {}

        local = {"filled": 0, "cleared": 0, "skipped": 0}

        # Pega todos os SDTs (inline e block)
        sdts = root.xpath(".//w:sdt", namespaces=NS)

        for sdt in sdts:
            key = self._get_sdt_key(sdt)

            # Sem chave => não dá pra identificar de forma confiável
            if not key:
                local["skipped"] += 1
                continue

            if key in values:
                value = values[key]

                if self._is_image_payload(value):
                    image_format = str(value.get("format", "PNG")).lower()
                    media_basename = f"qr_{uuid4().hex}.{image_format}"
                    media_path = f"word/media/{media_basename}"
                    media_part[media_path] = bytes(value["bytes"])

                    rel_id = self._next_rid(rels_root)
                    rel = etree.SubElement(rels_root, qn(REL_NS, "Relationship"))
                    rel.set("Id", rel_id)
                    rel.set(
                        "Type",
                        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
                    )
                    rel.set("Target", f"media/{media_basename}")
                    rels_changed = True

                    docpr_id = self._next_docpr_id(root)
                    self._set_sdt_image(sdt, rel_id, docpr_id)
                else:
                    self._set_sdt_text(sdt, str(value))

                local["filled"] += 1
                changed = True
            else:
                if self.clear_if_missing:
                    self._set_sdt_text(sdt, "")
                    local["cleared"] += 1
                    changed = True
                else:
                    local["skipped"] += 1

        xml_out = xml_bytes
        if changed:
            xml_out = etree.tostring(
                root, xml_declaration=True, encoding="UTF-8", standalone="yes"
            )

        rels_out = rels_bytes
        if rels_changed:
            rels_out = etree.tostring(
                rels_root, xml_declaration=True, encoding="UTF-8", standalone="yes"
            )

        return xml_out, rels_out, local, media_part

    def _get_sdt_key(self, sdt: etree._Element) -> Optional[str]:
        """
        Extrai a chave do SDT.

        Ordem:
        1) w:sdtPr/w:tag/@w:val (recomendado)
        2) (opcional) w:sdtPr/w:alias/@w:val
        """
        sdtPr = sdt.find(w("sdtPr"))
        if sdtPr is None:
            return None

        tag_el = sdtPr.find(w("tag"))
        if tag_el is not None:
            v = tag_el.get(w("val"))
            if v:
                return v

        if self.also_match_alias:
            alias_el = sdtPr.find(w("alias"))
            if alias_el is not None:
                v = alias_el.get(w("val"))
                if v:
                    return v

        return None

    def _set_sdt_text(self, sdt: etree._Element, text: str) -> None:
        """
        Troca o conteúdo do SDT (w:sdtContent) por `text`, preservando o máximo possível:
        - Se for inline: escreve em w:r (quebras de linha viram w:br dentro do run)
        - Se for block: cria w:p por linha
        - Copia estilos (rPr/pPr) de elementos já existentes dentro do SDT, quando possível
        """
        sdtContent = sdt.find(w("sdtContent"))
        if sdtContent is None:
            return

        # Identifica se o SDT é "block-level" (possui parágrafos) ou "inline"
        is_block = bool(sdtContent.find(w("p")) is not None)

        # Captura amostras de estilo, se existirem, para manter aparência
        sample_p = sdtContent.find(".//" + w("p"))
        sample_r = sdtContent.find(".//" + w("r"))

        sample_pPr = sample_p.find(w("pPr")) if sample_p is not None else None
        sample_rPr = sample_r.find(w("rPr")) if sample_r is not None else None

        # Limpa todo o conteúdo existente do SDT
        for child in list(sdtContent):
            sdtContent.remove(child)

        if is_block:
            # Cada linha vira um parágrafo w:p (bom para SDT em tabelas, blocos etc.)
            lines = text.splitlines() or [""]
            for line in lines:
                p = etree.SubElement(sdtContent, w("p"))

                # Copia pPr para manter estilo do parágrafo (alinhamento, espaçamento etc.)
                if sample_pPr is not None:
                    p.append(deepcopy(sample_pPr))

                r = etree.SubElement(p, w("r"))

                # Copia rPr para manter estilo do texto (fonte, tamanho, negrito etc.)
                if sample_rPr is not None:
                    r.append(deepcopy(sample_rPr))

                t = etree.SubElement(r, w("t"))
                if line and (line[0].isspace() or line[-1].isspace()):
                    t.set(f"{{{XML_NS}}}space", "preserve")
                t.text = line
        else:
            # Inline: escreve tudo em um run, quebrando linhas com w:br (caso exista \n)
            r = etree.SubElement(sdtContent, w("r"))
            if sample_rPr is not None:
                r.append(deepcopy(sample_rPr))

            parts = text.split("\n")
            for i, part in enumerate(parts):
                if i > 0:
                    etree.SubElement(r, w("br"))

                t = etree.SubElement(r, w("t"))
                if part and (part[0].isspace() or part[-1].isspace()):
                    t.set(f"{{{XML_NS}}}space", "preserve")
                t.text = part

    def _set_sdt_image(self, sdt: etree._Element, rel_id: str, docpr_id: int) -> None:
        sdtContent = sdt.find(w("sdtContent"))
        if sdtContent is None:
            return

        is_block = bool(sdtContent.find(w("p")) is not None)
        sample_p = sdtContent.find(".//" + w("p"))
        sample_r = sdtContent.find(".//" + w("r"))
        sample_pPr = sample_p.find(w("pPr")) if sample_p is not None else None
        sample_rPr = sample_r.find(w("rPr")) if sample_r is not None else None

        for child in list(sdtContent):
            sdtContent.remove(child)

        if is_block:
            p = etree.SubElement(sdtContent, w("p"))
            if sample_pPr is not None:
                p.append(deepcopy(sample_pPr))
            r = etree.SubElement(p, w("r"))
        else:
            r = etree.SubElement(sdtContent, w("r"))

        if sample_rPr is not None:
            r.append(deepcopy(sample_rPr))

        drawing = self._build_inline_drawing(rel_id=rel_id, docpr_id=docpr_id)
        r.append(drawing)
