"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PEspecieDialog } from "@/packages/administrativo/components/PEspecie/PEspecieDialog";
import { PEspecieFilter } from "@/packages/administrativo/components/PEspecie/PEspecieFilter";
import {
  buildPEspecieIndexQuery,
  defaultPEspecieFilterState,
  type PEspecieFilterState,
} from "@/packages/administrativo/components/PEspecie/pEspecieFilterUtils";
import { PEspecieTable } from "@/packages/administrativo/components/PEspecie/PEspecieTable";
import { usePEspecieDeleteHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieDeleteHook";
import { usePEspecieReadHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieReadHook";
import { usePEspecieSaveHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieSaveHook";
import type { PEspecieInterface } from "@/packages/administrativo/interfaces/PEspecie/PEspecieInterface";
import type { EspecieFormValues } from "@/packages/administrativo/schemas/PEspecie/PEspecieFormSchema";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

const PESPECIE_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

export default function PEspecieIndex() {
  const { especies, pagination, isLoading, fetchEspecies } = usePEspecieReadHook();
  const { saveEspecie } = usePEspecieSaveHook();
  const { deleteEspecie } = usePEspecieDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [filters, setFilters] = useState<PEspecieFilterState>(defaultPEspecieFilterState);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PEspecieInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [debouncedFilters, setDebouncedFilters] = useState<PEspecieFilterState>(filters);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedFilters(filters), 400);
    return () => window.clearTimeout(timer);
  }, [filters]);

  useEffect(() => {
    setPage(1);
  }, [debouncedFilters.search]);

  const apiFilters = useMemo(() => buildPEspecieIndexQuery(debouncedFilters), [debouncedFilters]);

  const indexQuery = useMemo(
    () => ({
      ...apiFilters,
      page,
      per_page: PESPECIE_PER_PAGE,
    }),
    [apiFilters, page],
  );

  const handleFiltersChange = useCallback((next: PEspecieFilterState) => {
    setFilters(next);
  }, []);

  const handleOpenDialog = useCallback((row?: PEspecieInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: EspecieFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveEspecie(formData, selected);
        await fetchEspecies(indexQuery);
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar espécie:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveEspecie, selected, fetchEspecies, handleCloseDialog, indexQuery],
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
      await deleteEspecie(id);
      await fetchEspecies(indexQuery);
    } catch (e) {
      console.error("Erro ao excluir espécie:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteEspecie, fetchEspecies, indexQuery]);

  useEffect(() => {
    void fetchEspecies(indexQuery);
  }, [fetchEspecies, indexQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Espécies</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Nova Espécie
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PEspecieFilter value={filters} onChange={handleFiltersChange} />
        <PEspecieTable data={especies} isLoading={isLoading} onEdit={handleOpenDialog} onDelete={openDeleteDialog} />
        <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
      </div>

      <PEspecieDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        especie={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Espécie"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir esta espécie?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
