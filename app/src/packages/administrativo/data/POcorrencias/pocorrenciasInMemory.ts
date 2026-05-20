import db from "@/db.json";
import type { POcorrenciasInterface } from "@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface";

export const pocorrenciasListRef: { current: POcorrenciasInterface[] } = {
  current: [...(db.ocorrencias || [])],
};
