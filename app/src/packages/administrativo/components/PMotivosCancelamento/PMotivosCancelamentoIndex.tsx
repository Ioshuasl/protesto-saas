"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PMotivosCancelamentoDialog } from "@/packages/administrativo/components/PMotivosCancelamento/PMotivosCancelamentoDialog";
import { PMotivosCancelamentoFilter } from "@/packages/administrativo/components/PMotivosCancelamento/PMotivosCancelamentoFilter";
import {
  buildPMotivosCancelamentoIndexQuery,
  defaultPMotivosCancelamentoFilterState,
  type PMotivosCancelamentoFilterState,
} from "@/packages/administrativo/components/PMotivosCancelamento/pmotivosCancelamentoFilterUtils";
import type { MotivoCancelamentoFormValues } from "@/packages/administrativo/schemas/PMotivosCancelamento/PMotivosCancelamentoFormSchema";
import { PMotivosCancelamentoTable } from "@/packages/administrativo/components/PMotivosCancelamento/PMotivosCancelamentoTable";
import { usePMotivosCancelamentoDeleteHook } from "@/packages/administrativo/hooks/PMotivosCancelamento/usePMotivosCancelamentoDeleteHook";
import { usePMotivosCancelamentoReadHook } from "@/packages/administrativo/hooks/PMotivosCancelamento/usePMotivosCancelamentoReadHook";
import { usePMotivosCancelamentoSaveHook } from "@/packages/administrativo/hooks/PMotivosCancelamento/usePMotivosCancelamentoSaveHook";
import type { PMotivosCancelamentoInterface } from "@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function PMotivosCancelamentoIndex() {
  const { motivosCancelamento, isLoading, fetchMotivosCancelamento } = usePMotivosCancelamentoReadHook();
  const { saveMotivoCancelamento } = usePMotivosCancelamentoSaveHook();
  const { deleteMotivoCancelamento } = usePMotivosCancelamentoDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [filters, setFilters] = useState<PMotivosCancelamentoFilterState>(
    defaultPMotivosCancelamentoFilterState,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PMotivosCancelamentoInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const apiFilters = useMemo(() => buildPMotivosCancelamentoIndexQuery(filters), [filters]);

  const handleFiltersChange = useCallback((next: PMotivosCancelamentoFilterState) => {
    setFilters(next);
  }, []);

  const handleOpenDialog = useCallback((row?: PMotivosCancelamentoInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: MotivoCancelamentoFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveMotivoCancelamento(formData, selected);
        await fetchMotivosCancelamento(apiFilters);
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar motivo de cancelamento:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveMotivoCancelamento, selected, fetchMotivosCancelamento, handleCloseDialog, apiFilters],
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
      await deleteMotivoCancelamento(id);
      await fetchMotivosCancelamento(apiFilters);
    } catch (e) {
      console.error("Erro ao excluir:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteMotivoCancelamento, fetchMotivosCancelamento, apiFilters]);

  useEffect(() => {
    void fetchMotivosCancelamento(apiFilters);
  }, [fetchMotivosCancelamento, apiFilters]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Motivos de Cancelamento</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Novo Motivo
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PMotivosCancelamentoFilter value={filters} onChange={handleFiltersChange} />
        <PMotivosCancelamentoTable
          data={motivosCancelamento}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
      </div>

      <PMotivosCancelamentoDialog
        open={isDialogOpen}
        onOpenChange={(open) => {
          setIsDialogOpen(open);
          if (!open) handleCloseDialog();
        }}
        motivoCancelamento={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Motivo de cancelamento"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir este motivo de cancelamento?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
