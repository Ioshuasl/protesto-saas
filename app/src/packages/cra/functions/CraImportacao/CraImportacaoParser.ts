import type {
  CraRemessaHeader,
  CraRemessaImportResult,
  CraRemessaParsed,
  CraRemessaTrailer,
  CraRemessaTransacao,
  CraRemessaValidationIssue,
} from "./CraImportacaoTypes";

const REMESSA_LAYOUT_VERSION = "043";
const REMESSA_LINE_SIZE = 600;

function field(line: string, from: number, to: number): string {
  return line.slice(from - 1, to);
}

function normalizeLines(content: string): string[] {
  return content
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .split("\n")
    .filter((line) => line.trim().length > 0);
}

function onlyDigits(value: string): string {
  return value.replace(/\D/g, "");
}

function parseNumber(value: string): number {
  const digits = onlyDigits(value);
  if (!digits) return 0;
  return Number.parseInt(digits, 10);
}

function parseDate(value: string): string {
  const digits = onlyDigits(value);
  if (digits.length !== 8) return "";
  const day = digits.slice(0, 2);
  const month = digits.slice(2, 4);
  const year = digits.slice(4, 8);
  return `${year}-${month}-${day}`;
}

function pushError(
  errors: CraRemessaValidationIssue[],
  code: string,
  message: string,
  line?: number,
) {
  errors.push({ code, message, line });
}

function pushWarning(
  warnings: CraRemessaValidationIssue[],
  code: string,
  message: string,
  line?: number,
) {
  warnings.push({ code, message, line });
}

function validateLineSize(lines: string[], errors: CraRemessaValidationIssue[]) {
  lines.forEach((line, index) => {
    if (line.length !== REMESSA_LINE_SIZE) {
      pushError(
        errors,
        "invalid_line_size",
        `A linha ${index + 1} possui ${line.length} caracteres. O layout CRA exige 600.`,
        index + 1,
      );
    }
  });
}

function parseHeader(line: string): CraRemessaHeader {
  return {
    idRegistro: field(line, 1, 1),
    codigoPortador: field(line, 2, 4),
    nomePortador: field(line, 5, 44).trim(),
    dataMovimento: parseDate(field(line, 45, 52)),
    remetente: field(line, 53, 55).trim(),
    destinatario: field(line, 56, 58).trim(),
    tipoTransacao: field(line, 59, 61).trim(),
    sequenciaRemessa: parseNumber(field(line, 62, 67)),
    quantidadeRegistros: parseNumber(field(line, 68, 71)),
    quantidadeTitulos: parseNumber(field(line, 72, 75)),
    quantidadeIndicacoes: parseNumber(field(line, 76, 79)),
    quantidadeOriginais: parseNumber(field(line, 80, 83)),
    versaoLayout: field(line, 90, 92).trim(),
    codigoIbgeMunicipio: field(line, 93, 99).trim(),
    sequenciaRegistro: parseNumber(field(line, 597, 600)),
  };
}

function parseTransacao(line: string, lineNumber: number): CraRemessaTransacao {
  return {
    linha: lineNumber,
    codigoPortador: field(line, 2, 4),
    agenciaCodigoCedente: field(line, 5, 19).trim(),
    nomeCedente: field(line, 20, 64).trim(),
    nomeSacador: field(line, 65, 109).trim(),
    documentoSacador: onlyDigits(field(line, 110, 123)),
    enderecoSacador: field(line, 124, 168).trim(),
    cepSacador: onlyDigits(field(line, 169, 176)),
    cidadeSacador: field(line, 177, 196).trim(),
    ufSacador: field(line, 197, 198).trim(),
    nossoNumero: field(line, 199, 213).trim(),
    especie: field(line, 214, 216).trim(),
    numeroTitulo: field(line, 217, 227).trim(),
    dataEmissao: parseDate(field(line, 228, 235)),
    dataVencimento: parseDate(field(line, 236, 243)),
    codigoMoeda: field(line, 244, 246).trim(),
    valorTituloCentavos: parseNumber(field(line, 247, 260)),
    saldoTituloCentavos: parseNumber(field(line, 261, 274)),
    pracaProtesto: field(line, 275, 294).trim(),
    tipoEndosso: field(line, 295, 295).trim() as "M" | "T" | "",
    tipoAceite: field(line, 296, 296).trim() as "A" | "N" | "",
    controleDevedor: field(line, 297, 297).trim(),
    nomeDevedor: field(line, 298, 342).trim(),
    tipoPessoaDevedor: field(line, 343, 345).trim() as "001" | "002" | "",
    documentoDevedor: onlyDigits(field(line, 346, 359)),
    enderecoDevedor: field(line, 371, 415).trim(),
    cepDevedor: onlyDigits(field(line, 416, 423)),
    cidadeDevedor: field(line, 424, 443).trim(),
    ufDevedor: field(line, 444, 445).trim(),
    codigoCartorio: field(line, 446, 447).trim(),
    protocolo: field(line, 448, 457).trim(),
    ocorrencia: field(line, 458, 458).trim(),
    dataProtocolo: parseDate(field(line, 459, 466)),
    custasCentavos: parseNumber(field(line, 467, 476)),
    declaracao: field(line, 477, 477).trim(),
    sequenciaRegistro: parseNumber(field(line, 597, 600)),
  };
}

function parseTrailer(line: string): CraRemessaTrailer {
  return {
    idRegistro: field(line, 1, 1),
    codigoPortador: field(line, 2, 4),
    nomePortador: field(line, 5, 44).trim(),
    dataMovimento: parseDate(field(line, 45, 52)),
    quantidadeRegistros: parseNumber(field(line, 53, 57)),
    somaValoresCentavos: parseNumber(field(line, 58, 75)),
    sequenciaRegistro: parseNumber(field(line, 597, 600)),
  };
}

function validateBasicStructure(
  fileName: string,
  lines: string[],
  errors: CraRemessaValidationIssue[],
) {
  if (!fileName.toUpperCase().startsWith("B")) {
    pushError(errors, "invalid_file_name", 'O nome do arquivo deve iniciar com "B".');
  }

  if (lines.length < 3) {
    pushError(errors, "invalid_file_structure", "Arquivo inválido. Esperado header, transações e trailer.");
    return;
  }

  if (field(lines[0], 1, 1) !== "0") {
    pushError(errors, "invalid_header", "A primeira linha deve ser registro Header (ID 0).", 1);
  }

  if (field(lines[lines.length - 1], 1, 1) !== "9") {
    pushError(errors, "invalid_trailer", "A última linha deve ser registro Trailer (ID 9).", lines.length);
  }

  for (let i = 1; i < lines.length - 1; i += 1) {
    if (field(lines[i], 1, 1) !== "1") {
      pushError(errors, "invalid_transaction", "Linhas intermediárias devem ser de transação (ID 1).", i + 1);
    }
  }
}

function validateSequenceByLine(
  lines: string[],
  errors: CraRemessaValidationIssue[],
  warnings: CraRemessaValidationIssue[],
) {
  lines.forEach((line, index) => {
    const expected = index + 1;
    const seq = parseNumber(field(line, 597, 600));
    if (seq === 0) {
      pushWarning(warnings, "missing_sequence", "Linha sem sequência de registro preenchida.", index + 1);
      return;
    }
    if (seq !== expected) {
      pushError(
        errors,
        "invalid_sequence",
        `Sequência de registro inválida na linha ${index + 1}. Esperado ${expected.toString().padStart(4, "0")}.`,
        index + 1,
      );
    }
  });
}

function validateHeader(
  header: CraRemessaHeader,
  errors: CraRemessaValidationIssue[],
  warnings: CraRemessaValidationIssue[],
) {
  if (header.remetente && header.remetente !== "BFO") {
    pushWarning(warnings, "unexpected_remetente", `Remetente esperado "BFO", recebido "${header.remetente}".`, 1);
  }
  if (header.destinatario && header.destinatario !== "SDT") {
    pushWarning(
      warnings,
      "unexpected_destinatario",
      `Destinatário esperado "SDT", recebido "${header.destinatario}".`,
      1,
    );
  }
  if (header.tipoTransacao && header.tipoTransacao !== "TPR") {
    pushWarning(
      warnings,
      "unexpected_tipo_transacao",
      `Tipo de transação esperado "TPR", recebido "${header.tipoTransacao}".`,
      1,
    );
  }
  if (header.versaoLayout !== REMESSA_LAYOUT_VERSION) {
    pushError(
      errors,
      "unsupported_layout_version",
      `Versão de layout inválida. Esperado ${REMESSA_LAYOUT_VERSION}, recebido "${header.versaoLayout || "-"}".`,
      1,
    );
  }
}

function validateTransacao(
  transacao: CraRemessaTransacao,
  errors: CraRemessaValidationIssue[],
  warnings: CraRemessaValidationIssue[],
) {
  if (!transacao.nossoNumero) {
    pushError(errors, "missing_nosso_numero", "Transação sem Nosso Número.", transacao.linha);
  }
  if (!transacao.numeroTitulo) {
    pushWarning(warnings, "missing_numero_titulo", "Transação sem Número do Título.", transacao.linha);
  }
  if (transacao.codigoMoeda && transacao.codigoMoeda !== "001") {
    pushWarning(
      warnings,
      "unexpected_moeda",
      `Moeda esperada "001", recebida "${transacao.codigoMoeda}".`,
      transacao.linha,
    );
  }
  if (!["M", "T"].includes(transacao.tipoEndosso)) {
    pushWarning(
      warnings,
      "invalid_endosso",
      `Endosso fora do padrão (M/T): "${transacao.tipoEndosso || "-"}".`,
      transacao.linha,
    );
  }
  if (!["A", "N"].includes(transacao.tipoAceite)) {
    pushWarning(
      warnings,
      "invalid_aceite",
      `Aceite fora do padrão (A/N): "${transacao.tipoAceite || "-"}".`,
      transacao.linha,
    );
  }
  if (!["001", "002"].includes(transacao.tipoPessoaDevedor)) {
    pushWarning(
      warnings,
      "invalid_tipo_pessoa_devedor",
      `Tipo de pessoa do devedor fora do padrão (001/002): "${transacao.tipoPessoaDevedor || "-"}".`,
      transacao.linha,
    );
  }
}

function validateCrossChecks(
  parsed: CraRemessaParsed,
  errors: CraRemessaValidationIssue[],
  warnings: CraRemessaValidationIssue[],
) {
  const transactionCount = parsed.transacoes.length;
  const totalLines = transactionCount + 2;
  const indicationCount = parsed.transacoes.filter((transacao) =>
    ["DMI", "DRI"].includes(transacao.especie.toUpperCase()),
  ).length;
  const originalCount = transactionCount - indicationCount;
  const sumSaldo = parsed.transacoes.reduce((acc, item) => acc + item.saldoTituloCentavos, 0);

  // Na prática, arquivos CRA costumam usar "Qtd Registros" do header como
  // quantidade de transações/títulos, embora alguns layouts descrevam total de linhas.
  // Aceitamos ambos para evitar falso negativo.
  const headerQtdRegistros = parsed.header.quantidadeRegistros;
  const headerQtdRegistrosMatchesTransactions = headerQtdRegistros === transactionCount;
  const headerQtdRegistrosMatchesTotalLines = headerQtdRegistros === totalLines;

  if (!headerQtdRegistrosMatchesTransactions && !headerQtdRegistrosMatchesTotalLines) {
    pushError(
      errors,
      "header_qtd_registros_mismatch",
      `Header informa ${headerQtdRegistros} registros, mas esperado ${transactionCount} (transações) ou ${totalLines} (linhas totais).`,
      1,
    );
  } else if (headerQtdRegistrosMatchesTotalLines && !headerQtdRegistrosMatchesTransactions) {
    pushWarning(
      warnings,
      "header_qtd_registros_total_lines",
      `Header usa quantidade total de linhas (${totalLines}) em vez de transações (${transactionCount}).`,
      1,
    );
  }
  if (parsed.header.quantidadeTitulos !== transactionCount) {
    pushError(
      errors,
      "header_qtd_titulos_mismatch",
      `Header informa ${parsed.header.quantidadeTitulos} títulos, mas foram lidas ${transactionCount} transações.`,
      1,
    );
  }
  if (parsed.header.quantidadeIndicacoes !== indicationCount) {
    pushWarning(
      warnings,
      "header_qtd_indicacoes_mismatch",
      `Header informa ${parsed.header.quantidadeIndicacoes} indicações, mas foram calculadas ${indicationCount}.`,
      1,
    );
  }
  if (parsed.header.quantidadeOriginais !== originalCount) {
    pushWarning(
      warnings,
      "header_qtd_originais_mismatch",
      `Header informa ${parsed.header.quantidadeOriginais} originais, mas foram calculados ${originalCount}.`,
      1,
    );
  }
  if (parsed.trailer.quantidadeRegistros !== totalLines) {
    pushError(
      errors,
      "trailer_qtd_registros_mismatch",
      `Trailer informa ${parsed.trailer.quantidadeRegistros} registros, mas o arquivo possui ${totalLines}.`,
      parsed.transacoes.length + 2,
    );
  }
  if (parsed.trailer.somaValoresCentavos !== sumSaldo) {
    pushError(
      errors,
      "trailer_soma_valores_mismatch",
      `Trailer informa soma de ${parsed.trailer.somaValoresCentavos}, mas a soma dos saldos é ${sumSaldo}.`,
      parsed.transacoes.length + 2,
    );
  }

  if (parsed.header.codigoPortador !== parsed.trailer.codigoPortador) {
    pushError(errors, "portador_mismatch", "Código de portador diferente entre Header e Trailer.");
  }
  if (parsed.header.dataMovimento !== parsed.trailer.dataMovimento) {
    pushError(errors, "data_movimento_mismatch", "Data de movimento diferente entre Header e Trailer.");
  }
}

export function parseCraRemessaContent(fileName: string, content: string): CraRemessaImportResult {
  const errors: CraRemessaValidationIssue[] = [];
  const warnings: CraRemessaValidationIssue[] = [];
  const lines = normalizeLines(content);

  validateBasicStructure(fileName, lines, errors);
  validateLineSize(lines, errors);
  validateSequenceByLine(lines, errors, warnings);

  if (errors.length > 0) {
    return { ok: false, errors, warnings };
  }

  const header = parseHeader(lines[0]);
  const transacoes = lines.slice(1, -1).map((line, idx) => parseTransacao(line, idx + 2));
  const trailer = parseTrailer(lines[lines.length - 1]);

  const parsed: CraRemessaParsed = { fileName, header, transacoes, trailer };

  validateHeader(header, errors, warnings);
  transacoes.forEach((transacao) => validateTransacao(transacao, errors, warnings));
  validateCrossChecks(parsed, errors, warnings);

  return {
    ok: errors.length === 0,
    parsed: errors.length === 0 ? parsed : undefined,
    errors,
    warnings,
  };
}

export async function importCraRemessaFile(file: File): Promise<CraRemessaImportResult> {
  const content = await file.text();
  return parseCraRemessaContent(file.name, content);
}
