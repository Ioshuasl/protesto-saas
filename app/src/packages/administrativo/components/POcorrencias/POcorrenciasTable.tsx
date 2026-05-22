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
import { POcorrenciasInterface } from "@/packages/administrativo/interfaces";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";

interface POcorrenciasTableProps {
  data: POcorrenciasInterface[];
  onEdit: (ocorrencia: POcorrenciasInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

const COL_WIDTH = "w-[25%] min-w-0";

function cellOrEmpty(value?: string | null) {
  return formatEmptyFieldTrimmed(value);
}

function TruncatedCell({
  value,
  className,
}: {
  value: string;
  className?: string;
}) {
  return (
    <span
      className={`block truncate ${className ?? ""}`}
      title={value !== EMPTY_FIELD_LABEL ? value : undefined}
    >
      {value}
    </span>
  );
}

export function POcorrenciasTable({ data, onEdit, onDelete, isLoading }: POcorrenciasTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando ocorrências...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhuma ocorrência encontrada.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border">
      <Table className="table-fixed w-full">
        <TableHeader>
          <TableRow>
            <TableHead className={COL_WIDTH}>Descrição</TableHead>
            <TableHead className={COL_WIDTH}>Código</TableHead>
            <TableHead className={COL_WIDTH}>Tipo</TableHead>
            <TableHead className={`${COL_WIDTH} text-right`}>Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((ocorrencia) => {
            const descricao = cellOrEmpty(ocorrencia.descricao);
            return (
              <TableRow
                key={ocorrencia.ocorrencias_id}
                className="cursor-pointer"
                onClick={() => onEdit(ocorrencia)}
              >
                <TableCell className={`${COL_WIDTH} font-medium`}>
                  <TruncatedCell value={descricao} />
                </TableCell>
                <TableCell className={COL_WIDTH}>
                  <TruncatedCell value={cellOrEmpty(ocorrencia.codigo)} />
                </TableCell>
                <TableCell className={COL_WIDTH}>
                  <TruncatedCell value={cellOrEmpty(ocorrencia.tipo)} />
                </TableCell>
                <TableCell className={`${COL_WIDTH} text-right`}>
                  <div className="flex justify-end gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={(event) => {
                        event.stopPropagation();
                        onEdit(ocorrencia);
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
                        onDelete(ocorrencia.ocorrencias_id);
                      }}
                      title="Excluir"
                      className="group"
                    >
                      <Trash2 className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-[#FF6B00]" />
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
