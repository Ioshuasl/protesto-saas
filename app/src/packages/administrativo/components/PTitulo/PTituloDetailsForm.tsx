"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import {
  pTituloDetailsFormSchema,
  type PTituloDetailsFormValues,
  type PTituloSelectOptionsByField,
} from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { getPTituloDetailsDefaultValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";
import { PTituloBasicSection } from "./form/PTituloBasicSection";
import {
  PTITULO_OPERATIONAL_SECTION_IDS,
  PTituloDetailsSection,
  type PTituloOperationalSectionId,
} from "./PTituloDetailsSection";
import { PTituloDetailsSideNavigation } from "./PTituloDetailsSideNavigation";
import { PTituloFeesSection } from "./form/PTituloFeesSection";
import { PTituloSectionCard } from "./form/PTituloFormLayout";
import { formatPTituloMoneyValue } from "./form/PTituloMoneyUtils";
import { PTituloPartesTable } from "./form/PTituloPartesTable";
import { PTituloSelosSection } from "./form/PTituloSelosSection";

interface PTituloDetailsFormProps {
  titulo: TituloListItem | null;
  onSubmit: (data: PTituloDetailsFormValues) => void;
  isLoading?: boolean;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

const tabTriggerClassName =
  "h-10 flex-none rounded-none border-0 border-b-2 border-transparent bg-transparent px-4 text-sm shadow-none data-[state=active]:border-[#FF6B00] data-[state=active]:bg-transparent data-[state=active]:text-[#FF6B00] data-[state=active]:shadow-none";

const tabs = [
  { value: "dados-basicos", label: "Dados básicos", className: "min-w-36" },
  { value: "detalhes-historico", label: "Detalhes & Histórico", className: "min-w-44" },
  { value: "selos", label: "Selos", className: "min-w-28" },
];

export function PTituloDetailsForm({
  titulo,
  onSubmit,
  isLoading,
  selectOptionsByField,
}: PTituloDetailsFormProps) {
  const form = useForm<PTituloDetailsFormValues>({
    resolver: zodResolver(pTituloDetailsFormSchema),
    defaultValues: getPTituloDetailsDefaultValues(titulo),
  });

  const { reset } = form;
  const sectionRefs = useRef<Partial<Record<PTituloOperationalSectionId, HTMLElement | null>>>({});
  const [activeOperationalSection, setActiveOperationalSection] =
    useState<PTituloOperationalSectionId>("apontamento");
  const [navigationRequest, setNavigationRequest] = useState(0);

  useEffect(() => {
    reset(getPTituloDetailsDefaultValues(titulo));
  }, [titulo, reset]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visibleEntries = entries
          .filter((entry) => entry.isIntersecting)
          .sort((left, right) => left.boundingClientRect.top - right.boundingClientRect.top);

        const nextSectionId = visibleEntries[0]?.target.id as PTituloOperationalSectionId | undefined;
        if (nextSectionId && PTITULO_OPERATIONAL_SECTION_IDS.includes(nextSectionId)) {
          setActiveOperationalSection(nextSectionId);
        }
      },
      {
        root: null,
        rootMargin: "-20% 0px -65% 0px",
        threshold: 0,
      },
    );

    PTITULO_OPERATIONAL_SECTION_IDS.forEach((sectionId) => {
      const element = sectionRefs.current[sectionId];
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, []);

  const registerOperationalSectionRef = useCallback(
    (sectionId: PTituloOperationalSectionId) => (element: HTMLElement | null) => {
      sectionRefs.current[sectionId] = element;
    },
    [],
  );

  const handleOperationalNavigation = (sectionId: PTituloOperationalSectionId) => {
    setActiveOperationalSection(sectionId);
    setNavigationRequest((current) => current + 1);

    window.setTimeout(() => {
      sectionRefs.current[sectionId]?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 0);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <Tabs defaultValue="dados-basicos" className="w-full">
          <TabsList className="h-auto w-fit justify-start rounded-none border-b bg-transparent p-0">
            {tabs.map((tab) => (
              <TabsTrigger
                key={tab.value}
                value={tab.value}
                className={`${tabTriggerClassName} ${tab.className}`}
              >
                {tab.label}
              </TabsTrigger>
            ))}
          </TabsList>

          <TabsContent value="dados-basicos" className="space-y-4">
            <PTituloSectionCard>
              <PTituloPartesTable />
            </PTituloSectionCard>

            <PTituloBasicSection
              control={form.control}
              titulo={titulo}
              selectOptionsByField={selectOptionsByField}
            />
            <PTituloFeesSection control={form.control} selectOptionsByField={selectOptionsByField} />
          </TabsContent>

          <TabsContent value="detalhes-historico" className="space-y-4 overflow-visible">
            <div className="relative grid items-start gap-4 overflow-visible lg:grid-cols-[minmax(0,1fr)_17rem]">
              <PTituloDetailsSection
                control={form.control}
                selectOptionsByField={selectOptionsByField}
                activeSection={activeOperationalSection}
                navigationRequest={navigationRequest}
                registerSectionRef={registerOperationalSectionRef}
              />
              <PTituloDetailsSideNavigation
                activeSection={activeOperationalSection}
                onNavigate={handleOperationalNavigation}
              />
            </div>
          </TabsContent>

          <TabsContent value="selos" className="space-y-4">
            <PTituloSelosSection
              tituloId={titulo?.titulo_id}
              initialSelos={titulo?.vinculos_selos}
            />
          </TabsContent>
        </Tabs>

        <div className="flex items-center justify-between border-t pt-4">
          <p className="text-sm text-muted-foreground">
            Valor atual: {formatPTituloMoneyValue(titulo?.valor_titulo ?? 0)}
          </p>
          <Button type="submit" disabled={isLoading} className="bg-[#FF6B00] text-white hover:bg-[#E56000]">
            {isLoading ? "Salvando..." : "Salvar"}
          </Button>
        </div>
      </form>
    </Form>
  );
}

export type { PTituloDetailsFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
