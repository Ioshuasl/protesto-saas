"use client";

import { useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";
import { GEmolumentoDetailDialog } from "@/packages/administrativo/components/GEmolumento/GEmolumentoDetailDialog";
import {
  buildGEmolumentoListFilter,
  GEmolumentoFilter,
  type GEmolumentoFilterValues,
} from "@/packages/administrativo/components/GEmolumento/GEmolumentoFilter";
import { GEmolumentoTable } from "@/packages/administrativo/components/GEmolumento/GEmolumentoTable";
import { useGEmolumentoListHooks } from "@/packages/administrativo/hooks/GEmolumentoList/useGEmolumentoListHooks";
import { useGEmolumentoPeriodoIndexHook } from "@/packages/administrativo/hooks/GEmolumentoPeriodo/useGEmolumentoPeriodoIndexHook";
import type { GEmolumentoListInterface } from "@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface";
import type { GEmolumentoPeriodoInterface } from "@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";

const INITIAL_FILTERS: GEmolumentoFilterValues = {
  emolumento_periodo_id: "",
  busca: "",
  sistema_id: null,
};
const GEMOLUMENTO_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

function getLatestPeriodoId(periodos: GEmolumentoPeriodoInterface[]): number | null {
  const ids = periodos
    .map((periodo) => Number(periodo.emolumento_periodo_id))
    .filter((id) => Number.isFinite(id));
  if (ids.length === 0) return null;
  return Math.max(...ids);
}

export default function GEmolumentoIndex() {
  const { list } = useGEmolumentoListHooks();
  const { itens, pagination, isLoading, fetchItens } = list;
  const { fetchPeriodos } = useGEmolumentoPeriodoIndexHook();

  const [filters, setFilters] = useState<GEmolumentoFilterValues>(INITIAL_FILTERS);
  const [page, setPage] = useState(1);
  const [selectedItem, setSelectedItem] = useState<GEmolumentoListInterface | null>(null);
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false);

  const handleSearch = useCallback(async () => {
    setPage(1);
    await fetchItens({
      ...buildGEmolumentoListFilter(filters),
      page: 1,
      per_page: GEMOLUMENTO_PER_PAGE,
    });
  }, [fetchItens, filters]);

  const handleClear = useCallback(async () => {
    const periodos = await fetchPeriodos();
    if (Array.isArray(periodos)) {
      const latestPeriodoId = getLatestPeriodoId(periodos);
      if (latestPeriodoId != null) {
        const nextFilters = {
          ...INITIAL_FILTERS,
          emolumento_periodo_id: String(latestPeriodoId),
        };
        setFilters(nextFilters);
        setPage(1);
        await fetchItens({
          ...buildGEmolumentoListFilter(nextFilters),
          page: 1,
          per_page: GEMOLUMENTO_PER_PAGE,
        });
        return;
      }
    }

    setFilters(INITIAL_FILTERS);
    setPage(1);
    await fetchItens({
      ...buildGEmolumentoListFilter(INITIAL_FILTERS),
      page: 1,
      per_page: GEMOLUMENTO_PER_PAGE,
    });
  }, [fetchItens, fetchPeriodos]);

  const handleRefresh = useCallback(async () => {
    await fetchItens({
      ...buildGEmolumentoListFilter(filters),
      page,
      per_page: GEMOLUMENTO_PER_PAGE,
    });
  }, [fetchItens, filters, page]);

  const handlePageChange = useCallback(
    async (nextPage: number) => {
      setPage(nextPage);
      await fetchItens({
        ...buildGEmolumentoListFilter(filters),
        page: nextPage,
        per_page: GEMOLUMENTO_PER_PAGE,
      });
    },
    [fetchItens, filters],
  );

  const handleOpenDetails = useCallback((item: GEmolumentoListInterface) => {
    setSelectedItem(item);
    setIsDetailDialogOpen(true);
  }, []);

  useEffect(() => {
    const initialize = async () => {
      const periodos = await fetchPeriodos();
      if (Array.isArray(periodos)) {
        const latestPeriodoId = getLatestPeriodoId(periodos);
        if (latestPeriodoId != null) {
          const nextFilters = {
            ...INITIAL_FILTERS,
            emolumento_periodo_id: String(latestPeriodoId),
          };
          setFilters(nextFilters);
          setPage(1);
          await fetchItens({
            ...buildGEmolumentoListFilter(nextFilters),
            page: 1,
            per_page: GEMOLUMENTO_PER_PAGE,
          });
          return;
        }
      }

      setPage(1);
      await fetchItens({
        ...buildGEmolumentoListFilter(INITIAL_FILTERS),
        page: 1,
        per_page: GEMOLUMENTO_PER_PAGE,
      });
    };

    void initialize();
  }, [fetchItens, fetchPeriodos]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Emolumentos</h1>
        <Button onClick={() => void handleRefresh()} variant="outline" disabled={isLoading}>
          <RefreshCw className="mr-2 h-4 w-4" />
          Atualizar
        </Button>
      </div>

      <GEmolumentoFilter
        value={filters}
        isLoading={isLoading}
        onChange={setFilters}
        onSubmit={() => void handleSearch()}
        onClear={() => void handleClear()}
      />

      <GEmolumentoTable data={itens} isLoading={isLoading} onViewDetails={handleOpenDetails} />
      <Pagination pagination={pagination} onPageChange={(nextPage) => void handlePageChange(nextPage)} disabled={isLoading} />

      <GEmolumentoDetailDialog
        open={isDetailDialogOpen}
        onOpenChange={setIsDetailDialogOpen}
        item={selectedItem}
      />
    </div>
  );
}
