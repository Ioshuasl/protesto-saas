import { ArrowUpDownIcon } from 'lucide-react';

import { Button } from '@/components/ui/button';

export const SortableHeader = (label: string, column: any) => (
  <Button 
    className='cursor-pointer'
    variant="ghost" 
    onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
  >
    {label}
    <ArrowUpDownIcon className="ml-1 h-4 w-4" />
  </Button>
);
