import db from "@/db.json";
import type { PMotivosCancelamentoInterface } from "@/packages/administrativo/interfaces/PMotivosCancelamento/PMotivosCancelamentoInterface";

export const pmotivosCancelamentoListRef: { current: PMotivosCancelamentoInterface[] } = {
  current: [...((db as { motivos_cancelamento?: PMotivosCancelamentoInterface[] }).motivos_cancelamento ?? [])],
};
