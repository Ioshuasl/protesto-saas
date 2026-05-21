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
import { GFeriadoInterface } from "@/packages/administrativo/interfaces";
import { SituacoesBadge } from "@/shared/components/situacoes/SituacoesBadge";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

function formatGFeriadoTipo(tipo?: string | null): string {
  const code = (tipo ?? "").trim().toUpperCase();
  if (code === "F" || code === "FIXO") return "Fixo";
  if (code === "V" || code === "VARIAVEL" || code === "VARIÁVEL") return "Variável";
  return tipo?.trim() || "-";
}

interface GFeriadoTableProps {
  data: GFeriadoInterface[];
  onEdit: (feriado: GFeriadoInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export function GFeriadoTable({ data, onEdit, onDelete, isLoading }: GFeriadoTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando feriados...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum feriado encontrado.
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[120px]">Data</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead>Tipo</TableHead>
            <TableHead>Situação</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((feriado) => (
            <TableRow
              key={feriado.feriado_id}
              className="cursor-pointer"
              onClick={() => onEdit(feriado)}
            >
              <TableCell className="font-medium">
                {feriado.data ? format(new Date(feriado.data), "dd/MM/yyyy", { locale: ptBR }) : "-"}
              </TableCell>
              <TableCell>{feriado.descricao}</TableCell>
              <TableCell>{formatGFeriadoTipo(feriado.tipo)}</TableCell>
              <TableCell>
                <SituacoesBadge situacao={feriado.situacao ?? "I"} />
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(feriado);
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
                      onDelete(feriado.feriado_id);
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
