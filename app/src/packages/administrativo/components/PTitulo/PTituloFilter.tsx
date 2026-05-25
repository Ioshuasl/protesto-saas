"use client";

import { format, parseISO } from "date-fns";
import { Search } from "lucide-react";
import type { DateRange } from "react-day-picker";
import { Input } from "@/components/ui/input";
import { PBancoSelectObject } from "@/packages/administrativo/components/PBanco/PBancoSelectObject";
import { PEspecieSelectObject } from "@/packages/administrativo/components/PEspecie/PEspecieSelectObject";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";

interface PTituloFilterProps {
  searchQuery: string;
  startDate: string;
  endDate: string;
  bancoId: string;
  especieId: string;
  ocorrenciaId: string;
  onSearchChange: (value: string) => void;
  onStartDateChange: (value: string) => void;
  onEndDateChange: (value: string) => void;
  onBancoChange: (value: string) => void;
  onEspecieChange: (value: string) => void;
  onOcorrenciaChange: (value: string) => void;
}

function toDateRange(startDate: string, endDate: string): DateRange | undefined {
  if (!startDate && !endDate) return undefined;
  return {
    from: startDate ? parseISO(startDate) : undefined,
    to: endDate ? parseISO(endDate) : undefined,
  };
}

export function PTituloFilter({
  searchQuery,
  startDate,
  endDate,
  bancoId,
  especieId,
  ocorrenciaId,
  onSearchChange,
  onStartDateChange,
  onEndDateChange,
  onBancoChange,
  onEspecieChange,
  onOcorrenciaChange,
}: PTituloFilterProps) {
  const handleDateRangeChange = (range: DateRange | undefined) => {
    if (!range) {
      onStartDateChange("");
      onEndDateChange("");
      return;
    }
    onStartDateChange(range.from ? format(range.from, "yyyy-MM-dd") : "");
    onEndDateChange(range.to ? format(range.to, "yyyy-MM-dd") : "");
  };

  return (
    <div className="grid w-full gap-3 md:grid-cols-2 xl:grid-cols-[minmax(18rem,1.35fr)_minmax(12rem,1fr)_minmax(12rem,1fr)_minmax(12rem,1fr)_minmax(14rem,1fr)]">
      <div className="relative w-full">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
        <Input
          type="search"
          placeholder="Pessoa, CPF/CNPJ, protocolo, nosso número ou título"
          className="pl-8"
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>

      <PBancoSelectObject
        value={bancoId}
        onValueChange={onBancoChange}
        placeholder="Todos os bancos"
        searchPlaceholder="Buscar banco..."
        emptyMessage="Nenhum banco disponível"
      />

      <PEspecieSelectObject
        value={especieId}
        onValueChange={onEspecieChange}
        placeholder="Todas as espécies"
        searchPlaceholder="Buscar espécie..."
        emptyMessage="Nenhuma espécie disponível"
      />

      <POcorrenciasSelectObject
        value={ocorrenciaId}
        onValueChange={onOcorrenciaChange}
        placeholder="Todas as ocorrências"
        searchPlaceholder="Buscar ocorrência..."
        emptyMessage="Nenhuma ocorrência disponível"
      />

      <DateRangePicker
        value={toDateRange(startDate, endDate)}
        onChange={handleDateRangeChange}
        placeholder="Período (data apontamento)"
        clearAriaLabel="Limpar filtro de período"
      />
    </div>
  );
}
