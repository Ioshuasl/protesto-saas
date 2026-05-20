import { GFeriadoDeleteService } from "@/packages/administrativo/services/GFeriado/GFeriadoDeleteService";
import { GFeriadoIndexService } from "@/packages/administrativo/services/GFeriado/GFeriadoIndexService";
import { GFeriadoSaveCreateService } from "@/packages/administrativo/services/GFeriado/GFeriadoSaveCreateService";
import { GFeriadoSaveUpdateService } from "@/packages/administrativo/services/GFeriado/GFeriadoSaveUpdateService";
import { GFeriadoShowService } from "@/packages/administrativo/services/GFeriado/GFeriadoShowService";

export const FeriadoService = {
  getAll: GFeriadoIndexService,
  getById: GFeriadoShowService,
  create: GFeriadoSaveCreateService,
  update: GFeriadoSaveUpdateService,
  delete: GFeriadoDeleteService,
};
