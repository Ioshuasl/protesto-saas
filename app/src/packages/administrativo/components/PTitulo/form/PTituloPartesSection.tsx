"use client";

import { useState } from "react";
import { useFieldArray, useFormContext } from "react-hook-form";
import { Pencil, Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import type { PessoaFormValues } from "@/packages/administrativo/components/PPessoa/PPessoaForm";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces";
import { PessoaService } from "@/packages/administrativo/services/PPessoa/PPessoaService";
import type { PTituloDetailsFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { PTituloParteDialog } from "../PTituloParteDialog";
import { pTituloParteRoleLabelMap, pTituloParteRoleOptions, type PTituloParteItem } from "../PTituloParteTypes";

export function PTituloPartesSection() {
  const { control, getValues } = useFormContext<PTituloDetailsFormValues>();
  const { fields, append, remove, update } = useFieldArray({ control, name: "partes" });

  const [isParteDialogOpen, setIsParteDialogOpen] = useState(false);
  const [isEditPPessoaDialogOpen, setIsEditPPessoaDialogOpen] = useState(false);
  const [selectedParteIndex, setSelectedParteIndex] = useState<number | null>(null);
  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [isSubmittingPessoa, setIsSubmittingPessoa] = useState(false);

  const handleAddPartesBatch = (novasPartes: PTituloParteItem[]) => {
    novasPartes.forEach((item) => append(item));
  };

  const handleUpdateTipoVinculo = (index: number, tipo: string) => {
    const current = getValues(`partes.${index}`);
    update(index, {
      ...current,
      tipo,
      descricao: pTituloParteRoleLabelMap.get(tipo) ?? "Outros",
    });
  };

  const handleEditParte = async (index: number) => {
    const parte = getValues(`partes.${index}`);
    try {
      let pessoa: PPessoaInterface | undefined =
        parte.pessoa_id != null
          ? ((await PessoaService.getById(parte.pessoa_id)) as unknown as PPessoaInterface)
          : undefined;

      if (!pessoa && parte.cpfcnpj) {
        const pessoas = (await PessoaService.getAll()) as unknown as PPessoaInterface[];
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
      update(selectedParteIndex, {
        ...current,
        pessoa_id: savedPessoa.pessoa_id,
        nome: savedPessoa.nome,
        cpfcnpj: savedPessoa.cpfcnpj,
      });

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

      {fields.length > 0 ? (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tipo de vínculo</TableHead>
                <TableHead>Nome</TableHead>
                <TableHead>CPF/CNPJ</TableHead>
                <TableHead className="w-[100px] text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {fields.map((field, index) => (
                <TableRow key={field.id}>
                  <TableCell className="min-w-[220px]">
                    <Select
                      value={field.tipo || "D"}
                      onValueChange={(value) => handleUpdateTipoVinculo(index, value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Tipo de vínculo">
                          {pTituloParteRoleLabelMap.get(field.tipo || "D")}
                        </SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        {pTituloParteRoleOptions.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </TableCell>
                  <TableCell>{field.nome ?? "-"}</TableCell>
                  <TableCell>{field.cpfcnpj ?? "-"}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-foreground hover:text-[#FF6B00]"
                        onClick={() => void handleEditParte(index)}
                        aria-label="Editar parte"
                      >
                        <Pencil className="h-4 w-4" strokeWidth={1.5} />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 text-foreground hover:text-[#FF6B00]"
                        onClick={() => remove(index)}
                        aria-label="Excluir parte"
                      >
                        <Trash2 className="h-4 w-4" strokeWidth={1.5} />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      ) : (
        <div className="rounded-md border p-3 text-sm text-muted-foreground">Nenhuma parte vinculada encontrada.</div>
      )}

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
