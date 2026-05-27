"use client";

import { Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { GEmolumentoPeriodoSelectObject } from "@/packages/administrativo/components/GEmolumentoPeriodo/GEmolumentoPeriodoSelectObject";
import type { GEmolumentoListFilter } from "@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface";

export interface GEmolumentoFilterValues {
  emolumento_periodo_id: string;
  busca: string;
  sistema_id: null;
}

export function buildGEmolumentoListFilter(values: GEmolumentoFilterValues): GEmolumentoListFilter {
  const trimmedPeriodo = values.emolumento_periodo_id.trim();
  const emolumento_periodo_id =
    trimmedPeriodo && Number.isFinite(Number(trimmedPeriodo))
      ? Number(trimmedPeriodo)
      : undefined;

  const trimmedBusca = values.busca.trim();

  return {
    emolumento_periodo_id,
    busca: trimmedBusca || undefined,
    sistema_id: null,
  };
}

interface GEmolumentoFilterProps {
  value: GEmolumentoFilterValues;
  isLoading?: boolean;
  onChange: (value: GEmolumentoFilterValues) => void;
  onSubmit: () => void;
  onClear: () => void;
}

export function GEmolumentoFilter({
  value,
  isLoading,
  onChange,
  onSubmit,
  onClear,
}: GEmolumentoFilterProps) {
  return (
    <div className="flex w-full flex-col gap-3 lg:flex-row lg:items-center">
      <div className="w-full sm:max-w-md">
        <GEmolumentoPeriodoSelectObject
          value={value.emolumento_periodo_id}
          onValueChange={(emolumentoPeriodoId) =>
            onChange({ ...value, emolumento_periodo_id: emolumentoPeriodoId })
          }
          placeholder="Período de emolumento"
          searchPlaceholder="Buscar período de emolumento..."
        />
      </div>

      <div className="relative w-full flex-1">
        <Search
          className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
          strokeWidth={1.5}
        />
        <Input
          type="search"
          placeholder="Descrição ou código do grupo de selo"
          className="pl-8"
          value={value.busca}
          onChange={(event) => onChange({ ...value, busca: event.target.value })}
        />
      </div>

      <div className="flex shrink-0 items-center gap-2">
        <Button onClick={onSubmit} disabled={isLoading} className="bg-[#FF6B00] text-white hover:bg-[#E56000]">
          Filtrar
        </Button>
        <Button onClick={onClear} variant="outline" disabled={isLoading}>
          Limpar
        </Button>
      </div>
    </div>
  );
}
