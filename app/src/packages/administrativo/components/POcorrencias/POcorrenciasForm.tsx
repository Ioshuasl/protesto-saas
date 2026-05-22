"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { POcorrenciasInterface } from "@/packages/administrativo/interfaces";
import {
  ocorrenciaFormSchema,
  type OcorrenciaFormValues,
} from "@/packages/administrativo/schemas/POcorrencias/POcorrenciasFormSchema";
import {
  POCORRENCIAS_TIPO_LABELS,
  POCORRENCIAS_TIPO_OPCOES,
} from "@/packages/administrativo/schemas/POcorrencias/pocorrenciasTipoConstants";
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export type { OcorrenciaFormValues };

const TIPO_NONE = "__none__";

interface POcorrenciasFormProps {
  defaultValues?: Partial<POcorrenciasInterface>;
  onSubmit: (data: OcorrenciaFormValues) => void;
  isLoading?: boolean;
}

export function POcorrenciasForm({ defaultValues, onSubmit, isLoading }: POcorrenciasFormProps) {
  const form = useForm<OcorrenciaFormValues>({
    resolver: zodResolver(ocorrenciaFormSchema),
    defaultValues: {
      codigo: defaultValues?.codigo || "",
      tipo: defaultValues?.tipo || "",
      descricao: defaultValues?.descricao || "",
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        codigo: defaultValues.codigo || "",
        tipo: defaultValues.tipo || "",
        descricao: defaultValues.descricao || "",
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
                  <Input placeholder="Ex: 1" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="tipo"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Tipo</FormLabel>
                <Select
                  value={field.value?.trim() ? field.value : TIPO_NONE}
                  onValueChange={(value) =>
                    field.onChange(value === TIPO_NONE ? "" : value)
                  }
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Opcional" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value={TIPO_NONE}>(Sem tipo)</SelectItem>
                    {POCORRENCIAS_TIPO_OPCOES.map((tipo) => (
                      <SelectItem key={tipo} value={tipo}>
                        {POCORRENCIAS_TIPO_LABELS[tipo]}
                      </SelectItem>
                    ))}
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
                <Input placeholder="Ex: Protestado" {...field} />
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
