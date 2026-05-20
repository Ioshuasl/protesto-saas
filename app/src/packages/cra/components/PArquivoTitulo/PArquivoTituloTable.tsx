"use client";

import { FileCheck2, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";

interface PArquivoTituloTableProps {
  data: PArquivoTituloInterface[];
  isLoading?: boolean;
  onGerarArquivoConfirmacao: (arquivo: PArquivoTituloInterface) => void;
  onEstornarRemessa: (arquivo: PArquivoTituloInterface) => void;
}

function formatImportDate(value?: Date): string {
  if (!value) return "-";
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "-";

  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export function PArquivoTituloTable({
  data,
  isLoading,
  onGerarArquivoConfirmacao,
  onEstornarRemessa,
}: PArquivoTituloTableProps) {
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
    <div className="overflow-x-auto rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Nome do Arquivo</TableHead>
            <TableHead>Data da Importação</TableHead>
            <TableHead>Quantidade</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((arquivo) => (
            <TableRow
              key={arquivo.arquivo_titulo_id}
              className="cursor-pointer"
              onClick={() => onGerarArquivoConfirmacao(arquivo)}
            >
              <TableCell className="max-w-[280px] truncate font-medium">{arquivo.nome_arquivo ?? "-"}</TableCell>
              <TableCell className="whitespace-nowrap">{formatImportDate(arquivo.data_importacao)}</TableCell>
              <TableCell>{arquivo.quantidade ?? 0}</TableCell>
              <TableCell>
                <div className="flex justify-end gap-2">
                  <Button type="button" variant="outline" size="sm" onClick={(event) => { event.stopPropagation(); onGerarArquivoConfirmacao(arquivo); }}>
                    <FileCheck2 className="mr-1 h-4 w-4" />
                    Gerar Arquivo de Confirmação
                  </Button>
                  <Button type="button" variant="ghost" size="sm" onClick={(event) => { event.stopPropagation(); onEstornarRemessa(arquivo); }}>
                    <RotateCcw className="mr-1 h-4 w-4" />
                    Estornar Remessa
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
