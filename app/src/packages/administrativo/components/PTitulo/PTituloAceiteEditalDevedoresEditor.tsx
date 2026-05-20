"use client";

import { CalendarIcon } from "lucide-react";
import type { Control } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { PTituloShowDevedoresItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloShowDevedoresItem";
import { tituloTipoAceiteSelectOptions } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import type { PTituloAceiteEditalFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloAceiteEditalSchema";
import { FormatDateTime } from "@/shared/actions/dateTime/FormatDateTime";
import {
  getTodayLocalIsoDateOnly,
  parseLocalIsoDateOnly,
  toLocalIsoDateOnly,
} from "@/shared/actions/dateTime/LocalDateOnly";
import { cn } from "@/lib/utils";

interface PTituloAceiteEditalDevedoresEditorProps {
  control: Control<PTituloAceiteEditalFormValues>;
  devedores: PTituloShowDevedoresItem[];
  isLoading?: boolean;
}

export function PTituloAceiteEditalDevedoresEditor({
  control,
  devedores,
  isLoading,
}: PTituloAceiteEditalDevedoresEditorProps) {
  if (isLoading) {
    return (
      <div className="w-full flex items-center justify-center rounded-md border p-6 text-muted-foreground">
        Carregando devedores...
      </div>
    );
  }

  if (devedores.length === 0) {
    return (
      <div className="w-full flex items-center justify-center rounded-md border p-6 text-muted-foreground">
        Nenhum devedor encontrado para este título.
      </div>
    );
  }

  return (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="min-w-[320px]">Devedor</TableHead>
            <TableHead className="min-w-[150px]">CPF/CNPJ</TableHead>
            <TableHead className="w-[170px]">Aceite ou Edital</TableHead>
            <TableHead className="w-[190px]">Data do aceite/edital</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {devedores.map((devedor, index) => (
            <TableRow key={devedor.pessoa_vinculo_id}>
              <TableCell className="font-medium">
                <span className="block truncate">{devedor.devedor_nome ?? "Devedor sem nome"}</span>
              </TableCell>
              <TableCell>{devedor.devedor_cpfcnpj ?? "Documento não informado"}</TableCell>
              <TableCell>
                <FormField
                  control={control}
                  name={`devedores.${index}.devedor_tipo_aceite`}
                  render={({ field }) => (
                    <FormItem>
                      <FormControl>
                        <Select value={field.value} onValueChange={field.onChange}>
                          <SelectTrigger
                            className={cn(!field.value && "border-amber-500/40 focus-visible:ring-amber-500/40")}
                          >
                            <SelectValue placeholder="Selecione" />
                          </SelectTrigger>
                          <SelectContent>
                            {tituloTipoAceiteSelectOptions.map((option) => (
                              <SelectItem key={option.value} value={option.value}>
                                {option.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </TableCell>
              <TableCell>
                <FormField
                  control={control}
                  name={`devedores.${index}.devedor_data_aceite`}
                  render={({ field }) => {
                    const selectedDate =
                      typeof field.value === "string" && field.value.length > 0
                        ? parseLocalIsoDateOnly(field.value)
                        : undefined;
                    return (
                      <FormItem>
                        <Popover>
                          <FormControl>
                            <PopoverTrigger asChild>
                              <Button
                                type="button"
                                variant="outline"
                                className={cn(
                                  "w-full justify-between text-left font-normal",
                                  !selectedDate && "text-muted-foreground border-amber-500/40",
                                )}
                              >
                                {selectedDate ? FormatDateTime(selectedDate) : "Selecionar data"}
                                <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                              </Button>
                            </PopoverTrigger>
                          </FormControl>
                          <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                              mode="single"
                              selected={selectedDate}
                              onSelect={(date) =>
                                field.onChange(date ? toLocalIsoDateOnly(date) : getTodayLocalIsoDateOnly())
                              }
                            />
                          </PopoverContent>
                        </Popover>
                        <FormMessage />
                      </FormItem>
                    );
                  }}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

