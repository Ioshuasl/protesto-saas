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
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";

interface PCertidaoTableProps {
  data: PCertidaoInterface[];
  isLoading?: boolean;
  onCancelarCertidao: (certidao: PCertidaoInterface) => void;
  onEditarCertidao: (certidao: PCertidaoInterface) => void;
  usuarioLabelById?: Map<number, string>;
}

function formatDateTime(dateValue?: Date, timeValue?: string): string {
  if (!dateValue && !timeValue) return "-";

  const date = dateValue ? new Date(dateValue) : null;
  const formattedDate =
    date && !Number.isNaN(date.getTime())
      ? new Intl.DateTimeFormat("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
        }).format(date)
      : "-";

  if (!timeValue) return formattedDate;
  if (formattedDate === "-") return timeValue;
  return `${formattedDate} ${timeValue}`;
}

function formatDateOnly(dateValue?: Date): string {
  if (!dateValue) return "-";
  const date = new Date(dateValue);
  if (Number.isNaN(date.getTime())) return "-";
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
}

function getInitials(name?: string): string {
  if (!name) return "--";
  const parts = name
    .split(" ")
    .map((part) => part.trim())
    .filter(Boolean);
  if (parts.length === 0) return "--";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return `${parts[0][0] ?? ""}${parts[parts.length - 1][0] ?? ""}`.toUpperCase();
}

function formatApresentante(value?: string, cpfcnpj?: string): string {
  if (value && cpfcnpj) return `${value} - ${cpfcnpj}`;
  if (value) return value;
  if (cpfcnpj) return cpfcnpj;
  return "-";
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
  return "-";
}

function getTipoCertidaoLabel(tipo?: PCertidaoInterface["tipo_certidao"] | string): string {
  const normalized = normalizeCode(tipo);
  if (normalized === "P" || normalized.startsWith("POSITIVA")) return "Positiva";
  if (normalized === "N" || normalized.startsWith("NEGATIVA")) return "Negativa";
  return "-";
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
    <div className="overflow-x-auto rounded-xl border bg-card shadow-sm">
      <Table>
        <TableHeader className="bg-muted/40">
          <TableRow className="hover:bg-transparent">
            <TableHead className="py-3">Status</TableHead>
            <TableHead className="py-3">Tipo Certidão</TableHead>
            <TableHead className="py-3">Data/Hora</TableHead>
            <TableHead className="py-3">Apresentante</TableHead>
            <TableHead className="py-3">Usuário</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((certidao) => (
            <TableRow
              key={certidao.certidao_id}
              className="group cursor-pointer transition-colors hover:bg-muted/30"
              onClick={() => onEditarCertidao(certidao)}
            >
              <TableCell>
                <Badge variant="outline" className={getStatusClassName(certidao.status)}>
                  {getStatusLabel(certidao.status)}
                </Badge>
              </TableCell>
              <TableCell>
                <span className="font-medium">{getTipoCertidaoLabel(certidao.tipo_certidao)}</span>
              </TableCell>
              <TableCell className="whitespace-nowrap">
                <div className="inline-flex items-center gap-2 text-sm">
                  <CalendarDays className="h-4 w-4 text-muted-foreground" />
                  <span>{formatDateOnly(certidao.data_certidao)}</span>
                  <span className="text-muted-foreground">{certidao.hora_certidao ?? "--:--"}</span>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex min-w-[240px] items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full border bg-muted/40 text-[11px] font-semibold">
                    {getInitials(certidao.apresentante)}
                  </div>
                  <div className="flex min-w-0 flex-col">
                    <span className="truncate font-medium">{certidao.apresentante ?? "-"}</span>
                    <span className="truncate text-xs text-muted-foreground">{certidao.cpfcnpj ?? "-"}</span>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <div className="inline-flex items-center gap-2">
                  <UserRound className="h-4 w-4 text-muted-foreground" />
                  <span>
                    {certidao.usuario_id ? usuarioLabelById?.get(certidao.usuario_id) || String(certidao.usuario_id) : "-"}
                  </span>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex justify-end gap-2">
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
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
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
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
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
