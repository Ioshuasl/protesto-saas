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
import { PPessoaInterface } from "@/packages/administrativo/interfaces";

interface PPessoaTableProps {
  data: PPessoaInterface[];
  onEdit: (pessoa: PPessoaInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export function PPessoaTable({ data, onEdit, onDelete, isLoading }: PPessoaTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando pessoas...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhuma pessoa encontrada.
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[80px]">ID</TableHead>
            <TableHead>Nome / Razão Social</TableHead>
            <TableHead>CPF / CNPJ</TableHead>
            <TableHead>Cidade / UF</TableHead>
            <TableHead>Telefone</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((pessoa) => (
            <TableRow
              key={pessoa.pessoa_id}
              className="cursor-pointer"
              onClick={() => onEdit(pessoa)}
            >
              <TableCell className="font-medium">{pessoa.pessoa_id}</TableCell>
              <TableCell>{pessoa.nome}</TableCell>
              <TableCell>{pessoa.cpfcnpj}</TableCell>
              <TableCell>
                {pessoa.cidade ? `${pessoa.cidade} / ${pessoa.uf || "-"}` : "-"}
              </TableCell>
              <TableCell>{pessoa.telefone || "-"}</TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(pessoa);
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
                      onDelete(pessoa.pessoa_id);
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
