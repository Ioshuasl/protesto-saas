"use client";

import { useMemo, useState } from "react";
import {
  useFieldArray,
  useFormContext,
  type UseFieldArrayUpdate,
  type UseFormGetValues,
} from "react-hook-form";
import { AlertCircle, HelpCircle, Pencil, Plus, Trash2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import type { PessoaFormValues } from "@/packages/administrativo/components/PPessoa/PPessoaForm";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces";
import { PPessoaVinculoTipoSelectObject } from "@/packages/administrativo/components/PPessoaVinculo/PPessoaVinculoTipoSelectObject";
import {
  PPessoaVinculoTipoEnum,
  formatPPessoaVinculoTipoLabel,
  normalizePPessoaVinculoTipo,
  type PPessoaVinculoTipo,
} from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum";
import { PessoaService } from "@/packages/administrativo/services/PPessoa/PPessoaService";
import type { PTituloDetailsFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { EMPTY_FIELD_LABEL } from "@/shared/const";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";
import { formatCpfCnpj } from "@/shared/utils/document";
import { formatEmptyField, isEmptyFieldValue } from "@/shared/utils/emptyField";
import { PTituloParteDialog } from "../PTituloParteDialog";
import { buildPTituloParteItem, type PTituloParteItem } from "../PTituloParteTypes";

const TIPO_VINCULO_INFO_MARKDOWN = `### 📄 Apresentante

É a pessoa (ou empresa/banco) que "apresenta", ou seja, que leva o título ou documento de dívida ao cartório para ser protestado. O papel dele envolve algumas responsabilidades importantes:

* É ele quem fornece os dados da dívida ao cartório, assumindo total responsabilidade pelo que está informando.
* Ele tem o dever de indicar a perfeita identificação do devedor e o seu endereço correto.
* Quando o envio do título é feito eletronicamente, o apresentante é quem declara que a dívida existe e guarda consigo o documento original (ou cópia autenticada) para provar a cobrança caso seja questionado na Justiça.
* É também o apresentante quem pode pedir a desistência do protesto e retirar o documento antes que o ato seja concluído (desde que pague as taxas).

### ✍️ Cedente / Sacador

* **Sacador:** Segundo o documento, o sacador é quem lança ou emite a cobrança originada de um negócio, como no caso de ser o responsável pela emissão de uma duplicata.
* **Cedente:** Para ser totalmente transparente e honesto com você sobre minha natureza como inteligência artificial que está seguindo estritamente a fonte fornecida, **o termo "Cedente" não é mencionado ou definido nas regras do documento enviado**. Na prática comercial do dia a dia (fora deste documento), o cedente costuma ser quem "cede" ou transfere o direito de receber essa dívida para um banco, mas essa definição não consta no Código de Normas que analisamos.

### 💰 Credor

É o dono do dinheiro, ou seja, o titular do direito de receber o valor daquela dívida.

* O Código menciona o credor como aquele que, ao lado do apresentante, indica quem é a pessoa responsável por cumprir a obrigação de pagar a dívida.
* Quando a dívida é paga diretamente no cartório, é para o credor (ou para o apresentante) que o cartório fará a entrega ou o repasse do pagamento.
*(Nota: Muitas vezes, o Credor e o Apresentante são a mesma pessoa, mas às vezes o credor usa um banco ou escritório como "apresentante" para levar o título ao cartório).*

### 👤 Devedor

É a pessoa física ou jurídica que não pagou a dívida no prazo e está sendo cobrada.

* O cartório tem o papel de intimar o devedor para que ele pague, devolva, aceite a cobrança ou justifique o não pagamento, sob pena de ter seu nome "sujo" (protestado).
* O Código define o devedor de forma ampla: pode ser quem emitiu uma nota promissória ou um cheque, quem é o "sacado" (cobrado) em uma letra de câmbio ou duplicata, ou simplesmente qualquer pessoa que o credor/apresentante tenha apontado como responsável por aquela obrigação.
* É obrigatório que o nome do devedor conste no documento oficial de registro do protesto.
`;

const TIPO_VINCULO_ORDER: Record<PPessoaVinculoTipo, number> = {
  [PPessoaVinculoTipoEnum.APRESENTANTE]: 0,
  [PPessoaVinculoTipoEnum.CEDENTE]: 1,
  [PPessoaVinculoTipoEnum.CREDOR]: 2,
  [PPessoaVinculoTipoEnum.DEVEDOR]: 3,
};

function getTipoVinculoOrder(tipo?: string | null): number {
  const normalizedTipo = normalizePPessoaVinculoTipo(tipo) ?? PPessoaVinculoTipoEnum.DEVEDOR;
  return TIPO_VINCULO_ORDER[normalizedTipo];
}

type PTituloParteRow = {
  id: string;
  fieldIndex: number;
  tipo?: string;
  nome?: string;
  cpfcnpj?: string;
  devedor_microempresa?: unknown;
  micro_empresa?: unknown;
};

function CpfcnpjCell({ cpfcnpj }: { cpfcnpj?: string | null }) {
  if (!isEmptyFieldValue(cpfcnpj)) {
    return <span className="font-mono text-xs text-muted-foreground">{formatCpfCnpj(cpfcnpj)}</span>;
  }

  return (
    <span className="inline-flex items-center gap-1.5 text-xs text-destructive">
      <span>{EMPTY_FIELD_LABEL}</span>
      <AlertCircle className="h-3.5 w-3.5 shrink-0" aria-hidden />
    </span>
  );
}

function isMicroempresaFlag(value: unknown): boolean {
  if (value === true || value === 1) return true;
  if (typeof value !== "string") return false;

  const normalized = value.trim().toLowerCase();
  return normalized === "true" || normalized === "1" || normalized === "s";
}

function isMicroempresaRow(row: PTituloParteRow): boolean {
  return isMicroempresaFlag(row.devedor_microempresa) || isMicroempresaFlag(row.micro_empresa);
}

function MicroempresaBadge() {
  return (
    <Badge
      variant="outline"
      className="rounded-md border-amber-500/30 bg-amber-50 px-1.5 py-0 text-[10px] font-medium text-amber-700 dark:bg-amber-950/30"
      title="Microempresa"
    >
      ME
    </Badge>
  );
}

function usePTituloPartePessoaEditor({
  getValues,
  update,
}: {
  getValues: UseFormGetValues<PTituloDetailsFormValues>;
  update: UseFieldArrayUpdate<PTituloDetailsFormValues, "partes">;
}) {
  const [isEditPPessoaDialogOpen, setIsEditPPessoaDialogOpen] = useState(false);
  const [selectedParteIndex, setSelectedParteIndex] = useState<number | null>(null);
  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [isSubmittingPessoa, setIsSubmittingPessoa] = useState(false);

  const handleEditParte = async (index: number) => {
    const parte = getValues(`partes.${index}`);
    try {
      let pessoa: PPessoaInterface | undefined =
        parte.pessoa_id != null
          ? ((await PessoaService.getById(parte.pessoa_id)) as unknown as PPessoaInterface)
          : undefined;

      if (!pessoa && parte.cpfcnpj) {
        const pessoas = await PessoaService.getAll({
          page: 1,
          per_page: 500,
          sort: "pessoa_id.desc",
        });
        pessoa = pessoas.find((item) => item.cpfcnpj === parte.cpfcnpj);
      }

      setSelectedParteIndex(index);
      setSelectedPessoa(
        pessoa ?? {
          pessoa_id: parte.pessoa_id ?? 0,
          nome: parte.nome,
          cpfcnpj: parte.cpfcnpj,
          micro_empresa: parte.micro_empresa as PPessoaInterface["micro_empresa"],
        },
      );
      setIsEditPPessoaDialogOpen(true);
    } catch (error) {
      console.error("Erro ao carregar dados da parte:", error);
    }
  };

  const handleSubmitPessoa = async (data: PessoaFormValues) => {
    if (selectedParteIndex === null) return;

    setIsSubmittingPessoa(true);
    try {
      const payload = {
        ...data,
        data_nascimento: data.data_nascimento || undefined,
      };

      const savedPessoa = (selectedPessoa?.pessoa_id && selectedPessoa.pessoa_id > 0
        ? await PessoaService.update(selectedPessoa.pessoa_id, payload)
        : await PessoaService.create(payload)) as unknown as PPessoaInterface;

      const current = getValues(`partes.${selectedParteIndex}`);
      update(
        selectedParteIndex,
        buildPTituloParteItem({
          ...current,
          pessoa_id: savedPessoa.pessoa_id,
          nome: savedPessoa.nome,
          cpfcnpj: savedPessoa.cpfcnpj,
          micro_empresa: savedPessoa.micro_empresa,
        }),
      );

      setIsEditPPessoaDialogOpen(false);
      setSelectedParteIndex(null);
      setSelectedPessoa(null);
    } catch (error) {
      console.error("Erro ao salvar pessoa da parte:", error);
    } finally {
      setIsSubmittingPessoa(false);
    }
  };

  return {
    handleEditParte,
    handleSubmitPessoa,
    isEditPPessoaDialogOpen,
    isSubmittingPessoa,
    selectedPessoa,
    setIsEditPPessoaDialogOpen,
  };
}

function PartesSectionHeader({
  count,
  onAdd,
}: {
  count: number;
  onAdd: () => void;
}) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <h3 className="text-base font-semibold tracking-tight text-foreground">Partes vinculadas</h3>
          <Badge
            variant="secondary"
            className="h-5 rounded-md border border-border/60 bg-muted/40 px-1.5 text-[11px] font-medium text-muted-foreground shadow-none"
          >
            {count}
          </Badge>
        </div>
        <p className="text-xs text-muted-foreground">
          Organize apresentante, cedente, credor e devedor em uma lista simples.
        </p>
      </div>

      <Button
        type="button"
        variant="outline"
        className="h-8 rounded-md border-border/70 bg-background px-3 text-xs font-medium shadow-none hover:bg-muted/50"
        onClick={onAdd}
      >
        <Plus className="mr-1.5 h-3.5 w-3.5" strokeWidth={1.75} />
        Adicionar Parte
      </Button>
    </div>
  );
}

function EmptyPartesState({ onAdd }: { onAdd: () => void }) {
  return (
    <button
      type="button"
      className="flex w-full flex-col items-center justify-center rounded-lg border border-dashed border-border/80 bg-muted/10 px-4 py-8 text-center transition-colors hover:border-[#FF6B00]/50 hover:bg-[#FF6B00]/5"
      onClick={onAdd}
    >
      <span className="mb-2 flex h-8 w-8 items-center justify-center rounded-md bg-background text-muted-foreground shadow-xs">
        <Plus className="h-4 w-4" strokeWidth={1.75} />
      </span>
      <span className="text-sm font-medium text-foreground">Nenhuma parte vinculada</span>
      <span className="mt-1 text-xs text-muted-foreground">
        Adicione a primeira pessoa para montar a lista do título.
      </span>
    </button>
  );
}

function ParteTableRow({
  row,
  onEdit,
  onRemove,
  onUpdateTipoVinculo,
}: {
  row: PTituloParteRow;
  onEdit: (index: number) => void;
  onRemove: (index: number) => void;
  onUpdateTipoVinculo: (index: number, tipo: PPessoaVinculoTipo) => void;
}) {
  const tipoValue = normalizePPessoaVinculoTipo(row.tipo) ?? PPessoaVinculoTipoEnum.DEVEDOR;
  const isMicroempresa = isMicroempresaRow(row);

  return (
    <TableRow className="group border-0 bg-background hover:bg-muted/25">
      <TableCell className="px-3 py-2.5">
        <PPessoaVinculoTipoSelectObject
          value={tipoValue}
          onValueChange={(tipo) => {
            if (!tipo) return;
            onUpdateTipoVinculo(row.fieldIndex, tipo);
          }}
          placeholder="Tipo de vínculo"
          clearable={false}
          className="w-[190px]"
          triggerClassName="h-8 rounded-md border-transparent bg-muted/35 px-2 text-xs font-medium shadow-none hover:bg-muted/60 focus:ring-1"
        />
      </TableCell>
      <TableCell className="min-w-[260px] px-3 py-2.5 whitespace-normal">
        <button
          type="button"
          className="block max-w-full rounded-md px-1.5 py-1 text-left transition-colors hover:bg-muted/50"
          onClick={() => onEdit(row.fieldIndex)}
          title={row.nome}
        >
          <span className="min-w-0">
            <span className="block truncate text-sm font-medium text-foreground">
              {formatEmptyField(row.nome)}
            </span>
            {isMicroempresa ? (
              <span className="mt-1 flex items-center gap-1.5">
                <MicroempresaBadge />
              </span>
            ) : null}
          </span>
        </button>
      </TableCell>
      <TableCell className="px-3 py-2.5">
        <CpfcnpjCell cpfcnpj={row.cpfcnpj} />
      </TableCell>
      <TableCell className="px-3 py-2.5 text-right">
        <div className="flex items-center justify-end gap-1 opacity-70 transition-opacity group-hover:opacity-100">
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="h-7 w-7 text-muted-foreground hover:bg-muted hover:text-[#FF6B00]"
            onClick={() => onEdit(row.fieldIndex)}
            aria-label={`Editar ${formatPPessoaVinculoTipoLabel(tipoValue)}`}
          >
            <Pencil className="h-3.5 w-3.5" strokeWidth={1.75} />
          </Button>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="h-7 w-7 text-muted-foreground hover:bg-muted hover:text-destructive"
            onClick={() => onRemove(row.fieldIndex)}
            aria-label={`Excluir ${row.nome ?? EMPTY_FIELD_LABEL}`}
          >
            <Trash2 className="h-3.5 w-3.5" strokeWidth={1.75} />
          </Button>
        </div>
      </TableCell>
    </TableRow>
  );
}

function PartesRowsTable({
  rows,
  onShowVinculoInfo,
  onEdit,
  onRemove,
  onUpdateTipoVinculo,
}: {
  rows: PTituloParteRow[];
  onShowVinculoInfo: () => void;
  onEdit: (index: number) => void;
  onRemove: (index: number) => void;
  onUpdateTipoVinculo: (index: number, tipo: PPessoaVinculoTipo) => void;
}) {
  return (
    <div className="overflow-hidden rounded-lg border border-border/70 bg-background">
      <Table className="min-w-[760px]">
        <TableHeader className="bg-muted/20">
          <TableRow className="border-border/70 hover:bg-transparent">
            <TableHead className="h-9 w-[260px] px-3 text-xs font-medium text-muted-foreground">
              <div className="flex items-center gap-1.5">
                <span>Tipo</span>
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="h-5 w-5 text-muted-foreground hover:bg-muted hover:text-[#FF6B00]"
                  onClick={onShowVinculoInfo}
                  aria-label="Ver explicação dos tipos de vínculo"
                >
                  <HelpCircle className="h-3.5 w-3.5" strokeWidth={2} />
                </Button>
              </div>
            </TableHead>
            <TableHead className="h-9 px-3 text-xs font-medium text-muted-foreground">
              Pessoa
            </TableHead>
            <TableHead className="h-9 w-[180px] px-3 text-xs font-medium text-muted-foreground">
              CPF/CNPJ
            </TableHead>
            <TableHead className="h-9 w-[92px] px-3 text-right text-xs font-medium text-muted-foreground">
              Ações
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody className="divide-y divide-border/60">
          {rows.map((row) => (
            <ParteTableRow
              key={row.id}
              row={row}
              onEdit={onEdit}
              onRemove={onRemove}
              onUpdateTipoVinculo={onUpdateTipoVinculo}
            />
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export function PTituloPartesTable() {
  const { control, getValues } = useFormContext<PTituloDetailsFormValues>();
  const { fields, append, remove, update } = useFieldArray({ control, name: "partes" });

  const [isParteDialogOpen, setIsParteDialogOpen] = useState(false);
  const [isVinculoInfoDialogOpen, setIsVinculoInfoDialogOpen] = useState(false);

  const orderedParteRows = useMemo<PTituloParteRow[]>(
    () =>
      fields
        .map((field, fieldIndex) => ({
          id: field.id,
          tipo: field.tipo,
          nome: field.nome,
          cpfcnpj: field.cpfcnpj,
          devedor_microempresa: field.devedor_microempresa,
          micro_empresa: field.micro_empresa,
          fieldIndex,
        }))
        .sort(
          (left, right) =>
            getTipoVinculoOrder(left.tipo) - getTipoVinculoOrder(right.tipo) ||
            left.fieldIndex - right.fieldIndex,
        ),
    [fields],
  );

  const handleAddPartesBatch = (novasPartes: PTituloParteItem[]) => {
    novasPartes.forEach((item) => append(buildPTituloParteItem(item)));
  };

  const handleUpdateTipoVinculo = (index: number, tipo: PPessoaVinculoTipo) => {
    const current = getValues(`partes.${index}`);
    update(index, buildPTituloParteItem({ ...current, tipo }));
  };

  const {
    handleEditParte,
    handleSubmitPessoa,
    isEditPPessoaDialogOpen,
    isSubmittingPessoa,
    selectedPessoa,
    setIsEditPPessoaDialogOpen,
  } = usePTituloPartePessoaEditor({ getValues, update });

  const hasParteRows = orderedParteRows.length > 0;

  return (
    <div className="space-y-3">
      <PartesSectionHeader count={orderedParteRows.length} onAdd={() => setIsParteDialogOpen(true)} />

      {hasParteRows ? (
        <PartesRowsTable
          rows={orderedParteRows}
          onShowVinculoInfo={() => setIsVinculoInfoDialogOpen(true)}
          onEdit={(index) => void handleEditParte(index)}
          onRemove={remove}
          onUpdateTipoVinculo={handleUpdateTipoVinculo}
        />
      ) : (
        <EmptyPartesState onAdd={() => setIsParteDialogOpen(true)} />
      )}

      <InfoDialog
        isOpen={isVinculoInfoDialogOpen}
        onOpenChange={setIsVinculoInfoDialogOpen}
        title="Explicando os tipos de vinculo no título"
        content={TIPO_VINCULO_INFO_MARKDOWN}
      />

      <PTituloParteDialog
        open={isParteDialogOpen}
        onOpenChange={setIsParteDialogOpen}
        onAddBatch={handleAddPartesBatch}
      />

      <PPessoaDialog
        open={isEditPPessoaDialogOpen}
        onOpenChange={setIsEditPPessoaDialogOpen}
        pessoa={selectedPessoa}
        onSubmit={handleSubmitPessoa}
        isLoading={isSubmittingPessoa}
      />
    </div>
  );
}
