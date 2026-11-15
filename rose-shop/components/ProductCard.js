'use client';
import Link from 'next/link';
import Visual from './Visual';
import { useCart } from './CartProvider';
import { money } from '@/lib/config';

export default function ProductCard({ p }) {
  const { wish, toggleWish } = useCart();
  const on = wish.includes(p.id);
  const href = `/produkti/${p.slug}`;
  return (
    <div className="card lion">
      <div className="card-img">
        <Link href={href} aria-label={p.name}><Visual p={p} /></Link>
        {p.isNew && <em className="tag">New</em>}
        {p.old && <em className="tag sale">-{Math.round((1 - p.price / p.old) * 100)}%</em>}
        <div className="qa">
          <Link href={href} className="qb" aria-label="View product">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><circle cx="11" cy="11" r="6.5" /><path d="M16 16l4.5 4.5" /></svg>
          </Link>
          <button className={`qb ${on ? 'on' : ''}`} onClick={() => toggleWish(p.id)} aria-pressed={on} aria-label={on ? 'Remove from saved' : 'Save'}>{on ? '♥' : '♡'}</button>
        </div>
        <Link href={href} className="opts">Select options</Link>
      </div>
      <Link href={href}><h3>{p.name}</h3></Link>
      <p className="price">{money(p.price)} {p.old && <s>{money(p.old)}</s>}</p>
      <div className="sw2">{p.colors.map((c) => <i key={c} style={{ background: c }} />)}</div>
    </div>
  );
}
