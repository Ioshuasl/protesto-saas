"use client";

import { format, parseISO } from "date-fns";
import { Search } from "lucide-react";
import type { DateRange } from "react-day-picker";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  PCERTIDAO_FILTER_ALL,
  defaultPCertidaoFilterState,
  type PCertidaoFilterState,
} from "@/packages/certidao/components/PCertidao/pCertidaoFilterUtils";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";
import { useHydrated } from "@/shared/hooks/useHydrated";

const TIPO_CERTIDAO_LABELS: Record<string, string> = {
  [PCERTIDAO_FILTER_ALL]: "Todos os tipos",
  P: "Positiva",
  N: "Negativa",
};

const STATUS_LABELS: Record<string, string> = {
  [PCERTIDAO_FILTER_ALL]: "Todos os status",
  A: "Ativa/Emitida",
  C: "Cancelada",
};

function parseDateValue(value: string): Date | undefined {
  if (!value) return undefined;
  const parsed = parseISO(value);
  return Number.isNaN(parsed.getTime()) ? undefined : parsed;
}

function filterStateToDateRange(value: PCertidaoFilterState): DateRange | undefined {
  const from = parseDateValue(value.data_inicio);
  const to = parseDateValue(value.data_fim);
  if (!from && !to) return undefined;
  return { from, to };
}

interface PCertidaoFilterProps {
  value: PCertidaoFilterState;
  onChange: (value: PCertidaoFilterState) => void;
  onSearch?: () => void;
  disabled?: boolean;
}

export function PCertidaoFilter({
  value,
  onChange,
  onSearch,
  disabled,
}: PCertidaoFilterProps) {
  const hydrated = useHydrated();
  const update = (patch: Partial<PCertidaoFilterState>) =>
    onChange({ ...value, ...patch });
  const dateRange = filterStateToDateRange(value);

  const clearFilters = () => {
    onChange(defaultPCertidaoFilterState);
  };

  return (
    <section className="rounded-xl border bg-card p-3 shadow-xs md:p-4">
      <div className="grid min-w-0 gap-3 2xl:grid-cols-[minmax(0,1fr)_auto]">
        <div className="grid min-w-0 gap-3 md:grid-cols-2 xl:grid-cols-[minmax(180px,1.25fr)_minmax(145px,0.85fr)_minmax(145px,0.85fr)_minmax(165px,1fr)]">
          <div className="space-y-1.5">
            <label className="text-[0.68rem] font-medium uppercase tracking-wide text-muted-foreground">
              Busca por CPF/CNPJ ou nome
            </label>
            <div className="relative">
              <Search className="absolute left-2.5 top-2 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Ex.: João da Silva ou 111.111.111-11"
                className="h-8 pl-8 text-xs"
                value={value.busca}
                onChange={(event) => update({ busca: event.target.value })}
                onKeyDown={(event) => {
                  if (event.key === "Enter") onSearch?.();
                }}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[0.68rem] font-medium uppercase tracking-wide text-muted-foreground">
              Tipo de certidão
            </label>
            {hydrated ? (
              <Select
                value={value.tipo_certidao}
                onValueChange={(tipo_certidao) => update({ tipo_certidao })}
              >
                <SelectTrigger size="sm" className="h-8 text-xs">
                  <SelectValue placeholder="Todos os tipos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={PCERTIDAO_FILTER_ALL}>Todos os tipos</SelectItem>
                  <SelectItem value="P">Positiva</SelectItem>
                  <SelectItem value="N">Negativa</SelectItem>
                </SelectContent>
              </Select>
            ) : (
              <Button type="button" variant="outline" size="sm" disabled className="w-full justify-between font-normal">
                {TIPO_CERTIDAO_LABELS[value.tipo_certidao] ?? "Tipo"}
              </Button>
            )}
          </div>

          <div className="space-y-1.5">
            <label className="text-[0.68rem] font-medium uppercase tracking-wide text-muted-foreground">
              Status
            </label>
            {hydrated ? (
              <Select value={value.status} onValueChange={(status) => update({ status })}>
                <SelectTrigger size="sm" className="h-8 text-xs">
                  <SelectValue placeholder="Todos os status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={PCERTIDAO_FILTER_ALL}>Todos os status</SelectItem>
                  <SelectItem value="A">Ativa/Emitida</SelectItem>
                  <SelectItem value="C">Cancelada</SelectItem>
                </SelectContent>
              </Select>
            ) : (
              <Button type="button" variant="outline" size="sm" disabled className="w-full justify-between font-normal">
                {STATUS_LABELS[value.status] ?? "Status"}
              </Button>
            )}
          </div>

          <div className="space-y-1.5">
            <label className="text-[0.68rem] font-medium uppercase tracking-wide text-muted-foreground">
              Período da certidão
            </label>
            <DateRangePicker
              value={dateRange}
              onChange={(range) =>
                update({
                  data_inicio: range?.from ? format(range.from, "yyyy-MM-dd") : "",
                  data_fim: range?.to ? format(range.to, "yyyy-MM-dd") : "",
                })
              }
              placeholder="Selecione o período"
              disabled={disabled}
              triggerClassName="h-8 text-xs"
            />
          </div>
        </div>

        <div className="flex flex-wrap items-end gap-2 md:justify-end 2xl:flex-nowrap">
          <Button
            type="button"
            size="sm"
            className="bg-[#FF6B00] text-white hover:bg-[#E56000]"
            onClick={onSearch}
            disabled={disabled}
          >
            <Search className="mr-1 h-4 w-4" />
            Pesquisar
          </Button>
          <Button type="button" variant="outline" size="sm" onClick={clearFilters} disabled={disabled}>
            Limpar
          </Button>
        </div>
      </div>
    </section>
  );
}
