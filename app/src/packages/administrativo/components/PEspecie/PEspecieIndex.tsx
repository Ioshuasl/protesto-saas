"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PEspecieDialog } from "@/packages/administrativo/components/PEspecie/PEspecieDialog";
import { PEspecieFilter } from "@/packages/administrativo/components/PEspecie/PEspecieFilter";
import type { EspecieFormValues } from "@/packages/administrativo/schemas/PEspecie/PEspecieFormSchema";
import { PEspecieTable } from "@/packages/administrativo/components/PEspecie/PEspecieTable";
import { usePEspecieDeleteHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieDeleteHook";
import { usePEspecieReadHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieReadHook";
import { usePEspecieSaveHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieSaveHook";
import type { PEspecieInterface } from "@/packages/administrativo/interfaces/PEspecie/PEspecieInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function PEspecieIndex() {
  const { especies, isLoading, fetchEspecies } = usePEspecieReadHook();
  const { saveEspecie } = usePEspecieSaveHook();
  const { deleteEspecie } = usePEspecieDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PEspecieInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

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
        await fetchEspecies();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar espécie:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveEspecie, selected, fetchEspecies, handleCloseDialog],
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
      await fetchEspecies();
    } catch (e) {
      console.error("Erro ao excluir espécie:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteEspecie, fetchEspecies]);

  useEffect(() => {
    void fetchEspecies();
  }, [fetchEspecies]);

  const filtered = useMemo(() => {
    if (!searchQuery) return especies;
    const q = searchQuery.toLowerCase();
    return especies.filter(
      (e) => e.descricao?.toLowerCase().includes(q) || e.especie?.toLowerCase().includes(q),
    );
  }, [especies, searchQuery]);

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
        <PEspecieFilter value={searchQuery} onChange={setSearchQuery} />
        <PEspecieTable data={filtered} isLoading={isLoading} onEdit={handleOpenDialog} onDelete={openDeleteDialog} />
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
