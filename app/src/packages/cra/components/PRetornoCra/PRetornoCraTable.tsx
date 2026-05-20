"use client";

import { Check } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";

interface PRetornoCraTableProps {
  data: PTituloInterface[];
  isLoading?: boolean;
  bancoLabelById?: Map<number, string>;
  ocorrenciaLabelById?: Map<number, string>;
}

function getStatusImportacaoLabel(status?: PTituloInterface["status_importacao"]): string {
  if (status === "D") return "Aguardando";
  if (status === "E") return "Exportado";
  return "-";
}

export function PRetornoCraTable({
  data,
  isLoading,
  bancoLabelById,
  ocorrenciaLabelById,
}: PRetornoCraTableProps) {
  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center p-8 text-muted-foreground">
        Carregando títulos...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex w-full items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum título encontrado para retorno.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Status Importação</TableHead>
            <TableHead>Número Apontamento</TableHead>
            <TableHead>Banco</TableHead>
            <TableHead>Ocorrência</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((titulo) => (
            <TableRow key={titulo.titulo_id}>
              <TableCell>
                {titulo.status_importacao === "E" ? (
                  <div className="inline-flex items-center gap-1.5 text-emerald-600">
                    <span className="font-medium">{getStatusImportacaoLabel(titulo.status_importacao)}</span>
                    <Check className="h-4 w-4" />
                  </div>
                ) : (
                  <span>{getStatusImportacaoLabel(titulo.status_importacao)}</span>
                )}
              </TableCell>
              <TableCell>{titulo.numero_apontamento ?? "-"}</TableCell>
              <TableCell>
                {titulo.banco_id ? bancoLabelById?.get(titulo.banco_id) || String(titulo.banco_id) : "-"}
              </TableCell>
              <TableCell>
                {titulo.ocorrencia_id
                  ? ocorrenciaLabelById?.get(titulo.ocorrencia_id) || String(titulo.ocorrencia_id)
                  : "-"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
