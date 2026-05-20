import Link from 'next/link';

import { signInAsDev } from './actions';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function LoginPage() {
  return (
    <main className="flex min-h-svh flex-col items-center justify-center bg-muted/30 p-6">
      <Card className="w-full max-w-md shadow-md">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-semibold tracking-tight">Orius Protesto</CardTitle>
          <CardDescription>Login fictício para desenvolvimento local</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground text-center text-sm">
            Não há backend de autenticação aqui. Use o botão abaixo para gravar um cookie de sessão de teste e acessar o
            painel.
          </p>
          <div className="space-y-2">
            <Label htmlFor="email">E-mail (ilustrativo)</Label>
            <Input id="email" name="email" type="email" autoComplete="username" placeholder="dev@orius.local" disabled />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Senha (ilustrativo)</Label>
            <Input id="password" name="password" type="password" autoComplete="current-password" placeholder="••••••••" disabled />
          </div>
          <form action={signInAsDev}>
            <Button type="submit" className="w-full bg-[#FF6B00] text-white hover:bg-[#E56000]">
              Entrar como desenvolvedor
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col gap-2 border-t pt-4 text-center text-xs text-muted-foreground">
          <p>
            Em produção, substitua por login real. Para pular o middleware sem cookie, use{' '}
            <code className="rounded bg-muted px-1 py-0.5">DISABLE_AUTH_MIDDLEWARE=true</code>.
          </p>
          <Link href="/register" className="text-sm font-medium text-[#FF6B00] hover:underline">
            Ir para registro (placeholder)
          </Link>
        </CardFooter>
      </Card>
    </main>
  );
}
