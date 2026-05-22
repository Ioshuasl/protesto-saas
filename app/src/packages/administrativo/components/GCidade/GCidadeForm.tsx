'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import z from 'zod';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useGUfReadHook } from '@/packages/administrativo/hooks/GUF/useGUfReadHook';
import { GCidadeSchema } from '@/packages/administrativo/schemas/GCidade/GCidadeSchema';

import GCidadeInterface from '../../interfaces/GCidade/GCidadeInterface';

// Hook responsável em trazer todos os estados brasileiros

// Define o tipo do formulário com base no schema Zod
type FormValues = z.infer<typeof GCidadeSchema>;

// Propriedades esperadas pelo componente
interface Props {
  isOpen: boolean; // controla se o Dialog está aberto
  data?: GCidadeInterface; // dados para edição (se existirem)
  onClose: (item: null, isFormStatus: boolean) => void; // callback para fechar
  onSave: (data: FormValues) => void; // callback para salvar
}

// Componente principal do formulário
export default function GCidadeForm({ isOpen, data, onClose, onSave }: Props) {
  //
  const { gUf, fetchGUf } = useGUfReadHook();

  // Inicializa o react-hook-form integrado ao Zod para validação
  const form = useForm<FormValues>({
    resolver: zodResolver(GCidadeSchema),
    defaultValues: {
      cidade_id: 0,
      uf: '',
      cidade_nome: '',
      codigo_ibge: '',
      codigo_gyn: '',
    },
  });

  // Quando recebe dados para edição, atualiza os valores do formulário
  useEffect(() => {
    if (data) {
      // Se for edição, carrega os dados recebidos
      form.reset({
        cidade_id: data.cidade_id,
        uf: data.uf ?? '',
        cidade_nome: data.cidade_nome ?? '',
        codigo_ibge: data.codigo_ibge ?? '',
        codigo_gyn: data.codigo_gyn ?? '',
      });
    } else {
      // Se for novo cadastro, limpa o formulário com valores padrão
      form.reset({
        cidade_id: 0,
        uf: '',
        cidade_nome: '',
        codigo_ibge: '',
        codigo_gyn: '',
      });
    }

    // Carrega todos os estados
    // brasileiros para o formulário
    const loadData = async () => {
      // Aguarda a busca terminar
      await fetchGUf();
    };

    // Dispara a função
    loadData();
  }, [data, form]);

  return (
    <Dialog
      open={isOpen}
      // Fecha o diálogo quando alterado para "false"
      onOpenChange={(open) => {
        if (!open) onClose(null, false);
      }}
    >
      <DialogContent className="sm:max-w-[425px]">
        {/* Cabeçalho do diálogo */}
        <DialogHeader>
          <DialogTitle>Cidades</DialogTitle>
          <DialogDescription>Controle de Cidades</DialogDescription>
        </DialogHeader>

        {/* Estrutura do formulário */}
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSave)} className="space-y-6">
            {/* Campo: Nome da cidade */}
            <FormField
              control={form.control}
              name="cidade_nome"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Descrição</FormLabel>
                  <FormControl>
                    <Input {...field} value={field.value ?? ''} placeholder="Digite a descrição" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Campo: Código IBGE */}
            <FormField
              name="codigo_ibge"
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Código IBGE</FormLabel>
                  <FormControl>
                    <Input {...field} value={field.value ?? ''} placeholder="Digite o código" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Tipo */}
            <FormField
              control={form.control}
              name="uf"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>UF</FormLabel>
                  <Select
                    value={field.value ?? ''} // garante que não será null
                    onValueChange={(val) => field.onChange(val)}
                  >
                    <FormControl className="w-full">
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione o estado desejado" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {gUf.map((item) => (
                        <SelectItem key={item.g_uf_id} value={String(item.sigla)}>
                          {item.nome}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Rodapé do diálogo com botões */}
            <DialogFooter className="mt-4">
              {/* Botão de cancelar */}
              <DialogClose asChild>
                <Button
                  variant="outline"
                  type="button"
                  onClick={() => onClose(null, false)}
                  className="cursor-pointer"
                >
                  Cancelar
                </Button>
              </DialogClose>

              {/* Botão de salvar */}
              <Button type="submit" className="cursor-pointer">
                Salvar
              </Button>
            </DialogFooter>

            {/* Campo oculto: ID da cidade */}
            <input type="hidden" {...form.register('cidade_id')} />
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
