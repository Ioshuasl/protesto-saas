"use client";

import { FileText, Pencil } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PTemplateInterface } from "@/packages/administrativo/interfaces/PTemplate/PTemplateInterface";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";

interface PTemplateTableProps {
  data: PTemplateInterface[];
  onEdit: (template: PTemplateInterface) => void;
  onOpenDocument: (template: PTemplateInterface) => void;
  isLoading?: boolean;
}

export function PTemplateTable({ data, onEdit, onOpenDocument, isLoading }: PTemplateTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando minutas...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhuma minuta encontrada.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border">
      <Table className="table-fixed w-full">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[120px]">ID</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead className="w-[120px] text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((template) => (
            <TableRow
              key={template.template_id}
              className="cursor-pointer"
              onClick={() => onEdit(template)}
            >
              <TableCell>{template.template_id}</TableCell>
              <TableCell>{formatEmptyFieldTrimmed(template.descricao) ?? EMPTY_FIELD_LABEL}</TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onOpenDocument(template);
                    }}
                    title="Editar texto"
                    className="group"
                  >
                    <FileText className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-[#FF6B00]" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(template);
                    }}
                    title="Editar"
                    className="group"
                  >
                    <Pencil className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-[#FF6B00]" />
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
