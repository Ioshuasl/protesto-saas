"use client";

import { AlertCircle, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { PPessoaVinculoTipoSelectObject } from "@/packages/administrativo/components/PPessoaVinculo/PPessoaVinculoTipoSelectObject";
import {
  PPessoaVinculoTipoEnum,
  formatPPessoaVinculoTipoLabel,
  normalizePPessoaVinculoTipo,
  type PPessoaVinculoTipo,
} from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyField, isEmptyFieldValue } from "@/shared/utils/emptyField";

function CpfcnpjCell({ cpfcnpj }: { cpfcnpj?: string | null }) {
  if (!isEmptyFieldValue(cpfcnpj)) {
    return <>{formatEmptyField(cpfcnpj)}</>;
  }

  return (
    <span className="inline-flex items-center gap-1.5 text-destructive">
      <span>{EMPTY_FIELD_LABEL}</span>
      <AlertCircle className="h-4 w-4 shrink-0" aria-hidden />
    </span>
  );
}

export type PPessoaVinculoTableRow = {
  id: string;
  tipo?: string;
  nome?: string;
  cpfcnpj?: string;
};

export interface PPessoaVinculoTableProps {
  rows: PPessoaVinculoTableRow[];
  onTipoChange: (index: number, tipo: PPessoaVinculoTipo) => void;
  onEdit: (index: number) => void;
  onRemove: (index: number) => void;
  emptyMessage?: string;
  tipoPlaceholder?: string;
}

export function PPessoaVinculoTable({
  rows,
  onTipoChange,
  onEdit,
  onRemove,
  emptyMessage = "Nenhuma parte vinculada encontrada.",
  tipoPlaceholder = "Tipo de vínculo",
}: PPessoaVinculoTableProps) {
  if (rows.length === 0) {
    return (
      <div className="rounded-md border p-3 text-sm text-muted-foreground">{emptyMessage}</div>
    );
  }

  return (
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
          {rows.map((row, index) => {
            const tipoValue =
              normalizePPessoaVinculoTipo(row.tipo) ?? PPessoaVinculoTipoEnum.DEVEDOR;

            return (
              <TableRow key={row.id}>
                <TableCell className="min-w-[220px]">
                  <PPessoaVinculoTipoSelectObject
                    value={tipoValue}
                    onValueChange={(tipo) => {
                      if (!tipo) return;
                      onTipoChange(index, tipo);
                    }}
                    placeholder={tipoPlaceholder}
                    clearable={false}
                  />
                </TableCell>
                <TableCell title={row.nome}>
                  {formatEmptyField(row.nome)}
                </TableCell>
                <TableCell>
                  <CpfcnpjCell cpfcnpj={row.cpfcnpj} />
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-foreground hover:text-[#FF6B00]"
                      onClick={() => onEdit(index)}
                      aria-label={`Editar ${formatPPessoaVinculoTipoLabel(tipoValue)}`}
                    >
                      <Pencil className="h-4 w-4" strokeWidth={1.5} />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8 text-foreground hover:text-[#FF6B00]"
                      onClick={() => onRemove(index)}
                      aria-label={`Excluir ${row.nome ?? EMPTY_FIELD_LABEL}`}
                    >
                      <Trash2 className="h-4 w-4" strokeWidth={1.5} />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
