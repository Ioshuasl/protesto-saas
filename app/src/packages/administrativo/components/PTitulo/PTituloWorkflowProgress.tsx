"use client";

import { CheckCircle2 } from "lucide-react";
import type { WorkflowProgressResult } from "@/packages/utils/PTitulo/ptituloWorkflowUtils";

interface PTituloWorkflowProgressProps {
  progress: WorkflowProgressResult;
}

export function PTituloWorkflowProgress({ progress }: PTituloWorkflowProgressProps) {
  return (
    <div className="rounded-lg bg-muted/20 p-2.5">
      <div className="h-2 overflow-hidden rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-[#FF6B00] transition-all duration-700 ease-out hover:brightness-110"
          style={{ width: `${progress.percent}%` }}
        />
      </div>
      <div
        className="mt-2 grid gap-2"
        style={{ gridTemplateColumns: `repeat(${Math.max(progress.steps.length, 1)}, minmax(0, 1fr))` }}
      >
        {progress.steps.map((step) => (
          <div
            key={step.label}
            className={`flex items-center gap-1 text-[11px] ${step.completed ? "text-emerald-600" : "text-muted-foreground"}`}
          >
            {step.completed ? (
              <CheckCircle2 className="h-3.5 w-3.5" />
            ) : (
              <span className="h-2 w-2 rounded-full bg-muted-foreground/40" />
            )}
            <span>{step.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
