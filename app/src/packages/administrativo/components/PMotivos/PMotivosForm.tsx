"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PMotivosInterface } from "@/packages/administrativo/interfaces";
import {
  motivoFormSchema,
  type MotivoFormValues,
} from "@/packages/administrativo/schemas/PMotivos/PMotivosFormSchema";
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

export type { MotivoFormValues };

interface PMotivosFormProps {
  defaultValues?: Partial<PMotivosInterface>;
  onSubmit: (data: MotivoFormValues) => void;
  isLoading?: boolean;
}

export function PMotivosForm({ defaultValues, onSubmit, isLoading }: PMotivosFormProps) {
  const form = useForm<MotivoFormValues>({
    resolver: zodResolver(motivoFormSchema),
    defaultValues: {
      codigo: defaultValues?.codigo || "",
      descricao: defaultValues?.descricao || "",
      situacao: defaultValues?.situacao || "Ativo",
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        codigo: defaultValues.codigo || "",
        descricao: defaultValues.descricao || "",
        situacao: defaultValues.situacao || "Ativo",
      });
    }
  }, [defaultValues, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="codigo"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Código</FormLabel>
                <FormControl>
                  <Input placeholder="Ex: 001" {...field} />
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
        </div>

        <FormField
          control={form.control}
          name="descricao"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Descrição</FormLabel>
              <FormControl>
                <Input placeholder="Ex: Ausência de aceite" {...field} />
              </FormControl>
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
