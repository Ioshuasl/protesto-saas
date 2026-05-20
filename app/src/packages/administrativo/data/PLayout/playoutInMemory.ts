import db from "@/db.json";
import type { PLayoutInterface } from "@/packages/administrativo/interfaces/PLayout/PLayoutInterface";

type DbWithLayouts = typeof db & { layouts?: PLayoutInterface[] };

export const playoutListRef: { current: PLayoutInterface[] } = {
  current: [...(((db as DbWithLayouts).layouts) ?? [])],
};
