"use client";

import { Accordion } from "@/components/ui/accordion";
import { Tabs } from "@/components/ui/tabs";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import type { PTituloDetailsFormValues, PTituloSelectOptionsByField } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import VerticalTabsSidebar from "@/shared/components/verticalTabs/VerticalTabsSidebar";
import { useMemo, useRef, useState } from "react";
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

interface PTituloDetailsSectionProps {
  control: Control<PTituloDetailsFormValues>;
  titulo: TituloListItem | null;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

export function PTituloDetailsSection({ control, titulo, selectOptionsByField }: PTituloDetailsSectionProps) {
  const [activeSection, setActiveSection] = useState("");
  const [openSections, setOpenSections] = useState<string[]>(["apontamento", "intimacao-aceite", "protesto"]);
  const sectionRefs = useRef<Record<string, HTMLDivElement | null>>({});

  const hasValue = (value: unknown) => value !== null && value !== undefined && value !== "";

  const hasApontamentoBase = hasValue(titulo?.numero_apontamento) && hasValue(titulo?.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo?.data_intimacao);
  const hasProtestoCompleto =
    hasIntimacao &&
    hasValue(titulo?.data_protesto) &&
    hasValue(titulo?.livro_id_protesto) &&
    hasValue(titulo?.folha_protesto);
  const hasCancelamentoConcluido =
    hasValue(titulo?.data_cancelamento) || hasValue(titulo?.data_desistencia) || hasValue(titulo?.data_pago);

  const navigationItems = useMemo(() => {
    if (hasProtestoCompleto) {
      return [
        { value: "apontamento", label: "Apontamento", completed: true },
        { value: "intimacao-aceite", label: "Intimação & Aceite", completed: true },
        { value: "protesto", label: "Protesto", completed: true },
        { value: "cancelamento-pagamento", label: "Cancelamento", completed: hasCancelamentoConcluido },
      ];
    }

    if (hasIntimacao) {
      return [
        { value: "apontamento", label: "Apontamento", completed: true },
        { value: "intimacao-aceite", label: "Intimação & Aceite", completed: true },
        { value: "protesto", label: "Protesto", completed: false },
        { value: "cancelamento-pagamento", label: "Cancelamento", completed: hasCancelamentoConcluido },
      ];
    }

    if (hasApontamentoBase) {
      return [
        { value: "apontamento", label: "Apontamento", completed: true },
        { value: "intimacao-aceite", label: "Intimação & Aceite", completed: false },
        { value: "protesto", label: "Protesto", disabled: true, completed: false },
        { value: "cancelamento-pagamento", label: "Cancelamento", disabled: true, completed: false },
      ];
    }

    return [
      { value: "apontamento", label: "Apontamento", completed: false },
      { value: "intimacao-aceite", label: "Intimação & Aceite", disabled: true, completed: false },
      { value: "protesto", label: "Protesto", disabled: true, completed: false },
      { value: "cancelamento-pagamento", label: "Cancelamento", disabled: true, completed: false },
    ];
  }, [hasApontamentoBase, hasCancelamentoConcluido, hasIntimacao, hasProtestoCompleto]);

  const handleSidebarNavigation = (value: string) => {
    setActiveSection(value);
    setOpenSections([value]);
    sectionRefs.current[value]?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const blockProps = { control, selectOptionsByField };

  return (
    <div className="space-y-4">
      <div className="p-2"></div>

      <Tabs value={activeSection} onValueChange={handleSidebarNavigation} className="gap-4 lg:flex-row">
        <div className="flex-1">
          <Accordion
            type="multiple"
            value={openSections}
            onValueChange={setOpenSections}
            className="space-y-3"
          >
            <div ref={(element) => { sectionRefs.current["apontamento"] = element; }}>
              <PTituloDetailAccordionSection
                sectionKey="apontamento"
                title="Apontamento"
                description="Dados de protocolo, livro e referência inicial do apontamento."
                isHighlighted={activeSection === "apontamento"}
              >
                <PTituloDetailFieldsApontamento {...blockProps} />
              </PTituloDetailAccordionSection>
            </div>
            <div ref={(element) => { sectionRefs.current["intimacao-aceite"] = element; }}>
              <PTituloDetailAccordionSection
                sectionKey="intimacao-aceite"
                title="Intimação & Aceite"
                description="Campos relacionados a aceite, intimação e cobrança derivada."
                isHighlighted={activeSection === "intimacao-aceite"}
              >
                <PTituloDetailFieldsIntimacaoAceite {...blockProps} />
              </PTituloDetailAccordionSection>
            </div>
            <div ref={(element) => { sectionRefs.current["protesto"] = element; }}>
              <PTituloDetailAccordionSection
                sectionKey="protesto"
                title="Protesto"
                description="Informações operacionais do protesto após a intimação."
                isHighlighted={activeSection === "protesto"}
              >
                <PTituloDetailFieldsProtesto control={control} />
              </PTituloDetailAccordionSection>
            </div>
            <div ref={(element) => { sectionRefs.current["cancelamento-pagamento"] = element; }}>
              <PTituloDetailAccordionSection
                sectionKey="cancelamento-pagamento"
                title="Cancelamento & Pagamento"
                description="Controle de sustação, pagamento e cancelamento do título."
                isHighlighted={activeSection === "cancelamento-pagamento"}
              >
                <PTituloDetailFieldsCancelamentoPagamento {...blockProps} />
              </PTituloDetailAccordionSection>
            </div>
            <PTituloDetailAccordionSection
              sectionKey="cra"
              title="CRA"
              description="Informações de integração e rastreabilidade do fluxo CRA."
              isHighlighted={activeSection === "cra"}
            >
              <PTituloDetailFieldsCra {...blockProps} />
            </PTituloDetailAccordionSection>
            <PTituloDetailAccordionSection
              sectionKey="cenprot"
              title="CENPROT"
              description="Permissões, chaves e eventos ligados à integração CENPROT."
              isHighlighted={activeSection === "cenprot"}
            >
              <PTituloDetailFieldsCenprot {...blockProps} />
            </PTituloDetailAccordionSection>
            <PTituloDetailAccordionSection
              sectionKey="serasa"
              title="SERASA"
              description="Datas e movimentações relacionadas ao envio e retorno SERASA."
              isHighlighted={activeSection === "serasa"}
            >
              <PTituloDetailFieldsSerasa {...blockProps} />
            </PTituloDetailAccordionSection>
          </Accordion>
        </div>

        <VerticalTabsSidebar
          title="Navegação"
          description="Acesse rapidamente os principais grupos de detalhes do título."
          items={navigationItems}
        />
      </Tabs>
    </div>
  );
}
