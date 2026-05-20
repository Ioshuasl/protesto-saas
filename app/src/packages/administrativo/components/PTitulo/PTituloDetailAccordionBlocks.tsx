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
import { cn } from "@/lib/utils";
import { GUsuarioSelectObject } from "@/packages/administrativo/components/GUsuario/GUsuarioSelectObject";
import { PMotivosSelectObject } from "@/packages/administrativo/components/PMotivos/PMotivosSelectObject";
import { PMotivosCancelamentoSelectObject } from "@/packages/administrativo/components/PMotivosCancelamento/PMotivosCancelamentoSelectObject";
import { PLivroAndamentoSelectObject } from "@/packages/administrativo/components/PLivroAndamento/PLivroAndamentoSelectObject";
import {
  tituloBooleanSelectOptions,
  tituloTipoAceiteSelectOptions,
  type PTituloDetailsFormValues,
  type PTituloSelectOptionsByField,
} from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { mergeTituloSelectOptions, parsePTituloIsoDate, sanitizePTituloPositiveNumber } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";

type TituloControl = Control<PTituloDetailsFormValues>;

interface BlockProps {
  control: TituloControl;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

export function PTituloDetailFieldsApontamento({ control, selectOptionsByField }: BlockProps) {
  return (
    <>
      <FormField
        control={control}
        name="data_apontamento"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de apontamento</FormLabel>
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
        name="motivo_apontamento_id"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Motivo de apontamento</FormLabel>
            <FormControl>
              <PMotivosSelectObject
                value={field.value}
                onValueChange={field.onChange}
                placeholder="Selecione o motivo de apontamento"
                optionsOverride={selectOptionsByField?.motivo_apontamento_id}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="folha_apontamento"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Folha de apontamento</FormLabel>
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
        name="livro_id_apontamento"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Livro de apontamento</FormLabel>
            <FormControl>
              <PLivroAndamentoSelectObject value={field.value} onValueChange={field.onChange} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="user_assina_apont"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Usuário assina apontamento</FormLabel>
            <FormControl>
              <GUsuarioSelectObject value={field.value} onValueChange={field.onChange} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="prazo"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Prazo</FormLabel>
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
        name="numero_livro_apont"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Número livro apontamento</FormLabel>
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
    </>
  );
}

export function PTituloDetailFieldsIntimacaoAceite({ control, selectOptionsByField }: BlockProps) {
  return (
    <>
      <FormField
        control={control}
        name="data_aceite"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de aceite</FormLabel>
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
        name="data_intimacao"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de intimação</FormLabel>
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
        name="data_vencimento_boleto"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data vencimento boleto</FormLabel>
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
        name="pessoa_aceitou"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Pessoa aceitou</FormLabel>
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
      <FormField
        control={control}
        name="motivo_isencao"
        render={({ field }) => {
          const merged = mergeTituloSelectOptions("motivo_isencao", tituloBooleanSelectOptions, selectOptionsByField);
          const selected = merged.find((option) => option.value === (field.value || ""));
          return (
            <FormItem>
              <FormLabel>Motivo de isenção</FormLabel>
              <Select value={field.value || ""} onValueChange={field.onChange}>
                <FormControl>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Selecione">{selected?.label}</SelectValue>
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
        name="tipo_aceite"
        render={({ field }) => {
          const merged = mergeTituloSelectOptions("tipo_aceite", tituloTipoAceiteSelectOptions, selectOptionsByField);
          const selected = merged.find((option) => option.value === (field.value || ""));
          return (
            <FormItem>
              <FormLabel>Tipo de aceite</FormLabel>
              <Select value={field.value || ""} onValueChange={field.onChange}>
                <FormControl>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Selecione o tipo de aceite">{selected?.label}</SelectValue>
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
        name="agencia_codigo_cedente"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Agência código cedente</FormLabel>
            <FormControl>
              <Input type="text" {...field} value={field.value ?? ""} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </>
  );
}

export function PTituloDetailFieldsProtesto({ control }: Pick<BlockProps, "control">) {
  return (
    <>
      <FormField
        control={control}
        name="data_protesto"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de protesto</FormLabel>
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
        name="user_assina_prot"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Usuário assina protesto</FormLabel>
            <FormControl>
              <GUsuarioSelectObject value={field.value} onValueChange={field.onChange} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="livro_id_protesto"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Livro de protesto</FormLabel>
            <FormControl>
              <PLivroAndamentoSelectObject value={field.value} onValueChange={field.onChange} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="folha_protesto"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Folha de protesto</FormLabel>
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
        name="numero_protesto"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Número de protesto</FormLabel>
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
        name="cobrar_juros"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Cobrar juros</FormLabel>
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
      <FormField
        control={control}
        name="letra_folha"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Letra folha</FormLabel>
            <FormControl>
              <Input type="text" {...field} value={field.value ?? ""} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </>
  );
}

export function PTituloDetailFieldsCancelamentoPagamento({ control, selectOptionsByField }: BlockProps) {
  return (
    <>
      <FormField
        control={control}
        name="data_cancelamento"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de cancelamento</FormLabel>
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
        name="motivo_cancelamento"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Motivo de cancelamento</FormLabel>
            <FormControl>
              <PMotivosCancelamentoSelectObject
                value={field.value}
                onValueChange={field.onChange}
                placeholder="Selecione o motivo de cancelamento"
                optionsOverride={selectOptionsByField?.motivo_cancelamento}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="data_sustado"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de sustado</FormLabel>
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
        name="data_pago"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de pago</FormLabel>
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
        name="data_desistencia"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de desistência</FormLabel>
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
        name="numero_cancelamento"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Número de cancelamento</FormLabel>
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
    </>
  );
}

export function PTituloDetailFieldsCra({ control }: BlockProps) {
  return (
    <FormField
      control={control}
      name="chave_importacao"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Chave de importação</FormLabel>
          <FormControl>
            <Input type="text" {...field} value={field.value ?? ""} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

export function PTituloDetailFieldsCenprot({ control }: BlockProps) {
  return (
    <>
      <FormField
        control={control}
        name="data_anuencia"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data de anuência</FormLabel>
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
        name="apresentante_permitido"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Apresentante permitido</FormLabel>
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
      <FormField
        control={control}
        name="cedente_permitido"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Cedente permitido</FormLabel>
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
      <FormField
        control={control}
        name="credor_permitido"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Credor permitido</FormLabel>
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
      <FormField
        control={control}
        name="anuencia"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Anuência</FormLabel>
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
      <FormField
        control={control}
        name="chave_unica_cenprot"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Chave única CENPROT</FormLabel>
            <FormControl>
              <Input type="text" {...field} value={field.value ?? ""} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={control}
        name="protesto_artigo_9"
        render={({ field }) => {
          const checked = field.value === "S" || field.value === "true" || field.value === "1";
          return (
            <FormItem>
              <FormLabel>Protesto artigo 9</FormLabel>
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
    </>
  );
}

export function PTituloDetailFieldsSerasa({ control }: BlockProps) {
  return (
    <>
      <FormField
        control={control}
        name="data_env_serasa"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data envio SERASA</FormLabel>
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
        name="data_ret_serasa"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data retorno SERASA</FormLabel>
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
        name="data_mov_serasa"
        render={({ field }) => (
          <FormItem className="flex flex-col">
            <FormLabel>Data movimentação SERASA</FormLabel>
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
    </>
  );
}
