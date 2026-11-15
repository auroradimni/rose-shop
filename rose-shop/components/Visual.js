// Foto e produktit; nëse s'ka foto, shfaq një sfond rozë të butë
export default function Visual({ p, big }) {
  if (p.image) return <img src={p.image} alt={p.name} className="visual" />;
  return (
    <div className={`visual ph ${big ? 'big' : ''}`} style={{ background: `linear-gradient(160deg, ${p.tone[0]}, ${p.tone[1]})` }}>
      <span>{p.name.split(' ')[0]}</span>
    </div>
  );
}
