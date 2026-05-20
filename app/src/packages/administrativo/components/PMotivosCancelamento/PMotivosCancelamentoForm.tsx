"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export type { MotivoCancelamentoFormValues };

interface PMotivosCancelamentoFormProps {
  defaultValues?: Partial<PMotivosCancelamentoInterface>;
  onSubmit: (data: MotivoCancelamentoFormValues) => void;
  isLoading?: boolean;
}

export function PMotivosCancelamentoForm({
  defaultValues,
  onSubmit,
  isLoading,
}: PMotivosCancelamentoFormProps) {
  const form = useForm<MotivoCancelamentoFormValues>({
    resolver: zodResolver(motivoCancelamentoFormSchema),
    defaultValues: {
      descricao: defaultValues?.descricao || "",
      situacao: defaultValues?.situacao || "Ativo",
      ord_jud_ou_rem_ind: (defaultValues?.ord_jud_ou_rem_ind as MotivoCancelamentoFormValues["ord_jud_ou_rem_ind"]) || "Outros",
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        descricao: defaultValues.descricao || "",
        situacao: defaultValues.situacao || "Ativo",
        ord_jud_ou_rem_ind:
          (defaultValues.ord_jud_ou_rem_ind as MotivoCancelamentoFormValues["ord_jud_ou_rem_ind"]) || "Outros",
      });
    }
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
                <Input placeholder="Ex: Cumprimento de ordem judicial" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="situacao"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Situação</FormLabel>
                <Select value={field.value} onValueChange={field.onChange}>
                  <FormControl>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Selecione a situação" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="Ativo">Ativo</SelectItem>
                    <SelectItem value="Inativo">Inativo</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="ord_jud_ou_rem_ind"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tipo</FormLabel>
                <Select value={field.value} onValueChange={field.onChange}>
                  <FormControl>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="Ordem Judicial">Ordem Judicial</SelectItem>
                    <SelectItem value="Remessa Indireta">Remessa Indireta</SelectItem>
                    <SelectItem value="Outros">Outros</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="flex justify-end pt-4">
          <Button type="submit" disabled={isLoading} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            {isLoading ? "Salvando..." : "Salvar"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
