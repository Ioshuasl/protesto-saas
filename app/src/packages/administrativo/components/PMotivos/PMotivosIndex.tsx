"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PMotivosDialog } from "@/packages/administrativo/components/PMotivos/PMotivosDialog";
import { PMotivosFilter } from "@/packages/administrativo/components/PMotivos/PMotivosFilter";
import type { MotivoFormValues } from "@/packages/administrativo/schemas/PMotivos/PMotivosFormSchema";
import { PMotivosTable } from "@/packages/administrativo/components/PMotivos/PMotivosTable";
import { usePMotivosDeleteHook } from "@/packages/administrativo/hooks/PMotivos/usePMotivosDeleteHook";
import { usePMotivosReadHook } from "@/packages/administrativo/hooks/PMotivos/usePMotivosReadHook";
import { usePMotivosSaveHook } from "@/packages/administrativo/hooks/PMotivos/usePMotivosSaveHook";
import type { PMotivosInterface } from "@/packages/administrativo/interfaces/PMotivos/PMotivosInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function PMotivosIndex() {
  const { motivos, isLoading, fetchMotivos } = usePMotivosReadHook();
  const { saveMotivo } = usePMotivosSaveHook();
  const { deleteMotivo } = usePMotivosDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedMotivo, setSelectedMotivo] = useState<PMotivosInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const handleOpenDialog = useCallback((motivo?: PMotivosInterface) => {
    setSelectedMotivo(motivo ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelectedMotivo(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: MotivoFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveMotivo(formData, selectedMotivo);
        await fetchMotivos();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar motivo:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveMotivo, selectedMotivo, fetchMotivos, handleCloseDialog],
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
      await deleteMotivo(id);
      await fetchMotivos();
    } catch (e) {
      console.error("Erro ao excluir motivo:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteMotivo, fetchMotivos]);

  useEffect(() => {
    void fetchMotivos();
  }, [fetchMotivos]);

  const filteredMotivos = useMemo(() => {
    if (!searchQuery) return motivos;
    const query = searchQuery.toLowerCase();
    return motivos.filter(
      (m) => m.codigo?.toLowerCase().includes(query) || m.descricao?.toLowerCase().includes(query),
    );
  }, [motivos, searchQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Motivos de Apontamento</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Novo Motivo
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <PMotivosFilter value={searchQuery} onChange={setSearchQuery} />
        </div>

        <PMotivosTable
          data={filteredMotivos}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
      </div>

      <PMotivosDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        motivo={selectedMotivo}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Motivo de apontamento"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir este motivo de apontamento?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
