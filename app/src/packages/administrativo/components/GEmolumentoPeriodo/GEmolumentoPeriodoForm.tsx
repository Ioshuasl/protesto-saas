"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from "@/lib/utils";
import type { GEmolumentoPeriodoInterface } from "@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface";
import {
  gEmolumentoPeriodoFormSchema,
  type GEmolumentoPeriodoFormValues,
} from "@/packages/administrativo/schemas/GEmolumentoPeriodo/GEmolumentoPeriodoFormSchema";

export type { GEmolumentoPeriodoFormValues };

interface GEmolumentoPeriodoFormProps {
  defaultValues?: Partial<GEmolumentoPeriodoInterface>;
  onSubmit: (data: GEmolumentoPeriodoFormValues) => void;
  isLoading?: boolean;
}

export function GEmolumentoPeriodoForm({
  defaultValues,
  onSubmit,
  isLoading,
}: GEmolumentoPeriodoFormProps) {
  const form = useForm<GEmolumentoPeriodoFormValues>({
    resolver: zodResolver(gEmolumentoPeriodoFormSchema),
    defaultValues: {
      descricao: defaultValues?.descricao || "",
      situacao: defaultValues?.situacao === "I" ? "I" : "A",
      data_inicial: defaultValues?.data_inicial ? new Date(defaultValues.data_inicial) : undefined,
    },
  });

  useEffect(() => {
    form.reset({
      descricao: defaultValues?.descricao || "",
      situacao: defaultValues?.situacao === "I" ? "I" : "A",
      data_inicial: defaultValues?.data_inicial ? new Date(defaultValues.data_inicial) : undefined,
    });
  }, [defaultValues, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="descricao"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Descricao</FormLabel>
              <FormControl>
                <Input placeholder="Informe a descricao" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <FormField
            control={form.control}
            name="data_inicial"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Data inicial</FormLabel>
                <Popover>
                  <FormControl>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className={cn(
                          "w-full justify-start text-left font-normal",
                          !field.value && "text-muted-foreground",
                        )}
                      >
                        {field.value ? (
                          format(field.value, "dd/MM/yyyy", { locale: ptBR })
                        ) : (
                          <span>Selecione a data</span>
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
            name="situacao"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Situacao</FormLabel>
                <Select onValueChange={field.onChange} value={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione a situacao" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="A">Ativo</SelectItem>
                    <SelectItem value="I">Inativo</SelectItem>
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
