"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GFeriadoDialog } from "@/packages/administrativo/components/GFeriado/GFeriadoDialog";
import { GFeriadoFilter } from "@/packages/administrativo/components/GFeriado/GFeriadoFilter";
import { GFeriadoTable } from "@/packages/administrativo/components/GFeriado/GFeriadoTable";
import { useGFeriadoDeleteHook } from "@/packages/administrativo/hooks/GFeriado/useGFeriadoDeleteHook";
import { useGFeriadoReadHook } from "@/packages/administrativo/hooks/GFeriado/useGFeriadoReadHook";
import {
  type FeriadoSavePayload,
  useGFeriadoSaveHook,
} from "@/packages/administrativo/hooks/GFeriado/useGFeriadoSaveHook";
import type { GFeriadoInterface } from "@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function GFeriadoIndex() {
  const { feriados, isLoading, fetchFeriados } = useGFeriadoReadHook();
  const { saveFeriado } = useGFeriadoSaveHook();
  const { deleteFeriado } = useGFeriadoDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<GFeriadoInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const handleOpenDialog = useCallback((row?: GFeriadoInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: FeriadoSavePayload) => {
      setButtonIsLoading(true);
      try {
        await saveFeriado(formData, selected);
        await fetchFeriados();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar feriado:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveFeriado, selected, fetchFeriados, handleCloseDialog],
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
      await deleteFeriado(id);
      await fetchFeriados();
    } catch (e) {
      console.error("Erro ao excluir feriado:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteFeriado, fetchFeriados]);

  useEffect(() => {
    void fetchFeriados();
  }, [fetchFeriados]);

  const filtered = useMemo(() => {
    if (!searchQuery) return feriados;
    const q = searchQuery.toLowerCase();
    return feriados.filter((f) => f.descricao?.toLowerCase().includes(q) || f.ano?.toString().includes(q));
  }, [feriados, searchQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Feriados</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" />
            Novo Feriado
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <GFeriadoFilter value={searchQuery} onChange={setSearchQuery} />
        <GFeriadoTable data={filtered} isLoading={isLoading} onEdit={handleOpenDialog} onDelete={openDeleteDialog} />
      </div>

      <GFeriadoDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        feriado={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Feriado"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir este feriado?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
