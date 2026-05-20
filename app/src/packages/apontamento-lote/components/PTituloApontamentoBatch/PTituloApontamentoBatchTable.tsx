"use client";

import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { PTituloApontamentoBatchInterface } from "@/packages/apontamento-lote/interface/PTituloApontamentoBatch/PTituloApontamentoBatchInterface";

interface PTituloApontamentoBatchTableProps {
  data: PTituloApontamentoBatchInterface[];
  isLoading?: boolean;
  selectedIds: Set<number>;
  onToggleOne: (tituloId: number, checked: boolean) => void;
  onToggleAll: (checked: boolean) => void;
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

function getStatusApontamentoLabel(item: PTituloApontamentoBatchInterface): string {
  if (item.data_apontamento) return "Já apontado";
  return "Pendente";
}

export function PTituloApontamentoBatchTable({
  data,
  isLoading,
  selectedIds,
  onToggleOne,
  onToggleAll,
}: PTituloApontamentoBatchTableProps) {
  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center p-8 text-muted-foreground">
        Carregando títulos para apontamento...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex w-full items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum título disponível para apontamento em lote.
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
            <TableHead className="py-3">Apresentante</TableHead>
            <TableHead className="py-3">Valor</TableHead>
            <TableHead className="py-3">Cadastro</TableHead>
            <TableHead className="py-3">Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((titulo) => {
            const statusLabel = getStatusApontamentoLabel(titulo);
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
                <TableCell>
                  <div className="flex min-w-[240px] flex-col">
                    <span className="truncate font-medium">{titulo.apresentante ?? "-"}</span>
                    <span className="truncate text-xs text-muted-foreground">{titulo.cpfcnpj ?? "-"}</span>
                  </div>
                </TableCell>
                <TableCell className="whitespace-nowrap">{formatMoney(titulo.valor_titulo)}</TableCell>
                <TableCell className="whitespace-nowrap">{formatDate(titulo.data_cadastro)}</TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={
                      titulo.data_apontamento
                        ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                        : "border-amber-200 bg-amber-50 text-amber-700"
                    }
                  >
                    {statusLabel}
                  </Badge>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
