"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import type { ColumnDef } from "@tanstack/react-table";
import { CheckCircle2, Circle } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import type { PessoaFormValues } from "@/packages/administrativo/schemas/PPessoa/PPessoaFormSchema";
import { usePPessoaReadHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaReadHook";
import { usePPessoaSaveHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaSaveHook";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";
import { DataTable } from "@/shared/components/dataTable/DataTable";
import LoadingButton from "@/shared/components/loadingButton/LoadingButton";
import { useResponse } from "@/shared/components/response/ResponseContext";

type PPessoaTableFormDialogProps = {
  isOpen: boolean;
  tipoPessoa?: "F" | "J" | "P";
  onClose: (open: boolean) => void;
  onSave: (pessoa: PPessoaInterface) => void;
  buttonIsLoading?: boolean;
};

const getTipoPessoaFromDocumento = (cpfcnpj?: string) => {
  const doc = (cpfcnpj ?? "").replace(/\D/g, "");
  if (doc.length === 11) return "F";
  if (doc.length === 14) return "J";
  return undefined;
};

export default function PPessoaTableFormDialog({
  isOpen,
  tipoPessoa,
  onClose,
  onSave,
  buttonIsLoading = false,
}: PPessoaTableFormDialogProps) {
  const { setResponse } = useResponse();
  const { pessoas, fetchPessoas, isLoading } = usePPessoaReadHook();
  const { savePessoa } = usePPessoaSaveHook();

  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [isOpenPPessoaForm, setIsOpenPPessoaForm] = useState(false);
  const [isSavingPessoa, setIsSavingPessoa] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  useEffect(() => {
    if (!isOpen) return;

    void fetchPessoas();
  }, [isOpen, fetchPessoas]);

  const data = useMemo(() => {
    if (!tipoPessoa || tipoPessoa === "P") return pessoas;

    return pessoas.filter((pessoa) => getTipoPessoaFromDocumento(pessoa.cpfcnpj) === tipoPessoa);
  }, [pessoas, tipoPessoa]);

  const columns = useMemo<ColumnDef<PPessoaInterface>[]>(
    () => [
      {
        id: "selecao",
        header: "",
        cell: ({ row }) => {
          const pessoa = row.original;
          const isSelected = selectedPessoa?.pessoa_id === pessoa.pessoa_id;

          return (
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={(event) => {
                event.stopPropagation();
                setSelectedPessoa(pessoa);
              }}
              aria-label={isSelected ? "Pessoa selecionada" : "Selecionar pessoa"}
            >
              {isSelected ? (
                <CheckCircle2 className="h-4 w-4 text-primary" />
              ) : (
                <Circle className="h-4 w-4 text-muted-foreground" />
              )}
            </Button>
          );
        },
        enableSorting: false,
      },
      {
        accessorKey: "pessoa_id",
        header: "ID",
      },
      {
        accessorKey: "nome",
        header: "Nome / Razão Social",
      },
      {
        accessorKey: "cpfcnpj",
        header: "CPF / CNPJ",
      },
      {
        id: "cidade_uf",
        header: "Cidade / UF",
        cell: ({ row }) => {
          const pessoa = row.original;
          return pessoa.cidade ? `${pessoa.cidade} / ${pessoa.uf || "-"}` : "-";
        },
      },
      {
        accessorKey: "telefone",
        header: "Telefone",
        cell: ({ row }) => row.original.telefone || "-",
      },
    ],
    [selectedPessoa],
  );

  const handleSelect = useCallback(() => {
    if (!selectedPessoa) {
      setResponse({
        status: 600,
        error: "Selecao obrigatoria.",
        message: "E necessario selecionar uma pessoa na tabela.",
      });
      return;
    }

    onSave(selectedPessoa);
  }, [onSave, selectedPessoa, setResponse]);

  const handleCreatePessoa = useCallback(
    async (formData: PessoaFormValues) => {
      setIsSavingPessoa(true);
      try {
        const response = await savePessoa(formData, null);

        if (response && typeof response === "object" && "pessoa_id" in response) {
          setSelectedPessoa(response as PPessoaInterface);
        }

        await fetchPessoas();
        setIsOpenPPessoaForm(false);
      } catch (error) {
        console.error("Erro ao salvar pessoa:", error);
      } finally {
        setIsSavingPessoa(false);
      }
    },
    [fetchPessoas, savePessoa],
  );

  return (
    <>
      <Dialog
        open={isOpen}
        onOpenChange={(open) => {
          if (!open) {
            setSelectedPessoa(null);
          }
          onClose(open);
        }}
      >
        <DialogContent className="flex h-[90vh] w-full max-w-full flex-col p-4 sm:max-w-4xl sm:p-6 md:max-w-6xl lg:max-w-6xl">
          <DialogHeader>
            <DialogTitle className="text-base sm:text-lg">Pessoa(s)</DialogTitle>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <DialogDescription className="text-xs sm:text-sm">
                Lista de pessoas cadastradas junto ao sistema
              </DialogDescription>

              <Button
                type="button"
                size="sm"
                className="w-full cursor-pointer sm:w-auto"
                onClick={() => setIsOpenPPessoaForm(true)}
              >
                Adicionar pessoa
              </Button>
            </div>
          </DialogHeader>

          <div className="min-h-0 flex-1">
            <DataTable
              data={data}
              columns={columns}
              loading={isLoading}
              filterColumn="nome"
              filterPlaceholder="Buscar por nome..."
              onRowClick={(pessoa) => setSelectedPessoa(pessoa)}
              onLoadMore={async () => {
                setIsLoadingMore(true);
                setIsLoadingMore(false);
              }}
              isLoadingMore={isLoadingMore}
            />
          </div>

          <DialogFooter className="mt-3 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
            <DialogClose asChild>
              <Button
                variant="outline"
                type="button"
                onClick={() => onClose(false)}
                className="w-full cursor-pointer sm:w-auto"
              >
                Cancelar
              </Button>
            </DialogClose>

            <LoadingButton
              text="Selecionar"
              textLoading="Aguarde..."
              loading={buttonIsLoading}
              className="w-full sm:w-auto"
              type="button"
              onClick={handleSelect}
            />
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <PPessoaDialog
        open={isOpenPPessoaForm}
        onOpenChange={setIsOpenPPessoaForm}
        onSubmit={handleCreatePessoa}
        isLoading={isSavingPessoa}
      />
    </>
  );
}
