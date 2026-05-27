"use client";

import { Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { GEmolumentoPeriodoInterface } from "@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyFieldDate, formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

interface GEmolumentoPeriodoTableProps {
  data: GEmolumentoPeriodoInterface[];
  onEdit: (periodo: GEmolumentoPeriodoInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

function formatSituacao(value?: string) {
  if (value === "A") return "Ativo";
  if (value === "I") return "Inativo";
  return formatEmptyFieldTrimmed(value);
}

export function GEmolumentoPeriodoTable({
  data,
  onEdit,
  onDelete,
  isLoading,
}: GEmolumentoPeriodoTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando periodos de emolumento...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum periodo de emolumento encontrado.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border">
      <Table className="table-fixed w-full">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[120px]">ID</TableHead>
            <TableHead>Descricao</TableHead>
            <TableHead className="w-[180px]">Data inicial</TableHead>
            <TableHead className="w-[140px]">Situacao</TableHead>
            <TableHead className="w-[100px] text-right">Acoes</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((periodo) => (
            <TableRow
              key={periodo.emolumento_periodo_id}
              className="cursor-pointer"
              onClick={() => onEdit(periodo)}
            >
              <TableCell className="font-medium">
                {periodo.emolumento_periodo_id ?? EMPTY_FIELD_LABEL}
              </TableCell>
              <TableCell>{formatEmptyFieldTrimmed(periodo.descricao)}</TableCell>
              <TableCell>
                {formatEmptyFieldDate(periodo.data_inicial, (date) =>
                  format(date, "dd/MM/yyyy", { locale: ptBR }),
                )}
              </TableCell>
              <TableCell>{formatSituacao(periodo.situacao)}</TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(periodo);
                    }}
                    title="Editar"
                    className="group"
                  >
                    <Pencil className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-[#FF6B00]" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onDelete(periodo.emolumento_periodo_id);
                    }}
                    title="Excluir"
                    className="group"
                  >
                    <Trash2 className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-[#FF6B00]" />
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
