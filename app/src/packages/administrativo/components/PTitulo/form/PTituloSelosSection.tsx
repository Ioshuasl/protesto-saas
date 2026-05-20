"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";
import { usePTituloSelosReadHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloSelosReadHook";
import type { PTituloSeloVinculadoItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem";
import { AlertTriangle, Check } from "lucide-react";
import { useEffect, useMemo, type ReactNode } from "react";

const moneyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const dateTimeFormatter = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

const labelClass = "text-muted-foreground text-[10px] font-medium uppercase tracking-wide";

/** Rótulos compactos na linha única do trigger (listagens tipo dashboard, ex.: Mosaic/Cruip). */
const triggerMicroLabel =
  "text-muted-foreground shrink-0 text-[10px] font-medium uppercase tracking-wider";

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
  if (value === undefined || value === null || value === "") return "—";
  if (value instanceof Date) {
    if (Number.isNaN(value.getTime())) return "—";
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
    seloAgrupador: pickString(row.selo_agrupador),
    sigla: pickString(row.sigla, row.numero_selo),
    numero: pickString(row.numero != null ? row.numero : undefined) || "—",
    tipoAto: pickString(row.codigo_ato, row.tipo_ato),
    descricao: pickString(row.descricao, row.descricao_ato),
    descricaoCompleta: pickString(row.descricao_completa),
    nomeApi: pickString(row.nome_completo),
    dataRaw: row.data_hora_utilizacao ?? row.data,
    emol: pickNumber(row.valor_emolumento),
    tj: pickNumber(row.valor_taxa_judiciaria),
    fund: pickNumber(row.valor_fundesp),
    total: pickNumber(row.valor_total),
  };
}

function FieldLabel({ children, className }: { children: ReactNode; className?: string }) {
  return <p className={cn(labelClass, className)}>{children}</p>;
}

/**
 * Todos os selos de um título devem compartilhar o mesmo selo agrupador.
 * Retorna o valor de referência (maioria entre não vazios) e, por índice, se a linha diverge.
 */
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
  selos: PTituloSeloVinculadoItem[] | undefined;
}

export function PTituloSelosSection({ tituloId, selos }: PTituloSelosSectionProps) {
  const { usuarios, fetchUsuarios, isLoading: isLoadingUsuarios } = useGUsuarioReadHook();
  const { selos: selosFromHook, fetchSelos, isLoading: isLoadingSelos, setSelos } = usePTituloSelosReadHook();

  useEffect(() => {
    void fetchUsuarios();
  }, [fetchUsuarios]);

  useEffect(() => {
    if (typeof tituloId === "number" && tituloId > 0) {
      void fetchSelos(tituloId);
      return;
    }
    setSelos(selos ?? []);
  }, [tituloId, fetchSelos, setSelos, selos]);

  const nomeServentuarioByUsuarioId = useMemo(() => {
    return new Map(
      usuarios.map((u) => [u.usuario_id, u.nome_completo?.trim() || u.login?.trim() || ""]),
    );
  }, [usuarios]);

  const rows = useMemo(() => selosFromHook ?? [], [selosFromHook]);
  const normalizedList = useMemo(() => rows.map((s) => normalizeRow(s)), [rows]);
  const agrupadorDivergencia = useMemo(
    () => getAgrupadorDivergencia(rows, normalizedList),
    [rows, normalizedList],
  );
  const selosComMesmoAgrupador = !agrupadorDivergencia.haInconsistencia;

  if (isLoadingSelos && rows.length === 0) {
    return (
      <div className="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground">
        Carregando selos vinculados...
      </div>
    );
  }

  if (rows.length === 0) {
    return (
      <div className="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground">
        Nenhum selo vinculado a este título.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-muted-foreground text-xs leading-relaxed">
        Cada selo aparece em uma linha compacta (sigla, ato, data e total). Clique para ver agrupador, serventuário e
        valores detalhados.
      </p>

      {agrupadorDivergencia.haInconsistencia && agrupadorDivergencia.referencia ? (
        <div
          className="flex items-start gap-2 rounded-lg border border-amber-500/50 bg-amber-500/10 px-3 py-2 text-xs text-amber-950 dark:text-amber-100"
          role="status"
        >
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" strokeWidth={1.75} />
          <p>
            <span className="font-medium">Selo agrupador incoerente: </span>
            os selos deste título deveriam usar o agrupador{" "}
            <span className="font-mono text-[11px]">{agrupadorDivergencia.referencia}</span>. Há um ou mais selos
            com valor diferente (ou sem agrupador) — eles estão sinalizados abaixo.
          </p>
        </div>
      ) : null}

      {agrupadorDivergencia.haInconsistencia && !agrupadorDivergencia.referencia ? (
        <div
          className="flex items-start gap-2 rounded-lg border border-amber-500/50 bg-amber-500/10 px-3 py-2 text-xs text-amber-950 dark:text-amber-100"
          role="status"
        >
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" strokeWidth={1.75} />
          <p>
            <span className="font-medium">Selo agrupador incoerente: </span>
            há mistura de selos com e sem número de agrupador.
          </p>
        </div>
      ) : null}

      <Accordion type="multiple" defaultValue={[]} className="flex flex-col gap-3">
        {rows.map((selo, index) => {
          const n = normalizedList[index]!;
          const uid = selo.usuario_id;
          const foraAgrupador = agrupadorDivergencia.foraDoPadrao(index);
          const nomeResolvido = uid != null ? nomeServentuarioByUsuarioId.get(uid) : undefined;
          const nomeServ = nomeResolvido != null && nomeResolvido !== "" ? nomeResolvido : undefined;
          const nomeDisplay =
            isLoadingUsuarios && uid != null && !nomeServ && !n.nomeApi
              ? "…"
              : pickString(n.nomeApi, nomeServ) || (uid != null ? `ID ${uid}` : "—");

          const itemId = `selo-${index}`;
          const descricaoResumo = n.descricao || n.descricaoCompleta || `Tipo de ato ${n.tipoAto || "—"}`;
          const dataFmt = formatDateTime(n.dataRaw as string | Date | undefined);
          const totalFmt = moneyFormatter.format(n.total ?? 0);
          const triggerSummary = [
            foraAgrupador ? "Agrupador divergente" : null,
            `Sel.: ${n.sigla || "—"}`,
            n.tipoAto ? `Tipo ${n.tipoAto}` : null,
            descricaoResumo,
            `Data: ${dataFmt}`,
            `Total: ${totalFmt}`,
          ]
            .filter(Boolean)
            .join(" · ");

          return (
            <AccordionItem
              key={itemId}
              value={itemId}
              data-slot="selo-card-row"
              className={cn(
                "data-[state=open]:shadow-md overflow-hidden rounded-xl border border-b-0 bg-card shadow-sm transition-shadow last:border-b-0",
                foraAgrupador
                  ? "border-amber-500/60 data-[state=open]:ring-1 data-[state=open]:ring-amber-500/30"
                  : "border-border",
              )}
            >
              <AccordionTrigger
                className={cn(
                  "group w-full max-w-full hover:bg-muted/40 focus-visible:ring-ring/50 !items-center gap-2 px-3 py-2 text-xs hover:no-underline focus-visible:ring-2 sm:gap-3 sm:px-4 sm:py-2.5 sm:text-sm",
                  "[&>svg]:size-4 [&>svg]:shrink-0 [&>svg]:translate-y-0 [&>svg]:transition-transform",
                  "[&[data-state=open]]:border-border/60 [&[data-state=open]]:border-b [&[data-state=open]]:bg-muted/20",
                  foraAgrupador
                    ? "bg-amber-500/[0.06] hover:bg-amber-500/12 data-[state=open]:bg-amber-500/10"
                    : "",
                )}
              >
                <div
                  className="flex w-full min-w-0 max-w-full flex-1 flex-nowrap items-center gap-x-2 overflow-hidden text-left sm:gap-x-3"
                  title={triggerSummary}
                >
                  {foraAgrupador ? (
                    <>
                      <span
                        className="inline-flex shrink-0 items-center gap-1 rounded-sm border border-amber-500/45 bg-amber-500/15 px-1 py-0.5 text-[10px] font-medium text-amber-950 dark:text-amber-50"
                        data-slot="selo-agrupador-aviso-trigger"
                        title={
                          agrupadorDivergencia.referencia
                            ? `Fora do agrupador esperado: ${agrupadorDivergencia.referencia}`
                            : "Fora do padrão de agrupador"
                        }
                      >
                        <AlertTriangle className="size-3 shrink-0 text-amber-700 dark:text-amber-400" strokeWidth={2} />
                        <span className="max-w-[5rem] truncate sm:max-w-[9rem]">
                          {agrupadorDivergencia.referencia ? (
                            <span className="font-mono">{agrupadorDivergencia.referencia}</span>
                          ) : (
                            "Aviso"
                          )}
                        </span>
                      </span>
                      <span className="bg-border/80 h-3.5 w-px shrink-0" aria-hidden />
                    </>
                  ) : null}

                  <span className="flex shrink-0 items-center gap-1.5">
                    <span className={triggerMicroLabel}>Sel.</span>
                    <span className="font-mono text-xs font-semibold whitespace-nowrap text-foreground tabular-nums sm:text-sm">
                      {n.sigla || "—"}
                    </span>
                  </span>

                  <span className="bg-border/80 h-3.5 w-px shrink-0" aria-hidden />

                  <span className="flex min-w-0 basis-[9rem] flex-1 items-center gap-1.5 overflow-hidden sm:basis-[12rem] md:basis-[16rem] lg:basis-[20rem]">
                    <span className={triggerMicroLabel}>Ato</span>
                    {n.tipoAto ? (
                      <Badge
                        variant="secondary"
                        className="h-5 shrink-0 px-1.5 py-0 font-mono text-[10px] leading-none sm:text-[11px]"
                      >
                        {n.tipoAto}
                      </Badge>
                    ) : null}
                    <span
                      className="text-foreground min-w-0 flex-1 truncate text-xs font-medium sm:text-sm"
                      title={descricaoResumo}
                    >
                      {descricaoResumo}
                    </span>
                  </span>

                  <span className="bg-border/80 h-3.5 w-px shrink-0" aria-hidden />

                  <span className="flex shrink-0 items-center gap-1.5">
                    <span className={triggerMicroLabel}>Data</span>
                    <time
                      className="whitespace-nowrap text-xs tabular-nums text-foreground sm:text-sm"
                      dateTime={String(n.dataRaw ?? "")}
                    >
                      {dataFmt}
                    </time>
                  </span>

                  <span className="bg-border/80 h-3.5 w-px shrink-0" aria-hidden />

                  <span className="flex shrink-0 items-center gap-1.5">
                    <span className={triggerMicroLabel}>Tot.</span>
                    <span className="text-xs font-semibold whitespace-nowrap tabular-nums text-foreground sm:text-sm">
                      {totalFmt}
                    </span>
                  </span>
                </div>
              </AccordionTrigger>

              <AccordionContent className="px-0 pb-0">
                <div className="bg-muted/20 space-y-4 px-4 py-4 sm:px-5">
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div
                      className={cn(
                        "space-y-1.5 rounded-lg border p-3 transition-colors",
                        foraAgrupador
                          ? "border-amber-500/60 bg-amber-500/5 ring-1 ring-amber-500/20"
                          : "border-transparent p-0",
                      )}
                      data-slot="selo-agrupador-bloco"
                    >
                      <div className="flex flex-wrap items-center gap-2">
                        <Label
                          htmlFor={`${itemId}-agrupador`}
                          className={cn(
                            labelClass,
                            foraAgrupador && "text-amber-900 dark:text-amber-100",
                          )}
                        >
                          Selo agrupador
                        </Label>
                        {foraAgrupador ? (
                          <span className="inline-flex items-center gap-1 rounded-md border border-amber-500/50 bg-amber-500/15 px-1.5 py-0.5 text-[10px] font-medium text-amber-950 dark:text-amber-100">
                            <AlertTriangle className="h-3 w-3" strokeWidth={1.75} />
                            Divergente
                          </span>
                        ) : null}
                      </div>
                      {foraAgrupador && agrupadorDivergencia.referencia ? (
                        <p className="text-amber-900/90 dark:text-amber-100/90 text-[11px] leading-snug">
                          Esperado para este título:{" "}
                          <span className="font-mono text-[11px]">{agrupadorDivergencia.referencia}</span>
                        </p>
                      ) : null}
                      {foraAgrupador && !agrupadorDivergencia.referencia && agrupadorDivergencia.haInconsistencia ? (
                        <p className="text-amber-900/90 dark:text-amber-100/90 text-[11px] leading-snug">
                          Todos os selos deveriam informar o mesmo número de agrupador (há mistura de preenchido e vazio).
                        </p>
                      ) : null}
                      <div className="relative">
                        <Input
                          id={`${itemId}-agrupador`}
                          readOnly
                          value={n.seloAgrupador || "—"}
                          aria-invalid={foraAgrupador}
                          aria-describedby={
                            selosComMesmoAgrupador && !foraAgrupador
                              ? `${itemId}-agrupador-ok-hint`
                              : undefined
                          }
                          className={cn(
                            "font-mono text-xs",
                            foraAgrupador &&
                              "border-amber-500/60 bg-amber-500/5 text-amber-950 focus-visible:ring-amber-500/40 dark:text-amber-50",
                            selosComMesmoAgrupador && !foraAgrupador && "pr-9",
                            selosComMesmoAgrupador &&
                              !foraAgrupador &&
                              "border-emerald-500/50 bg-white/50 focus-visible:ring-emerald-500/30 dark:bg-background/50",
                          )}
                        />
                        {selosComMesmoAgrupador && !foraAgrupador ? (
                          <>
                            <span id={`${itemId}-agrupador-ok-hint`} className="sr-only">
                              Selo agrupador coerente com os demais selos vinculados a este título.
                            </span>
                            <span
                              className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-emerald-600 dark:text-emerald-400"
                              aria-hidden
                              title="Mesmo selo agrupador em todos os selos do título"
                            >
                              <Check className="h-4 w-4" strokeWidth={2.5} />
                            </span>
                          </>
                        ) : null}
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <Label htmlFor={`${itemId}-serv`} className={labelClass}>
                        Serventuário
                      </Label>
                      <Input id={`${itemId}-serv`} readOnly value={nomeDisplay} className="text-sm" />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor={`${itemId}-desc-completa`} className={labelClass}>
                      Descrição completa (emolumentos)
                    </Label>
                    <Textarea
                      id={`${itemId}-desc-completa`}
                      readOnly
                      value={n.descricaoCompleta || "—"}
                      className="min-h-9 resize-none text-sm"
                      rows={1}
                    />
                  </div>

                  <div className="space-y-2">
                    <FieldLabel>Valores</FieldLabel>
                    <div className="grid w-full min-w-0 grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
                      <div className="space-y-1.5">
                        <Label htmlFor={`${itemId}-emol`} className={labelClass}>
                          Emolumento
                        </Label>
                        <Input
                          id={`${itemId}-emol`}
                          readOnly
                          value={moneyFormatter.format(n.emol ?? 0)}
                          className="text-right text-sm tabular-nums"
                        />
                      </div>
                      <div className="space-y-1.5">
                        <Label htmlFor={`${itemId}-tj`} className={labelClass}>
                          Taxa jud.
                        </Label>
                        <Input
                          id={`${itemId}-tj`}
                          readOnly
                          value={moneyFormatter.format(n.tj ?? 0)}
                          className="text-right text-sm tabular-nums"
                        />
                      </div>
                      <div className="space-y-1.5">
                        <Label htmlFor={`${itemId}-fund`} className={labelClass}>
                          Fundesp
                        </Label>
                        <Input
                          id={`${itemId}-fund`}
                          readOnly
                          value={moneyFormatter.format(n.fund ?? 0)}
                          className="text-right text-sm tabular-nums"
                        />
                      </div>
                      <div className="space-y-1.5">
                        <Label htmlFor={`${itemId}-vtot`} className={labelClass}>
                          Total
                        </Label>
                        <Input
                          id={`${itemId}-vtot`}
                          readOnly
                          value={moneyFormatter.format(n.total ?? 0)}
                          className="text-right text-sm font-medium tabular-nums"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </div>
  );
}
