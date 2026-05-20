import db from "@/db.json";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";

export const ptituloListRef: { current: PTituloInterface[] } = {
  current: [...(db.titulos as unknown as PTituloInterface[])],
};
