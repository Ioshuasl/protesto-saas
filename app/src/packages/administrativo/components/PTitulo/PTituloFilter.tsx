"use client";

import { format, parseISO } from "date-fns";
import { Search } from "lucide-react";
import type { DateRange } from "react-day-picker";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";

interface PTituloFilterProps {
  searchQuery: string;
  status: string;
  startDate: string;
  endDate: string;
  onSearchChange: (value: string) => void;
  onStatusChange: (value: string) => void;
  onStartDateChange: (value: string) => void;
  onEndDateChange: (value: string) => void;
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
  status,
  startDate,
  endDate,
  onSearchChange,
  onStatusChange,
  onStartDateChange,
  onEndDateChange,
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
    <div className="grid w-full gap-3 md:grid-cols-2 lg:grid-cols-3">
      <div className="relative w-full">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
        <Input
          type="search"
          placeholder="Nome/CPF das partes (devedor, apresentante...)"
          className="pl-8"
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>

      <Select value={status} onValueChange={onStatusChange}>
        <SelectTrigger>
          <SelectValue placeholder="Filtrar por status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">Todos os status</SelectItem>
          <SelectItem value="Apontado">Apontado</SelectItem>
          <SelectItem value="Em Tríduo">Em Tríduo</SelectItem>
          <SelectItem value="Liquidado">Liquidado</SelectItem>
          <SelectItem value="Pago">Pago</SelectItem>
          <SelectItem value="Protestado">Protestado</SelectItem>
          <SelectItem value="Desistido">Desistido</SelectItem>
          <SelectItem value="Cancelado">Cancelado</SelectItem>
        </SelectContent>
      </Select>

      <DateRangePicker
        value={toDateRange(startDate, endDate)}
        onChange={handleDateRangeChange}
        placeholder="Período (data apontamento)"
        clearAriaLabel="Limpar filtro de período"
      />
    </div>
  );
}
