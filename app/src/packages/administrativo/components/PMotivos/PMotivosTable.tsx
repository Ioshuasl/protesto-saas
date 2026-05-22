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
import { normalizeSituacaoKey } from "@/packages/administrativo/components/PLivroNatureza/plivroNaturezaSituacaoUtils";
import { PMotivosInterface } from "@/packages/administrativo/interfaces";
import { SituacoesBadge } from "@/shared/components/situacoes/SituacoesBadge";
import { formatEmptyField, formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";

interface PMotivosTableProps {
  data: PMotivosInterface[];
  onEdit: (motivo: PMotivosInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export function PMotivosTable({ data, onEdit, onDelete, isLoading }: PMotivosTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando motivos de apontamento...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum motivo de apontamento encontrado.
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Código</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead>Situação</TableHead>
            <TableHead className="text-right w-[120px]">Qtd. Titulos</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((motivo) => (
            <TableRow
              key={motivo.motivos_id}
              className="cursor-pointer"
              onClick={() => onEdit(motivo)}
            >
              <TableCell className="font-medium">{formatEmptyField(motivo.codigo)}</TableCell>
              <TableCell>{formatEmptyFieldTrimmed(motivo.descricao)}</TableCell>
              <TableCell>
                <SituacoesBadge situacao={normalizeSituacaoKey(motivo.situacao)} />
              </TableCell>
              <TableCell className="text-right tabular-nums">
                {Number(motivo.total_titulos ?? 0).toLocaleString("pt-BR")}
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button variant="ghost" size="icon" onClick={(event) => { event.stopPropagation(); onEdit(motivo); }} title="Editar" className="group">
                    <Pencil className="h-4 w-4 text-foreground transition-colors group-hover:text-[#FF6B00]" strokeWidth={1.5} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onDelete(motivo.motivos_id);
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
