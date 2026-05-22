"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Pencil, Trash2, X } from "lucide-react";
import { PLivroAndamentoInterface, PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyField, formatEmptyFieldDate } from "@/shared/utils/emptyField";

interface PLivroAndamentoTableProps {
  data: PLivroAndamentoInterface[];
  naturezas: PLivroNaturezaInterface[];
  onEdit: (livro: PLivroAndamentoInterface) => void;
  onFinalize: (livro: PLivroAndamentoInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export function PLivroAndamentoTable({ 
  data, 
  naturezas,
  onEdit,
  onFinalize,
  onDelete,
  isLoading,
}: PLivroAndamentoTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando livros em andamento...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum livro em andamento encontrado.
      </div>
    );
  }

  const getNaturezaDescricao = (id?: number) => {
    if (!id) return EMPTY_FIELD_LABEL;
    const natureza = naturezas.find((n) => n.livro_natureza_id === id);
    return natureza ? `${natureza.descricao} (${natureza.sigla})` : String(id);
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Nº Livro</TableHead>
            <TableHead>Natureza</TableHead>
            <TableHead>Folha Atual</TableHead>
            <TableHead>Data Abertura</TableHead>
            <TableHead>Situação</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((livro) => (
            <TableRow
              key={livro.livro_andamento_id}
              className="cursor-pointer"
              onClick={() => onEdit(livro)}
            >
              <TableCell>{formatEmptyField(livro.numero_livro)}</TableCell>
              <TableCell>{getNaturezaDescricao(livro.livro_natureza_id)}</TableCell>
              <TableCell>{livro.folha_atual} / {livro.numero_folhas}</TableCell>
              <TableCell>
                {formatEmptyFieldDate(livro.data_abertura, (date) =>
                  format(date, "dd/MM/yyyy", { locale: ptBR }),
                )}
              </TableCell>
              <TableCell>
                <Badge variant={livro.aberto ? "default" : "secondary"}>
                  {livro.aberto ? "Aberto" : "Fechado"}
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
                  {livro.aberto ? (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={(event) => {
                        event.stopPropagation();
                        onFinalize(livro);
                      }}
                      title="Finalizar"
                      className="group"
                    >
                      <X className="h-4 w-4 text-muted-foreground transition-colors group-hover:text-[#FF6B00]" />
                    </Button>
                  ) : null}
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onDelete(livro.livro_andamento_id);
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
