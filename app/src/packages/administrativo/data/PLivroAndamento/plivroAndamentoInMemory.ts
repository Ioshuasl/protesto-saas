import db from "@/db.json";
import type { PLivroAndamentoInterface } from "@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface";

export const plivroAndamentoListRef: { current: PLivroAndamentoInterface[] } = {
  current: [...(db.livros_andamento || [])],
};
