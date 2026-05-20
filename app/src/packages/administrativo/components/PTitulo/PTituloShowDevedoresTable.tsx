"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PTituloShowDevedoresItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloShowDevedoresItem";

interface PTituloShowDevedoresTableProps {
  data: PTituloShowDevedoresItem[];
  isLoading?: boolean;
  onRowClick?: (devedor: PTituloShowDevedoresItem) => void;
}

export function PTituloShowDevedoresTable({ data, isLoading, onRowClick }: PTituloShowDevedoresTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando devedores...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum devedor encontrado para este título.
      </div>
    );
  }

  return (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[70px]">Título</TableHead>
            <TableHead>Devedor</TableHead>
            <TableHead>CPF/CNPJ</TableHead>
            <TableHead>Tipo Aceite</TableHead>
            <TableHead>Data Aceite/Edital</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((devedor) => (
            <TableRow
              key={devedor.pessoa_vinculo_id}
              className={onRowClick ? "cursor-pointer" : undefined}
              onClick={onRowClick ? () => onRowClick(devedor) : undefined}
            >
              <TableCell className="font-medium">{devedor.titulo_id}</TableCell>
              <TableCell>{devedor.devedor_nome ?? "-"}</TableCell>
              <TableCell>{devedor.devedor_cpfcnpj ?? "-"}</TableCell>
              <TableCell>{devedor.devedor_tipo_aceite ?? "-"}</TableCell>
              <TableCell>
                {devedor.devedor_data_aceite instanceof Date
                  ? devedor.devedor_data_aceite.toLocaleDateString("pt-BR")
                  : "-"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

