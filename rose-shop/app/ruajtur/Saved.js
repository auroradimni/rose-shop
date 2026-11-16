'use client';
import Link from 'next/link';
import ProductCard from '@/components/ProductCard';
import { useCart } from '@/components/CartProvider';

export default function Saved({ products }) {
  const { wish } = useCart();
  const list = products.filter((p) => wish.includes(p.id));
  return (
    <section className="wrap">
      <h2>Saved items</h2>
      {list.length ? <div className="grid">{list.map((p) => <ProductCard key={p.id} p={p} />)}</div>
        : <p className="empty">You have not saved anything yet. Tap the heart on a product you like. <Link href="/" className="link">Browse the collection</Link></p>}
    </section>
  );
}
