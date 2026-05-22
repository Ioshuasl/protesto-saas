'use server';

import GUfIndexData from '@/packages/administrativo/data/GUf/GUfIndexData';

export default async function GUfIndexService() {
  const response = await GUfIndexData();

  return response;
}
