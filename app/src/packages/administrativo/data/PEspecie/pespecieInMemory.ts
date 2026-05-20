import db from "@/db.json";
import type { PEspecieInterface } from "@/packages/administrativo/interfaces/PEspecie/PEspecieInterface";

export const pespecieListRef: { current: PEspecieInterface[] } = {
  current: [...(db.especies || [])],
};
