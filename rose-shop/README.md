# Rosalie – dyqan online për rroba femrash (Next.js 14)

    npm install
    npm run dev      # http://localhost:3000

Ndrysho emrin, transportin dhe kontaktet te `lib/config.js`.
Produktet janë te `lib/products.js` (shto `image: '/products/foto.jpg'` për foto të vërteta).
Porositë shkojnë te `app/api/order/route.js`, ku mund t'i lidhësh me Django, email ose Telegram.

## Backend i porosive

Django ruan porosite me pagese ne dorezim dhe statuset e tyre. Katalogu,
cmimet dhe rregullat e transportit vine nga aplikacioni Next.js.

Hap PowerShell ne dosjen me `package.json` te aplikacionit. Vendos nje vlere
sekrete per `ORDER_API_TOKEN` dhe perdor te njejten vlere ne te dy terminalet.

Terminali i backend-it:

```powershell
$env:DJANGO_DEBUG = '1'
$env:ORDER_API_TOKEN = '<sekreti yt lokal>'
python -m pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py sync_stock
python backend/manage.py createsuperuser
python backend/manage.py runserver 127.0.0.1:8000
```

Terminali i frontend-it:

```powershell
$env:ORDER_API_TOKEN = '<i njejti sekret>'
npm run dev
```

Porosite shfaqen te [paneli i administrimit](http://127.0.0.1:8000/admin/).
Per deployment vendos edhe `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` dhe
`ORDER_BACKEND_URL` sipas hosteve te tu. Perdore `ROSE_DB_PATH` per nje disk
persistent dhe sherbe skedaret e admin-it pas `python backend/manage.py collectstatic`.

### Stoku

Pas migrimeve, ekzekuto `python backend/manage.py sync_stock` sa herë shton
produkte, masa ose ngjyra te `lib/products.js`. Komanda shton variantet e reja
me sasi zero dhe ruan sasitë ekzistuese. Vendos numrin real të njësive për çdo
variant te **Orders → Stock variants** në panelin e administrimit. Faqja e
produktit çaktivizon masat pa stok. Porosia ul sasinë e disponueshme dhe
anulimi nga paneli e kthen sasinë në stok. Porositë e krijuara para këtij
ndryshimi nuk kanë rezervuar stok.
