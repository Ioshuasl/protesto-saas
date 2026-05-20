import db from "@/db.json";
import type { GFeriadoInterface } from "@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface";

export const gferiadoListRef: { current: GFeriadoInterface[] } = {
  current: [...(db.feriados || [])],
};
