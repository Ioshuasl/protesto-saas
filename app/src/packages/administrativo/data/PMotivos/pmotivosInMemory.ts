import db from "@/db.json";
import type { PMotivosInterface } from "@/packages/administrativo/interfaces/PMotivos/PMotivosInterface";

export const pmotivosListRef: { current: PMotivosInterface[] } = {
  current: [...((db as { motivos?: PMotivosInterface[] }).motivos ?? [])],
};
