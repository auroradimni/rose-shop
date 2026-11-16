import { notFound } from 'next/navigation';
import Link from 'next/link';
import Visual from '@/components/Visual';
import AddToCart from '@/components/AddToCart';
import { bySlug } from '@/lib/products';
import { money } from '@/lib/config';

async function loadAvailability(slug) {
  try {
    const origin = process.env.ORDER_BACKEND_URL || 'http://127.0.0.1:8000';
    const response = await fetch(new URL(`/api/stock/${encodeURIComponent(slug)}/`, origin), {
      cache: 'no-store',
      signal: AbortSignal.timeout(3000),
    });
    if (response.ok) return (await response.json()).variants;
  } catch {
    return null;
  }
  return null;
}

export default async function Product({ params }) {
  const p = bySlug(params.slug);
  if (!p) notFound();
  const available = await loadAvailability(p.slug);
  return (
    <section className="wrap product">
      <Link href="/#koleksioni" className="back">← Back to collection</Link>
      <div className="pgrid">
        <Visual p={p} big />
        <div className="pinfo">
          <h1>{p.name}</h1>
          <p className="price lg">{money(p.price)} {p.old && <s>{money(p.old)}</s>}</p>
          <p className="desc">{p.desc}</p>
          <AddToCart p={p} available={available} />
          <ul className="perks"><li>Cash on delivery</li><li>Delivery across Albania</li><li>Size exchange within 3 days</li></ul>
        </div>
      </div>
    </section>
  );
}
