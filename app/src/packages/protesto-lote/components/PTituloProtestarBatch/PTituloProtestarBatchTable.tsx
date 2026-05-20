"use client";

import { FileText, Printer } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PTituloProtestarBatchInterface } from "@/packages/protesto-lote/interface/PTituloProtestarBatch/PTituloProtestarBatchInterface";

interface PTituloProtestarBatchTableProps {
  data: PTituloProtestarBatchInterface[];
  isLoading?: boolean;
  selectedIds: Set<number>;
  onToggleOne: (tituloId: number, checked: boolean) => void;
  onToggleAll: (checked: boolean) => void;
  onPrintInstrumentoProtesto: (titulo: PTituloProtestarBatchInterface) => void;
  onPrintCertidaoProtesto: (titulo: PTituloProtestarBatchInterface) => void;
}

function formatMoney(value?: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value ?? 0);
}

function formatDate(value?: Date): string {
  if (!value) return "-";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return "-";
  return parsed.toLocaleDateString("pt-BR");
}

function getStatusProtestoLabel(item: PTituloProtestarBatchInterface): string {
  if (item.data_protesto) return "Já protestado";
  return "Pendente";
}

export function PTituloProtestarBatchTable({
  data,
  isLoading,
  selectedIds,
  onToggleOne,
  onToggleAll,
  onPrintInstrumentoProtesto,
  onPrintCertidaoProtesto,
}: PTituloProtestarBatchTableProps) {
  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center p-8 text-muted-foreground">
        Carregando títulos para protesto...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex w-full items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum título disponível para protesto em lote.
      </div>
    );
  }

  const selectedCountInData = data.filter((item) => selectedIds.has(item.titulo_id)).length;
  const allChecked = selectedCountInData === data.length;
  const indeterminate = selectedCountInData > 0 && selectedCountInData < data.length;

  return (
    <div className="overflow-x-auto rounded-xl border bg-card shadow-sm">
      <Table>
        <TableHeader className="bg-muted/40">
          <TableRow className="hover:bg-transparent">
            <TableHead className="w-[44px] py-3">
              <Checkbox
                checked={allChecked ? true : indeterminate ? "indeterminate" : false}
                onCheckedChange={(checked) => onToggleAll(Boolean(checked))}
                aria-label="Selecionar todos os títulos"
              />
            </TableHead>
            <TableHead className="py-3">Título / Nosso número</TableHead>
            <TableHead className="py-3">Nº Apontamento</TableHead>
            <TableHead className="py-3">Apresentante</TableHead>
            <TableHead className="py-3">Intimação</TableHead>
            <TableHead className="py-3">Valor</TableHead>
            <TableHead className="py-3">Status</TableHead>
            <TableHead className="py-3 text-right">Impressão</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((titulo) => {
            const statusLabel = getStatusProtestoLabel(titulo);
            const isSelected = selectedIds.has(titulo.titulo_id);

            return (
              <TableRow key={titulo.titulo_id} className="transition-colors hover:bg-muted/30">
                <TableCell>
                  <Checkbox
                    checked={isSelected}
                    onCheckedChange={(checked) => onToggleOne(titulo.titulo_id, Boolean(checked))}
                    aria-label={`Selecionar título ${titulo.titulo_id}`}
                  />
                </TableCell>
                <TableCell>
                  <div className="flex min-w-[190px] flex-col">
                    <span className="font-medium">{titulo.numero_titulo ?? `Título ${titulo.titulo_id}`}</span>
                    <span className="text-xs text-muted-foreground">Nosso n. {titulo.nosso_numero ?? "-"}</span>
                  </div>
                </TableCell>
                <TableCell className="whitespace-nowrap font-medium">{titulo.numero_apontamento ?? "-"}</TableCell>
                <TableCell>
                  <div className="flex min-w-[240px] flex-col">
                    <span className="truncate font-medium">{titulo.apresentante ?? "-"}</span>
                    <span className="truncate text-xs text-muted-foreground">{titulo.cpfcnpj ?? "-"}</span>
                  </div>
                </TableCell>
                <TableCell className="whitespace-nowrap">{formatDate(titulo.data_intimacao)}</TableCell>
                <TableCell className="whitespace-nowrap">{formatMoney(titulo.valor_titulo)}</TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={
                      titulo.data_protesto
                        ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                        : "border-amber-200 bg-amber-50 text-amber-700"
                    }
                  >
                    {statusLabel}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex justify-end">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          type="button"
                          variant="outline"
                          size="icon"
                          className="group h-9 w-9 border-border/70 bg-background/80 text-foreground shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:scale-105 hover:border-[#FF6B00]/60 hover:bg-[#FF6B00]/10 hover:text-[#FF6B00] hover:shadow-md disabled:opacity-40 dark:bg-muted/30 dark:hover:bg-[#FF6B00]/20"
                          disabled={!titulo.data_protesto}
                          aria-label="Opções de impressão do protesto"
                          title={titulo.data_protesto ? "Imprimir protesto" : "Protesto ainda não lavrado"}
                        >
                          <Printer className="h-[18px] w-[18px] transition-opacity duration-200 group-hover:opacity-100" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => onPrintInstrumentoProtesto(titulo)}>
                          <FileText className="mr-2 h-4 w-4" />
                          Instrumento de Protesto
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => onPrintCertidaoProtesto(titulo)}>
                          <FileText className="mr-2 h-4 w-4" />
                          Certidão de Protesto
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
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
