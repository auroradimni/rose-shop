import { notFound } from 'next/navigation';
import Link from 'next/link';
import Visual from '@/components/Visual';
import AddToCart from '@/components/AddToCart';
import { loadCatalog, offlineCatalog } from '@/lib/catalog';
import { money } from '@/lib/config';

export default async function Product({ params }) {
  const { products } = (await loadCatalog()) ?? offlineCatalog;
  const p = products.find((product) => product.slug === params.slug);
  if (!p) notFound();
  return (
    <section className="wrap product">
      <Link href="/#koleksioni" className="back">← Back to collection</Link>
      <div className="pgrid">
        <Visual p={p} big />
        <div className="pinfo">
          <h1>{p.name}</h1>
          <p className="price lg">{money(p.price)} {p.old && <s>{money(p.old)}</s>}</p>
          <p className="desc">{p.desc}</p>
          <AddToCart p={p} available={p.available} />
          <ul className="perks"><li>Cash on delivery</li><li>Delivery across Albania</li><li>Size exchange within 3 days</li></ul>
        </div>
      </div>
    </section>
  );
}
