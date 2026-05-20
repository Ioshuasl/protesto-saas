'use server';

import jwt from 'jsonwebtoken';

import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

export default async function executeOnlyOfficeEditorTokenService(data: object) {
  const token = jwt.sign(data, 'WYe1zwtlDkh39_X3X3qTSICFDxts4VQrMyGLxnEpGUg', {
    algorithm: 'HS256',
    expiresIn: '5m',
  });

  // Define os dados
  const response = {
    data: token,
  };

  return response;
}

export const OnlyOfficeEditorTokenService = withClientErrorHandler(
  executeOnlyOfficeEditorTokenService,
);
