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
import { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";
import { normalizeSituacaoKey } from "@/packages/administrativo/components/PLivroNatureza/plivroNaturezaSituacaoUtils";
import { SituacoesBadge } from "@/shared/components/situacoes/SituacoesBadge";

interface PLivroNaturezaTableProps {
  data: PLivroNaturezaInterface[];
  onEdit: (livroNatureza: PLivroNaturezaInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export function PLivroNaturezaTable({ data, onEdit, onDelete, isLoading }: PLivroNaturezaTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando livros de natureza...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum livro de natureza encontrado.
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Sigla</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead>Situação</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((livro) => (
            <TableRow
              key={livro.livro_natureza_id}
              className="cursor-pointer"
              onClick={() => onEdit(livro)}
            >
              <TableCell>{livro.sigla ?? "—"}</TableCell>
              <TableCell>{livro.descricao?.trim() || "—"}</TableCell>
              <TableCell>
                <SituacoesBadge situacao={normalizeSituacaoKey(livro.situacao)} />
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(livro);
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
                      onDelete(livro.livro_natureza_id);
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
