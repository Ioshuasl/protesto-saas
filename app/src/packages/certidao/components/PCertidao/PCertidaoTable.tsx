"use client";

import { CalendarDays, Pencil, UserRound, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import { formatEmptyField, formatEmptyFieldDate, formatEmptyFieldTrimmed } from "@/shared/utils/emptyField";

interface PCertidaoTableProps {
  data: PCertidaoInterface[];
  isLoading?: boolean;
  onCancelarCertidao: (certidao: PCertidaoInterface) => void;
  onEditarCertidao: (certidao: PCertidaoInterface) => void;
  usuarioLabelById?: Map<number, string>;
}

function formatDateOnly(dateValue?: Date | string): string {
  return formatEmptyFieldDate(dateValue, (date) =>
    new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }).format(date),
  );
}

function normalizeCode(value?: string): string {
  return (value ?? "").trim().toUpperCase();
}

function getStatusClassName(status?: PCertidaoInterface["status"] | string): string {
  const normalized = normalizeCode(status);
  if (normalized === "A" || normalized === "ATIVA" || normalized === "ATIVO" || normalized === "EMITIDA") {
    return "border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100";
  }
  if (normalized === "C" || normalized === "CANCELADA" || normalized === "INATIVA") {
    return "border-rose-200 bg-rose-50 text-rose-700 hover:bg-rose-100";
  }
  return "border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100";
}

function getStatusLabel(status?: PCertidaoInterface["status"] | string): string {
  const normalized = normalizeCode(status);
  if (normalized === "A" || normalized === "ATIVA" || normalized === "ATIVO" || normalized === "EMITIDA") {
    return "Ativa/Emitida";
  }
  if (normalized === "C" || normalized === "CANCELADA" || normalized === "INATIVA") {
    return "Cancelada";
  }
  return EMPTY_FIELD_LABEL;
}

function isCertidaoCancelada(status?: PCertidaoInterface["status"] | string): boolean {
  const normalized = normalizeCode(status);
  return normalized === "C" || normalized === "CANCELADA" || normalized === "INATIVA";
}

function getTipoCertidaoLabel(tipo?: PCertidaoInterface["tipo_certidao"] | string): string {
  const normalized = normalizeCode(tipo);
  if (normalized === "R" || normalized.includes("SERASA")) return "Serasa";
  if (normalized === "P" || normalized.startsWith("POSITIVA")) return "Positiva";
  if (normalized === "N" || normalized.startsWith("NEGATIVA")) return "Negativa";
  return EMPTY_FIELD_LABEL;
}

function getUsuarioLabel(
  certidao: PCertidaoInterface,
  usuarioLabelById?: Map<number, string>,
): string {
  if (certidao.usuario_nome?.trim()) {
    return certidao.usuario_nome;
  }
  if (certidao.usuario_id) {
    return usuarioLabelById?.get(certidao.usuario_id) ?? String(certidao.usuario_id);
  }
  return EMPTY_FIELD_LABEL;
}

function ApresentanteCell({ certidao }: { certidao: PCertidaoInterface }) {
  const apresentante = formatEmptyField(certidao.apresentante);
  const documento = formatEmptyField(certidao.cpfcnpj);

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <div className="flex min-w-0 max-w-full cursor-help flex-col">
          <span className="block max-w-full truncate font-medium">{apresentante}</span>
          <span className="block max-w-full truncate text-xs text-muted-foreground">{documento}</span>
        </div>
      </TooltipTrigger>
      <TooltipContent className="max-w-xs bg-popover text-popover-foreground shadow-md" side="top" sideOffset={6}>
        <div className="space-y-0.5">
          <p className="font-medium">{apresentante}</p>
          <p className="text-muted-foreground">{documento}</p>
        </div>
      </TooltipContent>
    </Tooltip>
  );
}

export function PCertidaoTable({
  data,
  isLoading,
  onCancelarCertidao,
  onEditarCertidao,
  usuarioLabelById,
}: PCertidaoTableProps) {
  if (isLoading) {
    return (
      <div className="flex w-full items-center justify-center p-8 text-muted-foreground">
        Carregando certidões...
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="flex w-full items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhuma certidão encontrada.
      </div>
    );
  }

  return (
    <div className="min-w-0 overflow-x-auto rounded-xl border bg-card shadow-sm">
      <Table className="min-w-[780px] table-fixed">
        <TableHeader className="bg-muted/40">
          <TableRow className="hover:bg-transparent">
            <TableHead className="w-[96px] py-2.5 text-xs">Status</TableHead>
            <TableHead className="w-[82px] py-2.5 text-xs">Tipo</TableHead>
            <TableHead className="w-[140px] py-2.5 text-xs">Data/Hora</TableHead>
            <TableHead className="w-[230px] py-2.5 text-xs">Apresentante</TableHead>
            <TableHead className="w-[160px] py-2.5 text-xs">Usuário</TableHead>
            <TableHead className="w-[72px] py-2.5 text-right text-xs">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((certidao) => (
            <TableRow
              key={certidao.certidao_id}
              className="group cursor-pointer transition-colors hover:bg-muted/30"
              onClick={() => onEditarCertidao(certidao)}
            >
              <TableCell className="py-2">
                <Badge variant="outline" className={getStatusClassName(certidao.status)}>
                  {getStatusLabel(certidao.status)}
                </Badge>
              </TableCell>
              <TableCell className="py-2">
                <span className="font-medium">{getTipoCertidaoLabel(certidao.tipo_certidao)}</span>
              </TableCell>
              <TableCell className="py-2 whitespace-nowrap">
                <div className="inline-flex items-center gap-1.5 text-xs xl:text-sm">
                  <CalendarDays className="h-4 w-4 text-muted-foreground" />
                  <span>{formatDateOnly(certidao.data_certidao)}</span>
                  <span className="text-muted-foreground">{formatEmptyFieldTrimmed(certidao.hora_certidao)}</span>
                </div>
              </TableCell>
              <TableCell className="w-[230px] max-w-[230px] min-w-0 py-2">
                <ApresentanteCell certidao={certidao} />
              </TableCell>
              <TableCell className="min-w-0 py-2">
                <div className="inline-flex max-w-full min-w-0 items-center gap-2">
                  <UserRound className="h-4 w-4 text-muted-foreground" />
                  <span className="truncate">{formatEmptyField(getUsuarioLabel(certidao, usuarioLabelById))}</span>
                </div>
              </TableCell>
              <TableCell className="py-2">
                <div className="flex justify-end gap-2">
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon-sm"
                    className="transition-colors hover:bg-orange-50 hover:text-orange-600"
                    onClick={(event) => {
                      event.stopPropagation();
                      onEditarCertidao(certidao);
                    }}
                    aria-label="Editar certidão"
                    title="Editar certidão"
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  {!isCertidaoCancelada(certidao.status) ? (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon-sm"
                      className="transition-transform hover:-translate-y-0.5 hover:bg-rose-50"
                      onClick={(event) => {
                        event.stopPropagation();
                        onCancelarCertidao(certidao);
                      }}
                      aria-label="Cancelar certidão"
                      title="Cancelar certidão"
                    >
                      <X className="h-4 w-4 text-rose-600" />
                    </Button>
                  ) : null}
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
