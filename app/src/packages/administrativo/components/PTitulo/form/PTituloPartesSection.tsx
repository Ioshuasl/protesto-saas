"use client";

import { useState } from "react";
import { useFieldArray, useFormContext } from "react-hook-form";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PPessoaVinculoTable } from "@/packages/administrativo/components/PPessoaVinculo/PPessoaVinculoTable";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import type { PessoaFormValues } from "@/packages/administrativo/components/PPessoa/PPessoaForm";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces";
import type { PPessoaVinculoTipo } from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum";
import { PessoaService } from "@/packages/administrativo/services/PPessoa/PPessoaService";
import type { PTituloDetailsFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { PTituloParteDialog } from "../PTituloParteDialog";
import { buildPTituloParteItem, type PTituloParteItem } from "../PTituloParteTypes";

export function PTituloPartesSection() {
  const { control, getValues } = useFormContext<PTituloDetailsFormValues>();
  const { fields, append, remove, update } = useFieldArray({ control, name: "partes" });

  const [isParteDialogOpen, setIsParteDialogOpen] = useState(false);
  const [isEditPPessoaDialogOpen, setIsEditPPessoaDialogOpen] = useState(false);
  const [selectedParteIndex, setSelectedParteIndex] = useState<number | null>(null);
  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [isSubmittingPessoa, setIsSubmittingPessoa] = useState(false);

  const handleAddPartesBatch = (novasPartes: PTituloParteItem[]) => {
    novasPartes.forEach((item) => append(buildPTituloParteItem(item)));
  };

  const handleUpdateTipoVinculo = (index: number, tipo: PPessoaVinculoTipo) => {
    const current = getValues(`partes.${index}`);
    update(index, buildPTituloParteItem({ ...current, tipo }));
  };

  const handleEditParte = async (index: number) => {
    const parte = getValues(`partes.${index}`);
    try {
      let pessoa: PPessoaInterface | undefined =
        parte.pessoa_id != null
          ? ((await PessoaService.getById(parte.pessoa_id)) as unknown as PPessoaInterface)
          : undefined;

      if (!pessoa && parte.cpfcnpj) {
        const pessoas = await PessoaService.getAll({
          page: 1,
          per_page: 500,
          sort: "pessoa_id.desc",
        });
        pessoa = pessoas.find((item) => item.cpfcnpj === parte.cpfcnpj);
      }

      setSelectedParteIndex(index);
      setSelectedPessoa(
        pessoa ?? {
          pessoa_id: parte.pessoa_id ?? 0,
          nome: parte.nome,
          cpfcnpj: parte.cpfcnpj,
        },
      );
      setIsEditPPessoaDialogOpen(true);
    } catch (error) {
      console.error("Erro ao carregar dados da parte:", error);
    }
  };

  const handleSubmitPessoa = async (data: PessoaFormValues) => {
    if (selectedParteIndex === null) return;

    setIsSubmittingPessoa(true);
    try {
      const payload = {
        ...data,
        data_nascimento: data.data_nascimento || undefined,
      };

      const savedPessoa = (selectedPessoa?.pessoa_id && selectedPessoa.pessoa_id > 0
        ? await PessoaService.update(selectedPessoa.pessoa_id, payload)
        : await PessoaService.create(payload)) as unknown as PPessoaInterface;

      const current = getValues(`partes.${selectedParteIndex}`);
      update(
        selectedParteIndex,
        buildPTituloParteItem({
          ...current,
          pessoa_id: savedPessoa.pessoa_id,
          nome: savedPessoa.nome,
          cpfcnpj: savedPessoa.cpfcnpj,
        }),
      );

      setIsEditPPessoaDialogOpen(false);
      setSelectedParteIndex(null);
      setSelectedPessoa(null);
    } catch (error) {
      console.error("Erro ao salvar pessoa da parte:", error);
    } finally {
      setIsSubmittingPessoa(false);
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-end">
        <Button type="button" variant="outline" onClick={() => setIsParteDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
          Adicionar Parte
        </Button>
      </div>

      <PPessoaVinculoTable
        rows={fields.map((field) => ({
          id: field.id,
          tipo: field.tipo,
          nome: field.nome,
          cpfcnpj: field.cpfcnpj,
        }))}
        onTipoChange={handleUpdateTipoVinculo}
        onEdit={(index) => void handleEditParte(index)}
        onRemove={remove}
        emptyMessage="Nenhuma parte vinculada encontrada."
      />

      <PTituloParteDialog
        open={isParteDialogOpen}
        onOpenChange={setIsParteDialogOpen}
        onAddBatch={handleAddPartesBatch}
      />

      <PPessoaDialog
        open={isEditPPessoaDialogOpen}
        onOpenChange={setIsEditPPessoaDialogOpen}
        pessoa={selectedPessoa}
        onSubmit={handleSubmitPessoa}
        isLoading={isSubmittingPessoa}
      />
    </div>
  );
}
