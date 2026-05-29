"use client";

import { format, parseISO } from "date-fns";
import { Filter, Search } from "lucide-react";
import type { DateRange } from "react-day-picker";
import { Button } from "@/components/ui/button";
import { PBancoSelectObject } from "@/packages/administrativo/components/PBanco/PBancoSelectObject";
import {
  defaultPArquivoTituloFilterState,
  type PArquivoTituloFilterState,
} from "@/packages/cra/components/PArquivoTitulo/pArquivoTituloFilterUtils";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";

function toDateRange(dataInicio: string, dataFim: string): DateRange | undefined {
  if (!dataInicio && !dataFim) return undefined;
  return {
    from: dataInicio ? parseISO(dataInicio) : undefined,
    to: dataFim ? parseISO(dataFim) : undefined,
  };
}

interface PArquivoTituloFilterProps {
  value: PArquivoTituloFilterState;
  onChange: (next: PArquivoTituloFilterState) => void;
  onSearch?: () => void;
  disabled?: boolean;
}

export function PArquivoTituloFilter({
  value,
  onChange,
  onSearch,
  disabled,
}: PArquivoTituloFilterProps) {
  const update = (patch: Partial<PArquivoTituloFilterState>) =>
    onChange({ ...value, ...patch });

  const clearFilters = () => {
    onChange(defaultPArquivoTituloFilterState);
  };

  return (
    <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
      <div className="grid gap-4 xl:grid-cols-[1fr_auto]">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Banco (portador)
            </label>
            <PBancoSelectObject
              value={value.bancoId || undefined}
              onValueChange={(bancoId) => update({ bancoId })}
              placeholder="Todos os bancos"
              searchPlaceholder="Buscar banco (código ou descrição)..."
              emptyMessage="Nenhum banco disponível"
              disabled={disabled}
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Intervalo de importação (data)
            </label>
            <DateRangePicker
              value={toDateRange(value.data_inicio, value.data_fim)}
              onChange={(range) =>
                update({
                  data_inicio: range?.from ? format(range.from, "yyyy-MM-dd") : "",
                  data_fim: range?.to ? format(range.to, "yyyy-MM-dd") : "",
                })
              }
              placeholder="Todas as datas"
              clearAriaLabel="Limpar intervalo de importação"
              disabled={disabled}
            />
          </div>
        </div>

        <div className="flex flex-wrap items-end gap-2 xl:justify-end">
          <Button
            type="button"
            className="bg-[#FF6B00] text-white hover:bg-[#E56000]"
            onClick={onSearch}
            disabled={disabled}
          >
            <Search className="mr-1 h-4 w-4" />
            Pesquisar
          </Button>
          <Button type="button" variant="outline" onClick={clearFilters} disabled={disabled}>
            <Filter className="mr-1 h-4 w-4" />
            Limpar
          </Button>
        </div>
      </div>
    </section>
  );
}
