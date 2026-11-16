import { loadCatalog, offlineCatalog } from '@/lib/catalog';
import Saved from './Saved';

export default async function SavedPage() {
  const { products } = (await loadCatalog()) ?? offlineCatalog;
  return <Saved products={products} />;
}
