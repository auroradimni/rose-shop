export default function Logo({ size = 76 }) {
  const iw = 988, ih = 868, cx = 514, cy = 435.5, r = 392, k = size / (2 * r);
  return <span role="img" aria-label="Beauty Heaven Store" style={{ display: 'block', width: size, height: size, borderRadius: '50%', backgroundImage: 'url(/logo.jpeg)', backgroundRepeat: 'no-repeat', backgroundSize: `${iw * k}px ${ih * k}px`, backgroundPosition: `${size / 2 - cx * k}px ${size / 2 - cy * k}px` }} />;
}
