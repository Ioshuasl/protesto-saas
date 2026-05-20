import db from "@/db.json";
import type { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces/PLivroNatureza/PLivroNaturezaInterface";

export const plivroNaturezaListRef: { current: PLivroNaturezaInterface[] } = {
  current: [...(db.livros_natureza || [])],
};
