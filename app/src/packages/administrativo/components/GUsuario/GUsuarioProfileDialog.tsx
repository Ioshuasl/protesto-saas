'use client';

import { Loader2Icon } from 'lucide-react';
import { type ReactNode, useEffect } from 'react';

import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';
import { useGUsuarioMeHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioMeHook';

export type GUsuarioProfileDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

const EMPTY_FIELD_LABEL = 'Não Informado';

function displayValue(value: string | null | undefined) {
  if (value === null || value === undefined || String(value).trim() === '') {
    return '';
  }
  return String(value);
}

function fieldLabel(value: string | null | undefined) {
  const v = displayValue(value);
  return v === '' ? EMPTY_FIELD_LABEL : v;
}

function initialsFromProfile(name: string | null | undefined, login: string | null | undefined) {
  const base = (name ?? login ?? '?').trim();
  const parts = base.split(/\s+/).filter(Boolean);
  if (parts.length >= 2) {
    const a = parts[0]?.[0] ?? '';
    const b = parts[parts.length - 1]?.[0] ?? '';
    return `${a}${b}`.toUpperCase();
  }
  return base.slice(0, 2).toUpperCase() || '?';
}

function situacaoSelectValue(situacao: string | null | undefined): string {
  if (situacao === 'A' || situacao === 'I') return situacao;
  return '__none__';
}

function situacaoBadgeLabel(situacao: string | null | undefined) {
  if (situacao === 'A') return 'Ativo';
  if (situacao === 'I') return 'Inativo';
  return EMPTY_FIELD_LABEL;
}

function SectionTitle({ children }: { children: ReactNode }) {
  return (
    <h3 className="text-muted-foreground mb-4 text-xs font-semibold tracking-wide uppercase">{children}</h3>
  );
}

export function GUsuarioProfileDialog({ open, onOpenChange }: GUsuarioProfileDialogProps) {
  const { me, loading, fetchMe } = useGUsuarioMeHook();

  useEffect(() => {
    if (!open) return;
    void fetchMe();
  }, [open, fetchMe]);

  const nomeFieldId = 'gusuario-profile-nome-completo';
  const loginFieldId = 'gusuario-profile-login';
  const funcaoFieldId = 'gusuario-profile-funcao';
  const emailFieldId = 'gusuario-profile-email';
  const cpfFieldId = 'gusuario-profile-cpf';

  const displayName = displayValue(me?.nome_completo) || displayValue(me?.login) || 'Usuário';
  const situacaoIsActive = me?.situacao === 'A';

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        className={cn(
          'box-border flex max-h-[min(92vh,880px)] min-w-0 flex-col gap-0 overflow-hidden border p-0 shadow-lg',
          /* Sobrescreve sm:max-w-lg do dialog.tsx (tailwind-merge não elimina sm: vs max-w sem prefixo). */
          'w-[min(78vw,calc(100vw-2rem))] max-w-[min(90rem,calc(100vw-2rem))] sm:max-w-[min(90rem,calc(100vw-2rem))]',
        )}
      >
        <DialogHeader className="border-border min-w-0 space-y-1 border-b bg-muted/15 px-6 py-5 text-left sm:px-8">
          <DialogTitle className="text-xl font-semibold tracking-tight">Meu perfil</DialogTitle>
          <DialogDescription className="text-sm leading-relaxed">
            Somente leitura. Para alterar estes dados, fale com o administrador do sistema.
          </DialogDescription>
        </DialogHeader>

        <div className="relative min-h-0 min-w-0 flex-1 overflow-x-hidden overflow-y-auto overscroll-y-contain">
          {loading && (
            <div
              className="bg-background/85 absolute inset-0 z-10 flex items-center justify-center backdrop-blur-[2px]"
              aria-busy="true"
              aria-live="polite"
            >
              <Loader2Icon className="text-muted-foreground size-9 animate-spin" aria-hidden />
              <span className="sr-only">Carregando dados do usuário</span>
            </div>
          )}

          <div className="flex min-w-0 flex-col gap-0">
            {/* Resumo visual */}
            <div className="flex min-w-0 flex-col gap-4 border-b bg-gradient-to-br from-muted/40 via-background to-background px-6 py-6 sm:flex-row sm:items-center sm:gap-8 sm:px-8">
              <Avatar className="size-24 shrink-0 border-2 border-border shadow-md ring-2 ring-background">
                <AvatarFallback className="text-xl font-semibold tracking-tight">
                  {me ? initialsFromProfile(me.nome_completo, me.login) : '…'}
                </AvatarFallback>
              </Avatar>
              <div className="min-w-0 flex-1 space-y-2">
                <div>
                  <p className="truncate text-xl font-semibold tracking-tight">{displayName}</p>
                  <p className="text-muted-foreground mt-0.5 truncate text-sm">
                    {[
                      displayValue(me?.login) ? `@${displayValue(me?.login)}` : EMPTY_FIELD_LABEL,
                      fieldLabel(me?.email),
                    ].join(' · ')}
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <span
                    className={cn(
                      'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium',
                      situacaoIsActive
                        ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-700 dark:text-emerald-400'
                        : me?.situacao === 'I'
                          ? 'border-destructive/25 bg-destructive/10 text-destructive'
                          : 'border-border bg-muted text-muted-foreground',
                    )}
                  >
                    {situacaoBadgeLabel(me?.situacao)}
                  </span>
                  <span className="text-muted-foreground inline-flex items-center rounded-full border bg-background px-2.5 py-0.5 text-xs font-medium">
                    Assina: {me?.assina === 'S' ? 'Sim' : 'Não'}
                  </span>
                </div>
              </div>
            </div>

            {/* Campos — duas colunas em telas médias+ */}
            <div className="grid gap-8 px-6 py-6 sm:px-8 lg:grid-cols-2 lg:gap-10">
              <div>
                <SectionTitle>Dados da conta</SectionTitle>
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor={nomeFieldId}>Nome completo</Label>
                    <Input
                      id={nomeFieldId}
                      readOnly
                      disabled
                      className="bg-muted/40 h-10 min-w-0 max-w-full"
                      value={fieldLabel(me?.nome_completo)}
                      placeholder={EMPTY_FIELD_LABEL}
                    />
                  </div>
                  <div className="grid min-w-0 gap-4 sm:grid-cols-2">
                    <div className="grid min-w-0 gap-2">
                      <Label htmlFor={loginFieldId}>Login</Label>
                      <Input
                        id={loginFieldId}
                        readOnly
                        disabled
                        className="bg-muted/40 h-10 min-w-0 max-w-full font-mono text-sm"
                        value={fieldLabel(me?.login)}
                        placeholder={EMPTY_FIELD_LABEL}
                      />
                    </div>
                    <div className="grid min-w-0 gap-2">
                      <Label htmlFor={funcaoFieldId}>Função</Label>
                      <Input
                        id={funcaoFieldId}
                        readOnly
                        disabled
                        className="bg-muted/40 h-10 min-w-0 max-w-full"
                        value={fieldLabel(me?.funcao)}
                        placeholder={EMPTY_FIELD_LABEL}
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <SectionTitle>Contato e documentos</SectionTitle>
                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor={emailFieldId}>E-mail</Label>
                    <Input
                      id={emailFieldId}
                      readOnly
                      disabled
                      type="email"
                      className="bg-muted/40 h-10"
                      value={fieldLabel(me?.email)}
                      placeholder={EMPTY_FIELD_LABEL}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor={cpfFieldId}>CPF</Label>
                    <Input
                      id={cpfFieldId}
                      readOnly
                      disabled
                      className="bg-muted/40 h-10 min-w-0 max-w-full"
                      value={fieldLabel(me?.cpf)}
                      placeholder={EMPTY_FIELD_LABEL}
                    />
                  </div>
                </div>
              </div>

              <div className="min-w-0 lg:col-span-2">
                <SectionTitle>Status e permissões</SectionTitle>
                <div className="grid min-w-0 gap-4 sm:grid-cols-2">
                  <div className="grid min-w-0 gap-2">
                    <Label>Situação na API</Label>
                    <Select value={situacaoSelectValue(me?.situacao)} disabled>
                      <SelectTrigger className="bg-muted/40 h-10 min-w-0 w-full max-w-full font-normal [&_[data-slot=select-value]]:truncate">
                        <SelectValue placeholder={EMPTY_FIELD_LABEL} />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="A">Ativo (A)</SelectItem>
                        <SelectItem value="I">Inativo (I)</SelectItem>
                        <SelectItem value="__none__">{EMPTY_FIELD_LABEL}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid min-w-0 gap-2">
                    <Label htmlFor="gusuario-profile-assina-select">Assina documentos</Label>
                    <Select value={me?.assina === 'S' ? 'S' : 'N'} disabled>
                      <SelectTrigger
                        id="gusuario-profile-assina-select"
                        className="bg-muted/40 h-10 min-w-0 w-full max-w-full font-normal [&_[data-slot=select-value]]:truncate"
                      >
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="S">Sim (S)</SelectItem>
                        <SelectItem value="N">Não (N ou não informado)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
