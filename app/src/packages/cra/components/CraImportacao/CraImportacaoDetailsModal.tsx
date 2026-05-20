"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { CraRemessaTransacao } from "@/packages/cra/functions/CraImportacao";

interface CraImportacaoDetailsModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  transacao: CraRemessaTransacao | null;
  index?: number;
}

function formatDate(value?: string): string {
  if (!value) return "-";
  const [year, month, day] = value.split("-");
  if (!year || !month || !day) return value;
  return `${day}/${month}/${year}`;
}

function formatCurrency(cents?: number): string {
  if (!cents && cents !== 0) return "-";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(cents / 100);
}

export function CraImportacaoDetailsModal({
  open,
  onOpenChange,
  transacao,
  index,
}: CraImportacaoDetailsModalProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[85vh] overflow-y-auto sm:max-w-3xl">
        <DialogHeader>
          <DialogTitle>Detalhes do título {index !== undefined ? `#${index + 1}` : ""}</DialogTitle>
          <DialogDescription>Visualização completa dos dados da transação importada no arquivo CRA.</DialogDescription>
        </DialogHeader>

        {transacao ? (
          <div className="space-y-4">
            <section className="space-y-2 rounded-lg border p-3">
              <h3 className="text-sm font-semibold">Identificação</h3>
              <div className="grid gap-2 text-sm md:grid-cols-2">
                <p><span className="text-muted-foreground">Nosso número:</span> {transacao.nossoNumero || "-"}</p>
                <p><span className="text-muted-foreground">Número do título:</span> {transacao.numeroTitulo || "-"}</p>
                <p><span className="text-muted-foreground">Espécie:</span> {transacao.especie || "-"}</p>
                <p><span className="text-muted-foreground">Linha:</span> {transacao.linha}</p>
              </div>
            </section>

            <section className="space-y-2 rounded-lg border p-3">
              <h3 className="text-sm font-semibold">Cedente / Sacador</h3>
              <div className="grid gap-2 text-sm md:grid-cols-2">
                <p><span className="text-muted-foreground">Agência/Cód. Cedente:</span> {transacao.agenciaCodigoCedente || "-"}</p>
                <p><span className="text-muted-foreground">Nome Cedente:</span> {transacao.nomeCedente || "-"}</p>
                <p><span className="text-muted-foreground">Nome Sacador:</span> {transacao.nomeSacador || "-"}</p>
                <p><span className="text-muted-foreground">Documento Sacador:</span> {transacao.documentoSacador || "-"}</p>
                <p><span className="text-muted-foreground">Endereço Sacador:</span> {transacao.enderecoSacador || "-"}</p>
                <p><span className="text-muted-foreground">CEP/Cidade/UF Sacador:</span> {transacao.cepSacador || "-"} - {transacao.cidadeSacador || "-"} / {transacao.ufSacador || "-"}</p>
              </div>
            </section>

            <section className="space-y-2 rounded-lg border p-3">
              <h3 className="text-sm font-semibold">Financeiro</h3>
              <div className="grid gap-2 text-sm md:grid-cols-2">
                <p><span className="text-muted-foreground">Data emissão:</span> {formatDate(transacao.dataEmissao)}</p>
                <p><span className="text-muted-foreground">Data vencimento:</span> {formatDate(transacao.dataVencimento)}</p>
                <p><span className="text-muted-foreground">Moeda:</span> {transacao.codigoMoeda || "-"}</p>
                <p><span className="text-muted-foreground">Valor título:</span> {formatCurrency(transacao.valorTituloCentavos)}</p>
                <p><span className="text-muted-foreground">Saldo título:</span> {formatCurrency(transacao.saldoTituloCentavos)}</p>
                <p><span className="text-muted-foreground">Praça protesto:</span> {transacao.pracaProtesto || "-"}</p>
                <p><span className="text-muted-foreground">Tipo endosso:</span> {transacao.tipoEndosso || "-"}</p>
                <p><span className="text-muted-foreground">Tipo aceite:</span> {transacao.tipoAceite || "-"}</p>
              </div>
            </section>

            <section className="space-y-2 rounded-lg border p-3">
              <h3 className="text-sm font-semibold">Devedor</h3>
              <div className="grid gap-2 text-sm md:grid-cols-2">
                <p><span className="text-muted-foreground">Controle:</span> {transacao.controleDevedor || "-"}</p>
                <p><span className="text-muted-foreground">Nome Devedor:</span> {transacao.nomeDevedor || "-"}</p>
                <p><span className="text-muted-foreground">Tipo pessoa:</span> {transacao.tipoPessoaDevedor || "-"}</p>
                <p><span className="text-muted-foreground">Documento:</span> {transacao.documentoDevedor || "-"}</p>
                <p><span className="text-muted-foreground">Endereço:</span> {transacao.enderecoDevedor || "-"}</p>
                <p><span className="text-muted-foreground">CEP/Cidade/UF:</span> {transacao.cepDevedor || "-"} - {transacao.cidadeDevedor || "-"} / {transacao.ufDevedor || "-"}</p>
              </div>
            </section>

            <section className="space-y-2 rounded-lg border p-3">
              <h3 className="text-sm font-semibold">Campos de cartório / controle</h3>
              <div className="grid gap-2 text-sm md:grid-cols-2">
                <p><span className="text-muted-foreground">Código cartório:</span> {transacao.codigoCartorio || "-"}</p>
                <p><span className="text-muted-foreground">Protocolo:</span> {transacao.protocolo || "-"}</p>
                <p><span className="text-muted-foreground">Ocorrência:</span> {transacao.ocorrencia || "-"}</p>
                <p><span className="text-muted-foreground">Data protocolo:</span> {formatDate(transacao.dataProtocolo)}</p>
                <p><span className="text-muted-foreground">Custas:</span> {formatCurrency(transacao.custasCentavos)}</p>
                <p><span className="text-muted-foreground">Declaração:</span> {transacao.declaracao || "-"}</p>
                <p><span className="text-muted-foreground">Sequência registro:</span> {transacao.sequenciaRegistro || "-"}</p>
                <p><span className="text-muted-foreground">Código portador:</span> {transacao.codigoPortador || "-"}</p>
              </div>
            </section>
          </div>
        ) : null}
      </DialogContent>
    </Dialog>
  );
}
