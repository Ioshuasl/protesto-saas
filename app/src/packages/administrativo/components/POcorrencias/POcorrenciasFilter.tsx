"use client";

import { Search } from "lucide-react";

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
  POCORRENCIAS_FILTER_ALL,
  type POcorrenciasFilterState,
} from "@/packages/administrativo/components/POcorrencias/pocorrenciasFilterUtils";
import {
  POCORRENCIAS_TIPO_LABELS,
  POCORRENCIAS_TIPO_OPCOES,
} from "@/packages/administrativo/schemas/POcorrencias/pocorrenciasTipoConstants";
import { useHydrated } from "@/shared/hooks/useHydrated";

interface POcorrenciasFilterProps {
  value: POcorrenciasFilterState;
  onChange: (value: POcorrenciasFilterState) => void;
}

export function POcorrenciasFilter({ value, onChange }: POcorrenciasFilterProps) {
  const hydrated = useHydrated();
  const update = (patch: Partial<POcorrenciasFilterState>) => onChange({ ...value, ...patch });

  const tipoLabel =
    value.tipo === POCORRENCIAS_FILTER_ALL
      ? "Todos os tipos"
      : (POCORRENCIAS_TIPO_LABELS[value.tipo as keyof typeof POCORRENCIAS_TIPO_LABELS] ??
        value.tipo);

  return (
    <div className="flex w-full flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
        <Input
          type="search"
          placeholder="Buscar por código ou descrição..."
          className="pl-8"
          value={value.search}
          onChange={(e) => update({ search: e.target.value })}
        />
      </div>

      {hydrated ? (
        <Select value={value.tipo} onValueChange={(tipo) => update({ tipo })}>
          <SelectTrigger className="w-full sm:w-[200px]">
            <SelectValue placeholder="Tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={POCORRENCIAS_FILTER_ALL}>Todos os tipos</SelectItem>
            {POCORRENCIAS_TIPO_OPCOES.map((tipo) => (
              <SelectItem key={tipo} value={tipo}>
                {POCORRENCIAS_TIPO_LABELS[tipo]}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      ) : (
        <Button
          type="button"
          variant="outline"
          disabled
          className="w-full justify-between font-normal sm:w-[200px]"
        >
          {tipoLabel}
        </Button>
      )}
    </div>
  );
}
