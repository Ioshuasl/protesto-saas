"use client";

import {
  Accordion,
  AccordionCardContent,
  AccordionCardItem,
  AccordionCardTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { sortPTituloSelosVinculados } from "@/packages/administrativo/data/PTitulo/ptituloSelosUtils";
import { usePTituloSelosReadHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloSelosReadHook";
import type { PTituloSeloVinculadoItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem";
import { AlertTriangle } from "lucide-react";
import { useEffect, useMemo } from "react";
import { PTituloSectionCard } from "./PTituloFormLayout";

const moneyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const dateTimeFormatter = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function pickString(...candidates: unknown[]): string {
  const c = candidates.find((v) => v != null && String(v).trim() !== "");
  return c == null ? "" : String(c).trim();
}

function pickNumber(...candidates: unknown[]): number | undefined {
  const c = candidates.find((v) => {
    if (v == null) return false;
    if (typeof v === "number" && !Number.isNaN(v)) return true;
    return !Number.isNaN(Number(v));
  });
  if (c == null) return undefined;
  if (typeof c === "number" && !Number.isNaN(c)) return c;
  const n = Number(c);
  return Number.isNaN(n) ? undefined : n;
}

function formatDateTime(value: string | Date | undefined) {
  if (value === undefined || value === null || value === "") return "-";
  if (value instanceof Date) {
    if (Number.isNaN(value.getTime())) return "-";
    return dateTimeFormatter.format(value);
  }
  const s = String(value).trim();
  const mBr = s.match(/^(\d{2})\.(\d{2})\.(\d{4})(?:\s+(\d{2}):(\d{2}))?/);
  if (mBr) {
    const [, d, mo, y, h, min] = mBr;
    if (h != null && min != null) {
      return `${d}/${mo}/${y} ${h}:${min}`;
    }
    return `${d}/${mo}/${y}`;
  }
  const d = new Date(s);
  if (!Number.isNaN(d.getTime())) {
    return dateTimeFormatter.format(d);
  }
  return s;
}

function normalizeRow(row: PTituloSeloVinculadoItem) {
  return {
    notaFiscal: pickString(row.nota_fiscal),
    seloAgrupador: pickString(row.selo_agrupador),
    sigla: pickString(row.sigla, row.numero_selo),
    numero: pickString(row.numero != null ? row.numero : undefined) || "-",
    tipoAto: pickString(row.codigo_ato, row.tipo_ato),
    descricao: pickString(row.descricao, row.descricao_ato),
    descricaoCompleta: pickString(row.descricao_completa),
    nomeServentuario: pickString(row.nome_completo),
    dataRaw: row.data_hora_utilizacao ?? row.data,
    emol: pickNumber(row.valor_emolumento),
    tj: pickNumber(row.valor_taxa_judiciaria),
    fund: pickNumber(row.valor_fundesp),
    total: pickNumber(row.valor_total),
    seloLivroId: row.selo_livro_id,
  };
}

function SeloInfo({ label, value, className }: { label: string; value: string; className?: string }) {
  return (
    <div className={cn("min-w-0", className)}>
      <div className="text-xs font-medium text-muted-foreground">{label}</div>
      <div className="mt-0.5 truncate text-sm text-foreground" title={value}>
        {value}
      </div>
    </div>
  );
}

function SeloMoneyInfo({
  label,
  value,
  strong,
}: {
  label: string;
  value: number | undefined;
  strong?: boolean;
}) {
  return (
    <div className="rounded-md border border-border/60 bg-background px-3 py-2">
      <div className="text-xs font-medium text-muted-foreground">{label}</div>
      <div className={cn("mt-1 text-sm tabular-nums", strong ? "font-semibold text-foreground" : "text-foreground")}>
        {moneyFormatter.format(value ?? 0)}
      </div>
    </div>
  );
}

function getAgrupadorDivergencia(
  list: PTituloSeloVinculadoItem[],
  normalized: ReturnType<typeof normalizeRow>[],
) {
  const ags = normalized.map((r) => r.seloAgrupador);
  if (list.length < 2) {
    return {
      referencia: ags.find(Boolean) ?? "",
      foraDoPadrao: (() => false) as (i: number) => boolean,
      haInconsistencia: false,
    };
  }

  const comValor = ags.filter(Boolean);
  const unicos = new Set(comValor);
  const vazioMisturado = ags.some((a) => !a) && comValor.length > 0;
  const valoresDistintos = unicos.size > 1;
  const haInconsistencia = valoresDistintos || vazioMisturado;

  const counts = new Map<string, number>();
  comValor.forEach((a) => counts.set(a, (counts.get(a) ?? 0) + 1));
  let referencia = "";
  let max = 0;
  counts.forEach((c, a) => {
    if (c > max) {
      max = c;
      referencia = a;
    }
  });
  if (unicos.size > 0 && !referencia) {
    referencia = comValor[0] ?? "";
  }

  return {
    referencia,
    foraDoPadrao: (i: number) => {
      if (!haInconsistencia) return false;
      const a = ags[i];
      if (valoresDistintos && a && referencia) return a !== referencia;
      if (vazioMisturado && !a) return true;
      if (valoresDistintos && !a) return true;
      return false;
    },
    haInconsistencia,
  };
}

interface PTituloSelosSectionProps {
  tituloId?: number;
  /** Selos já vindos do show (exibição imediata antes do refresh da rota /selos). */
  initialSelos?: PTituloSeloVinculadoItem[];
}

export function PTituloSelosSection({ tituloId, initialSelos }: PTituloSelosSectionProps) {
  const { selos: selosFromHook, fetchSelos, isLoading: isLoadingSelos, setSelos } = usePTituloSelosReadHook();

  useEffect(() => {
    if (typeof tituloId !== "number" || tituloId <= 0) {
      setSelos([]);
      return;
    }
    if (Array.isArray(initialSelos) && initialSelos.length > 0) {
      setSelos(sortPTituloSelosVinculados(initialSelos));
    }
    void fetchSelos(tituloId);
  }, [tituloId, initialSelos, fetchSelos, setSelos]);

  const rows = useMemo(() => selosFromHook ?? [], [selosFromHook]);
  const normalizedList = useMemo(() => rows.map((s) => normalizeRow(s)), [rows]);
  const agrupadorDivergencia = useMemo(
    () => getAgrupadorDivergencia(rows, normalizedList),
    [rows, normalizedList],
  );

  return (
    <PTituloSectionCard className="overflow-hidden p-0">
      <div className="border-b border-border/70 px-3 py-2 md:px-4">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="text-lg font-semibold tracking-tight text-foreground">Selos</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Selos utilizados e valores associados a este título.
            </p>
          </div>
          <Badge
            variant="secondary"
            className="w-fit rounded-md border border-border/60 bg-muted/40 px-2 text-xs font-medium text-muted-foreground shadow-none"
          >
            {rows.length} {rows.length === 1 ? "selo" : "selos"}
          </Badge>
        </div>
      </div>

      <div className="space-y-2 px-3 py-2 md:px-4">
        {agrupadorDivergencia.haInconsistencia ? (
          <div
            className="flex items-start gap-2 rounded-lg border border-amber-500/50 bg-amber-500/10 px-3 py-2 text-sm text-amber-950 dark:text-amber-100"
            role="status"
          >
            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" strokeWidth={1.75} />
            <p>
              <span className="font-medium">Selo agrupador incoerente: </span>
              {agrupadorDivergencia.referencia ? (
                <>
                  os selos deste título deveriam usar o agrupador{" "}
                  <span className="font-mono text-xs">{agrupadorDivergencia.referencia}</span>.
                </>
              ) : (
                "há mistura de selos com e sem número de agrupador."
              )}
            </p>
          </div>
        ) : null}

        {isLoadingSelos && rows.length === 0 ? (
          <div className="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground">
            Carregando selos vinculados...
          </div>
        ) : rows.length === 0 ? (
          <div className="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground">
            Nenhum selo vinculado a este título.
          </div>
        ) : (
          <Accordion type="multiple" className="space-y-2">
            {rows.map((selo, index) => {
              const n = normalizedList[index]!;
              const foraAgrupador = agrupadorDivergencia.foraDoPadrao(index);
              const descricaoResumo =
                n.descricao || n.descricaoCompleta || `Tipo de ato ${n.tipoAto || "-"}`;
              const itemKey = n.seloLivroId != null ? `selo-${n.seloLivroId}` : `selo-row-${index}`;

              return (
                <AccordionCardItem
                  key={itemKey}
                  value={itemKey}
                  className={cn(
                    "border-border/70 bg-background",
                    foraAgrupador && "border-amber-500/60 bg-amber-500/[0.06]",
                  )}
                >
                  <AccordionCardTrigger
                    className={cn(
                      foraAgrupador && "bg-amber-500/[0.05] hover:bg-amber-500/10",
                    )}
                  >
                    <div className="flex min-w-0 flex-1 flex-col gap-1.5 sm:flex-row sm:items-center sm:gap-3">
                      <div className="flex min-w-0 flex-1 items-center gap-2">
                        <span className="shrink-0 font-mono text-base font-semibold text-foreground">
                          {n.sigla || "-"}
                        </span>
                        <span className="shrink-0 text-xs font-normal text-muted-foreground">Nº {n.numero}</span>
                        {n.tipoAto ? (
                          <Badge
                            variant="secondary"
                            className="h-5 shrink-0 px-1.5 py-0 font-mono text-[11px] leading-none"
                          >
                            {n.tipoAto}
                          </Badge>
                        ) : null}
                        <span className="min-w-0 truncate text-sm font-medium text-foreground" title={descricaoResumo}>
                          {descricaoResumo}
                        </span>
                      </div>
                      <div className="flex shrink-0 items-center gap-2 text-xs text-muted-foreground sm:justify-end">
                        <span>{formatDateTime(n.dataRaw as string | Date | undefined)}</span>
                        <span className="text-border">|</span>
                        <span className="font-semibold tabular-nums text-foreground">
                          {moneyFormatter.format(n.total ?? 0)}
                        </span>
                        {foraAgrupador ? (
                          <Badge
                            variant="outline"
                            className="border-amber-500/50 bg-amber-500/15 text-[10px] text-amber-950 dark:text-amber-100"
                            title={
                              agrupadorDivergencia.referencia
                                ? `Esperado: ${agrupadorDivergencia.referencia}`
                                : "Fora do padrão de agrupador"
                            }
                          >
                            Divergente
                          </Badge>
                        ) : null}
                      </div>
                    </div>
                  </AccordionCardTrigger>

                  <AccordionCardContent className="px-2.5 py-2.5">
                    <div className="space-y-2.5">
                      <div className="grid gap-2.5 md:grid-cols-2 xl:grid-cols-4">
                        <SeloInfo label="Agrupador" value={n.seloAgrupador || "-"} className="font-mono" />
                        <SeloInfo label="Data" value={formatDateTime(n.dataRaw as string | Date | undefined)} />
                        <SeloInfo label="Serventuário" value={n.nomeServentuario || "-"} />
                        <SeloInfo label="Nota fiscal" value={n.notaFiscal || "-"} className="font-mono" />
                      </div>

                      {n.descricaoCompleta && n.descricaoCompleta !== descricaoResumo ? (
                        <div className="rounded-md border border-border/60 bg-muted/20 px-2.5 py-2">
                          <div className="text-xs font-medium text-muted-foreground">Descrição completa</div>
                          <p className="mt-1 text-sm text-foreground">{n.descricaoCompleta}</p>
                        </div>
                      ) : null}

                      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
                        <SeloMoneyInfo label="Emolumento" value={n.emol} />
                        <SeloMoneyInfo label="Taxa judiciária" value={n.tj} />
                        <SeloMoneyInfo label="Fundesp" value={n.fund} />
                        <SeloMoneyInfo label="Total" value={n.total} strong />
                      </div>
                    </div>
                  </AccordionCardContent>
                </AccordionCardItem>
              );
            })}
          </Accordion>
        )}
      </div>
    </PTituloSectionCard>
  );
}
