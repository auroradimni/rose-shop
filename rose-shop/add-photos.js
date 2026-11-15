
const fs = require('fs'), path = require('path');
const dir = path.join('public', 'products');
if (!fs.existsSync(dir)) { console.log('Krijo folderin public/products dhe vendos 7 fotot brenda.'); process.exit(1); }

// 1) Riemërto fotot nga emrat e WhatsApp
const W = 'WhatsApp_Image_2026-11-12_at_22_35_';
const MAP = { [W + '00__1_']: 'black-dress', [W + '00']: 'pink-jumpsuit', [W + '01__1_']: 'white-dress', [W + '01__2_']: 'vest-shirt', [W + '01__3_']: 'logo', [W + '01__4_']: 'lilac-top', [W + '01']: 'white-blazer' };
for (const f of fs.readdirSync(dir)) {
  const ext = path.extname(f), key = path.basename(f, ext).replace(/[^A-Za-z0-9-]/g, '_');
  if (MAP[key]) fs.renameSync(path.join(dir, f), path.join(dir, MAP[key] + ext.toLowerCase()));
}
const find = (n) => fs.readdirSync(dir).find((f) => f.startsWith(n + '.'));
const miss = ['black-dress', 'pink-jumpsuit', 'white-dress', 'vest-shirt', 'logo', 'lilac-top', 'white-blazer'].filter((n) => !find(n));
if (miss.length) { console.log('Mungojnë këto foto:', miss.join(', ')); process.exit(1); }

// 2) Logo dhe hero
const logo = find('logo');
fs.copyFileSync(path.join(dir, logo), path.join('public', logo));
fs.copyFileSync(path.join(dir, find('white-dress')), path.join('public', 'hero.jpg'));
fs.writeFileSync('components/Logo.js', `export default function Logo({ size = 76 }) {
  const iw = 988, ih = 868, cx = 514, cy = 435.5, r = 392, k = size / (2 * r);
  return <span role="img" aria-label="Beauty Heaven Store" style={{ display: 'block', width: size, height: size, borderRadius: '50%', backgroundImage: 'url(/${logo})', backgroundRepeat: 'no-repeat', backgroundSize: \`\${iw * k}px \${ih * k}px\`, backgroundPosition: \`\${size / 2 - cx * k}px \${size / 2 - cy * k}px\` }} />;
}
`);
let h = fs.readFileSync('components/Header.js', 'utf8');
if (!h.includes("./Logo")) {
  h = h.replace("import { useCart } from './CartProvider';", "import { useCart } from './CartProvider';\nimport Logo from './Logo';")
       .replace('<Link href="/" className="logo">{SHOP.name}</Link>', '<Link href="/" className="logo" aria-label={SHOP.name}><Logo size={72} /></Link>');
  fs.writeFileSync('components/Header.js', h);
}

// 3) Produktet
const S = ['XS', 'S', 'M', 'L', 'XL'];
const items = [
  { id: 1, slug: 'ribbed-midi-dress', name: 'Ribbed Midi Dress', price: 3500, cat: 'fustane', isNew: true, best: true, colors: ['#1C1C1C'], tone: ['#D9D4D4', '#8E8888'], img: 'black-dress', desc: 'Fitted midi dress in a ribbed knit with a V-neckline and open back. Simple, clean and easy to dress up.' },
  { id: 2, slug: 'pink-jumpsuit', name: 'Pink Wide-Leg Jumpsuit', price: 3800, cat: 'sportive', isNew: true, colors: ['#E2559A'], tone: ['#F6C9D3', '#E2559A'], img: 'pink-jumpsuit', desc: 'Relaxed jumpsuit with thin straps, a drawstring waist and wide legs with side slits.' },
  { id: 3, slug: 'white-midi-dress', name: 'White Satin Midi Dress', price: 4800, old: 5800, cat: 'fustane', isNew: true, best: true, colors: ['#FFFFFF'], tone: ['#F3ECEC', '#D8CFCF'], img: 'white-dress', desc: 'Satin midi dress with a sweetheart neckline, low back and a full, pleated skirt.' },
  { id: 4, slug: 'knit-vest-shirt', name: 'Knit Vest & Oversized Shirt', price: 4200, cat: 'bluza', isNew: false, best: true, colors: ['#2B2B2B'], tone: ['#D9D4D4', '#8E8888'], img: 'vest-shirt', desc: 'Oversized white shirt layered under a chunky knit vest. Wear them together or separately.' },
  { id: 5, slug: 'lilac-flared-top', name: 'Lilac Flared Sleeve Top', price: 2800, cat: 'bluza', isNew: true, colors: ['#B79BD6'], tone: ['#E6DCF0', '#B79BD6'], img: 'lilac-top', desc: 'Fitted knit top in lilac with ruffled flared sleeves and contrast stripe trim.' },
  { id: 6, slug: 'white-blazer', name: 'White Tailored Blazer', price: 6500, old: 8500, cat: 'veshje-e-jashtme', isNew: false, colors: ['#FFFFFF'], tone: ['#EFE6E6', '#CFC4C4'], img: 'white-blazer', desc: 'Structured single-button blazer with strong shoulders and a deep shawl lapel.' },
].map(({ img, ...p }) => ({ ...p, sizes: S, image: '/products/' + find(img) }));
const cats = [{ slug: 'fustane', name: 'Dresses' }, { slug: 'bluza', name: 'Tops & Knits' }, { slug: 'veshje-e-jashtme', name: 'Blazers & Outerwear' }, { slug: 'sportive', name: 'Casual' }];
fs.writeFileSync('lib/products.js', `export const categories = ${JSON.stringify(cats, null, 1)};\nexport const products = ${JSON.stringify(items, null, 1)};\nexport const bySlug = (s) => products.find((p) => p.slug === decodeURIComponent(s));\n`);

// 4) Emri, Instagram, trendet, shporta me foto, CSS
const rep = (file, pairs) => { let s = fs.readFileSync(file, 'utf8'); for (const [a, b] of pairs) s = s.split(a).join(b); fs.writeFileSync(file, s); };
rep('lib/config.js', [["name: 'Rosalie'", "name: 'Beauty Heaven'"], ['https://instagram.com/yourshop', 'https://instagram.com/beauty.heaven.store'], ['Gym Ready', 'Weekend Casual']]);
rep('components/AddToCart.js', [['tone: p.tone,', 'tone: p.tone, image: p.image,']]);
rep('components/CartDrawer.js', [['style={{ background: i.tone[1] }}', "style={{ background: i.image ? `url(${i.image}) center/cover` : i.tone[1] }}"]]);
const css = fs.readFileSync('app/globals.css', 'utf8');
if (!css.includes('/* photos */')) fs.appendFileSync('app/globals.css', `\n/* photos */\n.logo{display:block;line-height:0}\n.header{padding-top:10px;padding-bottom:10px}\n.hero3{background-position:center,center 28%,center}\n`);
console.log('U krye. Rifresko faqen.');