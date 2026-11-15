const fs = require('fs');
const find = (n) => fs.readdirSync('public/products').find((f) => f.startsWith(n + '.'));
const T = { 'Holiday Season': 'white-dress', 'Rich Tones Only': 'black-dress', 'Outerwear Refresh': 'white-blazer', 'Weekend Casual': 'pink-jumpsuit' };
let c = fs.readFileSync('lib/config.js', 'utf8');
for (const [title, img] of Object.entries(T)) {
  if (!c.includes(`title: '${title}', image`)) c = c.replace(`title: '${title}',`, `title: '${title}', image: '/products/${find(img)}',`);
}
fs.writeFileSync('lib/config.js', c);
let p = fs.readFileSync('app/page.js', 'utf8');
const old = '<div style={{ background: `linear-gradient(170deg, ${t.tone[0]}, ${t.tone[1]})` }} />';
if (!p.includes('trendimg')) p = p.replace(old, '{t.image ? <img src={t.image} alt={t.title} className="trendimg" /> : ' + old + '}');
fs.writeFileSync('app/page.js', p);
const css = fs.readFileSync('app/globals.css', 'utf8');
if (!css.includes('.trendimg')) fs.appendFileSync('app/globals.css', '\n.trendimg{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;object-position:center top}\n');
console.log('U krye. Rifresko faqen.');