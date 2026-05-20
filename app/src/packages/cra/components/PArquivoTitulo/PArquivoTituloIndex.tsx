"use client";

import { useEffect, useMemo, useState } from "react";
import { Filter, Search } from "lucide-react";
import type { DateRange } from "react-day-picker";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { usePTituloArquivoReadHook } from "@/packages/cra/hooks/PTituloArquivo/usePTituloArquivoReadHook";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";
import { PArquivoTituloTable } from "./PArquivoTituloTable";

function getDateOnly(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

export default function PArquivoTituloIndex() {
  const { arquivosTitulo, isLoading, fetchArquivosTitulo } = usePTituloArquivoReadHook();
  const [dateRange, setDateRange] = useState<DateRange | undefined>(undefined);

  useEffect(() => {
    void fetchArquivosTitulo();
  }, [fetchArquivosTitulo]);

  const filteredArquivos = useMemo(() => {
    const from = dateRange?.from ? getDateOnly(dateRange.from) : undefined;
    const to = dateRange?.to ? getDateOnly(dateRange.to) : undefined;

    return arquivosTitulo.filter((arquivo) => {
      if (!from && !to) return true;
      if (!arquivo.data_importacao) return false;
      const current = getDateOnly(new Date(arquivo.data_importacao));
      if (from && current < from) return false;
      if (to && current > to) return false;
      return true;
    });
  }, [arquivosTitulo, dateRange?.from, dateRange?.to]);

  const handleGerarArquivoConfirmacao = (arquivo: PArquivoTituloInterface) => {
    toast.info("Funcionalidade em construção", {
      description: `Geração de confirmação para "${arquivo.nome_arquivo ?? "arquivo"}" ainda não implementada.`,
    });
  };

  const handleEstornarRemessa = (arquivo: PArquivoTituloInterface) => {
    toast.info("Funcionalidade em construção", {
      description: `Estorno da remessa "${arquivo.nome_arquivo ?? "arquivo"}" ainda não implementado.`,
    });
  };

  const handleClearFilters = () => setDateRange(undefined);

  return (
    <div className="flex w-full flex-col gap-4">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">CRA - Confirmação</h1>
        <p className="text-sm text-muted-foreground">
          Acompanhe os arquivos importados e execute as ações de confirmação da remessa.
        </p>
      </div>

      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="grid gap-4 xl:grid-cols-[1fr_auto]">
          <div className="max-w-md space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Intervalo de importação (data)
            </label>
            <DateRangePicker value={dateRange} onChange={setDateRange} placeholder="Todas as datas" />
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

      <PArquivoTituloTable
        data={filteredArquivos}
        isLoading={isLoading}
        onGerarArquivoConfirmacao={handleGerarArquivoConfirmacao}
        onEstornarRemessa={handleEstornarRemessa}
      />
    </div>
  );
}
