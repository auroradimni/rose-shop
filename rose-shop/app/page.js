import Link from 'next/link';
import ProductCard from '@/components/ProductCard';
import { products, categories } from '@/lib/products';
import { SHOP, TRENDS } from '@/lib/config';

export default function Home({ searchParams }) {
  const { k, q, sort, sale } = searchParams || {};
  const filtered = !!(k || q || sort || sale);
  let list = products.filter((p) => (!k || p.cat === k) && (!sale || p.old) && (!q || p.name.toLowerCase().includes(q.toLowerCase())));
  if (sort === 'best') list = list.filter((p) => p.best);
  if (sort === 'ulet') list = [...list].sort((a, b) => a.price - b.price);
  if (sort === 'larte') list = [...list].sort((a, b) => b.price - a.price);
  if (sort === 're') list = [...list].sort((a, b) => Number(b.isNew) - Number(a.isNew));
  const fresh = products.filter((p) => p.isNew);
  const q2 = (o) => `/?${new URLSearchParams({ ...(k && { k }), ...(q && { q }), ...o })}#koleksioni`;
  const title = k ? categories.find((c) => c.slug === k)?.name : q ? `Results for "${q}"` : sale ? 'Sale' : sort === 're' ? 'New In' : sort === 'best' ? 'Best Sellers' : 'Collection';

  return (
    <>
      {!filtered && (
        <>
          {/* Lioness: hero i plotë me tekst poshtë majtas */}
          <section className="hero3">
            <div>
              <small>All day with {SHOP.name}</small>
              <h1>Everyday Essentials</h1>
              <Link href="/?sort=re#koleksioni" className="shop-now">Shop now</Link>
            </div>
          </section>

          {/* Lioness: "New Releases" */}
          <section className="wide">
            <div className="row-head"><h2 className="fnh">New Releases</h2><Link href="/?sort=re#koleksioni" className="more">See more</Link></div>
            <p className="sub">Fresh drops, soft colours and pieces for every occasion.</p>
            <div className="strip5">{fresh.map((p) => <ProductCard key={p.id} p={p} />)}</div>
          </section>

          {/* Fashion Nova: "The Trend Report" */}
          <section className="wide" id="trendet">
            <h2 className="fnh">The Trend Report</h2>
            <div className="trends">
              {TRENDS.map((t) => (
                <Link key={t.title} href={t.href} className="trend">
                  {t.image ? <img src={t.image} alt={t.title} className="trendimg" /> : <div style={{ background: `linear-gradient(170deg, ${t.tone[0]}, ${t.tone[1]})` }} />}
                  <span>{t.title} ›</span>
                </Link>
              ))}
            </div>
          </section>
        </>
      )}

      <section id="koleksioni" className="wide">
        <h2 className="fnh">{title}</h2>
        <div className="bar">
          <div className="filters">
            <Link href="/#koleksioni" className={!k ? 'on' : ''}>All</Link>
            {categories.map((c) => <Link key={c.slug} href={q2({ k: c.slug })} className={k === c.slug ? 'on' : ''}>{c.name}</Link>)}
          </div>
          <div className="sortrow">
            <span>{list.length} styles found</span>
            <span className="sorts">Sort:
              <Link href={q2({ sort: 're' })} className={sort === 're' ? 'on' : ''}>Newest</Link>
              <Link href={q2({ sort: 'ulet' })} className={sort === 'ulet' ? 'on' : ''}>Price ↑</Link>
              <Link href={q2({ sort: 'larte' })} className={sort === 'larte' ? 'on' : ''}>Price ↓</Link>
            </span>
          </div>
        </div>
        {list.length ? <div className="grid5">{list.map((p) => <ProductCard key={p.id} p={p} />)}</div>
          : <p className="empty">Nothing found. Try another word or pick a category.</p>}
      </section>
    </>
  );
}
