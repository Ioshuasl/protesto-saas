"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import { PPessoaFilter } from "@/packages/administrativo/components/PPessoa/PPessoaFilter";
import type { PessoaFormValues } from "@/packages/administrativo/schemas/PPessoa/PPessoaFormSchema";
import { PPessoaTable } from "@/packages/administrativo/components/PPessoa/PPessoaTable";
import { usePPessoaDeleteHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaDeleteHook";
import { usePPessoaReadHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaReadHook";
import { usePPessoaSaveHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaSaveHook";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

/** Tela de cadastro no estilo `TCensecIndex`: Read + Save + Delete hooks. */
export default function PPessoaIndex() {
  const { pessoas, isLoading, fetchPessoas } = usePPessoaReadHook();
  const { savePessoa } = usePPessoaSaveHook();
  const { deletePessoa } = usePPessoaDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const handleOpenDialog = useCallback((pessoa?: PPessoaInterface) => {
    setSelectedPessoa(pessoa ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelectedPessoa(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: PessoaFormValues) => {
      setButtonIsLoading(true);
      try {
        await savePessoa(formData, selectedPessoa);
        await fetchPessoas();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar pessoa:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [savePessoa, selectedPessoa, fetchPessoas, handleCloseDialog],
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
      await deletePessoa(id);
      await fetchPessoas();
    } catch (e) {
      console.error("Erro ao excluir pessoa:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deletePessoa, fetchPessoas]);

  useEffect(() => {
    void fetchPessoas();
  }, [fetchPessoas]);

  const filteredPessoas = useMemo(() => {
    if (!searchQuery) return pessoas;
    const query = searchQuery.toLowerCase();
    return pessoas.filter(
      (p) =>
        p.nome?.toLowerCase().includes(query) ||
        p.cpfcnpj?.replace(/\D/g, "").includes(query.replace(/\D/g, "")),
    );
  }, [pessoas, searchQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Pessoas</h1>
          <Button
            onClick={() => handleOpenDialog()}
            className="bg-[#FF6B00] hover:bg-[#E56000] text-white"
          >
            <Plus className="mr-2 h-4 w-4" />
            Nova Pessoa
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <PPessoaFilter value={searchQuery} onChange={setSearchQuery} />
        </div>

        <PPessoaTable
          data={filteredPessoas}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
      </div>

      <PPessoaDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        pessoa={selectedPessoa}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Pessoa"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir esta pessoa?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
