export interface CraRemessaHeader {
  idRegistro: string;
  codigoPortador: string;
  nomePortador: string;
  dataMovimento: string;
  remetente: string;
  destinatario: string;
  tipoTransacao: string;
  sequenciaRemessa: number;
  quantidadeRegistros: number;
  quantidadeTitulos: number;
  quantidadeIndicacoes: number;
  quantidadeOriginais: number;
  versaoLayout: string;
  codigoIbgeMunicipio: string;
  sequenciaRegistro: number;
}

export interface CraRemessaTransacao {
  linha: number;
  codigoPortador: string;
  agenciaCodigoCedente: string;
  nomeCedente: string;
  nomeSacador: string;
  documentoSacador: string;
  enderecoSacador: string;
  cepSacador: string;
  cidadeSacador: string;
  ufSacador: string;
  nossoNumero: string;
  especie: string;
  numeroTitulo: string;
  dataEmissao: string;
  dataVencimento: string;
  codigoMoeda: string;
  valorTituloCentavos: number;
  saldoTituloCentavos: number;
  pracaProtesto: string;
  tipoEndosso: "M" | "T" | "";
  tipoAceite: "A" | "N" | "";
  controleDevedor: string;
  nomeDevedor: string;
  tipoPessoaDevedor: "001" | "002" | "";
  documentoDevedor: string;
  enderecoDevedor: string;
  cepDevedor: string;
  cidadeDevedor: string;
  ufDevedor: string;
  codigoCartorio: string;
  protocolo: string;
  ocorrencia: string;
  dataProtocolo: string;
  custasCentavos: number;
  declaracao: string;
  sequenciaRegistro: number;
}

export interface CraRemessaTrailer {
  idRegistro: string;
  codigoPortador: string;
  nomePortador: string;
  dataMovimento: string;
  quantidadeRegistros: number;
  somaValoresCentavos: number;
  sequenciaRegistro: number;
}

export interface CraRemessaParsed {
  fileName: string;
  header: CraRemessaHeader;
  transacoes: CraRemessaTransacao[];
  trailer: CraRemessaTrailer;
}

export interface CraRemessaValidationIssue {
  code: string;
  message: string;
  line?: number;
}

export interface CraRemessaImportResult {
  ok: boolean;
  parsed?: CraRemessaParsed;
  errors: CraRemessaValidationIssue[];
  warnings: CraRemessaValidationIssue[];
}
