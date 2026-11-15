'use client';
import { useState } from 'react';
import { useCart } from './CartProvider';

export default function AddToCart({ p }) {
  const { add } = useCart();
  const [size, setSize] = useState(null);
  const [color, setColor] = useState(p.colors[0]);
  const [err, setErr] = useState(false);
  const go = () => {
    if (!size) return setErr(true);
    add({ id: p.id, name: p.name, price: p.price, tone: p.tone, image: p.image, size, color });
  };
  return (
    <>
      <div className="opt"><b>Colour</b>
        <div className="dots big">{p.colors.map((c) => <button key={c} onClick={() => setColor(c)} className={c === color ? 'on' : ''} style={{ background: c }} aria-label={c} />)}</div>
      </div>
      <div className="opt"><b>Size</b>
        <div className="sizes">{p.sizes.map((s) => <button key={s} onClick={() => { setSize(s); setErr(false); }} className={s === size ? 'on' : ''}>{s}</button>)}</div>
        {err && <small className="err">Pick a size before adding to cart.</small>}
      </div>
      <button className="btn" onClick={go}>Add to cart</button>
    </>
  );
}
