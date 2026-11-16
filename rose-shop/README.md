# Rosalie – dyqan online për rroba femrash (Next.js 14)

    npm install
    npm run dev      # http://localhost:3000

Ndrysho emrin, transportin dhe kontaktet te `lib/config.js`.
Produktet janë te `lib/products.js` (shto `image: '/products/foto.jpg'` për foto të vërteta).
Porositë shkojnë te `app/api/order/route.js`, ku mund t'i lidhësh me Django, email ose Telegram.

## Backend i porosive

Django ruan porosite me pagese ne dorezim dhe statuset e tyre. Django menaxhon katalogun dhe çmimet. Rregullat e transportit janë në Next.js.

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

### Katalogu dhe stoku

Ekzekuto `python backend/manage.py sync_stock` pas migrimeve për të importuar
katalogun fillestar të Rose Shop dhe sasitë nga tabela e vjetër e stokut.
Komanda ruan produktet e krijuara ose të ndryshuara më parë në panel.

Në panel, krijo ose zgjidh një **Category** dhe pastaj
shto produktin te **Products**. Zgjidh masat dhe ngjyrat. Pas ruajtjes,
vendos sasitë te tabela e varianteve dhe ngarko fotot. Për të fshehur një
produkt, çaktivizoje nga paneli. Te **Hero slides** mund të ndryshosh
bannerin e faqes kryesore. Dyqani shfaq slide-in e parë aktiv sipas renditjes.

Për instalim në server, ruaje `backend/media` në disk persistent dhe
konfiguro shërbimin e skedarëve në `/media/`. Vendos `PUBLIC_API_ORIGIN`
me adresën publike të backend-it për fotot.
