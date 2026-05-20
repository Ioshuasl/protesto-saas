import { NextResponse, type NextRequest } from 'next/server';

/** Decodifica apenas o payload de um JWT (sem verificar assinatura). Adequado para checagem de expiração no middleware (Edge). */
function decodeJwtPayload(token: string): { exp?: number } | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = parts[1];
    if (!payload) return null;
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
    const pad = base64.length % 4;
    const padded = pad ? base64 + '='.repeat(4 - pad) : base64;
    const json = atob(padded);
    return JSON.parse(json) as { exp?: number };
  } catch {
    return null;
  }
}

const publicRoutes = [
  { path: '/login', whenAuthenticated: 'redirect' },
  { path: '/register', whenAuthenticated: 'redirect' },
] as const;

const LOGIN_PATH = '/login';
/** Destino após login em rotas públicas com `whenAuthenticated: 'redirect'`. */
const HOME_PATH = '/';

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  if (process.env.DISABLE_AUTH_MIDDLEWARE === "true") {
    return NextResponse.next();
  }

  if (path.endsWith('.docx')) {
    return NextResponse.next();
  }

  const publicRoute = publicRoutes.find((route) => route.path === path);
  const authToken = request.cookies.get('access_token');

  if (!authToken && publicRoute) {
    return NextResponse.next();
  }

  if (!authToken && !publicRoute) {
    return NextResponse.redirect(new URL(LOGIN_PATH, request.url));
  }

  if (authToken && publicRoute && publicRoute.whenAuthenticated === 'redirect') {
    return NextResponse.redirect(new URL(HOME_PATH, request.url));
  }

  if (authToken && !publicRoute) {
    const decoded = decodeJwtPayload(authToken.value);

    if (!decoded?.exp) {
      return NextResponse.redirect(new URL(LOGIN_PATH, request.url));
    }

    const currentTime = Math.floor(Date.now() / 1000);
    if (decoded.exp <= currentTime) {
      return NextResponse.redirect(new URL(LOGIN_PATH, request.url));
    }

    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|images|.*\\.docx$).*)',
  ],
};
