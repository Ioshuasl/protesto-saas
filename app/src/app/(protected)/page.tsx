"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, AlertTriangle, CheckCircle2, XCircle } from "lucide-react";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const data = [
  { name: "Seg", apontados: 40, liquidados: 24, protestados: 10 },
  { name: "Ter", apontados: 30, liquidados: 13, protestados: 8 },
  { name: "Qua", apontados: 20, liquidados: 58, protestados: 12 },
  { name: "Qui", apontados: 27, liquidados: 39, protestados: 15 },
  { name: "Sex", apontados: 18, liquidados: 48, protestados: 9 },
];

const recentActivity = [
  { id: "REM-001", type: "Remessa", date: "Hoje, 10:30", status: "Processado", items: 145 },
  { id: "RET-002", type: "Retorno", date: "Hoje, 09:15", status: "Processado", items: 89 },
  { id: "CNF-003", type: "Confirmação", date: "Ontem, 17:45", status: "Erro", items: 12 },
  { id: "REM-004", type: "Remessa", date: "Ontem, 14:20", status: "Processado", items: 230 },
];

export default function DashboardPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Visão geral dos títulos e operações da CRA.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Títulos</CardTitle>
            <FileText className="text-muted-foreground h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1.245</div>
            <p className="text-muted-foreground text-xs">+20% em relação ao mês passado</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Títulos em Tríduo</CardTitle>
            <AlertTriangle className="text-primary h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-primary text-2xl font-bold">342</div>
            <p className="text-muted-foreground text-xs">Aguardando prazo legal</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Liquidados</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">854</div>
            <p className="text-muted-foreground text-xs">Pagos antes do protesto</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Protestados</CardTitle>
            <XCircle className="text-destructive h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">49</div>
            <p className="text-muted-foreground text-xs">Lavrados no período</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Funil de Títulos (Semana)</CardTitle>
            <CardDescription>Apontamentos, Liquidações e Protestos nos últimos 5 dias.</CardDescription>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                  <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(value) => `${value}`}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      borderColor: "hsl(var(--border))",
                      borderRadius: "var(--radius)",
                    }}
                    itemStyle={{ color: "hsl(var(--foreground))" }}
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
            <CardDescription>Últimos arquivos processados.</CardDescription>
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
                      <Badge variant={activity.status === "Processado" ? "default" : "destructive"}>
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
