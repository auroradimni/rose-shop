'use client';
import { createContext, useContext, useEffect, useReducer, useState } from 'react';

const Ctx = createContext(null);
export const useCart = () => useContext(Ctx);

function reducer(state, a) {
  switch (a.type) {
    case 'load': return a.items;
    case 'add': {
      const key = `${a.item.id}-${a.item.size}-${a.item.color}`;
      const found = state.find((i) => i.key === key);
      if (found) return state.map((i) => (i.key === key ? { ...i, qty: i.qty + 1 } : i));
      return [...state, { ...a.item, key, qty: 1 }];
    }
    case 'qty': return state.map((i) => (i.key === a.key ? { ...i, qty: Math.max(1, i.qty + a.d) } : i));
    case 'remove': return state.filter((i) => i.key !== a.key);
    case 'clear': return [];
    default: return state;
  }
}

export default function CartProvider({ children }) {
  const [items, dispatch] = useReducer(reducer, []);
  const [open, setOpen] = useState(false);
  const [ready, setReady] = useState(false);
  const [wish, setWish] = useState([]);

  useEffect(() => {
    try { dispatch({ type: 'load', items: JSON.parse(localStorage.getItem('cart') || '[]') }); } catch {}
    try { setWish(JSON.parse(localStorage.getItem('wish') || '[]')); } catch {}
    setReady(true);
  }, []);
  useEffect(() => { if (ready) localStorage.setItem('cart', JSON.stringify(items)); }, [items, ready]);
  useEffect(() => { if (ready) localStorage.setItem('wish', JSON.stringify(wish)); }, [wish, ready]);
  const toggleWish = (id) => setWish((w) => (w.includes(id) ? w.filter((x) => x !== id) : [...w, id]));

  const count = items.reduce((s, i) => s + i.qty, 0);
  const subtotal = items.reduce((s, i) => s + i.qty * i.price, 0);
  const add = (item) => { dispatch({ type: 'add', item }); setOpen(true); };

  return <Ctx.Provider value={{ wish, toggleWish, items, dispatch, count, subtotal, add, open, setOpen }}>{children}</Ctx.Provider>;
}
