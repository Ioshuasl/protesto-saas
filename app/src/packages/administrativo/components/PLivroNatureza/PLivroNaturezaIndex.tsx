"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PLivroNaturezaDialog } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaDialog";
import { PLivroNaturezaFilter } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaFilter";
import type { LivroNaturezaFormValues } from "@/packages/administrativo/schemas/PLivroNatureza/PLivroNaturezaFormSchema";
import { PLivroNaturezaTable } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaTable";
import { usePLivroNaturezaDeleteHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaDeleteHook";
import { usePLivroNaturezaReadHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaReadHook";
import { usePLivroNaturezaSaveHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaSaveHook";
import type { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function PLivroNaturezaIndex() {
  const { naturezas, isLoading, fetchNaturezas } = usePLivroNaturezaReadHook();
  const { saveLivroNatureza } = usePLivroNaturezaSaveHook();
  const { deleteLivroNatureza } = usePLivroNaturezaDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PLivroNaturezaInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

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
        await fetchNaturezas();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar natureza:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveLivroNatureza, selected, fetchNaturezas, handleCloseDialog],
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
      await fetchNaturezas();
    } catch (e) {
      console.error("Erro ao excluir:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteLivroNatureza, fetchNaturezas]);

  useEffect(() => {
    void fetchNaturezas();
  }, [fetchNaturezas]);

  const filtered = useMemo(() => {
    if (!searchQuery) return naturezas;
    const q = searchQuery.toLowerCase();
    return naturezas.filter(
      (n) => n.descricao?.toLowerCase().includes(q) || n.sigla?.toLowerCase().includes(q),
    );
  }, [naturezas, searchQuery]);

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
        <PLivroNaturezaFilter value={searchQuery} onChange={setSearchQuery} />
        <PLivroNaturezaTable
          data={filtered}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
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
