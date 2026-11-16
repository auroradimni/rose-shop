'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useCart } from './CartProvider';
import Logo from './Logo';
import { SHOP, PROMO } from '@/lib/config';

const Svg = ({ children }) => <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{children}</svg>;

function Countdown() {
  const [t, setT] = useState('');
  useEffect(() => {
    const tick = () => {
      const d = Math.max(0, new Date(PROMO.ends) - new Date());
      const z = (n) => String(n).padStart(2, '0');
      setT(`${z(Math.floor(d / 36e5))}h ${z(Math.floor(d / 6e4) % 60)}m ${z(Math.floor(d / 1e3) % 60)}s`);
    };
    tick(); const id = setInterval(tick, 1000); return () => clearInterval(id);
  }, []);
  return <span className="count">Ends in: {t}</span>;
}

export default function Header({ categories }) {
  const { count, wish, setOpen } = useCart();
  return (
    <>
      {/* NA-KD: shirit promo me kohëmatës */}
      <div className="promo">
        <Countdown />
        <span className="mid">SALE DAYS | {PROMO.percent}% OFF EVERYTHING · CODE {PROMO.code}</span>
        <span className="ship">Free shipping over {SHOP.shipping.freeOver} {SHOP.currency}</span>
      </div>

      {/* NA-KD: navigim majtas, logo në mes, kërkim + ikona djathtas */}
      <header className="header">
        <nav>
          <Link href="/?sort=re#koleksioni">New In</Link>
          <Link href="/?sort=best#koleksioni">Best Sellers</Link>
          <Link href="/#koleksioni">All Products</Link>
          <Link href="/?sale=1#koleksioni">Sale</Link>
          <Link href="/#trendet">Trends</Link>
        </nav>
        <Link href="/" className="logo" aria-label={SHOP.name}><Logo /></Link>
        <div className="actions">
          {/* Fashion Nova: kërkim pill */}
          <form action="/#koleksioni" className="search" role="search">
            <button type="submit" aria-label="Submit search">
              <Svg><circle cx="11" cy="11" r="6.5" /><path d="M16 16l4.5 4.5" /></Svg>
            </button>
            <input type="search" name="q" placeholder="Search clothing" aria-label="Search clothing" />
          </form>
          <span className="region">AL</span>
          <Link href="/ruajtur" className="ico" aria-label="Saved items">
            <Svg><path d="M12 20s-7-4.5-7-10a4 4 0 017-2.5A4 4 0 0119 10c0 5.5-7 10-7 10z" /></Svg>
            {wish.length > 0 && <b>{wish.length}</b>}
          </Link>
          <button className="ico" onClick={() => setOpen(true)} aria-label="Cart">
            <Svg><path d="M5 8h14l-1 12H6L5 8z" /><path d="M9 8a3 3 0 016 0" /></Svg>
            {count > 0 && <b>{count}</b>}
          </button>
        </div>
      </header>

      {/* Fashion Nova: rreshti i dytë i kategorive */}
      <nav className="subnav" aria-label="Shop categories">
        <Link href="/?sort=re#koleksioni">New In</Link>
        <Link href="/#koleksioni">All Products</Link>
        <Link href="/?sale=1#koleksioni">Deals</Link>
        <Link href="/?k=fustane#koleksioni">Holiday Shop <sup>NEW</sup></Link>
        {categories.map((c) => <Link key={c.slug} href={`/?k=${c.slug}#koleksioni`}>{c.name}</Link>)}
      </nav>
      <Link href="/?sale=1#koleksioni" className="saleband"><b>UP TO 50% OFF</b><span>Shop now ›</span></Link>
    </>
  );
}
