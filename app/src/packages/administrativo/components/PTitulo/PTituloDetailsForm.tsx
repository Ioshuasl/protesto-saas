"use client";

import { useEffect } from "react";
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
import { PTituloDetailsSection } from "./PTituloDetailsSection";
import { PTituloFeesSection } from "./form/PTituloFeesSection";
import { PTituloPartesSection } from "./form/PTituloPartesSection";
import { PTituloSelosSection } from "./form/PTituloSelosSection";
import { PTituloValuesSection } from "./form/PTituloValuesSection";

interface PTituloDetailsFormProps {
  titulo: TituloListItem | null;
  onSubmit: (data: PTituloDetailsFormValues) => void;
  isLoading?: boolean;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

const moneyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

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

  useEffect(() => {
    reset(getPTituloDetailsDefaultValues(titulo));
  }, [titulo, reset]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <Tabs defaultValue="partes" className="w-full">
          <TabsList className="w-full justify-start">
            <TabsTrigger value="partes">Partes vinculadas</TabsTrigger>
            <TabsTrigger value="basicos">Dados básicos</TabsTrigger>
            <TabsTrigger value="detalhes">Detalhes</TabsTrigger>
            <TabsTrigger value="selos">Selos vinculados</TabsTrigger>
          </TabsList>

          <TabsContent value="partes" className="space-y-2">
            <PTituloPartesSection />
          </TabsContent>

          <TabsContent value="basicos" className="space-y-3">
            <PTituloBasicSection control={form.control} selectOptionsByField={selectOptionsByField} />
            <PTituloValuesSection control={form.control} />
            <PTituloFeesSection control={form.control} selectOptionsByField={selectOptionsByField} />
          </TabsContent>

          <TabsContent value="detalhes">
            <PTituloDetailsSection
              control={form.control}
              titulo={titulo}
              selectOptionsByField={selectOptionsByField}
            />
          </TabsContent>

          <TabsContent value="selos" className="space-y-2">
            <p className="text-sm text-muted-foreground">Selos utilizados e valores associados a este título.</p>
            <PTituloSelosSection tituloId={titulo?.titulo_id} selos={titulo?.vinculos_selos} />
          </TabsContent>
        </Tabs>

        <div className="flex items-center justify-between border-t pt-4">
          <p className="text-sm text-muted-foreground">
            Valor atual: {moneyFormatter.format(titulo?.valor_titulo ?? 0)}
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
