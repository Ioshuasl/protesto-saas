"use client";

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
import { Toggle } from "@/components/ui/toggle";
import { cn } from "@/lib/utils";
import { PLayoutSelectObject } from "@/packages/administrativo/components/PLayout/PLayoutSelectObject";
import { PBancoInterface, PBancoSimNao } from "@/packages/administrativo/interfaces";
import { bancoFormSchema, type BancoFormValues } from "@/packages/administrativo/schemas/PBanco/PBancoFormSchema";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useId } from "react";
import { useForm } from "react-hook-form";

export type { BancoFormValues };

interface PBancoFormProps {
  defaultValues?: Partial<PBancoInterface>;
  onSubmit: (data: BancoFormValues) => void;
  isLoading?: boolean;
}

function resolvePBancoSimNao(value: PBancoSimNao | string | undefined): PBancoSimNao {
  if (value === PBancoSimNao.Sim || value === "S") return PBancoSimNao.Sim;
  if (value === PBancoSimNao.Nao || value === "N") return PBancoSimNao.Nao;
  return PBancoSimNao.Nao;
}

export function PBancoForm({ defaultValues, onSubmit, isLoading }: PBancoFormProps) {
  const apontamentoToggleId = useId();
  const custasToggleId = useId();

  const form = useForm<BancoFormValues>({
    resolver: zodResolver(bancoFormSchema),
    defaultValues: {
      codigo_banco: defaultValues?.codigo_banco || "",
      descricao: defaultValues?.descricao || "",
      layout_id: defaultValues?.layout_id && defaultValues.layout_id > 0 ? defaultValues.layout_id : 0,
      apontamento_pag_posterior: resolvePBancoSimNao(defaultValues?.apontamento_pag_posterior),
      custas_na_confirmacao: resolvePBancoSimNao(defaultValues?.custas_na_confirmacao),
    },
  });

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        codigo_banco: defaultValues.codigo_banco || "",
        descricao: defaultValues.descricao || "",
        layout_id:
          defaultValues.layout_id != null && defaultValues.layout_id > 0 ? defaultValues.layout_id : 0,
        apontamento_pag_posterior: resolvePBancoSimNao(defaultValues.apontamento_pag_posterior),
        custas_na_confirmacao: resolvePBancoSimNao(defaultValues.custas_na_confirmacao),
      });
    }
  }, [defaultValues, form]);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div
          className={cn(
            "grid grid-cols-1 gap-4",
            "lg:grid-cols-2 lg:grid-rows-2 lg:items-end lg:gap-x-6 lg:gap-y-4",
          )}
        >
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-12 sm:items-start sm:gap-4 lg:col-start-1 lg:row-start-1">
            <FormField
              control={form.control}
              name="codigo_banco"
              render={({ field }) => (
                <FormItem className="sm:col-span-3">
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
              name="descricao"
              render={({ field }) => (
                <FormItem className="sm:col-span-9">
                  <FormLabel>Descrição</FormLabel>
                  <FormControl>
                    <Input placeholder="Ex: Banco do Brasil" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={form.control}
            name="layout_id"
            render={({ field }) => (
              <FormItem className="lg:col-start-1 lg:row-start-2">
                <FormLabel>Layout</FormLabel>
                <FormControl>
                  <PLayoutSelectObject
                    value={Number(field.value ?? 0) > 0 ? String(field.value) : ""}
                    onValueChange={(value) => {
                      field.onChange(Number(value));
                    }}
                    triggerClassName={cn(
                      Number(field.value ?? 0) <= 0 &&
                        "border-amber-500/40 focus-visible:ring-amber-500/40",
                    )}
                    placeholder="Selecione o layout"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="apontamento_pag_posterior"
            render={({ field }) => (
              <FormItem className="gap-1 lg:col-start-2 lg:row-start-1">
                <FormControl>
                  <div className="flex h-9 min-h-9 max-h-9 w-full items-center justify-between gap-3 rounded-md border border-input bg-transparent px-3 shadow-xs">
                    <FormLabel
                      htmlFor={apontamentoToggleId}
                      className="!mt-0 min-w-0 flex-1 cursor-pointer truncate text-sm font-normal leading-none"
                    >
                      Apontar como pagamento posterior
                    </FormLabel>
                    <Toggle
                      id={apontamentoToggleId}
                      size="sm"
                      pressed={field.value === PBancoSimNao.Sim}
                      onPressedChange={(pressed) =>
                        field.onChange(pressed ? PBancoSimNao.Sim : PBancoSimNao.Nao)
                      }
                      className="shrink-0"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="custas_na_confirmacao"
            render={({ field }) => (
              <FormItem className="gap-1 lg:col-start-2 lg:row-start-2">
                <FormControl>
                  <div className="flex h-9 min-h-9 max-h-9 w-full items-center justify-between gap-3 rounded-md border border-input bg-transparent px-3 shadow-xs">
                    <FormLabel
                      htmlFor={custasToggleId}
                      className="!mt-0 min-w-0 flex-1 cursor-pointer truncate text-sm font-normal leading-none"
                    >
                      Custas na confirmação
                    </FormLabel>
                    <Toggle
                      id={custasToggleId}
                      size="sm"
                      pressed={field.value === PBancoSimNao.Sim}
                      onPressedChange={(pressed) =>
                        field.onChange(pressed ? PBancoSimNao.Sim : PBancoSimNao.Nao)
                      }
                      className="shrink-0"
                    />
                  </div>
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
