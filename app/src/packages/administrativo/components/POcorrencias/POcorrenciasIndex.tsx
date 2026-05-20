"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { POcorrenciasDialog } from "@/packages/administrativo/components/POcorrencias/POcorrenciasDialog";
import { POcorrenciasFilter } from "@/packages/administrativo/components/POcorrencias/POcorrenciasFilter";
import type { OcorrenciaFormValues } from "@/packages/administrativo/schemas/POcorrencias/POcorrenciasFormSchema";
import { POcorrenciasTable } from "@/packages/administrativo/components/POcorrencias/POcorrenciasTable";
import { usePOcorrenciasDeleteHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasDeleteHook";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import { usePOcorrenciasSaveHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasSaveHook";
import type { POcorrenciasInterface } from "@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function POcorrenciasIndex() {
  const { ocorrencias, isLoading, fetchOcorrencias } = usePOcorrenciasReadHook();
  const { saveOcorrencia } = usePOcorrenciasSaveHook();
  const { deleteOcorrencia } = usePOcorrenciasDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<POcorrenciasInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const handleOpenDialog = useCallback((row?: POcorrenciasInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: OcorrenciaFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveOcorrencia(formData, selected);
        await fetchOcorrencias();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar ocorrência:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveOcorrencia, selected, fetchOcorrencias, handleCloseDialog],
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
      await deleteOcorrencia(id);
      await fetchOcorrencias();
    } catch (e) {
      console.error("Erro ao excluir ocorrência:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteOcorrencia, fetchOcorrencias]);

  useEffect(() => {
    void fetchOcorrencias();
  }, [fetchOcorrencias]);

  const filtered = useMemo(() => {
    if (!searchQuery) return ocorrencias;
    const q = searchQuery.toLowerCase();
    return ocorrencias.filter(
      (o) =>
        o.descricao?.toLowerCase().includes(q) ||
        o.codigo?.toLowerCase().includes(q) ||
        o.tipo?.toLowerCase().includes(q),
    );
  }, [ocorrencias, searchQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Ocorrências</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Nova Ocorrência
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <POcorrenciasFilter value={searchQuery} onChange={setSearchQuery} />
        <POcorrenciasTable data={filtered} isLoading={isLoading} onEdit={handleOpenDialog} onDelete={openDeleteDialog} />
      </div>

      <POcorrenciasDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        ocorrencia={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Ocorrência"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir esta ocorrência?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
