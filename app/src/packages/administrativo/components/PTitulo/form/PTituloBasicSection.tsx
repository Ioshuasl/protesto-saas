"use client";

import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { CalendarIcon } from "lucide-react";
import type { Control } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Checkbox } from "@/components/ui/checkbox";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PBancoSelectObject } from "@/packages/administrativo/components/PBanco/PBancoSelectObject";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import { PEspecieSelectObject } from "@/packages/administrativo/components/PEspecie/PEspecieSelectObject";
import { cn } from "@/lib/utils";
import { statusImportacaoOptions, tipoEndossoOptions } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailSelectOptions";
import type { PTituloDetailsFormValues, PTituloSelectOptionsByField } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { mergeTituloSelectOptions, parsePTituloIsoDate, sanitizePTituloPositiveNumber } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";

interface PTituloBasicSectionProps {
  control: Control<PTituloDetailsFormValues>;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

export function PTituloBasicSection({ control, selectOptionsByField }: PTituloBasicSectionProps) {
  return (
    <div className="space-y-3 rounded-md border p-4">
      <h3 className="text-sm font-semibold text-foreground">Dados gerais</h3>
      <div className="grid gap-3 md:grid-cols-3">
        <FormField
          control={control}
          name="numero_titulo"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Número do título</FormLabel>
              <FormControl>
                <Input
                  type="text"
                  inputMode="numeric"
                  {...field}
                  value={field.value ?? ""}
                  onChange={(event) =>
                    field.onChange(sanitizePTituloPositiveNumber(event.target.value, false))
                  }
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="numero_apontamento"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Número de apontamento</FormLabel>
              <FormControl>
                <Input
                  type="text"
                  inputMode="numeric"
                  {...field}
                  value={field.value ?? ""}
                  onChange={(event) =>
                    field.onChange(sanitizePTituloPositiveNumber(event.target.value, false))
                  }
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="numero_titulo_banco"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Número título banco</FormLabel>
              <FormControl>
                <Input type="text" {...field} value={field.value ?? ""} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="nosso_numero"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nosso número</FormLabel>
              <FormControl>
                <Input type="text" {...field} value={field.value ?? ""} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="especie_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Espécie</FormLabel>
              <FormControl>
                <PEspecieSelectObject
                  value={field.value}
                  onValueChange={field.onChange}
                  placeholder="Selecione a espécie"
                  optionsOverride={selectOptionsByField?.especie_id}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="ocorrencia_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Ocorrência</FormLabel>
              <FormControl>
                <POcorrenciasSelectObject
                  value={field.value}
                  onValueChange={field.onChange}
                  placeholder="Selecione a ocorrência"
                  optionsOverride={selectOptionsByField?.ocorrencia_id}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="banco_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Banco</FormLabel>
              <FormControl>
                <PBancoSelectObject
                  value={field.value}
                  onValueChange={field.onChange}
                  placeholder="Selecione o banco"
                  optionsOverride={selectOptionsByField?.banco_id}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="tipo_endosso"
          render={({ field }) => {
            const merged = mergeTituloSelectOptions("tipo_endosso", tipoEndossoOptions, selectOptionsByField);
            const selected = merged.find((option) => option.value === (field.value || ""));
            return (
              <FormItem>
                <FormLabel>Tipo de endosso</FormLabel>
                <Select value={field.value || ""} onValueChange={field.onChange}>
                  <FormControl>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Selecione o tipo de endosso">{selected?.label}</SelectValue>
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {merged.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            );
          }}
        />
        <FormField
          control={control}
          name="status_importacao"
          render={({ field }) => {
            const merged = mergeTituloSelectOptions(
              "status_importacao",
              statusImportacaoOptions,
              selectOptionsByField,
            );
            const selected = merged.find((option) => option.value === (field.value || ""));
            return (
              <FormItem>
                <FormLabel>Status de importação</FormLabel>
                <Select value={field.value || ""} onValueChange={field.onChange}>
                  <FormControl>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Selecione o status de importação">{selected?.label}</SelectValue>
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {merged.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            );
          }}
        />
        <FormField
          control={control}
          name="data_emissao_titulo"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data de emissão do título</FormLabel>
              <Popover>
                <FormControl>
                  <PopoverTrigger asChild>
                    <Button
                      type="button"
                      variant="outline"
                      className={cn(
                        "w-full justify-between text-left font-normal",
                        !field.value && "text-muted-foreground",
                      )}
                    >
                      {field.value
                        ? format(parsePTituloIsoDate(String(field.value))!, "dd/MM/yyyy", { locale: ptBR })
                        : "Selecionar data"}
                      <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                    </Button>
                  </PopoverTrigger>
                </FormControl>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={parsePTituloIsoDate(String(field.value ?? ""))}
                    onSelect={(date) => field.onChange(date ? format(date, "yyyy-MM-dd") : "")}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="data_vencimento_titulo"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data de vencimento do título</FormLabel>
              <Popover>
                <FormControl>
                  <PopoverTrigger asChild>
                    <Button
                      type="button"
                      variant="outline"
                      className={cn(
                        "w-full justify-between text-left font-normal",
                        !field.value && "text-muted-foreground",
                      )}
                    >
                      {field.value
                        ? format(parsePTituloIsoDate(String(field.value))!, "dd/MM/yyyy", { locale: ptBR })
                        : "Selecionar data"}
                      <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                    </Button>
                  </PopoverTrigger>
                </FormControl>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={parsePTituloIsoDate(String(field.value ?? ""))}
                    onSelect={(date) => field.onChange(date ? format(date, "yyyy-MM-dd") : "")}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="data_cadastro"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Data de cadastro</FormLabel>
              <Popover>
                <FormControl>
                  <PopoverTrigger asChild>
                    <Button
                      type="button"
                      variant="outline"
                      className={cn(
                        "w-full justify-between text-left font-normal",
                        !field.value && "text-muted-foreground",
                      )}
                    >
                      {field.value
                        ? format(parsePTituloIsoDate(String(field.value))!, "dd/MM/yyyy", { locale: ptBR })
                        : "Selecionar data"}
                      <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                    </Button>
                  </PopoverTrigger>
                </FormControl>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={parsePTituloIsoDate(String(field.value ?? ""))}
                    onSelect={(date) => field.onChange(date ? format(date, "yyyy-MM-dd") : "")}
                  />
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="observacoes"
          render={({ field }) => (
            <FormItem className="md:col-span-3">
              <FormLabel>Observações</FormLabel>
              <FormControl>
                <Input type="text" {...field} value={field.value ?? ""} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="titulo_antigo"
          render={({ field }) => {
            const checked = field.value === "S" || field.value === "true" || field.value === "1";
            return (
              <FormItem>
                <FormLabel>Título antigo</FormLabel>
                <FormControl>
                  <div className="flex h-10 items-center gap-2 rounded-md border px-3">
                    <Checkbox checked={checked} onCheckedChange={(value) => field.onChange(value ? "S" : "N")} />
                    <span className="text-sm text-muted-foreground">{checked ? "Sim" : "Não"}</span>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            );
          }}
        />
      </div>
    </div>
  );
}
