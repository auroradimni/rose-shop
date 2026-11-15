'use client';
import Link from 'next/link';
import { useCart } from './CartProvider';
import { money, SHOP } from '@/lib/config';

export default function CartDrawer() {
  const { items, dispatch, subtotal, open, setOpen } = useCart();
  const left = Math.max(0, SHOP.shipping.freeOver - subtotal);
  return (
    <>
      <div className={`overlay ${open ? 'show' : ''}`} onClick={() => setOpen(false)} />
      <aside className={`drawer ${open ? 'open' : ''}`} aria-hidden={!open}>
        <div className="drawer-head"><h2>My cart</h2><button onClick={() => setOpen(false)} aria-label="Close">✕</button></div>
        {items.length === 0 ? <p className="empty">Your cart is empty. Browse the collection and pick something you love.</p> : (
          <>
            <p className="free">{left > 0 ? `${money(left)} away from free shipping` : 'You got free shipping'}</p>
            <ul>
              {items.map((i) => (
                <li key={i.key}>
                  <div className="sw" style={{ background: i.image ? `url(${i.image}) center/cover` : i.tone[1] }} />
                  <div className="grow">
                    <b>{i.name}</b>
                    <small>Size {i.size}</small>
                    <div className="qty">
                      <button onClick={() => dispatch({ type: 'qty', key: i.key, d: -1 })}>−</button>
                      <span>{i.qty}</span>
                      <button onClick={() => dispatch({ type: 'qty', key: i.key, d: 1 })}>+</button>
                    </div>
                  </div>
                  <div className="right">
                    <span>{money(i.price * i.qty)}</span>
                    <button className="link" onClick={() => dispatch({ type: 'remove', key: i.key })}>Remove</button>
                  </div>
                </li>
              ))}
            </ul>
            <div className="drawer-foot">
              <p><span>Subtotal</span><b>{money(subtotal)}</b></p>
              <Link href="/arka" className="btn" onClick={() => setOpen(false)}>Continue to checkout</Link>
            </div>
          </>
        )}
      </aside>
    </>
  );
}
