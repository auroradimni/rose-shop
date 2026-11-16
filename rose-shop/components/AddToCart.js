'use client';
import { useState } from 'react';
import { useCart } from './CartProvider';

export default function AddToCart({ p, available }) {
  const { add } = useCart();
  const [size, setSize] = useState(null);
  const [color, setColor] = useState(p.colors[0]);
  const [err, setErr] = useState(false);
  const inStock = (s) => available?.some((variant) => variant.size === s && variant.color === color);
  const go = () => {
    if (!size) return setErr(true);
    if (!inStock(size)) return;
    add({ id: p.id, name: p.name, price: p.price, tone: p.tone, image: p.image, size, color });
  };
  return (
    <>
      <div className="opt"><b>Colour</b>
        <div className="dots big">{p.colors.map((c) => <button key={c} onClick={() => { setColor(c); setSize(null); setErr(false); }} className={c === color ? 'on' : ''} style={{ background: c === "Beige" ? "#e6d3b3" : c === "Burgundy" ? "#800020" : c }} aria-label={c} title={c} />)}</div>
      </div>
      <div className="opt"><b>Size</b>
        <div className="sizes">{p.sizes.map((s) => <button key={s} disabled={!inStock(s)} onClick={() => { setSize(s); setErr(false); }} className={s === size ? 'on' : ''}>{s}</button>)}</div>
        {err && <small className="err">Pick a size before adding to cart.</small>}
      </div>
      {available === null && <p role="status">Stock is temporarily unavailable.</p>}
      {available && !available.some((variant) => variant.color === color) && <p role="status">Out of stock.</p>}
      <button className="btn" onClick={go} disabled={!p.sizes.some(inStock)}>Add to cart</button>
    </>
  );
}
