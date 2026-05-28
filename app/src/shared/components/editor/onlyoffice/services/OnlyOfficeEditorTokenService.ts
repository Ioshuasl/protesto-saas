'use server';

import jwt from 'jsonwebtoken';

import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

export default async function executeOnlyOfficeEditorTokenService(data: object) {
  const jwtEnabled = (process.env.ORIUS_ONLYOFFICE_JWT_ENABLED ?? 'false').toLowerCase() === 'true';
  if (!jwtEnabled) {
    return {
      data: undefined,
    };
  }

  const secret = process.env.ORIUS_ONLYOFFICE_JWT_SECRET;
  if (!secret) {
    throw new Error('ORIUS_ONLYOFFICE_JWT_SECRET não configurado com JWT habilitado.');
  }

  const token = jwt.sign(data, secret, {
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
