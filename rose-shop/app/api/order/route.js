import { NextResponse } from 'next/server';

// Këtu lidh porositë me backend-in tënd (p.sh. Django REST, email ose Telegram).
// Tani për tani vetëm i regjistron në konsolë.
export async function POST(req) {
  const order = await req.json();
  if (!order?.name || !order?.phone || !order?.items?.length) {
    return NextResponse.json({ error: 'Incomplete data' }, { status: 400 });
  }
  console.log('NEW ORDER:', JSON.stringify(order, null, 2));
  return NextResponse.json({ ok: true });
}
