'use client';

import type { DateRange } from 'react-day-picker';
import { Filter, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DateRangePicker } from '@/shared/components/dateRangePicker/DateRangePicker';

type PTituloIntimacaoBatchFilterProps = {
  searchQuery: string;
  onSearchQueryChange: (value: string) => void;
  statusFilter: '' | 'P' | 'I';
  onStatusFilterChange: (value: '' | 'P' | 'I') => void;
  dateRange: DateRange | undefined;
  onDateRangeChange: (value: DateRange | undefined) => void;
  onSearch: () => void;
  onClear: () => void;
};

export function PTituloIntimacaoBatchFilter({
  searchQuery,
  onSearchQueryChange,
  statusFilter,
  onStatusFilterChange,
  dateRange,
  onDateRangeChange,
  onSearch,
  onClear,
}: PTituloIntimacaoBatchFilterProps) {
  return (
    <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
      <div className="grid gap-4 xl:grid-cols-[1fr_auto]">
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          <div className="space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Busca unificada
            </label>
            <div className="relative w-full">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
              <Input
                type="search"
                className="pl-8"
                placeholder="Pessoa, CPF/CNPJ, protocolo, nosso número ou título"
                value={searchQuery}
                onChange={(event) => onSearchQueryChange(event.target.value)}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Status intimação
            </label>
            <Select
              value={statusFilter || 'all'}
              onValueChange={(value) => onStatusFilterChange(value === 'P' || value === 'I' ? value : '')}
            >
              <SelectTrigger>
                <SelectValue placeholder="Todos os status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos os status</SelectItem>
                <SelectItem value="P">Pendente</SelectItem>
                <SelectItem value="I">Já intimado</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
              Intervalo (intimação / apontamento)
            </label>
            <DateRangePicker value={dateRange} onChange={onDateRangeChange} placeholder="Todas as datas" />
          </div>
        </div>

        <div className="flex items-end gap-2 xl:justify-end">
          <Button type="button" className="bg-[#FF6B00] text-white hover:bg-[#E56000]" onClick={onSearch}>
            <Search className="mr-1 h-4 w-4" />
            Pesquisar
          </Button>
          <Button type="button" variant="outline" onClick={onClear}>
            <Filter className="mr-1 h-4 w-4" />
            Limpar
          </Button>
        </div>
      </div>
    </section>
  );
}
