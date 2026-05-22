"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { normalizeSituacaoKey } from "@/packages/administrativo/components/PLivroNatureza/plivroNaturezaSituacaoUtils";
import { PMotivosCancelamentoInterface } from "@/packages/administrativo/interfaces";
import {
  motivoCancelamentoFormSchema,
  type MotivoCancelamentoFormValues,
} from "@/packages/administrativo/schemas/PMotivosCancelamento/PMotivosCancelamentoFormSchema";
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
import SituacoesSelect from "@/shared/components/situacoes/SituacoesSelect";

export type { MotivoCancelamentoFormValues };

interface PMotivosCancelamentoFormProps {
  defaultValues?: Partial<PMotivosCancelamentoInterface>;
  onSubmit: (data: MotivoCancelamentoFormValues) => void;
  isLoading?: boolean;
}

function buildFormDefaults(
  defaultValues?: Partial<PMotivosCancelamentoInterface>,
): MotivoCancelamentoFormValues {
  return {
    descricao: defaultValues?.descricao?.trim() || "",
    situacao: normalizeSituacaoKey(defaultValues?.situacao),
  };
}

export function PMotivosCancelamentoForm({
  defaultValues,
  onSubmit,
  isLoading,
}: PMotivosCancelamentoFormProps) {
  const form = useForm<MotivoCancelamentoFormValues>({
    resolver: zodResolver(motivoCancelamentoFormSchema),
    defaultValues: buildFormDefaults(defaultValues),
  });

  useEffect(() => {
    form.reset(buildFormDefaults(defaultValues));
  }, [defaultValues, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="descricao"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Descrição</FormLabel>
              <FormControl>
                <Input placeholder="Ex: Determinação judicial" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="situacao"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Situação</FormLabel>
              <SituacoesSelect field={field} />
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end pt-4">
          <Button type="submit" disabled={isLoading} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            {isLoading ? "Salvando..." : "Salvar"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
