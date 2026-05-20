"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useEffect } from "react";

export type { LivroNaturezaFormValues };

interface PLivroNaturezaFormProps {
  defaultValues?: Partial<PLivroNaturezaInterface>;
  onSubmit: (data: LivroNaturezaFormValues) => void;
  isLoading?: boolean;
}

export function PLivroNaturezaForm({ defaultValues, onSubmit, isLoading }: PLivroNaturezaFormProps) {
  const form = useForm<LivroNaturezaFormValues>({
    resolver: zodResolver(livroNaturezaFormSchema),
    defaultValues: {
      sigla: defaultValues?.sigla || "",
      descricao: defaultValues?.descricao || "",
      tipo: defaultValues?.tipo || "A",
      situacao: defaultValues?.situacao || "Ativo",
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        sigla: defaultValues.sigla || "",
        descricao: defaultValues.descricao || "",
        tipo: defaultValues.tipo || "A",
        situacao: defaultValues.situacao || "Ativo",
      });
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
                <Input placeholder="Ex: A" {...field} />
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
        
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="tipo"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tipo</FormLabel>
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="A">Apontamento</SelectItem>
                    <SelectItem value="P">Protesto</SelectItem>
                    <SelectItem value="PG">Pagamento</SelectItem>
                    <SelectItem value="C">Cancelamento</SelectItem>
                    <SelectItem value="PR">Protocolo</SelectItem>
                  </SelectContent>
                </Select>
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
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl>
                    <SelectTrigger>
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
