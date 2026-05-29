"use client";

import { ExternalLink, Loader2 } from "lucide-react";
import { useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { PArquivoTituloActionIconButton } from "@/packages/cra/components/PArquivoTitulo/PArquivoTituloActionIconButton";
import { usePTituloArquivoShowHook } from "@/packages/cra/hooks/PTituloArquivo/usePTituloArquivoShowHook";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import { formatEmptyField, formatEmptyFieldDate } from "@/shared/utils/emptyField";

const moneyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function formatTituloDate(value?: Date | string): string {
  return formatEmptyFieldDate(value, (date) =>
    new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(date),
  );
}

function formatTituloMoney(value?: number): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "-";
  }
  return moneyFormatter.format(value);
}

function openTituloInNewTab(tituloId: number) {
  const path = `/titulos/${tituloId}`;
  if (typeof window !== "undefined") {
    window.open(path, "_blank", "noopener,noreferrer");
  }
}

interface PArquivoTituloTitulosTableDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  arquivo: PArquivoTituloInterface | null;
}

export function PArquivoTituloTitulosTableDialog({
  open,
  onOpenChange,
  arquivo,
}: PArquivoTituloTitulosTableDialogProps) {
  const { arquivoTitulo, isLoading, fetchArquivoTitulo } = usePTituloArquivoShowHook();
  const arquivoTituloId = arquivo?.arquivo_titulo_id;
  const nomeArquivo = arquivo?.nome_arquivo ?? arquivoTitulo?.nome_arquivo;

  useEffect(() => {
    if (!open || arquivoTituloId == null) return;
    void fetchArquivoTitulo(arquivoTituloId, { include: "titulos" });
  }, [open, arquivoTituloId, fetchArquivoTitulo]);

  const titulos: PTituloInterface[] = arquivoTitulo?.titulos ?? [];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="flex max-h-[85vh] flex-col gap-0 overflow-hidden sm:max-w-5xl">
        <DialogHeader>
          <DialogTitle>Títulos do arquivo</DialogTitle>
          <DialogDescription>
            {nomeArquivo
              ? `Títulos vinculados ao arquivo "${nomeArquivo}".`
              : "Títulos vinculados ao arquivo de remessa."}
          </DialogDescription>
        </DialogHeader>

        <div className="min-h-0 flex-1 overflow-y-auto pt-2">
          {isLoading ? (
            <div className="flex items-center justify-center gap-2 py-10 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" />
              Carregando títulos...
            </div>
          ) : titulos.length === 0 ? (
            <div className="rounded-md border px-4 py-10 text-center text-sm text-muted-foreground">
              Nenhum título vinculado a este arquivo.
            </div>
          ) : (
            <div className="overflow-x-auto rounded-md border">
              <Table>
                <TableHeader className="bg-muted/40">
                  <TableRow className="hover:bg-transparent">
                    <TableHead className="text-xs">Nosso número</TableHead>
                    <TableHead className="text-xs">Nº título</TableHead>
                    <TableHead className="text-xs">Nº apontamento</TableHead>
                    <TableHead className="text-right text-xs">Valor</TableHead>
                    <TableHead className="text-xs">Vencimento</TableHead>
                    <TableHead className="min-w-[120px] text-right text-xs">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {titulos.map((titulo) => (
                    <TableRow key={titulo.titulo_id}>
                      <TableCell className="max-w-[180px] truncate">
                        {formatEmptyField(titulo.nosso_numero)}
                      </TableCell>
                      <TableCell className="max-w-[160px] truncate">
                        {formatEmptyField(titulo.numero_titulo)}
                      </TableCell>
                      <TableCell className="max-w-[140px] truncate tabular-nums">
                        {formatEmptyField(titulo.numero_apontamento)}
                      </TableCell>
                      <TableCell className="text-right whitespace-nowrap">
                        {formatTituloMoney(titulo.valor_titulo)}
                      </TableCell>
                      <TableCell className="whitespace-nowrap">
                        {formatTituloDate(titulo.data_vencimento_titulo)}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end">
                          <PArquivoTituloActionIconButton
                            label="Visualizar"
                            className="hover:bg-orange-50 hover:text-[#FF6B00]"
                            disabled={isLoading}
                            onClick={() => openTituloInNewTab(titulo.titulo_id)}
                          >
                            <ExternalLink />
                          </PArquivoTituloActionIconButton>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
