export const categories = [
 {
  "slug": "fustane",
  "name": "Dresses"
 },
 {
  "slug": "bluza",
  "name": "Tops & Knits"
 },
 {
  "slug": "veshje-e-jashtme",
  "name": "Blazers & Outerwear"
 },
 {
  "slug": "sportive",
  "name": "Casual"
 }
];
export const products = [
 {
  "id": 1,
  "slug": "ribbed-midi-dress",
  "name": "Ribbed Midi Dress",
  "price": 3500,
  "cat": "fustane",
  "isNew": true,
  "best": true,
  "colors": [
   "#1C1C1C"
  ],
  "tone": [
   "#D9D4D4",
   "#8E8888"
  ],
  "desc": "Fitted midi dress in a ribbed knit with a V-neckline and open back. Simple, clean and easy to dress up.",
  "sizes": [
   "XS",
   "S",
   "M",
   "L",
   "XL"
  ],
  "image": "/products/black-dress.jpeg"
 },
 {
  "id": 2,
  "slug": "pink-jumpsuit",
  "name": "Pink Wide-Leg Jumpsuit",
  "price": 3800,
  "cat": "sportive",
  "isNew": true,
  "colors": [
   "#E2559A"
  ],
  "tone": [
   "#F6C9D3",
   "#E2559A"
  ],
  "desc": "Relaxed jumpsuit with thin straps, a drawstring waist and wide legs with side slits.",
  "sizes": [
   "XS",
   "S",
   "M",
   "L",
   "XL"
  ],
  "image": "/products/pink-jumpsuit.jpeg"
 },
 {
  "id": 3,
  "slug": "white-midi-dress",
  "name": "White Satin Midi Dress",
  "price": 4800,
  "old": 5800,
  "cat": "fustane",
  "isNew": true,
  "best": true,
  "colors": [
   "#FFFFFF"
  ],
  "tone": [
   "#F3ECEC",
   "#D8CFCF"
  ],
  "desc": "Satin midi dress with a sweetheart neckline, low back and a full, pleated skirt.",
  "sizes": [
   "XS",
   "S",
   "M",
   "L",
   "XL"
  ],
  "image": "/products/white-dress.jpeg"
 },
 {
  "id": 4,
  "slug": "knit-vest-shirt",
  "name": "Knit Vest & Oversized Shirt",
  "price": 4200,
  "cat": "bluza",
  "isNew": false,
  "best": true,
  "colors": [
   "#2B2B2B"
  ],
  "tone": [
   "#D9D4D4",
   "#8E8888"
  ],
  "desc": "Oversized white shirt layered under a chunky knit vest. Wear them together or separately.",
  "sizes": [
   "XS",
   "S",
   "M",
   "L",
   "XL"
  ],
  "image": "/products/vest-shirt.jpeg"
 },
 {
  "id": 5,
  "slug": "lilac-flared-top",
  "name": "Lilac Flared Sleeve Top",
  "price": 2800,
  "cat": "bluza",
  "isNew": true,
  "colors": [
   "#B79BD6"
  ],
  "tone": [
   "#E6DCF0",
   "#B79BD6"
  ],
  "desc": "Fitted knit top in lilac with ruffled flared sleeves and contrast stripe trim.",
  "sizes": [
   "XS",
   "S",
   "M",
   "L",
   "XL"
  ],
  "image": "/products/lilac-top.jpeg"
 },
 {
  "id": 6,
  "slug": "white-blazer",
  "name": "White Tailored Blazer",
  "price": 6500,
  "old": 8500,
  "cat": "veshje-e-jashtme",
  "isNew": false,
  "colors": [
   "#FFFFFF"
  ],
  "tone": [
   "#EFE6E6",
   "#CFC4C4"
  ],
  "desc": "Structured single-button blazer with strong shoulders and a deep shawl lapel.",
  "sizes": [
   "XS",
   "S",
   "M",
   "L",
   "XL"
  ],
  "image": "/products/white-blazer.jpeg"
 }
];
export const bySlug = (s) => products.find((p) => p.slug === decodeURIComponent(s));
