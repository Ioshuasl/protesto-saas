"use client";

import { useState } from "react";
import { Download, FileCheck2, Loader2, Trash2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { PArquivoTituloActionIconButton } from "@/packages/cra/components/PArquivoTitulo/PArquivoTituloActionIconButton";
import { buildEstornarRemessaConfirmMessage } from "@/packages/cra/components/PArquivoTitulo/pArquivoTituloEstornarMessage";
import { usePArquivoTituloDownload } from "@/packages/cra/hooks/PTituloArquivo/usePArquivoTituloDownload";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { formatEmptyField, formatEmptyFieldDate } from "@/shared/utils/emptyField";

interface PArquivoTituloTableProps {
  data: PArquivoTituloInterface[];
  isLoading?: boolean;
  onGerarArquivoConfirmacao: (arquivo: PArquivoTituloInterface) => void;
  onEstornarRemessa: (arquivo: PArquivoTituloInterface) => void;
  onVerTitulos: (arquivo: PArquivoTituloInterface) => void;
}

function formatImportDate(value?: Date): string {
  return formatEmptyFieldDate(value, (date) =>
    new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date),
  );
}

export function PArquivoTituloTable({
  data,
  isLoading,
  onGerarArquivoConfirmacao,
  onEstornarRemessa,
  onVerTitulos,
}: PArquivoTituloTableProps) {
  const { downloadArquivo, isDownloading, isDownloadingAny } = usePArquivoTituloDownload();
  const [estornarDialogOpen, setEstornarDialogOpen] = useState(false);
  const [arquivoParaEstornar, setArquivoParaEstornar] =
    useState<PArquivoTituloInterface | null>(null);

  const openEstornarDialog = (arquivo: PArquivoTituloInterface) => {
    setArquivoParaEstornar(arquivo);
    setEstornarDialogOpen(true);
  };

  const closeEstornarDialog = () => {
    setEstornarDialogOpen(false);
    setArquivoParaEstornar(null);
  };

  const handleConfirmEstornar = () => {
    if (arquivoParaEstornar) {
      onEstornarRemessa(arquivoParaEstornar);
    }
    closeEstornarDialog();
  };

  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center p-8 text-muted-foreground">
        Carregando arquivos importados...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex w-full items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum arquivo importado encontrado.
      </div>
    );
  }

  return (
    <>
    <div className="overflow-x-auto rounded-md border">
      <Table>
        <TableHeader className="bg-muted/40">
          <TableRow className="hover:bg-transparent">
            <TableHead>Nome do Arquivo</TableHead>
            <TableHead>Data da Importação</TableHead>
            <TableHead className="w-[100px]">Quantidade</TableHead>
            <TableHead className="min-w-[320px] text-right text-xs">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((arquivo) => (
            <TableRow
              key={arquivo.arquivo_titulo_id}
              className="group cursor-pointer transition-colors hover:bg-muted/30"
              onClick={() => onVerTitulos(arquivo)}
            >
              <TableCell className="max-w-[280px] truncate font-medium">
                {formatEmptyField(arquivo.nome_arquivo)}
              </TableCell>
              <TableCell className="whitespace-nowrap">
                {formatImportDate(arquivo.data_importacao)}
              </TableCell>
              <TableCell className="tabular-nums">{arquivo.quantidade ?? 0}</TableCell>
              <TableCell className="text-right">
                <div
                  className="flex flex-wrap justify-end gap-0.5"
                  onClick={(event) => event.stopPropagation()}
                  onKeyDown={(event) => event.stopPropagation()}
                >
                  <PArquivoTituloActionIconButton
                    label="Baixar"
                    className="hover:bg-muted"
                    disabled={isDownloadingAny}
                    onClick={() =>
                      void downloadArquivo(
                        arquivo.arquivo_titulo_id,
                        arquivo.nome_arquivo ?? undefined,
                      )
                    }
                  >
                    {isDownloading(arquivo.arquivo_titulo_id) ? (
                      <Loader2 className="animate-spin" />
                    ) : (
                      <Download />
                    )}
                  </PArquivoTituloActionIconButton>
                  <PArquivoTituloActionIconButton
                    label="Confirmar"
                    className="hover:bg-orange-50 hover:text-[#FF6B00]"
                    disabled={isDownloadingAny}
                    onClick={() => onGerarArquivoConfirmacao(arquivo)}
                  >
                    <FileCheck2 />
                  </PArquivoTituloActionIconButton>
                  <PArquivoTituloActionIconButton
                    label="Estornar"
                    className="hover:bg-rose-50 hover:text-rose-600"
                    disabled={isDownloadingAny}
                    onClick={() => openEstornarDialog(arquivo)}
                  >
                    <Trash2 />
                  </PArquivoTituloActionIconButton>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>

    <ConfirmDialog
      isOpen={estornarDialogOpen}
      title={arquivoParaEstornar?.nome_arquivo ?? "Remessa"}
      description="Confirmar estorno"
      message={
        arquivoParaEstornar
          ? buildEstornarRemessaConfirmMessage(arquivoParaEstornar)
          : ""
      }
      confirmText="Estornar"
      onConfirm={handleConfirmEstornar}
      onCancel={closeEstornarDialog}
    />
    </>
  );
}
