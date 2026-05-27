"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  buildPTituloIndexQuery,
  defaultPTituloFilterState,
  type PTituloFilterState,
} from "@/packages/administrativo/components/PTitulo/pTituloFilterUtils";
import { usePTituloReadHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloReadHook";
import { usePTituloSaveHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloSaveHook";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import { PTituloFilter } from "./PTituloFilter";
import { PTituloTable } from "./PTituloTable";

export interface PTituloWorkflowState {
  hasApontamentoBase: boolean;
  hasIntimacao: boolean;
  hasProtestoCompleto: boolean;
}

const PTITULO_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

function getPTituloWorkflowState(titulo: TituloListItem): PTituloWorkflowState {
  const hasValue = (value: unknown) => value !== null && value !== undefined && value !== "";
  const hasApontamentoBase = hasValue(titulo.numero_apontamento) && hasValue(titulo.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo.data_intimacao);
  const hasProtestoCompleto =
    hasIntimacao &&
    hasValue(titulo.data_protesto) &&
    hasValue(titulo.livro_id_protesto) &&
    hasValue(titulo.folha_protesto);

  return { hasApontamentoBase, hasIntimacao, hasProtestoCompleto };
}

export default function PTituloIndex() {
  const router = useRouter();
  const { titulos, pagination, isLoading, fetchTitulos } = usePTituloReadHook();
  const { saveTituloStatus } = usePTituloSaveHook();

  const [filters, setFilters] = useState<PTituloFilterState>(defaultPTituloFilterState);
  const [debouncedFilters, setDebouncedFilters] = useState<PTituloFilterState>(filters);
  const [page, setPage] = useState(1);

  const updateFilter = useCallback(<K extends keyof PTituloFilterState>(key: K, value: PTituloFilterState[K]) => {
    setFilters((prev) => {
      if (prev[key] === value) return prev;
      return { ...prev, [key]: value };
    });
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedFilters(filters), 400);
    return () => window.clearTimeout(timer);
  }, [filters]);

  useEffect(() => {
    setPage(1);
  }, [
    debouncedFilters.search,
    debouncedFilters.startDate,
    debouncedFilters.endDate,
    debouncedFilters.bancoId,
    debouncedFilters.especieId,
    debouncedFilters.ocorrenciaId,
  ]);

  const indexQuery = useMemo(
    () => ({
      ...buildPTituloIndexQuery(debouncedFilters),
      page,
      per_page: PTITULO_PER_PAGE,
    }),
    [debouncedFilters, page],
  );

  useEffect(() => {
    void fetchTitulos(indexQuery);
  }, [fetchTitulos, indexQuery]);

  const filteredTitulos = useMemo(() => {
    return titulos;
  }, [titulos]);

  const tableData = useMemo(
    () => filteredTitulos.map((titulo) => ({ ...titulo, ...getPTituloWorkflowState(titulo) })),
    [filteredTitulos],
  );

  const handleViewDetails = (titulo: TituloListItem) => {
    router.push(`/titulos/${titulo.titulo_id}`);
  };

  const handleUpdateStatus = async (tituloId: number, status: "Em Tríduo" | "Pago" | "Protestado") => {
    try {
      await saveTituloStatus(tituloId, status);
      await fetchTitulos(indexQuery);
    } catch (error) {
      console.error("Erro ao atualizar status do título:", error);
    }
  };

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Gestão de Títulos</h1>
          <Button className="bg-[#FF6B00] hover:bg-[#E56000] text-white" onClick={() => router.push("/titulo/new")}>
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Novo Título
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PTituloFilter
          searchQuery={filters.search}
          startDate={filters.startDate}
          endDate={filters.endDate}
          bancoId={filters.bancoId}
          especieId={filters.especieId}
          ocorrenciaId={filters.ocorrenciaId}
          onSearchChange={(search) => updateFilter("search", search)}
          onStartDateChange={(startDate) => updateFilter("startDate", startDate)}
          onEndDateChange={(endDate) => updateFilter("endDate", endDate)}
          onBancoChange={(bancoId) => updateFilter("bancoId", bancoId)}
          onEspecieChange={(especieId) => updateFilter("especieId", especieId)}
          onOcorrenciaChange={(ocorrenciaId) => updateFilter("ocorrenciaId", ocorrenciaId)}
        />

        <PTituloTable
          data={tableData}
          isLoading={isLoading}
          searchQuery={debouncedFilters.search}
          onViewDetails={handleViewDetails}
          onUpdateStatus={handleUpdateStatus}
        />

        <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
      </div>
    </div>
  );
}
