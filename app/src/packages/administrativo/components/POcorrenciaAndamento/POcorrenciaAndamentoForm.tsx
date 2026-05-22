"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import type { POcorrenciaAndamentoInterface } from "@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface";
import {
  ocorrenciaAndamentoFormSchema,
  type OcorrenciaAndamentoFormValues,
} from "@/packages/administrativo/schemas/POcorrenciaAndamento/POcorrenciaAndamentoFormSchema";

export type { OcorrenciaAndamentoFormValues };

interface POcorrenciaAndamentoFormProps {
  defaultValues?: Partial<POcorrenciaAndamentoInterface>;
  onSubmit: (data: OcorrenciaAndamentoFormValues) => void;
  isLoading?: boolean;
}

function buildFormDefaults(
  defaultValues?: Partial<POcorrenciaAndamentoInterface>,
): OcorrenciaAndamentoFormValues {
  return {
    codigo: defaultValues?.codigo?.trim().toUpperCase() || "",
    descricao: defaultValues?.descricao?.trim() || "",
  };
}

export function POcorrenciaAndamentoForm({
  defaultValues,
  onSubmit,
  isLoading,
}: POcorrenciaAndamentoFormProps) {
  const form = useForm<OcorrenciaAndamentoFormValues>({
    resolver: zodResolver(ocorrenciaAndamentoFormSchema),
    defaultValues: buildFormDefaults(defaultValues),
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset(buildFormDefaults(defaultValues));
    }
  }, [defaultValues, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="codigo"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Código</FormLabel>
              <FormControl>
                <Input placeholder="Ex: AA" className="uppercase" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="descricao"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Descrição</FormLabel>
              <FormControl>
                <Input placeholder="Ex: Apontado" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end pt-4">
          <Button
            type="submit"
            disabled={isLoading}
            className="bg-[#FF6B00] hover:bg-[#E56000] text-white"
          >
            {isLoading ? "Salvando..." : "Salvar"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
