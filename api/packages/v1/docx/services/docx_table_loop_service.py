import re
import zipfile
from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from io import BytesIO
from pathlib import Path
from typing import Any, Optional

from lxml import etree

from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
)
from packages.v1.docx.schemas.docx_table_loop_schema import DOCXTableLoopSchema
from packages.v1.resolver.services.lista.resolver_lista_filler import ResolverListaFiller
from packages.v1.resolver.services.resolver_buscar_marcacao_service import (
    ResolverBuscarMarcacaoService,
)
from packages.v1.resolver.services.texto.resolver_texto_filler_service import (
    ResolverTextoFillerService,
)

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": WORD_NS}

FOR_MARKER_RE = re.compile(r"<!table_for:([A-Za-z0-9_]+)!>")
ENDFOR_MARKER_RE = re.compile(r"<!table_endfor(?::([A-Za-z0-9_]+))?!>")
MARKER_RE = re.compile(r"<![A-Za-z0-9_\.]+!>")


def w(tag: str) -> str:
    return f"{{{WORD_NS}}}{tag}"


@dataclass(frozen=True)
class TableLoopBlock:
    list_name: str
    start_index: int
    template_index: int
    end_index: int


class DOCXTableLoopService:
    def __init__(self):
        self._resolver_buscar_marcacao = None
        self._lista_filler = None
        self._texto_filler = None
        self._marcacao_cache: dict[str, Any] = {}
        self._valor_cache: dict[tuple[str, Any], str] = {}

    def execute(self, data: DOCXTableLoopSchema):
        self._validate_io(data)
        self._ensure_qualifier_dependencies(reset_cache=True)

        source_bytes = self._load_input_bytes(data)
        summary = {"loops_found": 0, "rows_generated": 0, "warnings": []}

        with zipfile.ZipFile(BytesIO(source_bytes), "r") as zin:
            files = {item.filename: zin.read(item.filename) for item in zin.infolist()}

        for part_name in list(files.keys()):
            if not self._is_word_xml_part(part_name):
                continue

            xml_out, part_summary = self._process_xml_part(
                xml_bytes=files[part_name],
                collections=data.collections,
                clear_when_empty=data.clear_when_empty,
                part_name=part_name,
            )
            files[part_name] = xml_out
            summary["loops_found"] += part_summary["loops_found"]
            summary["rows_generated"] += part_summary["rows_generated"]
            summary["warnings"].extend(part_summary["warnings"])

        result_bytes = self._build_docx_bytes(files)

        if data.save_to_disk:
            output_path = Path(str(data.output_docx)).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(result_bytes)
            return summary

        return result_bytes, summary

    def _validate_io(self, data: DOCXTableLoopSchema) -> None:
        has_input_docx = bool(data.input_docx)
        has_input_content = data.input_content is not None

        if has_input_docx == has_input_content:
            raise ValueError("Informe apenas input_docx ou input_content.")

        if data.save_to_disk and not data.output_docx:
            raise ValueError("output_docx e obrigatorio quando save_to_disk=True.")

        if has_input_docx:
            input_path = Path(str(data.input_docx)).resolve()
            if not input_path.exists():
                raise ValueError(f"Arquivo de entrada nao encontrado: {input_path}")

    def _load_input_bytes(self, data: DOCXTableLoopSchema) -> bytes:
        if data.input_content is not None:
            return bytes(data.input_content)
        return Path(str(data.input_docx)).resolve().read_bytes()

    def _build_docx_bytes(self, files: dict[str, bytes]) -> bytes:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w") as zout:
            for filename, file_content in files.items():
                zout.writestr(filename, file_content)
        return buffer.getvalue()

    def _process_xml_part(
        self,
        xml_bytes: bytes,
        collections: dict[str, list[Any]],
        clear_when_empty: bool,
        part_name: str,
    ) -> tuple[bytes, dict[str, Any]]:
        root = etree.fromstring(xml_bytes)
        tables = root.xpath(".//w:tbl", namespaces=NS)
        changed = False
        part_summary = {"loops_found": 0, "rows_generated": 0, "warnings": []}

        for table_index, table in enumerate(tables):
            blocks = self._find_table_loop_blocks(
                table=table,
                part_name=part_name,
                table_index=table_index,
            )
            if not blocks:
                continue

            part_summary["loops_found"] += len(blocks)

            for block in reversed(blocks):
                if block.list_name not in collections:
                    raise ValueError(
                        "Colecao nao encontrada para loop "
                        f"'{block.list_name}' em {part_name}, tabela {table_index}."
                    )

                raw_items = collections.get(block.list_name, [])
                generated_rows = self._generate_rows_for_block(
                    table=table,
                    block=block,
                    items=list(raw_items or []),
                    clear_when_empty=clear_when_empty,
                    summary=part_summary,
                    part_name=part_name,
                    table_index=table_index,
                )

                part_summary["rows_generated"] += len(generated_rows)
                self._replace_block_rows(table=table, block=block, generated_rows=generated_rows)
                changed = True

        if not changed:
            return xml_bytes, part_summary

        return (
            etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"),
            part_summary,
        )

    def _is_word_xml_part(self, filename: str) -> bool:
        if filename == "word/document.xml":
            return True
        if filename.startswith("word/header") and filename.endswith(".xml"):
            return True
        if filename.startswith("word/footer") and filename.endswith(".xml"):
            return True
        return False

    def _find_table_loop_blocks(
        self,
        table: etree._Element,
        part_name: str,
        table_index: int,
    ) -> list[TableLoopBlock]:
        rows = table.xpath("./w:tr", namespaces=NS)
        blocks: list[TableLoopBlock] = []
        idx = 0

        while idx < len(rows):
            row_text = self._extract_row_text(rows[idx]).strip()
            for_match = FOR_MARKER_RE.search(row_text)
            end_match = ENDFOR_MARKER_RE.search(row_text)

            if for_match:
                if end_match:
                    raise ValueError(
                        "Linha de controle invalida com for e endfor juntos em "
                        f"{part_name}, tabela {table_index}, linha {idx}."
                    )

                list_name = for_match.group(1)
                template_index = idx + 1
                end_index = idx + 2

                if template_index >= len(rows) or end_index >= len(rows):
                    raise ValueError(
                        "Bloco de loop incompleto em "
                        f"{part_name}, tabela {table_index}, linha {idx}."
                    )

                end_row_text = self._extract_row_text(rows[end_index]).strip()
                end_control = ENDFOR_MARKER_RE.search(end_row_text)
                if not end_control:
                    raise ValueError(
                        "Loop de tabela exige uma linha-template e um endfor na linha seguinte em "
                        f"{part_name}, tabela {table_index}, linha {idx}."
                    )

                end_name = end_control.group(1)
                if end_name and end_name != list_name:
                    raise ValueError(
                        "Nome da colecao no endfor nao corresponde ao table_for em "
                        f"{part_name}, tabela {table_index}, linha {idx}."
                    )

                blocks.append(
                    TableLoopBlock(
                        list_name=list_name,
                        start_index=idx,
                        template_index=template_index,
                        end_index=end_index,
                    )
                )
                idx = end_index + 1
                continue

            if end_match:
                raise ValueError(
                    "table_endfor encontrado sem table_for em "
                    f"{part_name}, tabela {table_index}, linha {idx}."
                )

            idx += 1

        return blocks

    def _extract_row_text(self, row: etree._Element) -> str:
        texts = row.xpath(".//w:t", namespaces=NS)
        raw = "".join((text_node.text or "") for text_node in texts)
        return self._sanitize_marker_text(raw)

    def _generate_rows_for_block(
        self,
        table: etree._Element,
        block: TableLoopBlock,
        items: list[Any],
        clear_when_empty: bool,
        summary: dict[str, Any],
        part_name: str,
        table_index: int,
    ) -> list[etree._Element]:
        rows = table.xpath("./w:tr", namespaces=NS)
        template_row = rows[block.template_index]

        if not items:
            if clear_when_empty:
                return []

            summary["warnings"].append(
                "Colecao vazia para loop "
                f"'{block.list_name}' em {part_name}, tabela {table_index}. Linha-template mantida."
            )
            row_copy = deepcopy(template_row)
            self._replace_item_placeholders_in_row(row_copy, item={}, item_id=None)
            return [row_copy]

        generated_rows: list[etree._Element] = []
        for item in items:
            row_copy = deepcopy(template_row)
            item_id = self._extract_item_id(item)
            self._replace_item_placeholders_in_row(row_copy, item=item, item_id=item_id)
            generated_rows.append(row_copy)
        return generated_rows

    def _extract_item_id(self, item: Any):
        if isinstance(item, dict):
            for key in ("servico_itempedido_id", "id", "campo_id_valor", "value"):
                if item.get(key) is not None:
                    return item.get(key)
            return None

        if isinstance(item, (str, int, float, Decimal)):
            return item

        for attr in ("servico_itempedido_id", "id", "campo_id_valor", "value"):
            value = getattr(item, attr, None)
            if value is not None:
                return value
        return None

    def _replace_block_rows(
        self,
        table: etree._Element,
        block: TableLoopBlock,
        generated_rows: list[etree._Element],
    ) -> None:
        rows = table.xpath("./w:tr", namespaces=NS)
        start_row = rows[block.start_index]
        rows_to_remove = rows[block.start_index : block.end_index + 1]
        insert_at = table.index(start_row)

        for row in generated_rows:
            table.insert(insert_at, row)
            insert_at += 1

        for row in rows_to_remove:
            if row.getparent() is table:
                table.remove(row)

    def _replace_item_placeholders_in_row(
        self,
        row: etree._Element,
        item: Any,
        item_id: Any,
    ) -> None:
        self._replace_item_sdt_placeholders_in_row(row, item, item_id)
        paragraphs = row.xpath(".//w:p", namespaces=NS)
        for paragraph in paragraphs:
            self._replace_item_placeholders_in_paragraph(paragraph, item, item_id)

    def _replace_item_sdt_placeholders_in_row(
        self,
        row: etree._Element,
        item: Any,
        item_id: Any,
    ) -> None:
        sdts = row.xpath(".//w:sdt", namespaces=NS)
        for sdt in sdts:
            marker_token = self._get_sdt_tag(sdt)
            if not self._is_loop_data_marker(marker_token):
                continue

            value = self._resolve_marker_value(marker_token, item, item_id)
            self._set_sdt_text(sdt, value)

    def _get_sdt_tag(self, sdt: etree._Element) -> Optional[str]:
        sdt_pr = sdt.find(w("sdtPr"))
        if sdt_pr is None:
            return None

        tag_el = sdt_pr.find(w("tag"))
        if tag_el is None:
            return None

        return tag_el.get(w("val"))

    def _set_sdt_text(self, sdt: etree._Element, text: str) -> None:
        sdt_content = sdt.find(w("sdtContent"))
        if sdt_content is None:
            return

        is_block = bool(sdt_content.find(w("p")) is not None)
        sample_p = sdt_content.find(".//" + w("p"))
        sample_r = sdt_content.find(".//" + w("r"))
        sample_p_pr = sample_p.find(w("pPr")) if sample_p is not None else None
        sample_r_pr = sample_r.find(w("rPr")) if sample_r is not None else None

        for child in list(sdt_content):
            sdt_content.remove(child)

        if is_block:
            for line in text.splitlines() or [""]:
                p = etree.SubElement(sdt_content, w("p"))
                if sample_p_pr is not None:
                    p.append(deepcopy(sample_p_pr))
                r = etree.SubElement(p, w("r"))
                if sample_r_pr is not None:
                    r.append(deepcopy(sample_r_pr))
                t = etree.SubElement(r, w("t"))
                if line and (line[0].isspace() or line[-1].isspace()):
                    t.set(f"{{{XML_NS}}}space", "preserve")
                t.text = line
            return

        r = etree.SubElement(sdt_content, w("r"))
        if sample_r_pr is not None:
            r.append(deepcopy(sample_r_pr))

        parts = text.split("\n")
        for index, part in enumerate(parts):
            if index > 0:
                etree.SubElement(r, w("br"))
            t = etree.SubElement(r, w("t"))
            if part and (part[0].isspace() or part[-1].isspace()):
                t.set(f"{{{XML_NS}}}space", "preserve")
            t.text = part

    def _replace_item_placeholders_in_paragraph(
        self,
        paragraph: etree._Element,
        item: Any,
        item_id: Any,
    ) -> None:
        runs = paragraph.xpath("./w:r", namespaces=NS)
        if not runs:
            return

        run_texts = [self._run_text(run) for run in runs]
        full_text = "".join(run_texts)
        matches = [
            match for match in MARKER_RE.finditer(full_text) if self._is_loop_data_marker(match.group(0))
        ]

        if not matches:
            return

        for match in reversed(matches):
            runs = paragraph.xpath("./w:r", namespaces=NS)
            run_texts = [self._run_text(run) for run in runs]

            marker_token = match.group(0)
            start, end = match.span()
            start_run_index, start_offset = self._index_to_runpos(run_texts, start)
            end_run_index, end_offset = self._index_to_runpos(run_texts, end)

            if start_run_index is None or end_run_index is None:
                continue
            if start_run_index >= len(runs) or end_run_index >= len(runs):
                continue

            start_run = runs[start_run_index]
            end_run = runs[end_run_index]
            prefix = run_texts[start_run_index][:start_offset]
            suffix = run_texts[end_run_index][end_offset:]
            value = self._resolve_marker_value(marker_token, item, item_id)

            try:
                insert_at = paragraph.index(start_run)
            except ValueError:
                continue

            for i in range(start_run_index, end_run_index + 1):
                run_to_remove = runs[i]
                if run_to_remove.getparent() is paragraph:
                    paragraph.remove(run_to_remove)

            nodes_to_insert = []
            if prefix:
                nodes_to_insert.append(self._make_text_run(start_run, prefix))

            nodes_to_insert.append(self._make_text_run(start_run, value))

            if suffix:
                nodes_to_insert.append(self._make_text_run(end_run, suffix))

            for offset, node in enumerate(nodes_to_insert):
                paragraph.insert(insert_at + offset, node)

    def _run_text(self, run: etree._Element) -> str:
        texts = run.xpath(".//w:t", namespaces=NS)
        raw = "".join((text_node.text or "") for text_node in texts)
        return self._sanitize_marker_text(raw)

    def _index_to_runpos(
        self,
        run_texts: list[str],
        index: int,
    ) -> tuple[Optional[int], Optional[int]]:
        acc = 0
        for run_index, run_text in enumerate(run_texts):
            next_acc = acc + len(run_text)
            if index < next_acc:
                return run_index, index - acc
            if index == next_acc:
                acc = next_acc
                continue
            acc = next_acc

        if index == acc and run_texts:
            return len(run_texts) - 1, len(run_texts[-1])
        return None, None

    def _make_text_run(self, sample_run: etree._Element, text: str) -> etree._Element:
        run = etree.Element(w("r"))
        run_props = sample_run.find(w("rPr"))
        if run_props is not None:
            run.append(deepcopy(run_props))

        text_node = etree.SubElement(run, w("t"))
        if text and (text[0].isspace() or text[-1].isspace()):
            text_node.set(f"{{{XML_NS}}}space", "preserve")
        text_node.text = text
        return run

    def _resolve_marker_value(self, marker_token: str, item: Any, item_id: Any) -> str:
        direct_value = self._resolve_direct_item_value(item, marker_token)
        if direct_value is not None:
            return direct_value

        if item_id is None:
            return ""

        cache_key = (marker_token, item_id)
        if cache_key in self._valor_cache:
            return self._valor_cache[cache_key]

        value = self._qualify_marker_token(marker_token, item_id)
        self._valor_cache[cache_key] = value
        return value

    def _resolve_direct_item_value(self, item: Any, marker_token: str) -> Optional[str]:
        if not isinstance(item, dict):
            return None

        field_name = self._extract_field_name_from_marker(marker_token)
        if field_name and field_name in item:
            return self._to_text_value(item.get(field_name))

        marker_core = marker_token[2:-2]
        if marker_core in item:
            return self._to_text_value(item.get(marker_core))

        return None

    def _extract_field_name_from_marker(self, marker_token: str) -> Optional[str]:
        if marker_token.startswith("<!item.") and marker_token.endswith("!>"):
            return marker_token[len("<!item.") : -2]
        if marker_token.startswith("<!item_") and marker_token.endswith("!>"):
            return marker_token[len("<!item_") : -2]
        return None

    def _qualify_marker_token(self, marker_token: str, item_id: Any) -> str:
        self._ensure_qualifier_dependencies(reset_cache=False)

        for marker_name in self._candidate_marker_names(marker_token):
            marcacao = self._get_marcacao(marker_name)
            if not marcacao:
                continue

            if getattr(marcacao, "texto", None):
                marcacao.texto.campo_id_valor = item_id

            marker_type = getattr(marcacao, "tipo_valor", None)
            if marker_type == "L":
                return self._to_text_value(self._lista_filler.execute(marcacao))
            if marker_type == "T":
                return self._to_text_value(self._texto_filler.execute(marcacao))

        return ""

    def _candidate_marker_names(self, marker_token: str) -> list[str]:
        names = [marker_token]
        core_name = marker_token[2:-2]
        names.append(core_name)

        if marker_token.startswith("<!item.") and marker_token.endswith("!>"):
            item_suffix = marker_token[len("<!item.") : -2]
            names.append(f"<!{item_suffix}!>")
            names.append(item_suffix)

            if item_suffix.startswith("item_"):
                stripped = item_suffix[len("item_") :]
                names.append(f"<!{stripped}!>")
                names.append(stripped)

        return names

    def _is_loop_data_marker(self, marker_token: Optional[str]) -> bool:
        if not marker_token:
            return False
        if not MARKER_RE.fullmatch(marker_token):
            return False
        if FOR_MARKER_RE.fullmatch(marker_token):
            return False
        if ENDFOR_MARKER_RE.fullmatch(marker_token):
            return False
        return True

    def _get_marcacao(self, marker_name: str):
        if marker_name in self._marcacao_cache:
            return self._marcacao_cache[marker_name]

        try:
            marcacao = self._resolver_buscar_marcacao.execute(
                GMarcacaoTipoNomeSchema(nome=marker_name, sistema_id=2)
            )
        except Exception:
            marcacao = None

        self._marcacao_cache[marker_name] = marcacao
        return marcacao

    def _to_text_value(self, value: Any) -> str:
        if isinstance(value, dict) and value.get("__type__") == "image":
            return ""
        return "" if value is None else str(value)

    def _sanitize_marker_text(self, text: str) -> str:
        if not text:
            return ""

        return (
            text.replace("\u00ad", "")
            .replace("\u200b", "")
            .replace("\ufeff", "")
        )

    def _ensure_qualifier_dependencies(self, reset_cache: bool) -> None:
        if self._resolver_buscar_marcacao is None:
            self._resolver_buscar_marcacao = ResolverBuscarMarcacaoService()
        if self._lista_filler is None:
            self._lista_filler = ResolverListaFiller()
        if self._texto_filler is None:
            self._texto_filler = ResolverTextoFillerService()

        if reset_cache:
            self._marcacao_cache = {}
            self._valor_cache = {}
