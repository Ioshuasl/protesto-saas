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
import { AlertCircle, Pencil, Trash2 } from "lucide-react";
import { PPessoaInterface } from "@/packages/administrativo/interfaces";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatCpfCnpj } from "@/shared/utils/document";
import { formatEmptyField, isEmptyFieldValue } from "@/shared/utils/emptyField";

interface PPessoaTableProps {
  data: PPessoaInterface[];
  onEdit: (pessoa: PPessoaInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

function formatCidadeUf(cidade?: string | null, uf?: string | null): string {
  const cidadeFmt = formatEmptyField(cidade);
  const ufFmt = formatEmptyField(uf);

  if (cidadeFmt === EMPTY_FIELD_LABEL && ufFmt === EMPTY_FIELD_LABEL) {
    return EMPTY_FIELD_LABEL;
  }
  if (cidadeFmt === EMPTY_FIELD_LABEL) {
    return ufFmt;
  }
  if (ufFmt === EMPTY_FIELD_LABEL) {
    return cidadeFmt;
  }
  return `${cidadeFmt} / ${ufFmt}`;
}

function isMicroempresaFlag(value: unknown): boolean {
  if (value === true || value === 1) return true;
  if (typeof value !== "string") return false;

  const normalized = value.trim().toLowerCase();
  return normalized === "true" || normalized === "1" || normalized === "s";
}

function MicroempresaBadge() {
  return (
    <Badge variant="outline" className="border-amber-500/60 text-amber-700" title="Microempresa">
      MEI
    </Badge>
  );
}

function CpfcnpjCell({ cpfcnpj }: { cpfcnpj?: string | null }) {
  if (!isEmptyFieldValue(cpfcnpj)) {
    return <>{formatCpfCnpj(cpfcnpj)}</>;
  }

  return (
    <span className="inline-flex items-center gap-1.5 text-destructive">
      <span>{EMPTY_FIELD_LABEL}</span>
      <AlertCircle className="h-4 w-4 shrink-0" aria-hidden />
    </span>
  );
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
            <TableHead>Nome / Razão Social</TableHead>
            <TableHead>CPF / CNPJ</TableHead>
            <TableHead>Cidade / UF</TableHead>
            <TableHead className="text-center">Qtd. Títulos</TableHead>
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
              <TableCell className="font-medium">
                <div className="flex items-center gap-2">
                  <span>{formatEmptyField(pessoa.nome)}</span>
                  {isMicroempresaFlag(pessoa.micro_empresa) ? <MicroempresaBadge /> : null}
                </div>
              </TableCell>
              <TableCell>
                <CpfcnpjCell cpfcnpj={pessoa.cpfcnpj} />
              </TableCell>
              <TableCell>{formatCidadeUf(pessoa.cidade, pessoa.uf)}</TableCell>
              <TableCell className="text-center tabular-nums">
                {pessoa.total_titulos ?? 0}
              </TableCell>
              <TableCell>{formatEmptyField(pessoa.telefone)}</TableCell>
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
