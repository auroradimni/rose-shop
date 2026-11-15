const fs = require('fs'), path = require('path');
const M = [
["Rroba femrash me elegancë dhe butësi","Soft, elegant clothing for women"],
["15% zbritje në gjithçka","15% off everything"],
["Fustane -20%","Dresses -20%"],["Sezoni i trikove","Knitwear season"],["Veshje e jashtme -45%","Outerwear -45%"],["Edicioni sportiv -50%","Sport edition -50%"],
["Ditët e festave","Holiday Season"],["Vetëm tone të pasura","Rich Tones Only"],["Rifreskim i veshjes së jashtme","Outerwear Refresh"],["Gati për palestër","Gym Ready"],
["Bluza & Triko","Tops & Knits"],["Pantallona & Xhinse","Pants & Jeans"],
["Fustan Satin Roze","Pink Satin Dress"],["Triko e Butë Blush","Soft Blush Knit"],["Xhinse Wide Leg","Wide Leg Jeans"],["Xhaketë Lëkure Kafe","Brown Leather Jacket"],["Set Sportiv Mauve","Mauve Sport Set"],["Fustan i Gjatë i Zi","Long Black Dress"],["Bluzë me Lidhëse","Tie Waist Blouse"],["Palto Bezhë","Beige Coat"],
["fustan-satin-roze","pink-satin-dress"],["triko-e-butë-blush","soft-blush-knit"],["xhinse-wide-leg","wide-leg-jeans"],["xhaketë-lëkure-kafe","brown-leather-jacket"],["set-sportiv-mauve","mauve-sport-set"],["fustan-i-gjatë-i-zi","long-black-dress"],["bluzë-me-lidhëse","tie-waist-blouse"],["palto-bezhë","beige-coat"],
["Fustan satini me prerje elegante dhe pëlhurë që bie bukur mbi trup. I përshtatshëm për darka dhe raste të veçanta.","Satin dress with an elegant cut and fabric that drapes beautifully. Perfect for dinners and special occasions."],
["Triko e ngrohtë me material të butë, që nuk të çjerr lëkurën. Mban formën edhe pas larjes.","Warm knit in a soft material that will not itch. Keeps its shape after washing."],
["Xhinse me këmbë të gjerë dhe bel të lartë. Shkojnë me çdo palë këpucë.","Wide-leg jeans with a high waist. They go with any pair of shoes."],
["Xhaketë nga lëkurë ekologjike me astar të brendshëm. Prerje e relaksuar.","Faux leather jacket with an inner lining. Relaxed fit."],
["Top dhe tajtse me bel të lartë, pëlhurë që merr frymë dhe nuk tejdukshme.","High-waist top and leggings set in breathable, non-see-through fabric."],
["Fustan i gjatë me të çarë anësore. Klasik dhe i lehtë për t\\'u kombinuar.","Long dress with a side slit. Classic and easy to style."],
["Bluzë e lehtë me lidhëse në bel. Për ditë të ngrohta ose me xhaketë sipër.","Light blouse with a tie at the waist. For warm days or under a jacket."],
["Palto e gjatë nga përzierje leshi, me kopsa të fshehura.","Long wool-blend coat with hidden buttons."],
["Kërko në veshje femrash","Search women clothing"],["Përfundon pas: ","Ends in: "],["DITËT E ZBRITJES | ","SALE DAYS | "],["% OFF GJITHÇKA · KODI ","% OFF EVERYTHING · CODE "],
["Transport falas mbi ","Free shipping over "],["ZBRITJE DERI -50%","UP TO 50% OFF"],["Bli tani ›","Shop now ›"],["Bli tani","Shop now"],
["Të rejat","Newest"],["Të sapoardhurat","New Releases"],["Të reja","New In"],["Më të shiturat","Best Sellers"],
["Veshje e jashtme","Outerwear"],["Veshje","Clothing"],["Fustane","Dresses"],["Sportive","Activewear"],
["POROSI E RE:","NEW ORDER:"],["Zbritje (","Discount ("],["Kodi i zbritjes","Discount code"],["Zbritje","Sale"],["Trendet","Trends"],["Ofertat","Deals"],["Sezoni i festave","Holiday Shop"],["E RE","NEW"],["E re","New"],
["Hiqe nga të ruajturat","Remove from saved"],["Të ruajturat","Saved items"],["Shiko produktin","View product"],["Zgjidh opsionet","Select options"],["Ruaje","Save"],
["Çdo ditë me ","All day with "],["Bazat e përditshme","Everyday Essentials"],["Shiko më shumë","See more"],
["Modele të reja, ngjyra të buta dhe pjesë për çdo rast.","Fresh drops, soft colours and pieces for every occasion."],
["Raporti i trendeve","The Trend Report"],["Rezultatet për ","Results for "],["Koleksioni","Collection"],["Të gjitha","All"],["stile të gjetura","styles found"],["Rendit:","Sort:"],["Çmimi","Price"],
["Nuk u gjet asgjë. Provo një fjalë tjetër ose zgjidh një kategori.","Nothing found. Try another word or pick a category."],
["lang=\"sq\"","lang=\"en\""],["Rroba femrash","Women’s Clothing"],["Dërgesa në të gjithë Shqipërinë","Delivery across Albania"],["Dërgesë në të gjithë Shqipërinë","Delivery across Albania"],
["Tiranë","Tirana"],["Rrethe","Other cities"],["Pagesa në dorëzim","Cash on delivery"],
["Kthehu te koleksioni","Back to collection"],["Ndërrim masash brenda 3 ditëve","Size exchange within 3 days"],
["Zgjidh një masë para se ta shtosh në shportë.","Pick a size before adding to cart."],["Shto në shportë","Add to cart"],["Ngjyra","Colour"],["Masa","Size"],
["Shporta ime","My cart"],["Mbyll","Close"],["Shporta është bosh. Shiko koleksionin dhe zgjidh diçka që të pëlqen.","Your cart is empty. Browse the collection and pick something you love."],
["Të mungojnë edhe ${money(left)} për transport falas","${money(left)} away from free shipping"],["Ke fituar transport falas","You got free shipping"],
[">Hiq<",">Remove<"],["Nëntotali","Subtotal"],["Vazhdo te porosia","Continue to checkout"],["Shporta është bosh","Your cart is empty"],["Shporta","Cart"],
["Faleminderit për porosinë","Thank you for your order"],["Do të të kontaktojmë në telefon për konfirmim. Paguan kur e merr produktin.","We will call you to confirm. You pay when you receive your order."],
["Kthehu te faqja kryesore","Back to home"],["Shiko koleksionin","Browse the collection"],["Të dhënat e dërgesës","Delivery details"],["Emri dhe mbiemri","Full name"],["Numri i telefonit","Phone number"],
["Qyteti","City"],["Adresa","Address"],["Zona e dërgesës","Delivery zone"],["Shënim (opsionale)","Note (optional)"],["Pagesa bëhet në dorëzim.","You pay on delivery."],
["Porosia nuk u dërgua. Provo përsëri ose na shkruaj në WhatsApp.","Your order was not sent. Try again or message us on WhatsApp."],["Po dërgohet…","Sending…"],["Konfirmo porosinë","Place order"],
["Përmbledhja","Order summary"],["Transporti","Shipping"],["Totali","Total"],["Falas","Free"],["Shtyp Apliko për ta kontrolluar kodin.","Press Apply to check the code."],["Apliko","Apply"],
["Ende nuk ke ruajtur asgjë. Shtyp zemrën në një produkt që të pëlqen. ","You have not saved anything yet. Tap the heart on a product you like. "],
["Kthehu lart","Back to top"],["Të dhëna të pakompletuara","Incomplete data"],["Kërko","Search"],
];
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => e.isDirectory() ? (e.name === 'node_modules' || e.name === '.next' ? [] : walk(path.join(d, e.name))) : e.name.endsWith('.js') ? [path.join(d, e.name)] : []);
for (const f of ['app', 'components', 'lib'].flatMap(walk)) {
  let s = fs.readFileSync(f, 'utf8'); const o = s;
  for (const [a, b] of M) s = s.split(a).join(b);
  if (s !== o) { fs.writeFileSync(f, s); console.log('OK', f); }
}