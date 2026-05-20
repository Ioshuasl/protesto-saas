"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { GFeriadoInterface } from "@/packages/administrativo/interfaces";
import { feriadoFormSchema, type FeriadoFormValues } from "@/packages/administrativo/schemas/GFeriado/GFeriadoFormSchema";
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
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { cn } from "@/lib/utils";
import { useEffect } from "react";

export type { FeriadoFormValues };

interface GFeriadoFormProps {
  defaultValues?: Partial<GFeriadoInterface>;
  onSubmit: (data: FeriadoFormValues & { dia: number; mes: number; ano: number }) => void;
  isLoading?: boolean;
}

export function GFeriadoForm({ defaultValues, onSubmit, isLoading }: GFeriadoFormProps) {
  const form = useForm<FeriadoFormValues>({
    resolver: zodResolver(feriadoFormSchema),
    defaultValues: {
      data: defaultValues?.data ? new Date(defaultValues.data) : undefined,
      descricao: defaultValues?.descricao || "",
      tipo: defaultValues?.tipo || "Municipal",
      situacao: defaultValues?.situacao || "Ativo",
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        data: defaultValues.data ? new Date(defaultValues.data) : undefined,
        descricao: defaultValues.descricao || "",
        tipo: defaultValues.tipo || "Municipal",
        situacao: defaultValues.situacao || "Ativo",
      });
    }
  }, [defaultValues, form]);

  const handleSubmit = (values: FeriadoFormValues) => {
    // Deriva dia, mes, ano a partir da data
    const dia = values.data.getDate();
    const mes = values.data.getMonth() + 1;
    const ano = values.data.getFullYear();

    onSubmit({
      ...values,
      dia,
      mes,
      ano,
    });
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="data"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data</FormLabel>
              <Popover>
                <FormControl>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "w-full pl-3 text-left font-normal",
                        !field.value && "text-muted-foreground"
                      )}
                    >
                      {field.value ? (
                        format(field.value, "PPP", { locale: ptBR })
                      ) : (
                        <span>Selecione uma data</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                </FormControl>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={field.value}
                    onSelect={field.onChange}
                    disabled={(date) =>
                      date < new Date("1900-01-01")
                    }
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
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
                <Input placeholder="Ex: Proclamação da República" {...field} />
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
                    <SelectItem value="Municipal">Municipal</SelectItem>
                    <SelectItem value="Estadual">Estadual</SelectItem>
                    <SelectItem value="Federal">Federal</SelectItem>
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
