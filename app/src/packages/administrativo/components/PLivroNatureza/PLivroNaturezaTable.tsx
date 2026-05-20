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
import { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";
import { Badge } from "@/components/ui/badge";

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
            <TableHead className="w-[80px]">ID</TableHead>
            <TableHead>Sigla</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead>Tipo</TableHead>
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
              <TableCell className="font-medium">{livro.livro_natureza_id}</TableCell>
              <TableCell>{livro.sigla}</TableCell>
              <TableCell>{livro.descricao}</TableCell>
              <TableCell>{livro.tipo}</TableCell>
              <TableCell>
                <Badge variant={livro.situacao === "Ativo" ? "default" : "secondary"}>
                  {livro.situacao || "Ativo"}
                </Badge>
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
