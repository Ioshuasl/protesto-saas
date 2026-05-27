"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { GEmolumentoListInterface } from "@/packages/administrativo/interfaces/GEmolumentoList/GEmolumentoListInterface";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import FormatMoney from "@/shared/actions/money/FormatMoney";

interface GEmolumentoDetailDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  item: GEmolumentoListInterface | null;
}

function toDisplayValue(value: unknown): string {
  if (value === null || value === undefined) return EMPTY_FIELD_LABEL;
  if (typeof value === "number") return String(value);
  if (typeof value === "boolean") return value ? "Sim" : "Não";
  const text = String(value).trim();
  return text ? text : EMPTY_FIELD_LABEL;
}

function toMoneyValue(value: unknown): string {
  if (value === null || value === undefined) return FormatMoney(0);
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return FormatMoney(0);
  return FormatMoney(numeric);
}

function FieldRow({
  label,
  value,
  isMoney,
}: {
  label: string;
  value: unknown;
  isMoney?: boolean;
}) {
  return (
    <div className="grid grid-cols-1 gap-1 border-b py-2 text-sm md:grid-cols-[260px_1fr] md:gap-3">
      <span className="font-medium text-muted-foreground">{label}</span>
      <span className="break-words">{isMoney ? toMoneyValue(value) : toDisplayValue(value)}</span>
    </div>
  );
}

function Section({
  title,
  rows,
}: {
  title: string;
  rows: Array<{ label: string; value: unknown; isMoney?: boolean }>;
}) {
  return (
    <section className="rounded-md border p-4">
      <h3 className="mb-2 text-base font-semibold">{title}</h3>
      <div className="space-y-0">
        {rows.map((row) => (
          <FieldRow key={row.label} label={row.label} value={row.value} isMoney={row.isMoney} />
        ))}
      </div>
    </section>
  );
}

export function GEmolumentoDetailDialog({
  open,
  onOpenChange,
  item,
}: GEmolumentoDetailDialogProps) {
  const seloGrupo = (item?.selo_grupo ?? null) as Record<string, unknown> | null;
  const emolumento = (item?.emolumento ?? null) as Record<string, unknown> | null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] w-[95vw] overflow-y-auto sm:max-w-[1200px]">
        <DialogHeader>
          <DialogTitle>Detalhes completos do emolumento e selo</DialogTitle>
        </DialogHeader>

        {!item ? (
          <div className="py-6 text-sm text-muted-foreground">Nenhum item selecionado.</div>
        ) : (
          <div className="flex flex-col gap-4">
            <Section
              title="Item de emolumento"
              rows={[
                { label: "Emolumento item ID", value: item.emolumento_item_id },
                { label: "Emolumento ID", value: item.emolumento_id },
                { label: "Período ID", value: item.emolumento_periodo_id },
                { label: "Selo grupo ID", value: item.selo_grupo_id },
                { label: "Código", value: item.codigo },
                { label: "Código selo", value: item.codigo_selo },
                { label: "Código tabela", value: item.codigo_tabela },
                { label: "Código KM", value: item.codigo_km },
                { label: "Página extra", value: item.pagina_extra },
                { label: "VRCEXT", value: item.vrcext },
              ]}
            />

            <Section
              title="Valores detalhados"
              rows={[
                { label: "Valor início", value: item.valor_inicio, isMoney: true },
                { label: "Valor fim", value: item.valor_fim, isMoney: true },
                { label: "Valor emolumento", value: item.valor_emolumento, isMoney: true },
                { label: "Valor taxa judiciária", value: item.valor_taxa_judiciaria, isMoney: true },
                { label: "Valor fundo RI", value: item.valor_fundo_ri, isMoney: true },
                { label: "Valor página extra", value: item.valor_pagina_extra, isMoney: true },
                { label: "Valor outra taxa 1", value: item.valor_outra_taxa1, isMoney: true },
                { label: "Emolumento acresce", value: item.emolumento_acresce, isMoney: true },
                { label: "Taxa acresce", value: item.taxa_acresce, isMoney: true },
                { label: "Funcivil acresce", value: item.funcivil_acresce, isMoney: true },
                { label: "Valor fração", value: item.valor_fracao, isMoney: true },
                {
                  label: "Valor por excedente emolumento",
                  value: item.valor_por_excedente_emol,
                  isMoney: true,
                },
                {
                  label: "Valor por excedente taxa judiciária",
                  value: item.valor_por_excedente_tj,
                  isMoney: true,
                },
                {
                  label: "Valor por excedente fundo",
                  value: item.valor_por_excedente_fundo,
                  isMoney: true,
                },
                {
                  label: "Valor limite excedente emolumento",
                  value: item.valor_limite_excedente_emol,
                  isMoney: true,
                },
                {
                  label: "Valor limite excedente taxa judiciária",
                  value: item.valor_limite_excedente_tj,
                  isMoney: true,
                },
                {
                  label: "Valor limite excedente fundo",
                  value: item.valor_limite_excedente_fundo,
                  isMoney: true,
                },
                { label: "Fundo selo", value: item.fundo_selo, isMoney: true },
                { label: "Distribuição", value: item.distribuicao, isMoney: true },
              ]}
            />

            <Section
              title="Include: emolumento"
              rows={[
                { label: "Emolumento ID", value: emolumento?.emolumento_id },
                { label: "Descrição", value: emolumento?.descricao },
                { label: "Tipo", value: emolumento?.tipo },
                { label: "Situação", value: emolumento?.situacao },
                { label: "Situação RI", value: emolumento?.situacao_ri },
                { label: "Sistema ID", value: emolumento?.sistema_id },
                { label: "Selo grupo ID", value: emolumento?.selo_grupo_id },
                { label: "Tipo objetivo", value: emolumento?.tipo_objetivo },
                { label: "Modelo tag", value: emolumento?.modelo_tag },
                { label: "Pré-definido", value: emolumento?.pre_definido },
                { label: "Com redução", value: emolumento?.com_reducao },
                { label: "Motivo redução", value: emolumento?.motivo_reducao },
                {
                  label: "Valor máximo certidão",
                  value: emolumento?.valor_maximo_certidao,
                  isMoney: true,
                },
              ]}
            />

            <Section
              title="Include: grupo de selo"
              rows={[
                { label: "Selo grupo ID", value: seloGrupo?.selo_grupo_id },
                { label: "Número", value: seloGrupo?.numero },
                { label: "Descrição", value: seloGrupo?.descricao },
                { label: "Descrição completa", value: seloGrupo?.descricao_completa },
                { label: "Tipo selo", value: seloGrupo?.tipo_selo },
                { label: "Sigla", value: seloGrupo?.sigla },
                { label: "Situação", value: seloGrupo?.situacao },
                { label: "Agrupador", value: seloGrupo?.agrupador },
                { label: "Um por protocolo", value: seloGrupo?.um_por_protocolo },
                { label: "Sistema ID", value: seloGrupo?.sistema_id },
                { label: "Tipo cartório", value: seloGrupo?.tipo_cartorio },
                { label: "Natureza", value: seloGrupo?.natureza },
                { label: "Valor", value: seloGrupo?.valor, isMoney: true },
                { label: "Envio automático", value: seloGrupo?.envio_automatico },
                { label: "Selo grupo ID principal", value: seloGrupo?.selo_grupo_id_principal },
                {
                  label: "Selo grupo ID agrupador",
                  value: seloGrupo?.selo_grupo_id_agrupador,
                },
                { label: "Grupos principal", value: seloGrupo?.grupos_principal },
                { label: "Número principal inicial", value: seloGrupo?.numero_principal_ini },
                { label: "Número principal final", value: seloGrupo?.numero_principal_fim },
                { label: "Código conta", value: seloGrupo?.codigo_conta },
                { label: "ID tipo ato antigo", value: seloGrupo?.id_tipo_ato_antigo },
              ]}
            />
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
