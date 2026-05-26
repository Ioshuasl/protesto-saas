"use client";

import { Accordion } from "@/components/ui/accordion";
import type { PTituloDetailsFormValues, PTituloSelectOptionsByField } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { useEffect, useState } from "react";
import type { Control } from "react-hook-form";
import {
  PTituloDetailFieldsApontamento,
  PTituloDetailFieldsCancelamentoPagamento,
  PTituloDetailFieldsCenprot,
  PTituloDetailFieldsCra,
  PTituloDetailFieldsIntimacaoAceite,
  PTituloDetailFieldsProtesto,
  PTituloDetailFieldsSerasa,
} from "./PTituloDetailAccordionBlocks";
import { PTituloDetailAccordionSection } from "./PTituloDetailAccordionSection";

export const PTITULO_OPERATIONAL_SECTION_IDS = [
  "apontamento",
  "intimacao-aceite",
  "protesto",
  "cancelamento-pagamento",
  "cra",
  "cenprot",
  "serasa",
] as const;

export type PTituloOperationalSectionId = (typeof PTITULO_OPERATIONAL_SECTION_IDS)[number];

interface PTituloDetailsSectionProps {
  control: Control<PTituloDetailsFormValues>;
  selectOptionsByField?: PTituloSelectOptionsByField;
  activeSection?: string;
  navigationRequest?: number;
  registerSectionRef?: (sectionId: PTituloOperationalSectionId) => (element: HTMLElement | null) => void;
}

export function PTituloDetailsSection({
  control,
  selectOptionsByField,
  activeSection,
  navigationRequest,
  registerSectionRef,
}: PTituloDetailsSectionProps) {
  const [openSections, setOpenSections] = useState<string[]>([...PTITULO_OPERATIONAL_SECTION_IDS]);

  useEffect(() => {
    if (!activeSection || !PTITULO_OPERATIONAL_SECTION_IDS.includes(activeSection as PTituloOperationalSectionId)) {
      return;
    }

    setOpenSections((current) => (current.includes(activeSection) ? current : [...current, activeSection]));
  }, [activeSection, navigationRequest]);

  const blockProps = { control, selectOptionsByField };

  return (
    <div className="space-y-4">
      <Accordion
        type="multiple"
        value={openSections}
        onValueChange={setOpenSections}
        className="space-y-3"
      >
        <div
          ref={registerSectionRef?.("apontamento")}
          id="apontamento"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="apontamento"
            title="Apontamento"
            description="Dados de protocolo, livro e referência inicial do apontamento."
            isHighlighted={activeSection === "apontamento"}
          >
            <PTituloDetailFieldsApontamento {...blockProps} />
          </PTituloDetailAccordionSection>
        </div>
        <div
          ref={registerSectionRef?.("intimacao-aceite")}
          id="intimacao-aceite"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="intimacao-aceite"
            title="Intimação & Aceite"
            description="Campos relacionados a aceite, intimação e cobrança derivada."
            isHighlighted={activeSection === "intimacao-aceite"}
          >
            <PTituloDetailFieldsIntimacaoAceite {...blockProps} />
          </PTituloDetailAccordionSection>
        </div>
        <div
          ref={registerSectionRef?.("protesto")}
          id="protesto"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="protesto"
            title="Protesto"
            description="Informações operacionais do protesto após a intimação."
            isHighlighted={activeSection === "protesto"}
          >
            <PTituloDetailFieldsProtesto control={control} />
          </PTituloDetailAccordionSection>
        </div>
        <div
          ref={registerSectionRef?.("cancelamento-pagamento")}
          id="cancelamento-pagamento"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="cancelamento-pagamento"
            title="Cancelamento & Pagamento"
            description="Controle de sustação, pagamento e cancelamento do título."
            isHighlighted={activeSection === "cancelamento-pagamento"}
          >
            <PTituloDetailFieldsCancelamentoPagamento {...blockProps} />
          </PTituloDetailAccordionSection>
        </div>
        <div
          ref={registerSectionRef?.("cra")}
          id="cra"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="cra"
            title="CRA"
            description="Informações de integração e rastreabilidade do fluxo CRA."
            isHighlighted={activeSection === "cra"}
          >
            <PTituloDetailFieldsCra {...blockProps} />
          </PTituloDetailAccordionSection>
        </div>
        <div
          ref={registerSectionRef?.("cenprot")}
          id="cenprot"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="cenprot"
            title="CENPROT"
            description="Permissões, chaves e eventos ligados à integração CENPROT."
            isHighlighted={activeSection === "cenprot"}
          >
            <PTituloDetailFieldsCenprot {...blockProps} />
          </PTituloDetailAccordionSection>
        </div>
        <div
          ref={registerSectionRef?.("serasa")}
          id="serasa"
          className="scroll-mt-24"
        >
          <PTituloDetailAccordionSection
            sectionKey="serasa"
            title="SERASA"
            description="Datas e movimentações relacionadas ao envio e retorno SERASA."
            isHighlighted={activeSection === "serasa"}
          >
            <PTituloDetailFieldsSerasa {...blockProps} />
          </PTituloDetailAccordionSection>
        </div>
      </Accordion>
    </div>
  );
}
