"use client";

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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { consultarCep, consultarCnpj } from "@/functions";
import { cn } from "@/lib/utils";
import { PPessoaInterface } from "@/packages/administrativo/interfaces";
import {
  pessoaFormSchema,
  type PessoaFormSchemaValues,
  type PessoaFormValues,
} from "@/packages/administrativo/schemas/PPessoa/PPessoaFormSchema";
import { zodResolver } from "@hookform/resolvers/zod";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { CalendarIcon, CircleHelp } from "lucide-react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";

const MICRO_EMPRESA_MEI_INFO_MARKDOWN = `- **Cancelamento por MEI/ME/EPP:** Quando o credor for MEI, Microempresa ou Empresa de Pequeno Porte (conforme a Lei Complementar Federal nº 123/2006), o cancelamento do registro de protesto poderá ser solicitado com benefícios específicos de custas, dependendo da comprovação da situação da empresa.`;

const formatDocumento = (value: string, tipoPessoa: "F" | "J") => {
  const v = value.replace(/\D/g, "");
  if (tipoPessoa === "F") {
    return v
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d{1,2})$/, "$1-$2")
      .slice(0, 14);
  } else {
    return v
      .replace(/^(\d{2})(\d)/, "$1.$2")
      .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
      .replace(/\.(\d{3})(\d)/, ".$1/$2")
      .replace(/(\d{4})(\d)/, "$1-$2")
      .slice(0, 18);
  }
};

const formatCep = (value: string) => {
  return value
    .replace(/\D/g, "")
    .replace(/(\d{5})(\d)/, "$1-$2")
    .slice(0, 9);
};

const formatTelefone = (value: string) => {
  const v = value.replace(/\D/g, "");
  if (v.length <= 10) {
    return v
      .replace(/(\d{2})(\d)/, "($1) $2")
      .replace(/(\d{4})(\d)/, "$1-$2")
      .slice(0, 14);
  } else {
    return v
      .replace(/(\d{2})(\d)/, "($1) $2")
      .replace(/(\d{5})(\d)/, "$1-$2")
      .slice(0, 15);
  }
};

export type { PessoaFormValues };

interface PPessoaFormProps {
  defaultValues?: Partial<PPessoaInterface>;
  onSubmit: (data: PessoaFormValues) => void;
  isLoading?: boolean;
}

export function PPessoaForm({ defaultValues, onSubmit, isLoading }: PPessoaFormProps) {
  const defaultTipoPessoa: "F" | "J" =
    defaultValues?.cpfcnpj?.replace(/\D/g, "").length === 14 ? "J" : "F";

  const form = useForm<PessoaFormSchemaValues>({
    resolver: zodResolver(pessoaFormSchema),
    defaultValues: {
      tipo_pessoa: defaultTipoPessoa,
      cpfcnpj: defaultValues?.cpfcnpj || "",
      nome: defaultValues?.nome || "",
      rg: defaultValues?.rg || "",
      nacionalidade: defaultValues?.nacionalidade || "",
      estado_civil_id: defaultValues?.estado_civil_id || undefined,
      data_nascimento: defaultValues?.data_nascimento ? new Date(defaultValues.data_nascimento) : undefined,
      nome_fantasia: defaultValues?.nome_fantasia || "",
      cod_cra: defaultValues?.cod_cra || "",
      micro_empresa: defaultValues?.micro_empresa || "N",
      cep: defaultValues?.cep || "",
      endereco: defaultValues?.endereco || "",
      bairro: defaultValues?.bairro || "",
      cidade: defaultValues?.cidade || "",
      uf: defaultValues?.uf || "",
      telefone: defaultValues?.telefone || "",
      email: defaultValues?.email || "",
      banco: defaultValues?.banco || "",
      nome_banco: defaultValues?.nome_banco || "",
      agencia: defaultValues?.agencia || "",
      conta: defaultValues?.conta || "",
      cidade_agencia: defaultValues?.cidade_agencia || "",
      observacoes: defaultValues?.observacoes || "",
    },
  });

  const tipoPessoa = form.watch("tipo_pessoa");
  const isPessoaJuridica = tipoPessoa === "J";
  const documentoPlaceholder = isPessoaJuridica ? "00.000.000/0000-00" : "000.000.000-00";
  const [isFetchingCnpj, setIsFetchingCnpj] = useState(false);
  const [isFetchingCep, setIsFetchingCep] = useState(false);
  const [meiInfoOpen, setMeiInfoOpen] = useState(false);

  useEffect(() => {
    if (defaultValues) {
      form.reset({
        tipo_pessoa: defaultValues.cpfcnpj?.replace(/\D/g, "").length === 14 ? "J" : "F",
        cpfcnpj: defaultValues.cpfcnpj || "",
        nome: defaultValues.nome || "",
        rg: defaultValues.rg || "",
        nacionalidade: defaultValues.nacionalidade || "",
        estado_civil_id: defaultValues.estado_civil_id || undefined,
        data_nascimento: defaultValues.data_nascimento ? new Date(defaultValues.data_nascimento) : undefined,
        nome_fantasia: defaultValues.nome_fantasia || "",
        cod_cra: defaultValues.cod_cra || "",
        micro_empresa: defaultValues.micro_empresa || "N",
        cep: defaultValues.cep || "",
        endereco: defaultValues.endereco || "",
        bairro: defaultValues.bairro || "",
        cidade: defaultValues.cidade || "",
        uf: defaultValues.uf || "",
        telefone: defaultValues.telefone || "",
        email: defaultValues.email || "",
        banco: defaultValues.banco || "",
        nome_banco: defaultValues.nome_banco || "",
        agencia: defaultValues.agencia || "",
        conta: defaultValues.conta || "",
        cidade_agencia: defaultValues.cidade_agencia || "",
        observacoes: defaultValues.observacoes || "",
      });
    }
  }, [defaultValues, form]);

  const handleSubmit = (data: PessoaFormSchemaValues) => {
    const { tipo_pessoa: _tipoPessoa, ...payload } = data;
    onSubmit(payload);
  };

  const parseBrDate = (value?: string): Date | undefined => {
    if (!value) return undefined;
    const [day, month, year] = value.split("/");
    if (!day || !month || !year) return undefined;
    const parsed = new Date(Number(year), Number(month) - 1, Number(day));
    return Number.isNaN(parsed.getTime()) ? undefined : parsed;
  };

  const handleConsultarCnpj = async () => {
    if (tipoPessoa !== "J") return;

    const cnpjAtual = form.getValues("cpfcnpj") ?? "";
    const cnpjLimpo = cnpjAtual.replace(/\D/g, "");
    if (cnpjLimpo.length !== 14) return;

    setIsFetchingCnpj(true);
    try {
      const data = await consultarCnpj(cnpjLimpo);

      if (data.nome) form.setValue("nome", data.nome, { shouldDirty: true });
      if (data.fantasia) form.setValue("nome_fantasia", data.fantasia, { shouldDirty: true });
      if (data.email) form.setValue("email", data.email, { shouldDirty: true });
      if (data.telefone) form.setValue("telefone", formatTelefone(data.telefone), { shouldDirty: true });
      if (data.cep) form.setValue("cep", formatCep(data.cep), { shouldDirty: true });
      if (data.logradouro) form.setValue("endereco", data.logradouro, { shouldDirty: true });
      if (data.bairro) form.setValue("bairro", data.bairro, { shouldDirty: true });
      if (data.municipio) form.setValue("cidade", data.municipio, { shouldDirty: true });
      if (data.uf) form.setValue("uf", data.uf, { shouldDirty: true });
      if (data.abertura) {
        const abertura = parseBrDate(data.abertura);
        if (abertura) form.setValue("data_nascimento", abertura, { shouldDirty: true });
      }

      if (typeof data.simei?.optante === "boolean") {
        form.setValue("micro_empresa", data.simei.optante ? "S" : "N", { shouldDirty: true });

        if (data.simei.optante) {
          const observacoesAtual = form.getValues("observacoes") || "";
          if (!observacoesAtual.toLowerCase().includes("mei")) {
            const prefixo = observacoesAtual ? `${observacoesAtual}\n` : "";
            form.setValue("observacoes", `${prefixo}Enquadramento consultado: optante pelo SIMEI (MEI).`, {
              shouldDirty: true,
            });
          }
        }
      }
    } catch (error) {
      console.error("Erro ao consultar CNPJ:", error);
    } finally {
      setIsFetchingCnpj(false);
    }
  };

  const handleConsultarCep = async () => {
    const cepAtual = form.getValues("cep") ?? "";
    const cepLimpo = cepAtual.replace(/\D/g, "");
    if (cepLimpo.length !== 8) return;

    setIsFetchingCep(true);
    try {
      const data = await consultarCep(cepLimpo);
      if (data.logradouro) form.setValue("endereco", data.logradouro, { shouldDirty: true });
      if (data.bairro) form.setValue("bairro", data.bairro, { shouldDirty: true });
      if (data.localidade) form.setValue("cidade", data.localidade, { shouldDirty: true });
      if (data.uf) form.setValue("uf", data.uf, { shouldDirty: true });
    } catch (error) {
      console.error("Erro ao consultar CEP:", error);
    } finally {
      setIsFetchingCep(false);
    }
  };

  return (
    <>
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <Tabs defaultValue="basicos" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="basicos">Dados Básicos</TabsTrigger>
            <TabsTrigger value="bancarios">Dados Bancários</TabsTrigger>
          </TabsList>

          <TabsContent value="basicos" className="space-y-4 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="tipo_pessoa"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Tipo de Pessoa</FormLabel>
                    <Select
                      onValueChange={(value) => {
                        field.onChange(value as "F" | "J");
                        form.setValue("cpfcnpj", "");
                      }}
                      value={field.value}
                    >
                      {(() => {
                        const tipoPessoaLabel =
                          field.value === "F" ? "Pessoa Física" : field.value === "J" ? "Pessoa Jurídica" : undefined;
                        return (
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione">{tipoPessoaLabel}</SelectValue>
                        </SelectTrigger>
                      </FormControl>
                        );
                      })()}
                      <SelectContent>
                        <SelectItem value="F">Pessoa Física</SelectItem>
                        <SelectItem value="J">Pessoa Jurídica</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="cpfcnpj"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>{isPessoaJuridica ? "CNPJ" : "CPF"}</FormLabel>
                    <FormControl>
                      <Input
                        placeholder={documentoPlaceholder}
                        {...field}
                        onChange={(e) => field.onChange(formatDocumento(e.target.value, tipoPessoa))}
                        onBlur={handleConsultarCnpj}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              {!isPessoaJuridica && (
                <FormField
                  control={form.control}
                  name="nome"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nome Completo</FormLabel>
                      <FormControl>
                        <Input placeholder="Nome Completo" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}
            </div>

            {isPessoaJuridica && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="nome"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Razão Social</FormLabel>
                      <FormControl>
                        <Input placeholder="Razão Social" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="nome_fantasia"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nome Fantasia</FormLabel>
                      <FormControl>
                        <Input placeholder="Nome Fantasia" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            )}

            {!isPessoaJuridica && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="rg"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>RG</FormLabel>
                      <FormControl>
                        <Input placeholder="RG" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="nacionalidade"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Nacionalidade</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: Brasileiro" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="estado_civil_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Estado Civil</FormLabel>
                      <Select
                        onValueChange={(value) => field.onChange(Number(value))}
                        value={field.value ? field.value.toString() : ""}
                      >
                        {(() => {
                          const estadoCivilMap: Record<string, string> = {
                            "1": "Solteiro(a)",
                            "2": "Casado(a)",
                            "3": "Divorciado(a)",
                            "4": "Viúvo(a)",
                          };
                          return (
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Selecione">
                              {field.value ? estadoCivilMap[field.value.toString()] : undefined}
                            </SelectValue>
                          </SelectTrigger>
                        </FormControl>
                          );
                        })()}
                        <SelectContent>
                          <SelectItem value="1">Solteiro(a)</SelectItem>
                          <SelectItem value="2">Casado(a)</SelectItem>
                          <SelectItem value="3">Divorciado(a)</SelectItem>
                          <SelectItem value="4">Viúvo(a)</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="data_nascimento"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>Data de Nascimento</FormLabel>
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
            )}

            {isPessoaJuridica && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="micro_empresa"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="flex items-center gap-1.5">
                        <span>MicroEmpresa (MEI)</span>
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="size-6 shrink-0 text-muted-foreground hover:text-foreground"
                          aria-label="Informações sobre MicroEmpresa (MEI)"
                          onClick={() => setMeiInfoOpen(true)}
                        >
                          <CircleHelp className="size-4" />
                        </Button>
                      </FormLabel>
                      <Select onValueChange={field.onChange} value={field.value}>
                        {(() => {
                          const microEmpresaLabel =
                            field.value === "S" ? "Sim" : field.value === "N" ? "Não" : undefined;
                          return (
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Selecione">{microEmpresaLabel}</SelectValue>
                          </SelectTrigger>
                        </FormControl>
                          );
                        })()}
                        <SelectContent>
                          <SelectItem value="S">Sim</SelectItem>
                          <SelectItem value="N">Não</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            )}
            <div className="space-y-4 pt-2">
              <h3 className="text-sm font-medium text-foreground">Endereço & Contato</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <FormField
                control={form.control}
                name="cep"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>CEP</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="00000-000"
                        {...field}
                        onChange={(e) => field.onChange(formatCep(e.target.value))}
                        onBlur={handleConsultarCep}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="endereco"
                render={({ field }) => (
                  <FormItem className="md:col-span-2">
                    <FormLabel>Endereço</FormLabel>
                    <FormControl>
                      <Input placeholder="Rua, Avenida, etc." {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <FormField
                control={form.control}
                name="bairro"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Bairro</FormLabel>
                    <FormControl>
                      <Input placeholder="Bairro" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="cidade"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Cidade</FormLabel>
                    <FormControl>
                      <Input placeholder="Cidade" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="uf"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>UF</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="UF" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"].map((uf) => (
                          <SelectItem key={uf} value={uf}>{uf}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="telefone"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Telefone</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="(00) 00000-0000"
                        {...field}
                        onChange={(e) => field.onChange(formatTelefone(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>E-mail</FormLabel>
                    <FormControl>
                      <Input type="email" placeholder="email@exemplo.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            </div>
          </TabsContent>

          <TabsContent value="bancarios" className="space-y-4 mt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="banco"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Código do Banco</FormLabel>
                    <FormControl>
                      <Input placeholder="Ex: 001" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="nome_banco"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nome do Banco</FormLabel>
                    <FormControl>
                      <Input placeholder="Ex: Banco do Brasil" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="agencia"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Agência</FormLabel>
                    <FormControl>
                      <Input placeholder="Agência" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="conta"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Conta</FormLabel>
                    <FormControl>
                      <Input placeholder="Conta" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="cidade_agencia"
                render={({ field }) => (
                  <FormItem className="md:col-span-2">
                    <FormLabel>Cidade da Agência</FormLabel>
                    <FormControl>
                      <Input placeholder="Cidade da Agência" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </TabsContent>
        </Tabs>

        <div className="flex justify-end pt-4">
          <Button
            type="submit"
            disabled={isLoading || isFetchingCnpj || isFetchingCep}
            className="bg-[#FF6B00] hover:bg-[#E56000] text-white"
          >
            {isLoading ? "Salvando..." : isFetchingCnpj ? "Consultando CNPJ..." : isFetchingCep ? "Consultando CEP..." : "Salvar"}
          </Button>
        </div>
      </form>
    </Form>
      <InfoDialog
        isOpen={meiInfoOpen}
        onOpenChange={setMeiInfoOpen}
        title="MicroEmpresa (MEI)"
        content={MICRO_EMPRESA_MEI_INFO_MARKDOWN}
      />
    </>
  );
}
