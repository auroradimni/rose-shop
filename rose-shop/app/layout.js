import { Cormorant_Garamond, Jost } from 'next/font/google';
import './globals.css';
import CartProvider from '@/components/CartProvider';
import Header from '@/components/Header';
import ScrollTop from '@/components/ScrollTop';
import CartDrawer from '@/components/CartDrawer';
import { SHOP } from '@/lib/config';

const display = Cormorant_Garamond({ subsets: ['latin', 'latin-ext'], weight: ['400', '500', '600'], style: ['normal', 'italic'], variable: '--f-display' });
const body = Jost({ subsets: ['latin', 'latin-ext'], variable: '--f-body' });

export const metadata = { title: `${SHOP.name} | Women’s Clothing`, description: SHOP.tagline };

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable}`}>
      <body>
        <CartProvider>
          <Header />
          <main>{children}</main>
          <CartDrawer />
          <ScrollTop />
          <footer className="footer">
            <div><h4>{SHOP.name}</h4><p>{SHOP.tagline}</p></div>
            <div><p>Delivery across Albania</p><p>Tirana {SHOP.shipping.tirana} {SHOP.currency} · Other cities {SHOP.shipping.rest} {SHOP.currency}</p><p>Cash on delivery</p></div>
            <div><a href={SHOP.instagram}>Instagram</a><a href={`https://wa.me/${SHOP.whatsapp}`}>WhatsApp</a></div>
          </footer>
        </CartProvider>
      </body>
    </html>
  );
}
