"use client";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { GEmolumentoListInterface } from "@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import FormatMoney from "@/shared/actions/money/FormatMoney";
import { formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";

interface GEmolumentoTableProps {
  data: GEmolumentoListInterface[];
  isLoading?: boolean;
  onViewDetails?: (item: GEmolumentoListInterface) => void;
}

const COLUMN_CLASSES = {
  grupoSelo: "min-w-0",
  codigoSelo: "w-[140px]",
  agrupador: "w-[120px]",
  valorEmolumento: "w-[160px]",
  taxaJudiciaria: "w-[170px]",
} as const;

function getNestedString(record: Record<string, unknown> | null | undefined, key: string): string {
  const value = record?.[key];
  return typeof value === "string" ? value : "";
}

function getNestedNumber(record: Record<string, unknown> | null | undefined, key: string): number | null {
  const value = record?.[key];
  if (typeof value === "number") return value;
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  }
  return null;
}

export function GEmolumentoTable({ data, isLoading, onViewDetails }: GEmolumentoTableProps) {
  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center p-8 text-muted-foreground">
        Carregando emolumentos...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex w-full items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum emolumento encontrado para os filtros informados.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border">
      <Table className="table-fixed w-full">
        <TableHeader>
          <TableRow>
            <TableHead className={`${COLUMN_CLASSES.grupoSelo} max-w-0`}>Grupo de selo</TableHead>
            <TableHead className={COLUMN_CLASSES.codigoSelo}>Código selo</TableHead>
            <TableHead className={COLUMN_CLASSES.agrupador}>Agrupador</TableHead>
            <TableHead className={`${COLUMN_CLASSES.valorEmolumento} text-right`}>Valor emolumento</TableHead>
            <TableHead className={`${COLUMN_CLASSES.taxaJudiciaria} text-right`}>Taxa judiciária</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item, index) => {
            const seloGrupo = item.selo_grupo as Record<string, unknown> | null | undefined;
            const descricaoGrupoSelo = formatEmptyFieldTrimmed(getNestedString(seloGrupo, "descricao"));
            const agrupador = formatEmptyFieldTrimmed(getNestedString(seloGrupo, "grupos_principal"));
            const numeroSelo = getNestedNumber(seloGrupo, "numero");
            const rowKey =
              item.emolumento_item_id != null
                ? `emolumento-item-${item.emolumento_item_id}-${index}`
                : `emolumento-item-fallback-${index}`;

            return (
              <TableRow
                key={rowKey}
                className={onViewDetails ? "cursor-pointer" : undefined}
                onClick={() => onViewDetails?.(item)}
              >
                <TableCell className={`${COLUMN_CLASSES.grupoSelo} max-w-0 overflow-hidden`}>
                  <span className="block truncate" title={descricaoGrupoSelo}>
                    {descricaoGrupoSelo}
                  </span>
                </TableCell>
                <TableCell className={COLUMN_CLASSES.codigoSelo}>{numeroSelo ?? EMPTY_FIELD_LABEL}</TableCell>
                <TableCell
                  className={`${COLUMN_CLASSES.agrupador} overflow-hidden truncate`}
                  title={agrupador}
                >
                  {agrupador}
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.valorEmolumento} text-right`}>
                  {FormatMoney(item.valor_emolumento)}
                </TableCell>
                <TableCell className={`${COLUMN_CLASSES.taxaJudiciaria} text-right`}>
                  {FormatMoney(item.valor_taxa_judiciaria)}
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
