"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Pencil, Trash2 } from "lucide-react";
import { PMotivosCancelamentoInterface } from "@/packages/administrativo/interfaces";

interface PMotivosCancelamentoTableProps {
  data: PMotivosCancelamentoInterface[];
  onEdit: (item: PMotivosCancelamentoInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export function PMotivosCancelamentoTable({
  data,
  onEdit,
  onDelete,
  isLoading,
}: PMotivosCancelamentoTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando motivos de cancelamento...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum motivo de cancelamento encontrado.
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[80px]">ID</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead>Situação</TableHead>
            <TableHead>Tipo (Ord. Jud./Rem. Ind.)</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item) => (
            <TableRow
              key={item.motivos_cancelamento_id}
              className="cursor-pointer"
              onClick={() => onEdit(item)}
            >
              <TableCell className="font-medium">{item.motivos_cancelamento_id}</TableCell>
              <TableCell>{item.descricao}</TableCell>
              <TableCell>{item.situacao}</TableCell>
              <TableCell>{item.ord_jud_ou_rem_ind}</TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button variant="ghost" size="icon" onClick={(event) => { event.stopPropagation(); onEdit(item); }} title="Editar" className="group">
                    <Pencil className="h-4 w-4 text-foreground transition-colors group-hover:text-[#FF6B00]" strokeWidth={1.5} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onDelete(item.motivos_cancelamento_id);
                    }}
                    title="Excluir"
                    className="group"
                  >
                    <Trash2 className="h-4 w-4 text-foreground transition-colors group-hover:text-[#FF6B00]" strokeWidth={1.5} />
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
