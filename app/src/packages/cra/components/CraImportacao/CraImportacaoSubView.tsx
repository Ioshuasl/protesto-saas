"use client";

import type { CraRemessaTransacao } from "@/packages/cra/functions/CraImportacao";

interface CraImportacaoSubViewProps {
  transacao: CraRemessaTransacao;
  index: number;
  onClick?: () => void;
}

function formatCurrency(cents: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(cents / 100);
}

function formatDate(value: string): string {
  if (!value) return "-";
  const [year, month, day] = value.split("-");
  if (!year || !month || !day) return value;
  return `${day}/${month}/${year}`;
}

export function CraImportacaoSubView({ transacao, index, onClick }: CraImportacaoSubViewProps) {
  return (
    <article
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onClick?.();
        }
      }}
      className="rounded-lg border bg-card p-4 transition-colors hover:bg-muted/20"
    >
      <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0 space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex rounded-full bg-[#FF6B00]/10 px-2 py-0.5 text-xs font-semibold text-[#FF6B00]">
              Titulo #{index + 1}
            </span>
            <span className="text-xs text-muted-foreground">Nosso numero: {transacao.nossoNumero || "-"}</span>
          </div>
          <div className="space-y-1">
            <p className="truncate text-sm font-semibold text-foreground">{transacao.nomeDevedor || "-"}</p>
            <p className="truncate text-xs text-muted-foreground">
              Cedente: <span className="font-medium text-foreground">{transacao.nomeCedente || "-"}</span>
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-x-5 gap-y-2 text-sm lg:min-w-[360px]">
          <div>
            <p className="text-xs text-muted-foreground">Numero do titulo</p>
            <p className="font-medium">{transacao.numeroTitulo || "-"}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Especie</p>
            <p className="font-medium">{transacao.especie || "-"}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Vencimento</p>
            <p className="font-medium">{formatDate(transacao.dataVencimento)}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">Saldo para protesto</p>
            <p className="font-medium">{formatCurrency(transacao.saldoTituloCentavos)}</p>
          </div>
        </div>
      </div>
    </article>
  );
}
