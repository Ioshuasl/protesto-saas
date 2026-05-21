'use client';

import { useEffect } from 'react';

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
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useGUsuarioFormHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioFormHook';
import { GUsuarioFormInterface } from '@/packages/administrativo/interfaces/GUsuario/GUsuarioFormInterface';
import { FormatCPF } from '@/shared/actions/CPF/FormatCPF';
import { ResetFormIfData } from '@/shared/actions/form/ResetFormIfData';
import LoadingButton from '@/shared/components/loadingButton/LoadingButton';

/**
 * Formulário de cadastro/edição de Natureza
 * Baseado nos campos da tabela G_NATUREZA
 */
export default function GUsuarioForm({
  isOpen,
  data,
  onClose,
  onSave,
  buttonIsLoading,
}: GUsuarioFormInterface) {
  const form = useGUsuarioFormHook({});

  // Atualiza o formulário quando recebe dados para edição
  useEffect(() => {
    ResetFormIfData(form, data);
  }, [data, form]);

  function onError(error: unknown) {
    console.log('Erro no formulário:', error);
  }

  return (
    <Dialog
      open={isOpen}
      onOpenChange={(open) => {
        if (!open) onClose(null, false);
      }}
    >
      <DialogContent className="w-full max-w-full p-6 sm:max-w-3xl md:max-w-2xl lg:max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-lg sm:text-xl">Cadastrar Usuários</DialogTitle>
          <DialogDescription className="text-muted-foreground text-sm">
            Formulário de Usuários para o sistema administrativo. Preencha os campos abaixo para criar ou editar um usuário.
          </DialogDescription>
        </DialogHeader>
        {/* Formulário principal */}
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSave, onError)} className="space-y-6">
            {/* GRID MOBILE FIRST */}
            <div className="grid w-full grid-cols-12 gap-4">
              {/* Palavra */}
              <div className="col-span-12 sm:col-span-6 md:col-span-12">
                <FormField
                  control={form.control}
                  name="nome_completo"
                  render={({ field }) => (
                    <FormItem className="col-span-1 sm:col-span-2">
                      <FormLabel>Nome Completo</FormLabel>
                      <FormControl>
                        <Input 
                          {...field} 
                          type="text" 
                          value={field.value ?? ''}
                          maxLength={150}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              {/* Prefixo */}
              <div className="col-span-12 sm:col-span-6 md:col-span-12">
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem className="col-span-1 sm:col-span-2">
                      <FormLabel>E-mail</FormLabel>
                      <FormControl>
                        <Input 
                          {...field} 
                          type="text"
                          maxLength={260} 
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              {/* Singular Masculino */}
              <div className="col-span-12 sm:col-span-6 md:col-span-6">
                <FormField
                  control={form.control}
                  name="cpf"
                  render={({ field }) => (
                    <FormItem className="col-span-1 sm:col-span-2">
                      <FormLabel>CPF</FormLabel>
                      <FormControl>
                        <Input {...field} 
                        type="text" 
                        value={FormatCPF(field.value)}
                        onChange={(e) => field.onChange(FormatCPF(e.target.value))}                        
                      />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              {/* Plural Masculino */}
              <div className="col-span-12 sm:col-span-6 md:col-span-6">
                <FormField
                  control={form.control}
                  name="funcao"
                  render={({ field }) => (
                    <FormItem className="col-span-1 sm:col-span-2">
                      <FormLabel>Função</FormLabel>
                      <FormControl>
                        <Input 
                          {...field} 
                          type="text" 
                          maxLength={60}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              {/* Singular Feminino */}
              <div className="col-span-12 sm:col-span-6 md:col-span-6">
                <FormField
                  control={form.control}
                  name="senha_api"
                  render={({ field }) => (
                    <FormItem className="col-span-1 sm:col-span-2">
                      <FormLabel>Senha da API</FormLabel>
                      <FormControl>
                        <Input 
                          {...field} 
                          type="password"
                          maxLength={10} 
                        />
                      </FormControl>

                        {/* Observação exibida apenas em edição */}
                        {data && (
                          <FormDescription>
                            Preencha a senha apenas se desejar alterá-la. 
                            Caso contrário, deixe este campo em branco.
                          </FormDescription>
                        )}

                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              {/* Plural Feminino */}
              <div className="col-span-12 sm:col-span-6 md:col-span-6">
                <FormField
                  control={form.control}
                  name="confirma_senha_api"
                  render={({ field }) => (
                    <FormItem className="col-span-1 sm:col-span-2">
                      <FormLabel>Confirmar senha API</FormLabel>
                      <FormControl>
                        <Input 
                          {...field} 
                          type="password" 
                          maxLength={10}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              {data && (
                <FormField
                  control={form.control}
                  name="usuario_id"
                  render={({ field }) => (
                    <input
                      type="hidden"
                      {...field}
                      value={data.usuario_id}
                    />
                  )}
                />
              )}              
            </div>
            {/* Rodapé */}
            <DialogFooter className="mt-6 flex flex-col justify-end gap-2 sm:flex-row">
              <DialogClose asChild>
                <Button 
                  className='cursor-pointer'
                  variant="outline" 
                  type="button"
                >
                  Cancelar
                </Button>
              </DialogClose>
              <LoadingButton
                text="Salvar"
                textLoading="Salvando..."
                type="submit"
                loading={buttonIsLoading}
              />
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
