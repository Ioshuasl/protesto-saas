export default function SkeletonCard() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <div className="h-4 w-24 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
        <div className="h-10 w-full animate-pulse rounded-md bg-gray-200 dark:bg-slate-700"></div>
      </div>

      <div className="space-y-2">
        <div className="h-4 w-32 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
        <div className="h-10 w-full animate-pulse rounded-md bg-gray-200 dark:bg-slate-700"></div>
      </div>

      <div className="space-y-2">
        <div className="h-4 w-28 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
        <div className="h-20 w-full animate-pulse rounded-md bg-gray-200 dark:bg-slate-700"></div>
      </div>

      <div className="space-y-2">
        <div className="h-4 w-20 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
        <div className="h-10 w-full animate-pulse rounded-md bg-gray-200 dark:bg-slate-700"></div>
      </div>

      <div>
        <div className="h-10 w-32 animate-pulse rounded-full bg-gray-200 dark:bg-slate-700"></div>
      </div>
    </div>
  );
}
