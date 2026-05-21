"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";
import { normalizeSituacaoKey } from "@/packages/administrativo/components/PLivroNatureza/plivroNaturezaSituacaoUtils";
import {
  livroNaturezaFormSchema,
  type LivroNaturezaFormValues,
} from "@/packages/administrativo/schemas/PLivroNatureza/PLivroNaturezaFormSchema";
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

export type { LivroNaturezaFormValues };

interface PLivroNaturezaFormProps {
  defaultValues?: Partial<PLivroNaturezaInterface>;
  onSubmit: (data: LivroNaturezaFormValues) => void;
  isLoading?: boolean;
}

function buildFormDefaults(
  defaultValues?: Partial<PLivroNaturezaInterface>,
): LivroNaturezaFormValues {
  return {
    sigla: defaultValues?.sigla?.trim() || "",
    descricao: defaultValues?.descricao?.trim() || "",
    situacao: normalizeSituacaoKey(defaultValues?.situacao),
  };
}

export function PLivroNaturezaForm({ defaultValues, onSubmit, isLoading }: PLivroNaturezaFormProps) {
  const form = useForm<LivroNaturezaFormValues>({
    resolver: zodResolver(livroNaturezaFormSchema),
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
          name="sigla"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Sigla</FormLabel>
              <FormControl>
                <Input placeholder="Ex: AP" maxLength={3} {...field} />
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
                <Input placeholder="Ex: Apontamento" {...field} />
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
