'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import type { DateRange } from 'react-day-picker';
import { CheckCheck } from 'lucide-react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import type { PTituloBatchRowBase } from '@/packages/administrativo/data/PTitulo/ptituloIndexItemToBatchMapper';
import { buildPTituloWorkflowBatchQuery } from '@/packages/administrativo/data/PTitulo/ptituloWorkflowBatchQuery';
import { usePTituloWorkflowBatchReadHook } from '@/packages/administrativo/hooks/PTitulo/usePTituloWorkflowBatchReadHook';
import { Pagination } from '@/shared/components/pagination/Pagination';
import { PTituloApontamentoBatchFilter } from './PTituloApontamentoBatchFilter';
import { PTituloApontamentoBatchTable } from './PTituloApontamentoBatchTable';

const PER_PAGE = 20;

function getDateOnly(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function calculateSelectedTotal(data: PTituloBatchRowBase[], selectedIds: Set<number>): number {
  return data.reduce((acc, item) => (selectedIds.has(item.titulo_id) ? acc + (item.valor_titulo ?? 0) : acc), 0);
}

export default function PTituloApontamentoBatchIndex() {
  const { titulos, isLoading, fetchTitulos } = usePTituloWorkflowBatchReadHook({
    successMessage: 'Títulos para apontamento em lote listados com sucesso',
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'' | 'P' | 'A'>('P');
  const [dateRange, setDateRange] = useState<DateRange | undefined>(undefined);
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);

  const buildWorkflowQuery = useCallback(
    (busca?: string) =>
      buildPTituloWorkflowBatchQuery({
        workflow_etapa: 'apontamento',
        statusFilter,
        busca,
      }),
    [statusFilter],
  );

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedSearchQuery(searchQuery.trim()), 400);
    return () => window.clearTimeout(timer);
  }, [searchQuery]);

  useEffect(() => {
    void fetchTitulos(buildWorkflowQuery(debouncedSearchQuery));
  }, [fetchTitulos, buildWorkflowQuery, debouncedSearchQuery]);

  useEffect(() => {
    setCurrentPage(1);
  }, [statusFilter, debouncedSearchQuery, dateRange?.from, dateRange?.to]);

  const filteredData = useMemo(() => {
    const from = dateRange?.from ? getDateOnly(dateRange.from) : undefined;
    const to = dateRange?.to ? getDateOnly(dateRange.to) : undefined;

    return titulos.filter((item) => {
      if (from || to) {
        const ref = item.data_apontamento ?? item.data_cadastro;
        if (!ref) return false;
        const current = getDateOnly(ref);
        if (from && current < from) return false;
        if (to && current > to) return false;
      }
      return true;
    });
  }, [dateRange?.from, dateRange?.to, titulos]);

  const totalPages = useMemo(() => (filteredData.length > 0 ? Math.ceil(filteredData.length / PER_PAGE) : 0), [filteredData.length]);

  useEffect(() => {
    if (totalPages === 0 && currentPage !== 1) {
      setCurrentPage(1);
      return;
    }
    if (totalPages > 0 && currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * PER_PAGE;
    return filteredData.slice(start, start + PER_PAGE);
  }, [currentPage, filteredData]);

  const pagination = useMemo(
    () => ({
      page: currentPage,
      per_page: PER_PAGE,
      total: filteredData.length,
      total_pages: totalPages,
    }),
    [currentPage, filteredData.length, totalPages],
  );

  const resumo = useMemo(() => {
    const total = filteredData.length;
    const pendentes = filteredData.filter((item) => (item.data_apontamento ? 'A' : 'P') === 'P').length;
    const concluidos = filteredData.filter((item) => (item.data_apontamento ? 'A' : 'P') !== 'P').length;
    const selecionados = filteredData.filter((item) => selectedIds.has(item.titulo_id)).length;
    const valorSelecionado = calculateSelectedTotal(filteredData, selectedIds);
    return { total, pendentes, concluidos, selecionados, valorSelecionado };
  }, [filteredData, selectedIds]);

  const handleToggleOne = useCallback((tituloId: number, checked: boolean) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (checked) next.add(tituloId);
      else next.delete(tituloId);
      return next;
    });
  }, []);

  const handleToggleAll = useCallback(
    (checked: boolean) => {
      setSelectedIds((prev) => {
        const next = new Set(prev);
        if (checked) filteredData.forEach((item) => next.add(item.titulo_id));
        else filteredData.forEach((item) => next.delete(item.titulo_id));
        return next;
      });
    },
    [filteredData],
  );

  const clearSelection = useCallback(() => {
    setSelectedIds(new Set());
  }, []);

  const getSelectedRows = useCallback((): PTituloBatchRowBase[] => {
    return filteredData.filter((item) => selectedIds.has(item.titulo_id));
  }, [filteredData, selectedIds]);

  const handleSearch = useCallback(() => {
    const normalizedSearch = searchQuery.trim();
    setDebouncedSearchQuery(normalizedSearch);
    setCurrentPage(1);
    void fetchTitulos(buildWorkflowQuery(normalizedSearch));
  }, [searchQuery, fetchTitulos, buildWorkflowQuery]);

  const handleClearFilters = useCallback(() => {
    setSearchQuery('');
    setDebouncedSearchQuery('');
    setStatusFilter('P');
    setDateRange(undefined);
    setCurrentPage(1);
    void fetchTitulos(
      buildPTituloWorkflowBatchQuery({
        workflow_etapa: 'apontamento',
        statusFilter: 'P',
      }),
    );
  }, [fetchTitulos]);

  const handleApontarSelecionados = () => {
    const selectedRows = getSelectedRows();
    if (selectedRows.length === 0) {
      toast.warning('Nenhum título selecionado', {
        description: 'Selecione ao menos um título para iniciar o apontamento em lote.',
      });
      return;
    }

    toast.info('Fluxo em construção', {
      description: `${selectedRows.length} título(s) pronto(s) para apontamento em lote.`,
    });
  };

  return (
    <div className="flex w-full flex-col gap-5">
      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight">Apontar Títulos em Lote</h1>
            <p className="text-sm text-muted-foreground">
              Selecione títulos pendentes e execute apontamentos em massa com mais agilidade.
            </p>
          </div>
          <Button
            type="button"
            className="bg-[#FF6B00] text-white transition-transform duration-200 hover:-translate-y-0.5 hover:bg-[#E56000]"
            onClick={handleApontarSelecionados}
          >
            <CheckCheck className="mr-1 h-4 w-4" />
            Apontar selecionados
          </Button>
        </div>

        <div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-5">
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">Total: <span className="font-semibold">{resumo.total}</span></div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">Pendentes: <span className="font-semibold text-amber-700">{resumo.pendentes}</span></div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">Já apontados: <span className="font-semibold text-emerald-700">{resumo.concluidos}</span></div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">Selecionados: <span className="font-semibold">{resumo.selecionados}</span></div>
          <div className="rounded-md border bg-muted/30 px-3 py-2 text-sm">
            Valor selecionado:{' '}
            <span className="font-semibold">{new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(resumo.valorSelecionado)}</span>
          </div>
        </div>
      </section>

      <PTituloApontamentoBatchFilter
        searchQuery={searchQuery}
        onSearchQueryChange={setSearchQuery}
        statusFilter={statusFilter}
        onStatusFilterChange={setStatusFilter}
        dateRange={dateRange}
        onDateRangeChange={setDateRange}
        onSearch={handleSearch}
        onClear={handleClearFilters}
      />

      {selectedIds.size > 0 ? (
        <div className="flex justify-start px-1 py-1">
          <span
            role="button"
            tabIndex={0}
            className="inline-flex cursor-pointer items-center gap-1.5 rounded-md px-2 py-1 text-xs font-medium text-[#FF6B00] transition-all duration-200 hover:-translate-y-0.5 hover:bg-[#FF6B00]/12 hover:text-[#E56000] hover:shadow-sm active:translate-y-0 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#FF6B00]/35"
            onClick={clearSelection}
            onKeyDown={(event) => {
              if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                clearSelection();
              }
            }}
          >
            Limpar seleção
          </span>
        </div>
      ) : null}

      <PTituloApontamentoBatchTable
        data={paginatedData}
        isLoading={isLoading}
        selectedIds={selectedIds}
        onToggleOne={handleToggleOne}
        onToggleAll={handleToggleAll}
      />

      <Pagination pagination={pagination} onPageChange={setCurrentPage} disabled={isLoading} />
    </div>
  );
}
