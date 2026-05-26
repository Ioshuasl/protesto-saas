"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { format, startOfDay, subYears } from "date-fns";
import {
  AlertCircle,
  CheckCircle2,
  ChevronRight,
  Info,
  Loader2,
  Search,
  ShieldAlert,
} from "lucide-react";
import type { DateRange } from "react-day-picker";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { GUsuarioSelectObject } from "@/packages/administrativo/components/GUsuario/GUsuarioSelectObject";
import PPessoaTableFormDialog from "@/packages/administrativo/components/PPessoa/PPessoaTableFormDialog";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";
import type { PCertidaoFormValues } from "@/packages/certidao/components/PCertidao/PCertidaoFormValues";
import { usePCertidaoConsultaApresentanteHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoConsultaApresentanteHook";
import { isPCertidaoConsultaApresentanteResult } from "@/packages/certidao/interface/PCertidao/PCertidaoConsultaApresentanteInterface";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";

export interface PCertidaoEmissaoFormProps {
  open: boolean;
  isLoadingUsuarios: boolean;
  onEmit: (values: PCertidaoFormValues) => Promise<void>;
  onCancel: () => void;
  isSaving: boolean;
}

function getNowDateAndTime() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  return {
    date: `${year}-${month}-${day}`,
    time: `${hours}:${minutes}`,
  };
}

function getDefaultFiveYearRange(): DateRange {
  const end = startOfDay(new Date());
  const start = startOfDay(subYears(end, 5));
  return { from: start, to: end };
}

function normalizeDigits(value?: string): string {
  return (value ?? "").replace(/\D/g, "");
}

function formatMoney(value?: number): string {
  if (value === undefined || Number.isNaN(value)) return "—";
  return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
}

function formatDataPt(value?: Date | string): string {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString("pt-BR");
}

export function PCertidaoEmissaoForm({
  open,
  isLoadingUsuarios,
  onEmit,
  onCancel,
  isSaving,
}: PCertidaoEmissaoFormProps) {
  const { analise, isLoading: isLoadingConsulta, consultarApresentante, resetConsulta } =
    usePCertidaoConsultaApresentanteHook();

  const [apresentante, setApresentante] = useState("");
  const [cpfcnpj, setCpfcnpj] = useState("");
  const [dateRange, setDateRange] = useState<DateRange | undefined>(() => getDefaultFiveYearRange());
  const [consultationDone, setConsultationDone] = useState(false);
  const [homonimiaConfirmada, setHomonimiaConfirmada] = useState(false);
  const [isPPessoaDialogOpen, setIsPPessoaDialogOpen] = useState(false);

  const [usuarioId, setUsuarioId] = useState("");
  const [observacao, setObservacao] = useState("");

  const invalidateConsultation = useCallback(() => {
    setConsultationDone(false);
    setHomonimiaConfirmada(false);
    resetConsulta();
  }, [resetConsulta]);

  useEffect(() => {
    if (!open) return;
    setApresentante("");
    setCpfcnpj("");
    setDateRange(getDefaultFiveYearRange());
    setConsultationDone(false);
    setHomonimiaConfirmada(false);
    resetConsulta();
    setUsuarioId("");
    setObservacao("");
  }, [open, resetConsulta]);

  const tipoDerivado: "P" | "N" | null = useMemo(() => {
    if (!analise) return null;
    if (analise.titulosPorDocumento.length > 0) return "P";
    if (analise.candidatosHomonimia.length > 0 && !homonimiaConfirmada) return null;
    return "N";
  }, [analise, homonimiaConfirmada]);

  const emitDisabled = isSaving || isLoadingUsuarios || !analise || tipoDerivado === null;

  const handleSelectPessoa = (pessoa: PPessoaInterface) => {
    setApresentante(pessoa.nome ?? "");
    setCpfcnpj(pessoa.cpfcnpj ?? "");
    setIsPPessoaDialogOpen(false);
    invalidateConsultation();
  };

  const handleConsultar = async () => {
    const response = await consultarApresentante({
      apresentante: apresentante.trim(),
      cpfcnpj: cpfcnpj.trim(),
      data_inicio: dateRange?.from ? format(dateRange.from, "yyyy-MM-dd") : undefined,
      data_fim: dateRange?.to ? format(dateRange.to, "yyyy-MM-dd") : undefined,
    });
    setConsultationDone(isPCertidaoConsultaApresentanteResult(response));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!analise || tipoDerivado === null) return;

    const tipo_certidao = analise.titulosPorDocumento.length > 0 ? "P" : "N";
    let obs = observacao.trim();
    if (
      tipo_certidao === "N" &&
      analise.candidatosHomonimia.length > 0 &&
      analise.titulosPorDocumento.length === 0 &&
      homonimiaConfirmada
    ) {
      obs = [
        obs,
        "Certidão negativa após conferência de homonímia (Art. 300): registros localizados pelo nome não foram vinculados ao documento do requerente.",
      ]
        .filter(Boolean)
        .join("\n\n");
    }

    const emissaoTimestamp = getNowDateAndTime();

    await onEmit({
      apresentante: apresentante.trim(),
      cpfcnpj: cpfcnpj.trim(),
      tipo_certidao,
      status: "A",
      data_certidao: new Date(`${emissaoTimestamp.date}T00:00:00`),
      hora_certidao: emissaoTimestamp.time,
      usuario_id: usuarioId ? Number(usuarioId) : undefined,
      observacao: obs,
      qtd_protestos: tipo_certidao === "P" ? analise.titulosPorDocumento.length : 0,
    });
  };

  const busy = isLoadingConsulta;

  const stepSummary = [
    { id: "296", label: "296", title: "Dados", dim: false },
    { id: "299", label: "299", title: "Consulta", dim: false },
    {
      id: "297",
      label: "297",
      title: "Tipo",
      dim: !consultationDone,
    },
    {
      id: "300",
      label: "300",
      title: "Hom.",
      dim: !(
        consultationDone &&
        analise &&
        analise.candidatosHomonimia.length > 0 &&
        analise.titulosPorDocumento.length === 0
      ),
    },
  ];

  return (
    <>
      <form className="space-y-3 text-sm" onSubmit={handleSubmit}>
        <nav
          className="flex flex-wrap items-center gap-1 text-[11px] text-muted-foreground"
          aria-label="Referência das etapas (Arts. 296–300)"
        >
          {stepSummary.map((s, i) => (
            <span key={s.id} className="flex items-center gap-1">
              {i > 0 ? <ChevronRight className="h-3 w-3 opacity-50" /> : null}
              <span
                className={cn(
                  "rounded-full border px-2 py-0.5 tabular-nums",
                  s.dim ? "border-transparent opacity-40" : "border-border/80 bg-muted/40",
                )}
              >
                <span className="font-semibold text-[#FF6B00]">{s.label}</span>{" "}
                <span className="text-muted-foreground">{s.title}</span>
              </span>
            </span>
          ))}
        </nav>

        <div className="rounded-lg border border-border/70 bg-muted/15 p-3">
          <p className="mb-2 text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
            Requerimento · Art. 296
          </p>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-[minmax(0,1fr)_minmax(11rem,14rem)]">
            <div className="min-w-0 space-y-1">
              <Label htmlFor="emissao-apresentante" className="text-xs">
                Nome completo
              </Label>
              <div className="relative">
                <Input
                  id="emissao-apresentante"
                  value={apresentante}
                  onChange={(e) => {
                    setApresentante(e.target.value);
                    invalidateConsultation();
                  }}
                  placeholder="Conforme o requerimento"
                  className="h-9 pr-9 text-sm"
                  required
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="absolute top-1/2 right-0.5 h-8 w-8 -translate-y-1/2"
                  onClick={() => setIsPPessoaDialogOpen(true)}
                  aria-label="Buscar pessoa cadastrada"
                >
                  <Search className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
            <div className="min-w-0 space-y-1">
              <Label htmlFor="emissao-doc" className="text-xs">
                CPF ou CNPJ
              </Label>
              <Input
                id="emissao-doc"
                value={cpfcnpj}
                onChange={(e) => {
                  setCpfcnpj(e.target.value);
                  invalidateConsultation();
                }}
                placeholder="CPF ou CNPJ"
                className="h-9 text-sm"
                required
              />
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-2 sm:flex-row sm:items-end">
          <div className="min-w-0 flex-1 space-y-1">
            <Label className="text-xs">Período · padrão 5 anos (Art. 299)</Label>
            <DateRangePicker
              value={dateRange}
              onChange={(range) => {
                setDateRange(range);
                invalidateConsultation();
              }}
              placeholder="Intervalo"
              triggerClassName="h-9 text-sm"
            />
          </div>
          <Button
            type="button"
            size="sm"
            disabled={busy || !apresentante.trim() || !normalizeDigits(cpfcnpj)}
            className="w-full shrink-0 bg-[#FF6B00] text-white hover:bg-[#E56000] sm:w-auto"
            onClick={() => void handleConsultar()}
          >
            {busy ? (
              <>
                <Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />
                Consultando…
              </>
            ) : (
              <>
                <Search className="mr-2 h-3.5 w-3.5" />
                Consultar
              </>
            )}
          </Button>
        </div>

        <p className="text-[11px] leading-snug text-muted-foreground">
          Considera todos os títulos com protesto registrado no período, incluindo pagos e cancelados.
        </p>

        {consultationDone && analise ? (
          <>
            <Separator />
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                {analise.titulosPorDocumento.length > 0 ? (
                  <Badge className="border-green-700/30 bg-green-600/10 font-normal text-green-900 dark:text-green-100">
                    <CheckCircle2 className="mr-1 h-3 w-3" />
                    Positiva · Arts. 297–299
                  </Badge>
                ) : (
                  <Badge variant="secondary" className="font-normal">
                    <Info className="mr-1 h-3 w-3 opacity-70" />
                    Negativa (nada consta)
                  </Badge>
                )}
                <Badge variant="outline" className="font-normal tabular-nums">
                  {analise.titulosPorDocumento.length} débito(s) no documento
                </Badge>
              </div>

              {analise.titulosPorDocumento.length > 0 ? (
                <Alert className="border-green-600/25 bg-green-50/70 py-2 dark:bg-green-950/15">
                  <CheckCircle2 className="h-4 w-4 text-green-700" />
                  <AlertTitle className="text-sm">Relação para a certidão</AlertTitle>
                  <AlertDescription className="text-xs">
                    Lista dos protestos vinculados ao documento informado, incluindo pagos e cancelados.
                  </AlertDescription>
                </Alert>
              ) : (
                <Alert className="py-2">
                  <Info className="h-4 w-4" />
                  <AlertTitle className="text-sm">Sem protesto para o documento</AlertTitle>
                  <AlertDescription className="text-xs">
                    Salvo conferência de homonímia abaixo.
                  </AlertDescription>
                </Alert>
              )}

              {analise.titulosPorDocumento.length > 0 ? (
                <ScrollArea className="max-h-[148px] rounded-md border">
                  <div className="min-w-[300px]">
                    <div className="grid grid-cols-[minmax(0,1fr)_5rem_4rem_3rem] gap-x-2 border-b bg-muted/40 px-2 py-1.5 text-[10px] font-medium uppercase tracking-wide text-muted-foreground">
                      <span>Credor</span>
                      <span className="text-right">Valor</span>
                      <span className="text-center">Ref.</span>
                      <span className="truncate">Tit.</span>
                    </div>
                    {analise.titulosPorDocumento.map((row) => (
                      <div
                        key={row.titulo_id}
                        className="grid grid-cols-[minmax(0,1fr)_5rem_4rem_3rem] gap-x-2 border-b px-2 py-1.5 text-xs last:border-0"
                      >
                        <span className="truncate font-medium">{row.credor_nome ?? "—"}</span>
                        <span className="text-right tabular-nums text-muted-foreground">{formatMoney(row.valor_titulo)}</span>
                        <span className="text-center text-muted-foreground">
                          {formatDataPt(
                            (row.data_protesto ?? row.data_intimacao ?? row.data_apontamento) as string | Date,
                          )}
                        </span>
                        <span className="truncate text-muted-foreground">{row.numero_titulo ?? "—"}</span>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              ) : null}
            </div>

            {analise.titulosPorDocumento.length === 0 && analise.candidatosHomonimia.length > 0 ? (
              <Accordion type="single" collapsible defaultValue="homonym" className="rounded-lg border border-amber-500/35 bg-amber-50/40 dark:bg-amber-950/15">
                <AccordionItem value="homonym" className="border-0">
                  <AccordionTrigger className="px-3 py-2 text-sm hover:no-underline">
                    <span className="flex items-center gap-2 text-left">
                      <ShieldAlert className="h-4 w-4 shrink-0 text-amber-800" />
                      <span>
                        Art. 300 · Homonímia ({analise.candidatosHomonimia.length})
                      </span>
                    </span>
                  </AccordionTrigger>
                  <AccordionContent className="space-y-3 px-3 pb-3 pt-0">
                    <Alert className="border-amber-600/35 bg-amber-50/90 py-2 dark:bg-amber-950/25">
                      <AlertCircle className="h-4 w-4 text-amber-800" />
                      <AlertTitle className="text-amber-950 text-sm dark:text-amber-50">Nome igual, documento distinto</AlertTitle>
                      <AlertDescription className="text-xs text-amber-950/90 dark:text-amber-100/90">
                        Confira no livro antes de emitir negativa.
                      </AlertDescription>
                    </Alert>
                    <ScrollArea className="max-h-[88px] rounded-md border border-dashed bg-background/80">
                      <ul className="space-y-1 p-2 text-xs">
                        {analise.candidatosHomonimia.slice(0, 12).map((row) => (
                          <li key={row.titulo_id} className="truncate">
                            <span className="font-medium">{row.devedor_nome}</span>
                            <span className="text-muted-foreground"> · </span>
                            <span className="tabular-nums">{row.devedor_cpfcnpj ?? "—"}</span>
                          </li>
                        ))}
                      </ul>
                    </ScrollArea>
                    <div className="flex items-start gap-2 rounded-md border bg-card p-2">
                      <Checkbox
                        id="homonimia-ok"
                        checked={homonimiaConfirmada}
                        onCheckedChange={(v) => setHomonimiaConfirmada(Boolean(v))}
                        className="mt-0.5"
                      />
                      <label htmlFor="homonimia-ok" className="cursor-pointer text-xs leading-snug">
                        Após conferência do tabelião, confirmo que não se tratam do requerente — emitir{" "}
                        <strong>certidão negativa</strong>.
                      </label>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            ) : null}
          </>
        ) : null}

        <Separator />

        <div className="grid gap-2 sm:grid-cols-2">
          <p className="text-[11px] font-medium uppercase tracking-wide text-muted-foreground sm:col-span-2">
            Responsável e observação
          </p>
          <div className="space-y-1 sm:col-span-2">
            <Label htmlFor="emissao-usuario" className="text-xs">
              Usuário responsável
            </Label>
            <GUsuarioSelectObject
              value={usuarioId}
              onValueChange={setUsuarioId}
              placeholder="Opcional"
              disabled={isLoadingUsuarios}
              triggerClassName="h-9 text-sm"
            />
          </div>
          <div className="space-y-1 sm:col-span-2">
            <Label htmlFor="emissao-obs" className="text-xs">
              Observação
            </Label>
            <Textarea
              id="emissao-obs"
              rows={2}
              value={observacao}
              onChange={(e) => setObservacao(e.target.value)}
              placeholder="Opcional"
              className="min-h-[52px] resize-y text-sm"
            />
          </div>
        </div>

        <div className="flex flex-col gap-2 border-t pt-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="min-h-4 text-[11px] text-muted-foreground">
            {tipoDerivado === null && consultationDone && analise?.titulosPorDocumento.length === 0 && analise &&
            analise.candidatosHomonimia.length > 0 ? (
              <span>Marque a confirmação de homonímia (Art. 300).</span>
            ) : !consultationDone ? (
              <span>Consulte os registros antes de emitir.</span>
            ) : null}
          </p>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" size="sm" onClick={onCancel}>
              Cancelar
            </Button>
            <Button
              type="submit"
              size="sm"
              disabled={emitDisabled}
              className="bg-[#FF6B00] text-white hover:bg-[#E56000]"
            >
              {isSaving ? (
                <>
                  <Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />
                  Emitindo…
                </>
              ) : (
                "Emitir"
              )}
            </Button>
          </div>
        </div>
      </form>

      <PPessoaTableFormDialog
        isOpen={isPPessoaDialogOpen}
        tipoPessoa="P"
        onClose={setIsPPessoaDialogOpen}
        onSave={handleSelectPessoa}
        buttonIsLoading={false}
      />
    </>
  );
}
