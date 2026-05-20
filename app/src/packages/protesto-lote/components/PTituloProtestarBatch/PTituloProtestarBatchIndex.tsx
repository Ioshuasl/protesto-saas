"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { DateRange } from "react-day-picker";
import { Filter, Gavel, PlusCircle, Search } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";
import { usePTituloProtestarBatchReadHook } from "@/packages/protesto-lote/hooks/PTituloProtestarBatch/usePTituloProtestarBatchReadHook";
import type { PTituloProtestarBatchInterface } from "@/packages/protesto-lote/interface/PTituloProtestarBatch/PTituloProtestarBatchInterface";
import { PTituloProtestarBatchTable } from "./PTituloProtestarBatchTable";

function getStatusProtestoCode(item: PTituloProtestarBatchInterface): "P" | "R" {
  return item.data_protesto ? "R" : "P";
}

function calculateSelectedTotal(data: PTituloProtestarBatchInterface[], selectedIds: Set<number>): number {
  return data.reduce((acc, item) => (selectedIds.has(item.titulo_id) ? acc + (item.valor_titulo ?? 0) : acc), 0);
}

function getDateOnly(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

export default function PTituloProtestarBatchIndex() {
  const { titulosProtestarBatch, isLoading, fetchTitulosProtestarBatch } = usePTituloProtestarBatchReadHook();
  const initialFetchDoneRef = useRef(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<"" | "P" | "R">("P");
  const [dateRange, setDateRange] = useState<DateRange | undefined>(undefined);
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (initialFetchDoneRef.current) return;
    initialFetchDoneRef.current = true;
    void fetchTitulosProtestarBatch();
  }, [fetchTitulosProtestarBatch]);

  const filteredData = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    const from = dateRange?.from ? getDateOnly(dateRange.from) : undefined;
    const to = dateRange?.to ? getDateOnly(dateRange.to) : undefined;

    return titulosProtestarBatch
      .filter((item) => Boolean(item.data_intimacao))
      .filter((item) => {
        if (query) {
          const searchContent = [
            item.numero_titulo,
            item.nosso_numero,
            item.numero_apontamento?.toString(),
            item.apresentante,
            item.cpfcnpj,
          ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();
          if (!searchContent.includes(query)) return false;
        }

        if (statusFilter) {
          if (getStatusProtestoCode(item) !== statusFilter) return false;
        }

        if (from || to) {
          const ref = item.data_protesto ?? item.data_intimacao;
          if (!ref) return false;
          const current = getDateOnly(new Date(ref));
          if (from && current < from) return false;
          if (to && current > to) return false;
        }

        return true;
      });
  }, [searchQuery, statusFilter, dateRange?.from, dateRange?.to, titulosProtestarBatch]);

  const resumo = useMemo(() => {
    const total = filteredData.length;
    const pendentes = filteredData.filter((item) => getStatusProtestoCode(item) === "P").length;
    const protestados = filteredData.filter((item) => getStatusProtestoCode(item) === "R").length;
    const selecionados = filteredData.filter((item) => selectedIds.has(item.titulo_id)).length;
    const valorSelecionado = calculateSelectedTotal(filteredData, selectedIds);

    return { total, pendentes, protestados, selecionados, valorSelecionado };
  }, [filteredData, selectedIds]);

  const handleToggleOne = (tituloId: number, checked: boolean) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (checked) next.add(tituloId);
      else next.delete(tituloId);
      return next;
    });
  };

  const handleToggleAll = (checked: boolean) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (checked) {
        filteredData.forEach((item) => next.add(item.titulo_id));
      } else {
        filteredData.forEach((item) => next.delete(item.titulo_id));
      }
      return next;
    });
  };

  const handleClearFilters = () => {
    setSearchQuery("");
    setStatusFilter("P");
    setDateRange(undefined);
  };

  const handleProtestarSelecionados = () => {
    const selectedRows = filteredData.filter((item) => selectedIds.has(item.titulo_id));
    if (selectedRows.length === 0) {
      toast.warning("Nenhum título selecionado", {
        description: "Selecione ao menos um título para iniciar o protesto em lote.",
      });
      return;
    }

    toast.info("Fluxo em construção", {
      description: `${selectedRows.length} título(s) pronto(s) para protesto em lote.`,
    });
  };

  const handlePrintInstrumentoProtesto = (titulo: PTituloProtestarBatchInterface) => {
    if (!titulo.data_protesto) {
      toast.warning("Protesto pendente", {
        description: `O título #${titulo.titulo_id} ainda não possui data de protesto para impressão do instrumento.`,
      });
      return;
    }

    toast.info("Impressão em construção", {
      description: `Instrumento de protesto do título #${titulo.titulo_id} será integrado em seguida.`,
    });
  };

  const handlePrintCertidaoProtesto = (titulo: PTituloProtestarBatchInterface) => {
    if (!titulo.data_protesto) {
      toast.warning("Protesto pendente", {
        description: `O título #${titulo.titulo_id} ainda não possui data de protesto para emissão da certidão.`,
      });
      return;
    }

    toast.info("Impressão em construção", {
      description: `Certidão de protesto do título #${titulo.titulo_id} será integrada em seguida.`,
    });
  };

  return (
    <div className="flex w-full flex-col gap-5">
      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight">Protestar Títulos em Lote</h1>
            <p className="text-sm text-muted-foreground">
              Concentre os títulos intimados e execute o protesto em lote com controle operacional.
            </p>
          </div>
          <Button
            type="button"
            className="bg-[#FF6B00] text-white transition-transform duration-200 hover:-translate-y-0.5 hover:bg-[#E56000]"
            onClick={handleProtestarSelecionados}
          >
            <Gavel className="mr-1 h-4 w-4" />
            Protestar selecionados
          </Button>
        </div>

        <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-5">
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">
            Total: <span className="font-semibold">{resumo.total}</span>
          </div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">
            Pendentes: <span className="font-semibold text-amber-700">{resumo.pendentes}</span>
          </div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">
            Já protestados: <span className="font-semibold text-emerald-700">{resumo.protestados}</span>
          </div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">
            Selecionados: <span className="font-semibold">{resumo.selecionados}</span>
          </div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">
            Valor selecionado:{" "}
            <span className="font-semibold">
              {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(resumo.valorSelecionado)}
            </span>
          </div>
        </div>
      </section>

      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="grid gap-4 xl:grid-cols-[1fr_auto]">
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Busca por título / nosso número / número apontamento / apresentante
              </label>
              <Input
                placeholder="Ex.: 1001, 900000001, 5001, João da Silva"
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Status protesto</label>
              <Select value={statusFilter || "all"} onValueChange={(value) => setStatusFilter(value === "P" || value === "R" ? value : "")}>
                <SelectTrigger>
                  <SelectValue placeholder="Todos os status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os status</SelectItem>
                  <SelectItem value="P">Pendente</SelectItem>
                  <SelectItem value="R">Já protestado</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Intervalo (protesto / intimação)
              </label>
              <DateRangePicker value={dateRange} onChange={setDateRange} placeholder="Todas as datas" />
            </div>
          </div>

          <div className="flex items-end gap-2 xl:justify-end">
            <Button type="button" className="bg-[#FF6B00] text-white hover:bg-[#E56000]">
              <Search className="mr-1 h-4 w-4" />
              Pesquisar
            </Button>
            <Button type="button" variant="outline" onClick={handleClearFilters}>
              <Filter className="mr-1 h-4 w-4" />
              Limpar
            </Button>
          </div>
        </div>
      </section>

      {selectedIds.size > 0 ? (
        <div className="flex justify-start px-1 py-1">
          <span
            role="button"
            tabIndex={0}
            className="inline-flex cursor-pointer items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium text-[#FF6B00] transition-all duration-200 hover:-translate-y-0.5 hover:bg-[#FF6B00]/12 hover:text-[#E56000] hover:shadow-sm active:translate-y-0 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#FF6B00]/35"
            onClick={() => setSelectedIds(new Set())}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                setSelectedIds(new Set());
              }
            }}
          >
            <PlusCircle className="h-3.5 w-3.5 shrink-0" strokeWidth={1.5} aria-hidden />
            Limpar seleção
          </span>
        </div>
      ) : null}

      <PTituloProtestarBatchTable
        data={filteredData}
        isLoading={isLoading}
        selectedIds={selectedIds}
        onToggleOne={handleToggleOne}
        onToggleAll={handleToggleAll}
        onPrintInstrumentoProtesto={handlePrintInstrumentoProtesto}
        onPrintCertidaoProtesto={handlePrintCertidaoProtesto}
      />
    </div>
  );
}
