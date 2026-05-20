import re
import zipfile
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from lxml import etree

from packages.v1.resolver.schemas.resolver_schema import DOCXSdtConvertSchema

# Namespace do WordprocessingML (DOCX / Word XML)
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
# Namespace XML padrão (usado para xml:space="preserve")
XML_NS = "http://www.w3.org/XML/1998/namespace"

# Mapa de namespaces para usar em XPath
NS = {"w": WORD_NS}


def w(tag: str) -> str:
    """
    Helper para montar tags com namespace do Word.
    Ex.: w("p") -> "{.../wordprocessingml/2006/main}p"
    Isso evita lidar com prefixo "w:" diretamente ao criar elementos.
    """
    return f"{{{WORD_NS}}}{tag}"


@dataclass(frozen=True)
class DocxMarkerToSdtConverter:
    """
    Converte marcações do tipo <!chave!> em SDT (Structured Document Tag / Content Control).

    O que é SDT?
    - É um "content control" do Word.
    - Permite que você marque um trecho com metadados (tag/alias) para depois localizar,
      preencher, proteger, etc.

    Como a conversão é feita (alto nível):
    1) Abre o .docx como um ZIP.
    2) Para cada XML relevante (document, headers, footers), percorre parágrafos.
    3) Em cada parágrafo, concatena o texto dos runs (w:r / w:t) e procura por <!...!>.
    4) Para cada marcação encontrada, remove os runs correspondentes e substitui por:
       - (prefixo antes da marcação) run normal
       - SDT com tag/alias = chave
       - (sufixo depois da marcação) run normal

    Observação importante:
    - Este conversor assume o caso mais comum em templates: a marcação aparece em texto "corrente"
      dentro de parágrafos (w:p) e em runs (w:r). Se o Word fragmentar demais o texto, ainda funciona
      porque mapeamos o índice global -> posição de run/offset.
    """

    # Regex padrão: captura a chave dentro de <! ... !>
    marker_regex: str = r"<!([A-Za-z0-9_]+)!>"
    # Se True, mantém o texto original (ex.: "<!escrevente_nome!>") dentro do SDT.
    # Se False, cria SDT com texto vazio (e você preenche depois).
    keep_marker_text: bool = True

    def convert(self, data: DOCXSdtConvertSchema) -> Optional[bytes]:
        """
        Executa a conversão em um arquivo .docx.

        - data.input_docx: caminho do docx original (contém marcações <!chave!>)
        - data.output_docx: caminho do docx final (marcações viram SDT)
        - data.save_to_disk:
            - True  -> salva em disco (comportamento padrão) e retorna None
            - False -> NÃO salva em disco e retorna os bytes do DOCX resultante

        Observações:
        - Quando data.save_to_disk=True, data.output_docx é obrigatório.
        - Quando data.save_to_disk=False, data.output_docx é ignorado.
        """
        data.input_docx = Path(data.input_docx)
        data.output_docx = (
            Path(data.output_docx) if data.output_docx is not None else None
        )

        if data.save_to_disk and data.output_docx is None:
            raise ValueError(
                "data.output_docx é obrigatório quando data.save_to_disk=True"
            )

        # Compila o regex uma única vez para eficiência
        marker_re = re.compile(self.marker_regex)

        # Um .docx é um arquivo ZIP com vários XMLs internos
        with zipfile.ZipFile(data.input_docx, "r") as zin:

            # Se for salvar em disco, escreve diretamente no ZIP de saída
            if data.save_to_disk:
                with zipfile.ZipFile(data.output_docx, "w") as zout:

                    # Itera por todos os itens do ZIP (XMLs, imagens, rels, etc.)
                    for item in zin.infolist():
                        data = zin.read(item.filename)

                        # Só alteramos os XMLs de conteúdo do Word:
                        # - word/document.xml (principal)
                        # - word/header*.xml e word/footer*.xml (cabeçalhos/rodapés)
                        if self._is_word_xml_part(item.filename):
                            data = self._convert_xml_part(data, marker_re)

                        # Escreve de volta no ZIP de saída (alterado ou não)
                        zout.writestr(item, data)

                return None

            # Caso contrário, gera o DOCX em memória e retorna bytes
            else:
                from io import BytesIO

                buffer = BytesIO()
                with zipfile.ZipFile(buffer, "w") as zout:

                    # Itera por todos os itens do ZIP (XMLs, imagens, rels, etc.)
                    for item in zin.infolist():
                        data = zin.read(item.filename)

                        # Só alteramos os XMLs de conteúdo do Word:
                        # - word/document.xml (principal)
                        # - word/header*.xml e word/footer*.xml (cabeçalhos/rodapés)
                        if self._is_word_xml_part(item.filename):
                            data = self._convert_xml_part(data, marker_re)

                        # Escreve de volta no ZIP de saída (alterado ou não)
                        zout.writestr(item, data)

                return buffer.getvalue()

    def _is_word_xml_part(self, filename: str) -> bool:
        """
        Define quais partes do DOCX (ZIP) devem ser processadas.

        Motivação:
        - As marcações podem existir no corpo (document.xml), cabeçalho e rodapé.
        - Outras partes (estilos, numbering, rels, etc.) não precisam ser processadas.
        """
        if filename == "word/document.xml":
            return True
        if filename.startswith("word/header") and filename.endswith(".xml"):
            return True
        if filename.startswith("word/footer") and filename.endswith(".xml"):
            return True
        return False

    def _convert_xml_part(self, xml_bytes: bytes, marker_re: re.Pattern) -> bytes:
        """
        Converte uma parte XML do Word (document/header/footer).

        Passos:
        1) Parseia o XML em árvore (lxml).
        2) Percorre cada parágrafo (w:p).
        3) Em cada parágrafo, tenta localizar marcações e substituir por SDT.
        4) Se nada mudar, retorna o XML original (evita reserializar desnecessariamente).
        """
        root = etree.fromstring(xml_bytes)
        changed = False

        # Percorre todos os parágrafos na parte atual
        for p in root.xpath(".//w:p", namespaces=NS):
            changed |= self._convert_paragraph_markers(p, marker_re)

        # Se não houve alterações, retorna o original (mais rápido e preserva bytes exatos)
        if not changed:
            return xml_bytes

        # Serializa de volta para bytes com cabeçalho XML
        return etree.tostring(
            root,
            xml_declaration=True,
            encoding="UTF-8",
            standalone="yes",
        )

    def _convert_paragraph_markers(
        self, p: etree._Element, marker_re: re.Pattern
    ) -> bool:
        """
        Converte marcações dentro de um parágrafo (w:p).

        Estratégia:
        - Obtém os runs diretos do parágrafo (w:r).
        - Extrai o texto de cada run e concatena para formar uma string completa do parágrafo.
        - Busca todas as ocorrências de <!chave!> nessa string completa.
        - Processa de trás para frente (direita -> esquerda) para não invalidar índices ao editar.
        - Para cada ocorrência:
            * Localiza o run e offset de início e fim
            * Remove os runs envolvidos
            * Insere prefixo (run), SDT, sufixo (run) no lugar correto
        """
        # Runs diretos do parágrafo (o caso mais comum em templates)
        runs = p.xpath("./w:r", namespaces=NS)
        if not runs:
            return False

        # Texto de cada run, na ordem
        run_texts = [self._run_text(r) for r in runs]

        # Texto total do parágrafo (concatenação)
        full_text = "".join(run_texts)

        # Todas as marcações do tipo <!...!>
        matches = list(marker_re.finditer(full_text))
        if not matches:
            return False

        # Processar reverso é crucial:
        # - Se processarmos do começo, ao remover/inserir runs, os índices mudam
        # - No reverso, índices anteriores continuam válidos
        for m in reversed(matches):

            # 🔒 Recalcula runs e textos (DOM é mutável)
            runs = p.xpath("./w:r", namespaces=NS)
            run_texts = [self._run_text(r) for r in runs]

            key = m.group(1)  # chave interna: escrevente_nome, selo_agrupador, etc.
            marker_text = m.group(0)  # texto completo: "<!escrevente_nome!>"
            start, end = m.span()  # posições no texto concatenado do parágrafo

            # Converte índice absoluto (start/end) em (índice do run, offset dentro do run)
            sr, so = self._index_to_runpos(run_texts, start)
            er, eo = self._index_to_runpos(run_texts, end)

            # Se não conseguiu mapear (caso anômalo), ignora
            if sr is None or er is None:
                continue

            if sr >= len(runs) or er >= len(runs):
                continue

            start_run = runs[sr]
            end_run = runs[er]

            # Parte de texto do run inicial antes da marcação
            prefix = run_texts[sr][:so]
            # Parte de texto do run final depois da marcação
            suffix = run_texts[er][eo:]

            # Posição onde vamos inserir os elementos (onde estava o start_run)
            try:
                insert_at = p.index(start_run)
            except ValueError:
                continue

            # Remove todos os runs que cobrem a marcação (inclusive)
            # Ex.: se a marcação "cortou" múltiplos runs, remove sr..er
            for i in range(sr, er + 1):
                r = runs[i]
                if r.getparent() is p:
                    p.remove(r)

            # Monta a lista de nós a inserir na posição original:
            # - prefixo (se houver)
            # - SDT
            # - sufixo (se houver)
            to_insert: list[etree._Element] = []

            if prefix:
                # Cria um run normal com o prefixo e copia formatação do run original
                to_insert.append(self._make_text_run(start_run, prefix))

            # Cria o SDT com tag/alias = TEXTO COMPLETO DA MARCAÇÃO
            sdt = self._build_sdt(
                key=marker_text,
                sample_run=start_run,
                display_text=(marker_text if self.keep_marker_text else ""),
            )
            to_insert.append(sdt)

            if suffix:
                # Cria run normal com sufixo e copia formatação do run final
                to_insert.append(self._make_text_run(end_run, suffix))

            # Insere na árvore XML (no local correto dentro do parágrafo)
            for offset, el in enumerate(to_insert):
                p.insert(insert_at + offset, el)

        return True

    def _run_text(self, r: etree._Element) -> str:
        """
        Extrai o texto de um run (w:r).

        Observação:
        - O texto pode estar em um ou vários w:t dentro do run (Word pode quebrar).
        - Somamos todos os w:t para formar o texto do run.
        """
        ts = r.xpath(".//w:t", namespaces=NS)
        return "".join((t.text or "") for t in ts)

    def _index_to_runpos(
        self, run_texts: list[str], index: int
    ) -> tuple[Optional[int], Optional[int]]:
        """
        Converte um índice absoluto (na string full_text do parágrafo) em:
        - (run_index, offset_in_run)

        Por quê?
        - As marcações são encontradas na string concatenada.
        - Para editar o XML, precisamos saber em quais runs e offsets a marcação começa/termina.

        Regra de borda (index exatamente na "divisa" entre runs):
        - Se index == fim de um run, ele "cai" no próximo run (offset 0),
          para evitar cortar o run anterior desnecessariamente.
        """
        acc = 0
        for i, txt in enumerate(run_texts):
            nxt = acc + len(txt)

            # Index está dentro do run i
            if index < nxt:
                return i, index - acc

            # Index caiu exatamente no final do run i: seguimos
            if index == nxt:
                acc = nxt
                continue

            # Caso geral: avança acumulador
            acc = nxt

        # Se index for exatamente o comprimento total, aponta para o fim do último run
        if index == acc and run_texts:
            return len(run_texts) - 1, len(run_texts[-1])

        # Não foi possível mapear
        return None, None

    def _make_text_run(self, sample_run: etree._Element, text: str) -> etree._Element:
        """
        Cria um run (w:r) com um texto simples (w:t), copiando a formatação (w:rPr)
        de um run de amostra.

        Isso é importante para:
        - manter negrito/itálico/fonte/tamanho/cor etc. do documento original
        - evitar que prefixo/sufixo percam estilo ao serem re-inseridos
        """
        r = etree.Element(w("r"))

        # Copia propriedades de run (formatação), se existirem
        rPr = sample_run.find(w("rPr"))
        if rPr is not None:
            r.append(deepcopy(rPr))

        # Cria nó de texto (w:t)
        t = etree.SubElement(r, w("t"))

        # Se o texto começa/termina com espaços, preserva (Word costuma colapsar)
        if text and (text[0].isspace() or text[-1].isspace()):
            t.set(f"{{{XML_NS}}}space", "preserve")

        t.text = text
        return r

    def _build_sdt(
        self, key: str, sample_run: etree._Element, display_text: str
    ) -> etree._Element:
        """
        Cria um SDT (Structured Document Tag / Content Control) do Word.

        Estrutura base:
        <w:sdt>
          <w:sdtPr>
            <w:tag w:val="KEY" />
            <w:alias w:val="KEY" />
          </w:sdtPr>
          <w:sdtContent>
            <w:r> ... <w:t>...</w:t> ... </w:r>
          </w:sdtContent>
        </w:sdt>

        - tag e alias são úteis para localizar o controle depois.
        - O conteúdo textual inicial pode ser a própria marcação (debug/template) ou vazio.
        - Copiamos rPr (estilo) do run de amostra para manter aparência.
        """
        sdt = etree.Element(w("sdt"))

        # Propriedades do SDT (metadados do content control)
        sdtPr = etree.SubElement(sdt, w("sdtPr"))

        # tag = TEXTO COMPLETO DA MARCAÇÃO
        etree.SubElement(sdtPr, w("tag"), {w("val"): key})

        # alias = TEXTO COMPLETO DA MARCAÇÃO
        etree.SubElement(sdtPr, w("alias"), {w("val"): key})

        # Conteúdo do SDT (onde fica o texto / runs)
        sdtContent = etree.SubElement(sdt, w("sdtContent"))

        # Criamos um run dentro do SDT para armazenar o texto inicial
        r = etree.SubElement(sdtContent, w("r"))

        # Copia estilo do run de amostra para manter a mesma formatação visual
        rPr = sample_run.find(w("rPr"))
        if rPr is not None:
            r.append(deepcopy(rPr))

        # Texto do SDT
        t = etree.SubElement(r, w("t"))

        # Preserva espaços extremos, se houver
        if display_text and (display_text[0].isspace() or display_text[-1].isspace()):
            t.set(f"{{{XML_NS}}}space", "preserve")

        t.text = display_text
        return sdt
