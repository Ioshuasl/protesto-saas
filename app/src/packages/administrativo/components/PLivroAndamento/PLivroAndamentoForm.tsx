"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PLivroAndamentoInterface, PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";
import { useProximoNumeroPorNatureza } from "@/packages/administrativo/hooks/PLivroAndamento/useProximoNumeroPorNatureza";
import {
  livroAndamentoFormSchema,
  type LivroAndamentoFormValues,
} from "@/packages/administrativo/schemas/PLivroAndamento/PLivroAndamentoFormSchema";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { DatePicker } from "@/components/ui/date-picker";
import { Input } from "@/components/ui/input";
import { GUsuarioSelectObject } from "@/packages/administrativo/components/GUsuario/GUsuarioSelectObject";
import { PLivroNaturezaSelectObject } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaSelectObject";
import { useEffect, useMemo } from "react";

function isLivroDateDisabled(date: Date) {
  return date > new Date() || date < new Date("1900-01-01");
}

export type { LivroAndamentoFormValues };

interface PLivroAndamentoFormProps {
  defaultValues?: Partial<PLivroAndamentoInterface>;
  naturezas?: PLivroNaturezaInterface[];
  onSubmit: (data: LivroAndamentoFormValues) => void;
  isLoading?: boolean;
}

export function PLivroAndamentoForm({
  defaultValues,
  naturezas = [],
  onSubmit,
  isLoading,
}: PLivroAndamentoFormProps) {
  const isEditing = !!defaultValues?.livro_andamento_id;

  const naturezaIds = useMemo(
    () =>
      naturezas
        .map((n) => n.livro_natureza_id)
        .filter((id): id is number => id != null && id > 0),
    [naturezas],
  );

  const { proximoNumeroPorNatureza, isLoadingProximos } = useProximoNumeroPorNatureza(
    naturezaIds,
    !isEditing,
  );

  const form = useForm<LivroAndamentoFormValues>({
    resolver: zodResolver(livroAndamentoFormSchema),
    defaultValues: {
      numero_livro: defaultValues?.numero_livro || 0,
      livro_natureza_id: defaultValues?.livro_natureza_id || 0,
      folha_atual: defaultValues?.folha_atual || 0,
      numero_folhas: defaultValues?.numero_folhas || 0,
      data_abertura: defaultValues?.data_abertura ? new Date(defaultValues.data_abertura) : undefined,
      data_fechamento: defaultValues?.data_fechamento ? new Date(defaultValues.data_fechamento) : undefined,
      sigla: defaultValues?.sigla || "",
      usuario_id: defaultValues?.usuario_id || undefined,
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        numero_livro: defaultValues.numero_livro || 0,
        livro_natureza_id: defaultValues.livro_natureza_id || 0,
        folha_atual: defaultValues.folha_atual || 0,
        numero_folhas: defaultValues.numero_folhas || 0,
        data_abertura: defaultValues.data_abertura ? new Date(defaultValues.data_abertura) : undefined,
        data_fechamento: defaultValues.data_fechamento ? new Date(defaultValues.data_fechamento) : undefined,
        sigla: defaultValues.sigla || "",
        usuario_id: defaultValues.usuario_id || undefined,
      });
    }
  }, [defaultValues, form]);

  const livroNaturezaId = form.watch("livro_natureza_id");
  const proximoNumeroAtual =
    livroNaturezaId > 0 ? proximoNumeroPorNatureza[livroNaturezaId] : undefined;

  const numeroLivroPlaceholder =
    proximoNumeroAtual != null
      ? String(proximoNumeroAtual)
      : isLoadingProximos
        ? "Carregando sugestão..."
        : "Ex: 100";

  useEffect(() => {
    if (!livroNaturezaId || livroNaturezaId < 1) return;
    const natureza = naturezas.find((n) => n.livro_natureza_id === livroNaturezaId);
    if (natureza?.sigla) {
      form.setValue("sigla", natureza.sigla);
    }
  }, [livroNaturezaId, naturezas, form]);

  useEffect(() => {
    if (isEditing || !livroNaturezaId || livroNaturezaId < 1) return;
    const sugerido = proximoNumeroPorNatureza[livroNaturezaId];
    if (sugerido == null) return;
    form.setValue("numero_livro", sugerido, { shouldValidate: true });
  }, [livroNaturezaId, proximoNumeroPorNatureza, isEditing, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
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
            name="numero_livro"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Nº do Livro</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    placeholder={numeroLivroPlaceholder}
                    name={field.name}
                    ref={field.ref}
                    onBlur={field.onBlur}
                    value={field.value ?? ""}
                    onChange={(e) => {
                      const raw = e.target.value;
                      field.onChange(raw === "" ? 0 : Number(raw));
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="livro_natureza_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Natureza do Livro</FormLabel>
                <FormControl>
                  <PLivroNaturezaSelectObject
                    value={field.value ? field.value.toString() : undefined}
                    onValueChange={(value) => field.onChange(Number(value))}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="usuario_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Usuário Responsável</FormLabel>
                <FormControl>
                  <GUsuarioSelectObject
                    value={field.value ? field.value.toString() : undefined}
                    onValueChange={(value) => field.onChange(Number(value))}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="folha_atual"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Folha Atual</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    placeholder="Ex: 1"
                    name={field.name}
                    ref={field.ref}
                    onBlur={field.onBlur}
                    value={field.value ?? ""}
                    onChange={(e) => {
                      const raw = e.target.value;
                      field.onChange(raw === "" ? 0 : Number(raw));
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="numero_folhas"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Número de Folhas</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    placeholder="Ex: 300"
                    name={field.name}
                    ref={field.ref}
                    onBlur={field.onBlur}
                    value={field.value ?? ""}
                    onChange={(e) => {
                      const raw = e.target.value;
                      field.onChange(raw === "" ? 0 : Number(raw));
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="data_abertura"
            render={({ field, fieldState }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Data de Abertura</FormLabel>
                <FormControl>
                  <DatePicker
                    variant="hybrid"
                    value={field.value}
                    onChange={field.onChange}
                    calendarDisabled={isLivroDateDisabled}
                    placeholder="dd/mm/aaaa"
                    aria-invalid={!!fieldState.error}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="data_fechamento"
            render={({ field, fieldState }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Data de Fechamento</FormLabel>
                <FormControl>
                  <DatePicker
                    variant="hybrid"
                    value={field.value ?? undefined}
                    onChange={field.onChange}
                    calendarDisabled={isLivroDateDisabled}
                    placeholder="dd/mm/aaaa"
                    aria-invalid={!!fieldState.error}
                  />
                </FormControl>
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
