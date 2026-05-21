"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PLivroNaturezaDialog } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaDialog";
import { PLivroNaturezaFilter } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaFilter";
import {
  buildPLivroNaturezaIndexQuery,
  defaultPLivroNaturezaFilterState,
  type PLivroNaturezaFilterState,
} from "@/packages/administrativo/components/PLivroNatureza/pLivroNaturezaFilterUtils";
import { PLivroNaturezaTable } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaTable";
import { usePLivroNaturezaDeleteHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaDeleteHook";
import { usePLivroNaturezaReadHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaReadHook";
import { usePLivroNaturezaSaveHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaSaveHook";
import type { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface";
import type { LivroNaturezaFormValues } from "@/packages/administrativo/schemas/PLivroNatureza/PLivroNaturezaFormSchema";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

const PLIVRO_NATUREZA_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

export default function PLivroNaturezaIndex() {
  const { naturezas, pagination, isLoading, fetchNaturezas } = usePLivroNaturezaReadHook();
  const { saveLivroNatureza } = usePLivroNaturezaSaveHook();
  const { deleteLivroNatureza } = usePLivroNaturezaDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [filters, setFilters] = useState<PLivroNaturezaFilterState>(defaultPLivroNaturezaFilterState);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PLivroNaturezaInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [debouncedFilters, setDebouncedFilters] = useState<PLivroNaturezaFilterState>(filters);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedFilters(filters), 400);
    return () => window.clearTimeout(timer);
  }, [filters]);

  useEffect(() => {
    setPage(1);
  }, [debouncedFilters.search]);

  const apiFilters = useMemo(
    () => buildPLivroNaturezaIndexQuery(debouncedFilters),
    [debouncedFilters],
  );

  const indexQuery = useMemo(
    () => ({
      ...apiFilters,
      page,
      per_page: PLIVRO_NATUREZA_PER_PAGE,
    }),
    [apiFilters, page],
  );

  const handleFiltersChange = useCallback((next: PLivroNaturezaFilterState) => {
    setFilters(next);
  }, []);

  const handleOpenDialog = useCallback((row?: PLivroNaturezaInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: LivroNaturezaFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveLivroNatureza(formData, selected);
        await fetchNaturezas(indexQuery);
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar natureza:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveLivroNatureza, selected, fetchNaturezas, handleCloseDialog, indexQuery],
  );

  const openDeleteDialog = useCallback((id: number) => {
    setPendingDeleteId(id);
    setDeleteDialogOpen(true);
  }, []);

  const closeDeleteDialog = useCallback(() => {
    setDeleteDialogOpen(false);
    setPendingDeleteId(null);
  }, []);

  const confirmDelete = useCallback(async () => {
    const id = pendingDeleteId;
    if (id == null) return;
    closeDeleteDialog();
    try {
      await deleteLivroNatureza(id);
      await fetchNaturezas(indexQuery);
    } catch (e) {
      console.error("Erro ao excluir:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteLivroNatureza, fetchNaturezas, indexQuery]);

  useEffect(() => {
    void fetchNaturezas(indexQuery);
  }, [fetchNaturezas, indexQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Livro Natureza</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Nova Natureza
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PLivroNaturezaFilter value={filters} onChange={handleFiltersChange} />
        <PLivroNaturezaTable
          data={naturezas}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
        <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
      </div>

      <PLivroNaturezaDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        livroNatureza={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Natureza de livro"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir esta natureza de livro?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
