"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PEspecieInterface } from "@/packages/administrativo/interfaces";
import { especieFormSchema, type EspecieFormValues } from "@/packages/administrativo/schemas/PEspecie/PEspecieFormSchema";
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
import { useEffect } from "react";

export type { EspecieFormValues };

interface PEspecieFormProps {
  defaultValues?: Partial<PEspecieInterface>;
  onSubmit: (data: EspecieFormValues) => void;
  isLoading?: boolean;
}

export function PEspecieForm({ defaultValues, onSubmit, isLoading }: PEspecieFormProps) {
  const form = useForm<EspecieFormValues>({
    resolver: zodResolver(especieFormSchema),
    defaultValues: {
      especie: defaultValues?.especie || "",
      descricao: defaultValues?.descricao || "",
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        especie: defaultValues.especie || "",
        descricao: defaultValues.descricao || "",
      });
    }
  }, [defaultValues, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="especie"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Sigla (Espécie)</FormLabel>
              <FormControl>
                <Input placeholder="Ex: DMI" {...field} />
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
                <Input placeholder="Ex: Duplicata Mercantil por Indicação" {...field} />
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
