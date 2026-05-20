"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Item, ItemContent, ItemDescription, ItemGroup, ItemMedia, ItemTitle } from "@/components/ui/item";
import { PTituloCancelamentoForm } from "@/packages/administrativo/components/PTitulo/forms/PTituloCancelamentoForm";
import { PTituloDesistenciaForm } from "@/packages/administrativo/components/PTitulo/forms/PTituloDesistenciaForm";
import { PTituloLiquidacaoForm } from "@/packages/administrativo/components/PTitulo/forms/PTituloLiquidacaoForm";
import { PTituloRetiradaForm } from "@/packages/administrativo/components/PTitulo/forms/PTituloRetiradaForm";
import { PTituloSustacaoForm } from "@/packages/administrativo/components/PTitulo/forms/PTituloSustacaoForm";
import { usePTituloCancelamentoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloCancelamentoHook";
import { usePTituloDesistenciaHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloDesistenciaHook";
import { usePTituloLiquidacaoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloLiquidacaoHook";
import { usePTituloRetiradaHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloRetiradaHook";
import { usePTituloSustacaoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloSustacaoHook";
import { isTituloListItem, type TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import type { PTituloCancelamentoFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloCancelamentoFormSchema";
import type { PTituloDesistenciaFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDesistenciaFormSchema";
import type { PTituloLiquidacaoFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloLiquidacaoFormSchema";
import type { PTituloRetiradaFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloRetiradaFormSchema";
import type { PTituloSustacaoFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloSustacaoFormSchema";
import type { WorkflowActionButton, WorkflowActionKey } from "@/packages/utils/PTitulo/ptituloWorkflowUtils";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";
import { cn } from "@/lib/utils";
import { CheckCircle2, ChevronLeft, Circle, CircleHelp } from "lucide-react";

const PTITULO_CANCELAMENTO_OPCOES_INFO_MARKDOWN = `### 1. Liquidação (Pagamento)
É o "final feliz" imediato. Acontece quando o devedor recebe a notícia do cartório e decide pagar a dívida logo de cara.

*   **Estágio:** Ocorre logo após o **apontamento** (quando o cartório recebe o título) e durante o período da **intimação**.
*   **Prazo:** O devedor tem **3 dias úteis** após ser avisado para pagar.
*   **Custas:** O devedor paga o valor da dívida + emolumentos (o serviço do cartório) + taxas e despesas de envio da intimação.
*   **Condição:** O pagamento deve ser feito diretamente ao Tabelião. Assim que o dinheiro cai, o cartório dá quitação e devolve o documento original ao devedor.

### 2. Sustação
É como apertar o botão de "pausa" (ou "parar") por ordem de um juiz.

*   **Estágio:** Pode ocorrer no estágio de **apontamento** ou **intimação**, impedindo que o protesto seja registrado.
*   **Competência:** Exclusiva do **Poder Judiciário**. O cartório não pode sustar nada sozinho; ele precisa receber um mandado do juiz.
*   **Regras:** O título fica "congelado" no cartório à disposição do juiz. Se o juiz revogar a ordem depois, o cartório volta a contar o prazo e protesta o título no dia seguinte.
*   **Condição:** O documento só pode ser pago ou retirado se o juiz autorizar expressamente.

### 3. Desistência
É quando o credor (quem levou o título ao cartório) muda de ideia antes do devedor ser protestado.

*   **Estágio:** Ocorre **antes** da lavratura do protesto.
*   **Competência:** Do **apresentante** (o credor ou seu banco).
*   **Regras:** O credor pede o título de volta por escrito ou sistema eletrônico.
*   **Custas:** O apresentante deve pagar os emolumentos e despesas do cartório pelo trabalho feito até ali.
*   **Prazo:** Enquanto o protesto não estiver assinado no livro, ele pode desistir.

### 4. Cancelamento
Aqui o "nome já está sujo". O cancelamento serve para apagar o registro de um protesto que já aconteceu.

*   **Estágio:** Ocorre **após o protesto** ter sido registrado no livro.
*   **Requisitos:** É preciso provar que a dívida foi paga (mostrando o título original protestado ou uma "carta de anuência" do credor com firma reconhecida).
*   **Custas:** O interessado paga custas de averbação e taxas para "limpar" o registro.
*   **Competência:** Qualquer interessado pode pedir o cancelamento, desde que traga os documentos certos.

### 5. Retirada
Muitas vezes confundida com a desistência, a retirada tem uma nuance importante sobre custos.

*   **Estágio:** Pode ocorrer na fase de **exame formal** (antes de virar um processo oficial) ou como consequência da desistência.
*   **Regra de "Custas Zero":** Se o Tabelião notar um erro no título (falta de endereço, CPF errado, etc.) e devolvê-lo ao credor antes de protocolar, **não se cobram emolumentos**.
*   **Retirada após Protocolo:** Se o título já foi protocolado e o credor retira, vira uma **Desistência** (item 3) e as custas devem ser pagas.
*   **Condição:** A retirada por erro formal protege o devedor de ser intimado por uma dívida mal preenchida.
`;

const FORM_DOM_ID = "ptitulo-cancelamento-etapas-form";

type DialogStep = "escolher" | "formulario";

interface PTituloCancelamentoOptionsDIalogProps {
  id: number;
  titulo: TituloListItem | null;
  options: WorkflowActionButton[];
  onSuccess: (titulo: TituloListItem) => void;
}

export function PTituloCancelamentoOptionsDIalog({
  id,
  titulo,
  options,
  onSuccess,
}: PTituloCancelamentoOptionsDIalogProps) {
  const { cancelarTitulo } = usePTituloCancelamentoHook();
  const { desistirTitulo } = usePTituloDesistenciaHook();
  const { liquidarTitulo } = usePTituloLiquidacaoHook();
  const { sustarTitulo } = usePTituloSustacaoHook();
  const { retiradaTitulo } = usePTituloRetiradaHook();

  const [isOpen, setIsOpen] = useState(false);
  const [isInfoOpen, setIsInfoOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState<DialogStep>("escolher");
  const [selectedAction, setSelectedAction] = useState<WorkflowActionKey | "">("");

  const selectedLabel = useMemo(
    () => options.find((option) => option.key === selectedAction)?.label ?? "",
    [options, selectedAction],
  );

  const resetFlowState = () => {
    setStep("escolher");
    setSelectedAction("");
  };

  const handleOpenChange = (open: boolean) => {
    setIsOpen(open);
    if (!open) {
      resetFlowState();
    }
  };

  const openDialog = () => {
    resetFlowState();
    setIsOpen(true);
  };

  const closeDialog = () => handleOpenChange(false);

  const handleContinuarParaFormulario = () => {
    if (!selectedAction) return;
    setStep("formulario");
  };

  const finishSuccess = (response: unknown) => {
    if (isTituloListItem(response)) {
      onSuccess(response);
      closeDialog();
    }
  };

  const submitSustacao = async (values: PTituloSustacaoFormValues) => {
    setIsLoading(true);
    try {
      const response = await sustarTitulo(id, values);
      finishSuccess(response);
    } finally {
      setIsLoading(false);
    }
  };

  const submitCancelamento = async (values: PTituloCancelamentoFormValues) => {
    setIsLoading(true);
    try {
      const response = await cancelarTitulo(id, values);
      finishSuccess(response);
    } finally {
      setIsLoading(false);
    }
  };

  const submitRetirada = async (values: PTituloRetiradaFormValues) => {
    setIsLoading(true);
    try {
      const response = await retiradaTitulo(id, values);
      finishSuccess(response);
    } finally {
      setIsLoading(false);
    }
  };

  const submitDesistencia = async (values: PTituloDesistenciaFormValues) => {
    setIsLoading(true);
    try {
      const response = await desistirTitulo(id, values);
      finishSuccess(response);
    } finally {
      setIsLoading(false);
    }
  };

  const submitLiquidacao = async (values: PTituloLiquidacaoFormValues) => {
    setIsLoading(true);
    try {
      const response = await liquidarTitulo(id, values);
      finishSuccess(response);
    } finally {
      setIsLoading(false);
    }
  };

  const renderFormulario = () => {
    if (!titulo) {
      return (
        <p className="text-sm text-muted-foreground">
          Carregue os dados do título para preencher o formulário.
        </p>
      );
    }

    switch (selectedAction) {
      case "sustarTitulo":
        return (
          <PTituloSustacaoForm
            id={FORM_DOM_ID}
            titulo={titulo}
            onSubmit={submitSustacao}
          />
        );
      case "cancelarTitulo":
        return (
          <PTituloCancelamentoForm
            id={FORM_DOM_ID}
            titulo={titulo}
            onSubmit={submitCancelamento}
          />
        );
      case "retiradaTitulo":
        return (
          <PTituloRetiradaForm id={FORM_DOM_ID} titulo={titulo} onSubmit={submitRetirada} />
        );
      case "desistirTitulo":
        return (
          <PTituloDesistenciaForm
            id={FORM_DOM_ID}
            titulo={titulo}
            onSubmit={submitDesistencia}
          />
        );
      case "liquidarTitulo":
        return (
          <PTituloLiquidacaoForm
            id={FORM_DOM_ID}
            titulo={titulo}
            onSubmit={submitLiquidacao}
          />
        );
      default:
        return (
          <p className="text-sm text-muted-foreground">
            Selecione uma opção válida na etapa anterior.
          </p>
        );
    }
  };

  return (
    <>
      <Button
        variant="outline"
        type="button"
        data-skip-global-confirm="true"
        disabled={isLoading}
        className="h-9 rounded-md border bg-muted px-3 text-sm font-medium shadow-none transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-muted/80 md:h-10 md:px-4"
        onClick={openDialog}
      >
        Cancelar Título
      </Button>

      <Dialog open={isOpen} onOpenChange={handleOpenChange}>
        <DialogContent className="flex max-h-[min(90vh,840px)] w-[calc(100vw-2rem)] flex-col gap-0 overflow-hidden sm:max-w-3xl">
          <DialogHeader className="shrink-0 space-y-1 pr-8">
            <div className="flex items-center gap-1.5">
              <DialogTitle className="text-left">
                {step === "escolher" ? "Opções de cancelamento" : selectedLabel || "Dados da ação"}
              </DialogTitle>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-7 w-7 shrink-0 text-muted-foreground hover:text-foreground"
                aria-label="Ajuda: conceitos de liquidação, sustação, desistência, cancelamento e retirada"
                onClick={(event) => {
                  event.stopPropagation();
                  setIsInfoOpen(true);
                }}
              >
                <CircleHelp className="size-5" strokeWidth={1.5} />
              </Button>
            </div>
            <DialogDescription className="text-left">
              {step === "escolher"
                ? "Primeiro escolha uma ação compatível com o estágio do título; na sequência você informará ocorrência, motivo e data."
                : `Etapa 2 de 2 — preencha os campos para concluir ${selectedLabel ? `“${selectedLabel}”` : "a ação"}.`}
            </DialogDescription>
          </DialogHeader>

          <div
            className={cn(
              "min-h-0 flex-1 overflow-x-hidden overflow-y-auto py-4",
              step === "escolher" &&
                "[scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden",
            )}
          >
            {step === "escolher" ? (
              <div className="grid max-w-full gap-2">
                <span className="text-sm font-medium">Ação (escolha única)</span>
                <ItemGroup className="max-w-full gap-2">
                  {options.map((option) => {
                    const isSelected = selectedAction === option.key;
                    return (
                      <Item
                        key={option.key}
                        role="button"
                        tabIndex={0}
                        variant={isSelected ? "outline" : "muted"}
                        size="sm"
                        className="max-w-full cursor-pointer select-none transform-gpu transition-[transform,box-shadow] duration-200 ease-out hover:-translate-y-0.5 hover:shadow-sm data-[variant=outline]:border-emerald-500/60 data-[variant=outline]:bg-emerald-50/40 dark:data-[variant=outline]:bg-emerald-900/10"
                        onClick={() => setSelectedAction(option.key)}
                        onKeyDown={(event) => {
                          if (event.key === "Enter" || event.key === " ") {
                            event.preventDefault();
                            setSelectedAction(option.key);
                          }
                        }}
                      >
                        <ItemMedia variant="default">
                          {isSelected ? (
                            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                          ) : (
                            <Circle className="h-4 w-4 text-muted-foreground" />
                          )}
                        </ItemMedia>
                        <ItemContent>
                          <ItemTitle>{option.label}</ItemTitle>
                          <ItemDescription>
                            {isSelected
                              ? "Opção selecionada — avance para preencher o formulário."
                              : "Clique para selecionar esta opção."}
                          </ItemDescription>
                        </ItemContent>
                      </Item>
                    );
                  })}
                </ItemGroup>
              </div>
            ) : (
              renderFormulario()
            )}
          </div>

          <DialogFooter className="shrink-0 gap-2 border-t pt-4 sm:justify-between">
            {step === "escolher" ? (
              <>
                <Button type="button" variant="outline" onClick={closeDialog} disabled={isLoading}>
                  Fechar
                </Button>
                <Button
                  type="button"
                  onClick={handleContinuarParaFormulario}
                  disabled={!selectedAction || isLoading}
                >
                  Continuar
                </Button>
              </>
            ) : (
              <>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setStep("escolher")}
                  disabled={isLoading}
                  className="gap-1"
                >
                  <ChevronLeft className="h-4 w-4" strokeWidth={1.5} />
                  Voltar
                </Button>
                <div className="flex gap-2">
                  <Button type="button" variant="outline" onClick={closeDialog} disabled={isLoading}>
                    Fechar
                  </Button>
                  <Button
                    type="submit"
                    form={FORM_DOM_ID}
                    disabled={isLoading || !titulo}
                  >
                    Confirmar
                  </Button>
                </div>
              </>
            )}
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <InfoDialog
        isOpen={isInfoOpen}
        title="Conceitos do fluxo edital"
        description="Resumo das principais situações relacionadas a liquidação, sustação, desistência, cancelamento e retirada."
        content={PTITULO_CANCELAMENTO_OPCOES_INFO_MARKDOWN}
        onOpenChange={setIsInfoOpen}
      />
    </>
  );
}
