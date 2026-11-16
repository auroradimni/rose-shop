import { NextResponse } from 'next/server';
import { PROMO, SHOP } from '@/lib/config';
import { loadCatalog } from '@/lib/catalog';

const invalid = () => NextResponse.json({ error: 'Invalid order' }, { status: 400 });
const unavailable = () => NextResponse.json({ error: 'Order service unavailable' }, { status: 503 });

export async function POST(req) {
  const order = await req.json().catch(() => null);
  const { name, phone, city, address, zone, note = '', items, code } = order ?? {};
  const details = { name, phone, city, address };
  const limits = { name: 200, phone: 30, city: 100, address: 1000 };

  if (Object.entries(details).some(([key, value]) =>
    typeof value !== 'string' || !value.trim() || value.length > limits[key]
  )) return invalid();
  if (typeof note !== 'string' || note.length > 2000 || !['tirana', 'rest'].includes(zone)) {
    return invalid();
  }
  if (!Array.isArray(items) || !items.length || items.length > 100) return invalid();

  const catalog = await loadCatalog();
  if (!catalog) return unavailable();

  const lines = [];
  for (const item of items) {
    const product = catalog.products.find((p) => p.id === item?.id);
    if (!product || !product.sizes.includes(item.size) || !product.colors.includes(item.color) ||
        !Number.isInteger(item.qty) || item.qty < 1 || item.qty > 100) return invalid();
    lines.push({
      product_slug: product.slug,
      product_name: product.name,
      size: item.size,
      color: item.color,
      quantity: item.qty,
      price: product.price,
    });
  }

  const subtotal = lines.reduce((sum, line) => sum + line.quantity * line.price, 0);
  const shipping = subtotal >= SHOP.shipping.freeOver ? 0 : SHOP.shipping[zone];
  const discounted = typeof code === 'string' && code.trim().toUpperCase() === PROMO.code;
  const discount = discounted ? Math.round(subtotal * PROMO.percent / 100) : 0;
  const origin = process.env.ORDER_BACKEND_URL || 'http://127.0.0.1:8000';
  const token = process.env.ORDER_API_TOKEN;
  if (!token) return unavailable();

  try {
    const response = await fetch(new URL('/api/orders/', origin), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        name: name.trim(), phone: phone.trim(), city: city.trim(), address: address.trim(),
        zone, note: note.trim(), items: lines, subtotal, shipping, discount,
        total: subtotal - discount + shipping,
      }),
      signal: AbortSignal.timeout(8000),
    });
    if (response.status === 409) {
      return NextResponse.json(await response.json(), { status: 409 });
    }
    if (response.status !== 201) return unavailable();
    return NextResponse.json(await response.json(), { status: 201 });
  } catch {
    return unavailable();
  }
}
