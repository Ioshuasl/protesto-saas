'use client';

import { useEffect, useMemo } from 'react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertTriangle, CheckCircle2, FileText, XCircle } from 'lucide-react';
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { useTabelionatoProtestoDashboardResumoHook } from '@/packages/administrativo/hooks/TabelionatoProtestoDashboard/useTabelionatoProtestoDashboardResumoHook';
import { useTabelionatoProtestoDashboardFunilHook } from '@/packages/administrativo/hooks/TabelionatoProtestoDashboard/useTabelionatoProtestoDashboardFunilHook';

const recentActivity = [
  { id: 'REM-001', type: 'Remessa', date: 'Hoje, 10:30', status: 'Processado', items: 145 },
  { id: 'RET-002', type: 'Retorno', date: 'Hoje, 09:15', status: 'Processado', items: 89 },
  { id: 'CNF-003', type: 'Confirmacao', date: 'Ontem, 17:45', status: 'Erro', items: 12 },
  { id: 'REM-004', type: 'Remessa', date: 'Ontem, 14:20', status: 'Processado', items: 230 },
];

function formatNumber(value: number | undefined): string {
  return Number(value ?? 0).toLocaleString('pt-BR');
}

function formatDateToBrazilian(value: string | undefined): string {
  if (!value) return '';
  const [year, month, day] = value.split('-');
  if (!year || !month || !day) return value;
  return `${day}/${month}/${year}`;
}

export function TabelionatoProtestoDashboardIndex() {
  const { resumo, fetchResumo } = useTabelionatoProtestoDashboardResumoHook();
  const { funil, fetchFunil } = useTabelionatoProtestoDashboardFunilHook();

  useEffect(() => {
    fetchResumo();
    fetchFunil();
  }, [fetchResumo, fetchFunil]);

  const funilData = useMemo(
    () =>
      funil.map((item) => ({
        name: item.label,
        apontados: item.apontados,
        liquidados: item.liquidados,
        protestados: item.protestados,
      })),
    [funil],
  );

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Visao geral dos titulos e operacoes da CRA.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Titulos</CardTitle>
            <FileText className="text-muted-foreground h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(resumo?.total_titulos)}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Titulos em Triduo</CardTitle>
            <AlertTriangle className="text-primary h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-primary text-2xl font-bold">{formatNumber(resumo?.titulos_em_triduo)}</div>
            <p className="text-muted-foreground text-xs">Aguardando prazo legal</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Liquidados</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(resumo?.liquidados)}</div>
            <p className="text-muted-foreground text-xs">Pagos antes do protesto</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Protestados</CardTitle>
            <XCircle className="text-destructive h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(resumo?.protestados)}</div>
            <p className="text-muted-foreground text-xs">Lavrados no periodo</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Funil de Titulos (Semana)</CardTitle>
            <CardDescription>Apontamentos, Liquidacoes e Protestos nos ultimos 7 dias.</CardDescription>
            <div className="mt-2 flex flex-wrap items-center gap-4 text-xs">
              <span className="inline-flex items-center gap-2 text-muted-foreground">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-black" />
                Apontados
              </span>
              <span className="inline-flex items-center gap-2 text-muted-foreground">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-green-500" />
                Liquidados
              </span>
              <span className="inline-flex items-center gap-2 text-muted-foreground">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-red-500" />
                Protestados
              </span>
            </div>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={funilData}>
                  <XAxis
                    dataKey="name"
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => formatDateToBrazilian(String(value))}
                  />
                  <YAxis
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => `${value}`}
                  />
                  <Tooltip
                    labelFormatter={(label) => formatDateToBrazilian(String(label))}
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      borderColor: 'hsl(var(--border))',
                      borderRadius: 'var(--radius)',
                    }}
                    itemStyle={{ color: 'hsl(var(--foreground))' }}
                  />
                  <Bar dataKey="apontados" fill="hsl(var(--muted-foreground))" radius={[4, 4, 0, 0]} name="Apontados" />
                  <Bar dataKey="liquidados" fill="#22c55e" radius={[4, 4, 0, 0]} name="Liquidados" />
                  <Bar dataKey="protestados" fill="#ef4444" radius={[4, 4, 0, 0]} name="Protestados" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Atividade Recente CRA</CardTitle>
            <CardDescription>Ultimos arquivos processados.</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Arquivo</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentActivity.map((activity) => (
                  <TableRow key={activity.id}>
                    <TableCell className="font-medium">
                      <div className="flex flex-col">
                        <span>{activity.id}</span>
                        <span className="text-muted-foreground text-xs">{activity.date}</span>
                      </div>
                    </TableCell>
                    <TableCell>{activity.type}</TableCell>
                    <TableCell>
                      <Badge variant={activity.status === 'Processado' ? 'default' : 'destructive'}>
                        {activity.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
