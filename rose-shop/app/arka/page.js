'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useCart } from '@/components/CartProvider';
import { money, SHOP, PROMO } from '@/lib/config';

export default function Checkout() {
  const { items, subtotal, dispatch } = useCart();
  const [f, setF] = useState({ name: '', phone: '', city: '', address: '', zone: 'tirana', note: '' });
  const [state, setState] = useState('idle');
  const [code, setCode] = useState('');
  const [applied, setApplied] = useState(false);
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  const ship = subtotal >= SHOP.shipping.freeOver ? 0 : SHOP.shipping[f.zone];
  const disc = applied ? Math.round(subtotal * PROMO.percent / 100) : 0;
  const total = subtotal - disc + ship;

  const submit = async (e) => {
    e.preventDefault();
    setState('loading');
    try {
      const r = await fetch('/api/order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...f, items, subtotal, ship, disc, code: applied ? code : null, total }) });
      if (!r.ok) throw new Error();
      dispatch({ type: 'clear' });
      setState('done');
    } catch { setState('error'); }
  };

  if (state === 'done') return (
    <section className="wrap narrow center"><h1>Thank you for your order</h1><p>We will call you to confirm. You pay when you receive your order.</p><Link href="/" className="btn">Back to home</Link></section>
  );
  if (!items.length) return (
    <section className="wrap narrow center"><h1>Your cart is empty</h1><Link href="/" className="btn">Browse the collection</Link></section>
  );

  return (
    <section className="wrap checkout">
      <form onSubmit={submit}>
        <h1>Delivery details</h1>
        <label>Full name<input required value={f.name} onChange={set('name')} autoComplete="name" /></label>
        <label>Phone number<input required type="tel" value={f.phone} onChange={set('phone')} autoComplete="tel" /></label>
        <label>City<input required value={f.city} onChange={set('city')} autoComplete="address-level2" /></label>
        <label>Address<input required value={f.address} onChange={set('address')} autoComplete="street-address" /></label>
        <label>Delivery zone
          <select value={f.zone} onChange={set('zone')}>
            <option value="tirana">Tirana ({SHOP.shipping.tirana} {SHOP.currency})</option>
            <option value="rest">Other cities ({SHOP.shipping.rest} {SHOP.currency})</option>
          </select>
        </label>
        <label>Note (optional)<textarea rows="3" value={f.note} onChange={set('note')} /></label>
        <p className="pay">You pay on delivery.</p>
        {state === 'error' && <p className="err">Your order was not sent. Try again or message us on WhatsApp.</p>}
        <button className="btn" disabled={state === 'loading'}>{state === 'loading' ? 'Sending…' : 'Place order'}</button>
      </form>
      <aside className="summary">
        <h2>Order summary</h2>
        <div className="codebox"><input placeholder="Discount code" value={code} onChange={(e) => { setCode(e.target.value); setApplied(false); }} /><button type="button" className="btn sm" onClick={() => setApplied(code.trim().toUpperCase() === PROMO.code)}>Apply</button></div>
        {code && !applied && <small className="hint">Press Apply to check the code.</small>}
        {items.map((i) => <p key={i.key}><span>{i.name} · {i.size} × {i.qty}</span><span>{money(i.price * i.qty)}</span></p>)}
        <p><span>Subtotal</span><span>{money(subtotal)}</span></p>
        {disc > 0 && <p><span>Discount ({PROMO.code})</span><span>-{money(disc)}</span></p>}
        <p><span>Shipping</span><span>{ship ? money(ship) : 'Free'}</span></p>
        <p className="total"><span>Total</span><b>{money(total)}</b></p>
      </aside>
    </section>
  );
}
