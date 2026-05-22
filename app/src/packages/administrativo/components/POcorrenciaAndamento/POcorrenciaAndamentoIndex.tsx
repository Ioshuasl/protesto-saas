"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { POcorrenciaAndamentoDialog } from "@/packages/administrativo/components/POcorrenciaAndamento/POcorrenciaAndamentoDialog";
import { POcorrenciaAndamentoFilter } from "@/packages/administrativo/components/POcorrenciaAndamento/POcorrenciaAndamentoFilter";
import {
  buildPOcorrenciaAndamentoIndexQuery,
  defaultPOcorrenciaAndamentoFilterState,
  type POcorrenciaAndamentoFilterState,
} from "@/packages/administrativo/components/POcorrenciaAndamento/pocorrenciaAndamentoFilterUtils";
import { POcorrenciaAndamentoTable } from "@/packages/administrativo/components/POcorrenciaAndamento/POcorrenciaAndamentoTable";
import { usePOcorrenciaAndamentoDeleteHook } from "@/packages/administrativo/hooks/POcorrenciaAndamento/usePOcorrenciaAndamentoDeleteHook";
import { usePOcorrenciaAndamentoReadHook } from "@/packages/administrativo/hooks/POcorrenciaAndamento/usePOcorrenciaAndamentoReadHook";
import { usePOcorrenciaAndamentoSaveHook } from "@/packages/administrativo/hooks/POcorrenciaAndamento/usePOcorrenciaAndamentoSaveHook";
import type { POcorrenciaAndamentoInterface } from "@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface";
import type { OcorrenciaAndamentoFormValues } from "@/packages/administrativo/schemas/POcorrenciaAndamento/POcorrenciaAndamentoFormSchema";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

const POCORRENCIA_ANDAMENTO_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

export default function POcorrenciaAndamentoIndex() {
  const { ocorrenciasAndamento, pagination, isLoading, fetchOcorrenciasAndamento } =
    usePOcorrenciaAndamentoReadHook();
  const { saveOcorrenciaAndamento } = usePOcorrenciaAndamentoSaveHook();
  const { deleteOcorrenciaAndamento } = usePOcorrenciaAndamentoDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [filters, setFilters] = useState<POcorrenciaAndamentoFilterState>(
    defaultPOcorrenciaAndamentoFilterState,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<POcorrenciaAndamentoInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [debouncedFilters, setDebouncedFilters] = useState<POcorrenciaAndamentoFilterState>(
    filters,
  );

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedFilters(filters), 400);
    return () => window.clearTimeout(timer);
  }, [filters]);

  useEffect(() => {
    setPage(1);
  }, [debouncedFilters.search]);

  const apiFilters = useMemo(
    () => buildPOcorrenciaAndamentoIndexQuery(debouncedFilters),
    [debouncedFilters],
  );

  const indexQuery = useMemo(
    () => ({
      ...apiFilters,
      page,
      per_page: POCORRENCIA_ANDAMENTO_PER_PAGE,
    }),
    [apiFilters, page],
  );

  const handleFiltersChange = useCallback((next: POcorrenciaAndamentoFilterState) => {
    setFilters(next);
  }, []);

  const handleOpenDialog = useCallback((row?: POcorrenciaAndamentoInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: OcorrenciaAndamentoFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveOcorrenciaAndamento(formData, selected);
        await fetchOcorrenciasAndamento(indexQuery);
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar ocorrência de andamento:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveOcorrenciaAndamento, selected, fetchOcorrenciasAndamento, handleCloseDialog, indexQuery],
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
      await deleteOcorrenciaAndamento(id);
      await fetchOcorrenciasAndamento(indexQuery);
    } catch (e) {
      console.error("Erro ao excluir ocorrência de andamento:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteOcorrenciaAndamento, fetchOcorrenciasAndamento, indexQuery]);

  useEffect(() => {
    void fetchOcorrenciasAndamento(indexQuery);
  }, [fetchOcorrenciasAndamento, indexQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Ocorrências de andamento</h1>
          <Button
            onClick={() => handleOpenDialog()}
            className="bg-[#FF6B00] hover:bg-[#E56000] text-white"
          >
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Nova ocorrência
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <POcorrenciaAndamentoFilter value={filters} onChange={handleFiltersChange} />
        <POcorrenciaAndamentoTable
          data={ocorrenciasAndamento}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
        <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
      </div>

      <POcorrenciaAndamentoDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        ocorrenciaAndamento={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Ocorrência de andamento"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir esta ocorrência de andamento?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
