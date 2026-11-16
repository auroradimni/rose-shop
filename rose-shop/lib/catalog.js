import { categories as originalCategories, products as originals } from './products';

export async function loadCatalog() {
  try {
    const origin = process.env.ORDER_BACKEND_URL || 'http://127.0.0.1:8000';
    const response = await fetch(new URL('/api/catalog/', origin), {
      cache: 'no-store',
      signal: AbortSignal.timeout(3000),
    });
    if (!response.ok) return null;
    const catalog = await response.json();
    return {
      ...catalog,
      products: catalog.products.map((product) => {
        const original = originals.find((item) => item.slug === product.slug);
        return {
          ...product,
          id: original?.id ?? product.slug,
          image: product.image || original?.image,
          tone: original?.tone ?? ['#FBE4E8', '#E8A5B5'],
        };
      }),
    };
  } catch {
    return null;
  }
}

export const offlineCatalog = {
  categories: originalCategories,
  products: originals.map((product) => ({ ...product, available: null })),
  hero: null,
};
