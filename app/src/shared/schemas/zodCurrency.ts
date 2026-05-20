import { z } from 'zod';

import BRLCurrencyFormatter from '../actions/money/BRLCurrencyFormatter';

export const zodCurrency = () =>
  z.preprocess((value) => {
    if (typeof value === 'string') {
      const cents = BRLCurrencyFormatter.toCents(value);
      return cents / 100;
    }
    return value;
  }, z.number().min(0));
