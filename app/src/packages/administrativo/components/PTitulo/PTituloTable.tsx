"use client";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import { TituloListItem } from "@/packages/administrativo/services/PTitulo/PTituloService";
import { matchesSearchText } from "@/shared/actions/text/comboboxSearchFilter";
import {
  CircleDollarSign,
  EllipsisVertical,
  FileSearch,
  FileX2,
  Gavel,
  RotateCcw,
  ScrollText,
  Send,
} from "lucide-react";
import { useEffect, useMemo } from "react";
import { getTriduoMessage, moneyFormatter } from "./titulo-list-utils";
import { formatCpfCnpj } from "@/shared/utils/document";
import { formatEmptyField } from "@/shared/utils/emptyField";

const COLUMN_CLASSES = {
  numero: "w-[18%]",
  protocolo: "w-[10%]",
  apresentante: "w-[27%]",
  especie: "hidden w-[10%] lg:table-cell",
  valor: "w-[11%]",
  ocorrencia: "w-[16%]",
  acoes: "w-[8%]",
} as const;

type PTituloTableWorkflowItem = TituloListItem & {
  hasApontamentoBase?: boolean;
  hasIntimacao?: boolean;
  hasProtestoCompleto?: boolean;
};

interface PTituloTableProps {
  data: PTituloTableWorkflowItem[];
  isLoading?: boolean;
  searchQuery?: string;
  onViewDetails: (titulo: TituloListItem) => void;
  onUpdateStatus: (tituloId: number, status: "Em Tríduo" | "Pago" | "Protestado") => void;
}

function TruncatedText({
  value,
  className,
  prefix,
}: {
  value: string | number | null | undefined;
  className?: string;
  prefix?: string;
}) {
  const text = `${prefix ?? ""}${formatEmptyField(value)}`;
  return (
    <span className={className ? `block truncate ${className}` : "block truncate"} title={text}>
      {text}
    </span>
  );
}

function findMatchedPessoaVinculo(titulo: TituloListItem, searchQuery?: string) {
  const search = searchQuery?.trim();
  if (!search) return null;

  return (
    titulo.vinculos_partes.find((vinculo) =>
      matchesSearchText([vinculo.nome, vinculo.cpfcnpj].filter(Boolean).join(" "), search),
    ) ?? null
  );
}

function PessoaMatchIndicator({ label, title }: { label: string; title: string }) {
  return (
    <span
      className="inline-flex h-4 max-w-[7.5rem] shrink-0 items-center gap-1 rounded-full border border-amber-200 bg-amber-50 px-1.5 text-[10px] font-medium leading-none text-amber-800"
      title={title}
      aria-label={title}
    >
      <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500" aria-hidden />
      <span className="truncate">{label}</span>
    </span>
  );
}

export function PTituloTable({ data, isLoading, searchQuery, onViewDetails, onUpdateStatus }: PTituloTableProps) {
  const { ocorrencias, fetchOcorrencias } = usePOcorrenciasReadHook();

  useEffect(() => {
    void fetchOcorrencias();
  }, [fetchOcorrencias]);

  const ocorrenciaLabelById = useMemo(
    () =>
      new Map(
        ocorrencias.map((ocorrencia) => [
          ocorrencia.ocorrencias_id,
          ocorrencia.descricao || ocorrencia.tipo || ocorrencia.codigo || "Sem ocorrência",
        ]),
      ),
    [ocorrencias],
  );

  if (isLoading) {
    return <div className="w-full flex items-center justify-center p-8 text-muted-foreground">Carregando títulos...</div>;
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum título encontrado.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border overflow-x-auto">
      <Table className="w-full table-fixed">
        <TableHeader>
          <TableRow>
            <TableHead className={COLUMN_CLASSES.numero}>Número/Nosso Número</TableHead>
            <TableHead className={COLUMN_CLASSES.protocolo}>Protocolo</TableHead>
            <TableHead className={COLUMN_CLASSES.apresentante}>Apresentante (Nome/CPF-CNPJ)</TableHead>
            <TableHead className={COLUMN_CLASSES.especie}>Espécie</TableHead>
            <TableHead className={COLUMN_CLASSES.valor}>Valor Total</TableHead>
            <TableHead className={COLUMN_CLASSES.ocorrencia}>Ocorrência</TableHead>
            <TableHead className={`${COLUMN_CLASSES.acoes} text-right`}>Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((titulo) => {
            const triduo = getTriduoMessage(titulo);
            const valorTotal = titulo.valor_total ?? titulo.valor_total_custas ?? titulo.valor_titulo ?? 0;
            const ocorrenciaLabel =
              titulo.status_descricao ||
              (titulo.ocorrencia_id
                ? ocorrenciaLabelById.get(titulo.ocorrencia_id) || "Sem ocorrência"
                : "Sem ocorrência");
            const hasValue = (value: unknown) => value !== null && value !== undefined && value !== "";
            const hasApontamentoBase =
              titulo.hasApontamentoBase ??
              (hasValue(titulo.numero_apontamento) && hasValue(titulo.data_apontamento));
            const hasIntimacao = titulo.hasIntimacao ?? (hasApontamentoBase && hasValue(titulo.data_intimacao));
            const hasProtestoCompleto =
              titulo.hasProtestoCompleto ??
              (hasIntimacao &&
                hasValue(titulo.data_protesto) &&
                hasValue(titulo.livro_id_protesto) &&
                hasValue(titulo.folha_protesto));
            const matchedPessoaVinculo = findMatchedPessoaVinculo(titulo, searchQuery);
            const matchedPessoaVinculoText = matchedPessoaVinculo
              ? `Pessoa encontrada nesse título como ${matchedPessoaVinculo.descricao}`
              : "";
            const matchedPessoaVinculoLabel = matchedPessoaVinculo?.descricao ?? "";

            return (
              <TableRow
                key={titulo.titulo_id}
                className="cursor-pointer"
                onClick={() => onViewDetails(titulo)}
              >
                <TableCell className={`${COLUMN_CLASSES.numero} min-w-0 overflow-hidden`}>
                  <div className="flex min-w-0 flex-col">
                    <TruncatedText value={titulo.numero_titulo} />
                    <TruncatedText
                      value={titulo.nosso_numero}
                      prefix="Nosso n. "
                      className="text-xs text-muted-foreground"
                    />
                  </div>
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.protocolo} min-w-0 overflow-hidden`}>
                  <TruncatedText value={titulo.numero_apontamento} />
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.apresentante} min-w-0 overflow-hidden`}>
                  <div className="flex min-w-0 flex-col gap-0.5">
                    <TruncatedText value={titulo.apresentante_nome} />
                    <span className="flex min-w-0 items-center gap-1.5">
                      <TruncatedText
                        value={formatCpfCnpj(titulo.apresentante_cpfcnpj)}
                        className="min-w-0 flex-1 text-xs text-muted-foreground"
                      />
                      {matchedPessoaVinculo ? (
                        <PessoaMatchIndicator
                          label={matchedPessoaVinculoLabel}
                          title={matchedPessoaVinculoText}
                        />
                      ) : null}
                    </span>
                  </div>
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.especie} min-w-0 overflow-hidden`}>
                  <TruncatedText value={titulo.especie?.especie ?? titulo.especie_sigla} />
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.valor} min-w-0 overflow-hidden`}>
                  <TruncatedText value={moneyFormatter.format(valorTotal)} />
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.ocorrencia} min-w-0 overflow-hidden`}>
                  <div className="flex min-w-0 flex-col gap-1">
                    <TruncatedText value={ocorrenciaLabel} />
                    {triduo ? <TruncatedText value={triduo} className="text-xs text-muted-foreground" /> : null}
                  </div>
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.acoes} text-right`}>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-foreground hover:text-[#FF6B00]"
                        onClick={(event) => event.stopPropagation()}
                      >
                        <EllipsisVertical className="h-4 w-4" strokeWidth={1.5} />
                        <span className="sr-only">Ações</span>
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onViewDetails(titulo); }}>
                        <FileSearch className="mr-2 h-4 w-4" strokeWidth={1.5} />
                        Ver Detalhes
                      </DropdownMenuItem>
                      {hasProtestoCompleto ? (
                        <>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Voltar para Intimação" ainda não implementada'); }}>
                            <RotateCcw className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Voltar para Intimação
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Cancelar Título" ainda não implementada'); }}>
                            <FileX2 className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Cancelar Título
                          </DropdownMenuItem>
                        </>
                      ) : hasIntimacao ? (
                        <>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Voltar para Apontamento" ainda não implementada'); }}>
                            <RotateCcw className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Voltar para Apontamento
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Aceite/Edital" ainda não implementada'); }}>
                            <ScrollText className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Aceite/Edital
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onUpdateStatus(titulo.titulo_id, "Pago"); }}>
                            <CircleDollarSign className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Desistir/Liquidar Título
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onUpdateStatus(titulo.titulo_id, "Protestado"); }}>
                            <Gavel className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Protestar Título
                          </DropdownMenuItem>
                        </>
                      ) : hasApontamentoBase ? (
                        <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onUpdateStatus(titulo.titulo_id, "Em Tríduo"); }}>
                          <Send className="mr-2 h-4 w-4" strokeWidth={1.5} />
                          Intimar Título
                        </DropdownMenuItem>
                      ) : null}
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
