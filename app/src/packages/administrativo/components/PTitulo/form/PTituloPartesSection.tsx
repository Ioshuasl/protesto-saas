"use client";

import { useState } from "react";
import { useFieldArray, useFormContext } from "react-hook-form";
import { HelpCircle, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PPessoaVinculoTable } from "@/packages/administrativo/components/PPessoaVinculo/PPessoaVinculoTable";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import type { PessoaFormValues } from "@/packages/administrativo/components/PPessoa/PPessoaForm";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces";
import type { PPessoaVinculoTipo } from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum";
import { PessoaService } from "@/packages/administrativo/services/PPessoa/PPessoaService";
import type { PTituloDetailsFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";
import { PTituloParteDialog } from "../PTituloParteDialog";
import { buildPTituloParteItem, type PTituloParteItem } from "../PTituloParteTypes";

const TIPO_VINCULO_INFO_MARKDOWN = `### 📄 Apresentante

É a pessoa (ou empresa/banco) que "apresenta", ou seja, que leva o título ou documento de dívida ao cartório para ser protestado. O papel dele envolve algumas responsabilidades importantes:

* É ele quem fornece os dados da dívida ao cartório, assumindo total responsabilidade pelo que está informando.
* Ele tem o dever de indicar a perfeita identificação do devedor e o seu endereço correto.
* Quando o envio do título é feito eletronicamente, o apresentante é quem declara que a dívida existe e guarda consigo o documento original (ou cópia autenticada) para provar a cobrança caso seja questionado na Justiça.
* É também o apresentante quem pode pedir a desistência do protesto e retirar o documento antes que o ato seja concluído (desde que pague as taxas).

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

### ✍️ Cedente / Sacador

* **Sacador:** Segundo o documento, o sacador é quem lança ou emite a cobrança originada de um negócio, como no caso de ser o responsável pela emissão de uma duplicata.
* **Cedente:** Para ser totalmente transparente e honesto com você sobre minha natureza como inteligência artificial que está seguindo estritamente a fonte fornecida, **o termo "Cedente" não é mencionado ou definido nas regras do documento enviado**. Na prática comercial do dia a dia (fora deste documento), o cedente costuma ser quem "cede" ou transfere o direito de receber essa dívida para um banco, mas essa definição não consta no Código de Normas que analisamos.
`;

export function PTituloPartesSection() {
  const { control, getValues } = useFormContext<PTituloDetailsFormValues>();
  const { fields, append, remove, update } = useFieldArray({ control, name: "partes" });

  const [isParteDialogOpen, setIsParteDialogOpen] = useState(false);
  const [isVinculoInfoDialogOpen, setIsVinculoInfoDialogOpen] = useState(false);
  const [isEditPPessoaDialogOpen, setIsEditPPessoaDialogOpen] = useState(false);
  const [selectedParteIndex, setSelectedParteIndex] = useState<number | null>(null);
  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [isSubmittingPessoa, setIsSubmittingPessoa] = useState(false);

  const handleAddPartesBatch = (novasPartes: PTituloParteItem[]) => {
    novasPartes.forEach((item) => append(buildPTituloParteItem(item)));
  };

  const handleUpdateTipoVinculo = (index: number, tipo: PPessoaVinculoTipo) => {
    const current = getValues(`partes.${index}`);
    update(index, buildPTituloParteItem({ ...current, tipo }));
  };

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

  return (
    <div className="space-y-2">
      <div className="flex justify-end">
        <Button type="button" variant="outline" onClick={() => setIsParteDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
          Adicionar Parte
        </Button>
      </div>

      <PPessoaVinculoTable
        rows={fields.map((field) => ({
          id: field.id,
          tipo: field.tipo,
          nome: field.nome,
          cpfcnpj: field.cpfcnpj,
          devedor_microempresa: field.devedor_microempresa,
          micro_empresa: field.micro_empresa,
        }))}
        onTipoChange={handleUpdateTipoVinculo}
        onEdit={(index) => void handleEditParte(index)}
        onRemove={remove}
        emptyMessage="Nenhuma parte vinculada encontrada."
        tipoHeaderAction={
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="h-6 w-6 font-bold text-foreground hover:text-[#FF6B00]"
            onClick={() => setIsVinculoInfoDialogOpen(true)}
            aria-label="Ver explicação dos tipos de vínculo"
          >
            <HelpCircle className="h-4 w-4" strokeWidth={2.75} />
          </Button>
        }
      />

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
