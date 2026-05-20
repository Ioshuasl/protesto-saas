export default function SkeletonTable() {
  return (
    <div>
      <div role="status" aria-busy="true" aria-label="Carregando tabela" className="w-full p-4">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left">
                  <div className="h-4 w-20 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </th>
                <th className="px-4 py-2 text-left">
                  <div className="h-4 w-28 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </th>
                <th className="px-4 py-2 text-left">
                  <div className="h-4 w-24 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </th>
                <th className="px-4 py-2 text-left">
                  <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t">
                <td className="px-4 py-3">
                  <div className="h-4 w-24 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-32 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-20 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
              </tr>

              <tr className="border-t">
                <td className="px-4 py-3">
                  <div className="h-4 w-20 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-24 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-28 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
              </tr>

              <tr className="border-t">
                <td className="px-4 py-3">
                  <div className="h-4 w-28 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-20 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-24 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
                <td className="px-4 py-3">
                  <div className="h-4 w-16 animate-pulse rounded bg-gray-200 dark:bg-slate-700"></div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
