"use client";

import { useCallback, useEffect, useState } from "react";
import { Plus, RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { GEmolumentoPeriodoDialog } from "@/packages/administrativo/components/GEmolumentoPeriodo/GEmolumentoPeriodoDialog";
import { GEmolumentoPeriodoTable } from "@/packages/administrativo/components/GEmolumentoPeriodo/GEmolumentoPeriodoTable";
import { useGEmolumentoPeriodoDeleteHook } from "@/packages/administrativo/hooks/GEmolumentoPeriodo/useGEmolumentoPeriodoDeleteHook";
import { useGEmolumentoPeriodoIndexHook } from "@/packages/administrativo/hooks/GEmolumentoPeriodo/useGEmolumentoPeriodoIndexHook";
import { useGEmolumentoPeriodoSaveHook } from "@/packages/administrativo/hooks/GEmolumentoPeriodo/useGEmolumentoPeriodoSaveHook";
import type { GEmolumentoPeriodoInterface } from "@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface";
import type { GEmolumentoPeriodoFormValues } from "@/packages/administrativo/components/GEmolumentoPeriodo/GEmolumentoPeriodoForm";

export default function GEmolumentoPeriodoIndex() {
  const { periodos, isLoading, fetchPeriodos } = useGEmolumentoPeriodoIndexHook();
  const { savePeriodo } = useGEmolumentoPeriodoSaveHook();
  const { deletePeriodo } = useGEmolumentoPeriodoDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<GEmolumentoPeriodoInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const handleRefresh = useCallback(async () => {
    await fetchPeriodos();
  }, [fetchPeriodos]);

  const handleOpenDialog = useCallback((row?: GEmolumentoPeriodoInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: GEmolumentoPeriodoFormValues) => {
      setButtonIsLoading(true);
      try {
        await savePeriodo(formData, selected);
        await fetchPeriodos();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar periodo de emolumento:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [savePeriodo, selected, fetchPeriodos, handleCloseDialog],
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
      await deletePeriodo(id);
      await fetchPeriodos();
    } catch (e) {
      console.error("Erro ao excluir periodo de emolumento:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deletePeriodo, fetchPeriodos]);

  useEffect(() => {
    void fetchPeriodos();
  }, [fetchPeriodos]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Periodos de Emolumento</h1>
          <div className="flex items-center gap-2">
            <Button onClick={() => void handleRefresh()} variant="outline" disabled={isLoading}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Atualizar
            </Button>
            <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
              <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
              Novo Emolumento
            </Button>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <GEmolumentoPeriodoTable
          data={periodos}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
      </div>

      <GEmolumentoPeriodoDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        periodo={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Periodo de Emolumento"
        description="Confirmar exclusao"
        message="Tem certeza que deseja excluir este periodo de emolumento?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
