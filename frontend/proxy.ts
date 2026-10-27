import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getAuthHeader } from './lib/auth';

export default async function proxy(request: NextRequest) {
    const headers = await getAuthHeader();

    if (headers?.Authorization) {
        return NextResponse.next();
    }

    return NextResponse.redirect(new URL("/login", request.url));
}

export const config = {
    matcher: [
        "/perfil/favoritos",
        "/perfil"
    ]
}