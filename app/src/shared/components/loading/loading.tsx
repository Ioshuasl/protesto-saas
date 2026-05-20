import React from 'react';

import SkeletonCard from './skeletonCard';
import SkeletonTable from './skeletonTable';

export default function Loading({ type }: any) {
  switch (type) {
    case 1:
      return <SkeletonCard />;
      break;
    case 2:
      return <SkeletonTable />;
      break;
  }
}
