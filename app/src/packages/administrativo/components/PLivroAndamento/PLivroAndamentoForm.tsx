"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PLivroAndamentoInterface } from "@/packages/administrativo/interfaces";
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
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { GUsuarioSelectObject } from "@/packages/administrativo/components/GUsuario/GUsuarioSelectObject";
import { PLivroNaturezaSelectObject } from "@/packages/administrativo/components/PLivroNatureza/PLivroNaturezaSelectObject";
import { Calendar } from "@/components/ui/calendar";
import { CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { cn } from "@/lib/utils";
import { useEffect } from "react";

export type { LivroAndamentoFormValues };

interface PLivroAndamentoFormProps {
  defaultValues?: Partial<PLivroAndamentoInterface>;
  onSubmit: (data: LivroAndamentoFormValues) => void;
  isLoading?: boolean;
}

export function PLivroAndamentoForm({ 
  defaultValues, 
  onSubmit, 
  isLoading 
}: PLivroAndamentoFormProps) {
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
                    placeholder="Ex: 100"
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
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Data de Abertura</FormLabel>
                <Popover>
                  <PopoverTrigger asChild>
                    <FormControl>
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
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={field.value}
                      onSelect={field.onChange}
                      disabled={(date) =>
                        date > new Date() || date < new Date("1900-01-01")
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
            name="data_fechamento"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Data de Fechamento</FormLabel>
                <Popover>
                  <PopoverTrigger asChild>
                    <FormControl>
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
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      mode="single"
                      selected={field.value || undefined}
                      onSelect={field.onChange}
                      disabled={(date) =>
                        date > new Date() || date < new Date("1900-01-01")
                      }
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
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
