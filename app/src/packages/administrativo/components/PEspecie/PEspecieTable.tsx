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
import { PEspecieInterface } from "@/packages/administrativo/interfaces";
import { cn } from "@/lib/utils";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyField, formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";

interface PEspecieTableProps {
  data: PEspecieInterface[];
  onEdit: (especie: PEspecieInterface) => void;
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

function TruncatedDescription({ text }: { text?: string | null }) {
  const ref = useRef<HTMLSpanElement>(null);
  const label = formatEmptyFieldTrimmed(text);
  const isTruncated = useIsTextTruncated(ref, label);

  if (label === EMPTY_FIELD_LABEL) {
    return <span className="text-muted-foreground">{EMPTY_FIELD_LABEL}</span>;
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

export function PEspecieTable({ data, onEdit, onDelete, isLoading }: PEspecieTableProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground">
        Carregando espécies...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center p-8 text-muted-foreground border rounded-md">
        Nenhuma espécie encontrada.
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 rounded-md border">
      <Table className="table-fixed w-full">
        <TableHeader>
          <TableRow>
            <TableHead className="w-[88px]">Sigla</TableHead>
            <TableHead className="min-w-0">Descrição</TableHead>
            <TableHead className="w-[96px] text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((especie) => (
            <TableRow
              key={especie.especie_id}
              className="cursor-pointer"
              onClick={() => onEdit(especie)}
            >
              <TableCell className="w-[88px] truncate">{formatEmptyField(especie.especie)}</TableCell>
              <TableCell className="max-w-0 min-w-0 overflow-visible">
                <TruncatedDescription text={especie.descricao} />
              </TableCell>
              <TableCell className="w-[96px] text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEdit(especie);
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
                      onDelete(especie.especie_id);
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
