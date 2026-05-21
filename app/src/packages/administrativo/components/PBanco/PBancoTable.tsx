"use client";

import { useLayoutEffect, useRef, useState, type RefObject } from "react";
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
import { PBancoInterface, PBancoSimNao } from "@/packages/administrativo/interfaces";
import { cn } from "@/lib/utils";

function formatApontamentoPagPosterior(
  value: PBancoInterface["apontamento_pag_posterior"],
): string {
  if (value === PBancoSimNao.Sim) return "Sim";
  if (value === PBancoSimNao.Nao) return "Não";
  return "—";
}

interface PBancoTableProps {
  data: PBancoInterface[];
  onEdit: (banco: PBancoInterface) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

function useIsTextTruncated(ref: RefObject<HTMLSpanElement | null>, text: string) {
  const [isTruncated, setIsTruncated] = useState(false);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;

    const measure = () => {
      setIsTruncated(el.scrollWidth > el.clientWidth);
    };

    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(el);
    return () => observer.disconnect();
  }, [text]);

  return isTruncated;
}

function TruncatedTableText({ text }: { text?: string | null }) {
  const ref = useRef<HTMLSpanElement>(null);
  const label = text?.trim() || "—";
  const isTruncated = useIsTextTruncated(ref, label);

  if (label === "—") {
    return <span className="text-muted-foreground">—</span>;
  }

  return (
    <span className="group/desc relative block min-w-0 max-w-full">
      <span ref={ref} className="block truncate text-left">
        {label}
      </span>
      {isTruncated ? (
        <span
          role="tooltip"
          className={cn(
            "pointer-events-none absolute bottom-full left-0 z-50 mb-1.5 max-w-md rounded-md border bg-popover px-3 py-2 text-left text-sm font-normal whitespace-normal break-words text-popover-foreground shadow-md",
            "invisible translate-y-1 opacity-0 transition-all duration-200 ease-out",
            "group-hover/desc:visible group-hover/desc:translate-y-0 group-hover/desc:opacity-100",
          )}
        >
          {label}
        </span>
      ) : null}
    </span>
  );
}

export function PBancoTable({ data, onEdit, onDelete, isLoading }: PBancoTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando bancos...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhum banco encontrado.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border">
      <Table className="table-fixed w-full">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[88px]">Código</TableHead>
            <TableHead className="min-w-0">Descrição</TableHead>
            <TableHead className="w-[200px] min-w-[200px] max-w-[200px]">
              <TruncatedTableText text="Apontar como pag. posterior" />
            </TableHead>
            <TableHead className="w-[96px] text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((banco) => (
            <TableRow
              key={banco.banco_id}
              className="cursor-pointer"
              onClick={() => onEdit(banco)}
            >
              <TableCell className="w-[88px] truncate">{banco.codigo_banco ?? "—"}</TableCell>
              <TableCell className="max-w-0 min-w-0 overflow-visible">
                <TruncatedTableText text={banco.descricao} />
              </TableCell>
              <TableCell className="w-[200px] min-w-[200px] max-w-[200px] whitespace-nowrap">
                {formatApontamentoPagPosterior(banco.apontamento_pag_posterior)}
              </TableCell>
              <TableCell className="w-[96px] text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(banco);
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
                      onDelete(banco.banco_id);
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
