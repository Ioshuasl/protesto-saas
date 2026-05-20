"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import type { PessoaFormValues } from "@/packages/administrativo/components/PPessoa/PPessoaForm";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces";
import { PessoaService } from "@/packages/administrativo/services/PPessoa/PPessoaService";
import { pTituloParteRoleOptions, PTituloParteItem } from "./PTituloParteTypes";

interface PTituloParteDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onAddBatch: (partes: PTituloParteItem[]) => void;
}

function getDefaultVinculosByPessoa(selectedIds: number[], currentMap: Record<number, string>) {
  return Object.fromEntries(selectedIds.map((id) => [id, currentMap[id] || "D"]));
}

export function PTituloParteDialog({ open, onOpenChange, onAddBatch }: PTituloParteDialogProps) {
  const [step, setStep] = useState<1 | 2>(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectionError, setSelectionError] = useState("");
  const [selectedPessoaIds, setSelectedPessoaIds] = useState<number[]>([]);
  const [vinculosByPessoa, setVinculosByPessoa] = useState<Record<number, string>>({});
  const [pessoas, setPessoas] = useState<PPessoaInterface[]>([]);
  const [isPPessoaDialogOpen, setIsPPessoaDialogOpen] = useState(false);
  const [isSubmittingPessoa, setIsSubmittingPessoa] = useState(false);

  useEffect(() => {
    if (!open) return;

    const fetchPessoas = async () => {
      try {
        const data = (await PessoaService.getAll()) as unknown as PPessoaInterface[];
        setPessoas(data);
      } catch (error) {
        console.error("Erro ao buscar pessoas:", error);
      }
    };

    void fetchPessoas();
  }, [open]);

  const filteredPessoas = useMemo(() => {
    if (!searchQuery.trim()) return pessoas;
    const normalizedQuery = searchQuery.toLowerCase();

    return pessoas.filter(
      (pessoa) =>
        pessoa.nome?.toLowerCase().includes(normalizedQuery) ||
        pessoa.cpfcnpj?.toLowerCase().includes(normalizedQuery),
    );
  }, [pessoas, searchQuery]);

  const resetDialogState = () => {
    setStep(1);
    setSearchQuery("");
    setSelectionError("");
    setSelectedPessoaIds([]);
    setVinculosByPessoa({});
  };

  const togglePessoaSelection = (pessoaId: number, checked: boolean) => {
    setSelectedPessoaIds((prev) => (checked ? [...prev, pessoaId] : prev.filter((id) => id !== pessoaId)));
    setSelectionError("");
  };

  const handleContinue = () => {
    if (selectedPessoaIds.length === 0) {
      setSelectionError("Selecione ao menos uma parte para vincular.");
      return;
    }

    setVinculosByPessoa((prev) => getDefaultVinculosByPessoa(selectedPessoaIds, prev));
    setSelectionError("");
    setStep(2);
  };

  const handleConfirm = () => {
    const hasMissingRole = selectedPessoaIds.some((id) => !vinculosByPessoa[id]);
    if (hasMissingRole) {
      setSelectionError("Defina o tipo de vínculo para todas as partes selecionadas.");
      return;
    }

    const batch = selectedPessoaIds
      .map((id) => pessoas.find((pessoa) => pessoa.pessoa_id === id))
      .filter(Boolean)
      .map((pessoa) => {
        const tipo = vinculosByPessoa[pessoa!.pessoa_id];
        const descricao = pTituloParteRoleOptions.find((option) => option.value === tipo)?.label ?? "Outros";

        return {
          pessoa_id: pessoa?.pessoa_id,
          tipo,
          descricao,
          nome: pessoa?.nome,
          cpfcnpj: pessoa?.cpfcnpj,
        };
      });

    onAddBatch(batch);
    resetDialogState();
    onOpenChange(false);
  };

  const handleCreatePessoa = async (data: PessoaFormValues) => {
    setIsSubmittingPessoa(true);
    try {
      const novaPessoa = await PessoaService.create({
        ...data,
        data_nascimento: data.data_nascimento || undefined,
      });

      const updatedPessoas = (await PessoaService.getAll()) as unknown as PPessoaInterface[];
      setPessoas(updatedPessoas);
      const created = novaPessoa as unknown as PPessoaInterface;
      setSelectedPessoaIds((prev) => (prev.includes(created.pessoa_id) ? prev : [...prev, created.pessoa_id]));
      setSearchQuery(created.nome ?? "");
      setSelectionError("");
      setIsPPessoaDialogOpen(false);
    } catch (error) {
      console.error("Erro ao criar pessoa:", error);
    } finally {
      setIsSubmittingPessoa(false);
    }
  };

  return (
    <>
      <Dialog
        open={open}
        onOpenChange={(nextOpen) => {
          if (!nextOpen) resetDialogState();
          onOpenChange(nextOpen);
        }}
      >
        <DialogContent className="sm:max-w-[520px]">
          <DialogHeader>
            <DialogTitle>{step === 1 ? "Selecionar Partes" : "Definir Vínculo por Parte"}</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            {step === 1 ? (
              <div className="space-y-2">
                <p className="text-sm font-medium">Partes disponíveis</p>

                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
                  <Input
                    type="search"
                    placeholder="Buscar por nome ou CPF/CNPJ..."
                    className="pl-8"
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                  />
                </div>

                <div className="max-h-64 space-y-2 overflow-y-auto rounded-md border p-3">
                  {filteredPessoas.length > 0 ? (
                    filteredPessoas.map((pessoa) => {
                      const checked = selectedPessoaIds.includes(pessoa.pessoa_id);

                      return (
                        <label
                          key={pessoa.pessoa_id}
                          className="flex cursor-pointer items-start gap-2 rounded-sm px-1 py-1 hover:bg-muted/50"
                        >
                          <Checkbox
                            checked={checked}
                            onCheckedChange={(value) => togglePessoaSelection(pessoa.pessoa_id, Boolean(value))}
                          />
                          <div className="flex flex-col">
                            <span className="text-sm">{pessoa.nome ?? "-"}</span>
                            <span className="text-xs text-muted-foreground">{pessoa.cpfcnpj ?? "-"}</span>
                          </div>
                        </label>
                      );
                    })
                  ) : (
                    <div className="space-y-3">
                      <p className="text-sm text-muted-foreground">Nenhuma parte encontrada.</p>
                      <Button type="button" variant="outline" className="w-full" onClick={() => setIsPPessoaDialogOpen(true)}>
                        <UserPlus className="mr-2 h-4 w-4" strokeWidth={1.5} />
                        Cadastrar nova pessoa
                      </Button>
                    </div>
                  )}
                </div>

                {filteredPessoas.length > 0 ? (
                  <Button type="button" variant="outline" className="w-full" onClick={() => setIsPPessoaDialogOpen(true)}>
                    <UserPlus className="mr-2 h-4 w-4" strokeWidth={1.5} />
                    Cadastrar nova pessoa
                  </Button>
                ) : null}

                {selectionError ? <p className="text-sm text-destructive">{selectionError}</p> : null}
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-sm font-medium">Vínculo por parte selecionada</p>

                <div className="max-h-64 space-y-2 overflow-y-auto rounded-md border p-3">
                  {selectedPessoaIds.map((id) => {
                    const pessoa = pessoas.find((item) => item.pessoa_id === id);
                    if (!pessoa) return null;

                    return (
                      <div key={id} className="grid grid-cols-1 gap-2 rounded-sm border p-2">
                        <div>
                          <p className="text-sm">{pessoa.nome ?? "-"}</p>
                          <p className="text-xs text-muted-foreground">{pessoa.cpfcnpj ?? "-"}</p>
                        </div>

                        <Select
                          value={vinculosByPessoa[id] || "D"}
                          onValueChange={(value) =>
                            setVinculosByPessoa((prev) => ({
                              ...prev,
                              [id]: value,
                            }))
                          }
                        >
                          <SelectTrigger className="w-full">
                            <SelectValue placeholder="Tipo de vínculo" />
                          </SelectTrigger>
                          <SelectContent>
                            {pTituloParteRoleOptions.map((option) => (
                              <SelectItem key={option.value} value={option.value}>
                                {option.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                    );
                  })}
                </div>

                {selectionError ? <p className="text-sm text-destructive">{selectionError}</p> : null}
              </div>
            )}

            <div className="flex justify-end gap-2 pt-4">
              {step === 2 ? (
                <Button type="button" variant="outline" onClick={() => setStep(1)}>
                  Voltar
                </Button>
              ) : null}

              <Button
                type="button"
                className="bg-[#FF6B00] text-white hover:bg-[#E56000]"
                onClick={step === 1 ? handleContinue : handleConfirm}
              >
                {step === 1 ? "Próxima Etapa" : "Vincular em Lote"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <PPessoaDialog
        open={isPPessoaDialogOpen}
        onOpenChange={setIsPPessoaDialogOpen}
        onSubmit={handleCreatePessoa}
        isLoading={isSubmittingPessoa}
      />
    </>
  );
}
