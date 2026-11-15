// Ndrysho emrin, kontaktet dhe çmimet e transportit këtu
export const SHOP = {
  name: 'Beauty Heaven',
  tagline: 'Soft, elegant clothing for women',
  instagram: 'https://instagram.com/beauty.heaven.store',
  whatsapp: '355690000000',
  shipping: { tirana: 200, rest: 300, freeOver: 2000 },
  currency: 'L',
};
export const money = (n) => `${n} ${SHOP.currency}`;

export const PROMO = { text: '15% off everything', code: 'ROSE15', percent: 15, ends: '2026-11-20T23:59:59' };
export const TILES = [
  { k: 'fustane', label: 'Dresses -20%', tone: ['#F6C9D3', '#D9788F'] },
  { k: 'bluza', label: 'Knitwear season', tone: ['#FBE4E8', '#E8A5B5'] },
  { k: 'veshje-e-jashtme', label: 'Outerwear -45%', tone: ['#EBD3CB', '#B98A7B'] },
  { k: 'sportive', label: 'Sport edition -50%', tone: ['#EBCFDD', '#B07A93'] },
];

export const TRENDS = [
  { title: 'Holiday Season', image: '/products/white-dress.jpeg', href: '/?k=fustane#koleksioni', tone: ['#FBE4E8', '#E8A5B5'] },
  { title: 'Rich Tones Only', image: '/products/black-dress.jpeg', href: '/?k=bluza#koleksioni', tone: ['#EBCFDD', '#B07A93'] },
  { title: 'Outerwear Refresh', image: '/products/white-blazer.jpeg', href: '/?k=veshje-e-jashtme#koleksioni', tone: ['#F1E1DA', '#C79F8E'] },
  { title: 'Weekend Casual', image: '/products/pink-jumpsuit.jpeg', href: '/?k=sportive#koleksioni', tone: ['#F6C9D3', '#D9788F'] },
];
