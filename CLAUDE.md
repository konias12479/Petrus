# Petrus — kontext pro Claude Code

## Kontrola modelu a kontextu — udělej TOTO JAKO PRVNÍ, před jakoukoli prací

Vstupní kontrola má dvě části: (A) sedí nastavený model na náročnost
úkolu? (B) není kontextové okno session už příliš plné na to, aby mělo
smysl pokračovat tady? Obě proveď při každém požadavku, výsledek obou
patří do jedné potvrzovací řádky.

### Část A — kontrola modelu

1. **Zařaď úkol:**
   - **Rutinní** (přejmenování, drobná oprava textu/stylu, jednoduchý
     bugfix, doplnění řádku do existujícího seznamu) → stačí **menší
     model (Sonnet), nízký effort**.
   - **Středně náročný** (nová funkce v rámci existujícího vzoru,
     úprava více provázaných míst) → **Sonnet s vysokým effort**, nebo
     větší model se středním.
   - **Architektonický / citlivý** (změna datového modelu, přístupová
     práva, peníze/bezpečnost, refaktoring napříč soubory, cokoliv
     „navrhni/vymysli/rozhodni") → **nejsilnější dostupný model,
     vysoký effort**.
2. **Porovnej se skutečně nastaveným modelem** (vidíš ho v UI u pole
   pro zadání).
3. **Pokud nesedí — v KTERÉMKOLI směru — ZASTAV ÚLOHU.** „Nesedí"
   znamená: nastavený model je **slabší**, než úkol žádá, **NEBO
   zbytečně silnější** (dražší), než je potřeba. V obou případech
   napiš jen doporučení, jaký model a effort přepnout a proč, a
   **nezačínej pracovat**, dokud uživatel model nepřepne a nepotvrdí
   to. Formulace typu „klidně by stačil menší model — pokračuji" je
   porušení tohoto pravidla: správná reakce je zastavit a doporučit
   menší model. (Model nejde přepnout programově — přepíná ho uživatel
   v UI.) Žádná výjimka typu „pokračuj i tak" neplatí — úloha čeká na
   přepnutí.
4. **Pokud sedí,** napiš jednu potvrzovací řádku a pokračuj — je to
   jediný způsob, jak uživatel pozná, že kontrola proběhla.
5. Kontrolu prováděj při **každém** požadavku, i uprostřed dlouhé
   konverzace a po spuštění skillů/nástrojů. První řádek každé odpovědi
   na nový požadavek je buď potvrzení, nebo doporučení.

### Část B — kontrola kontextu (zdraví session)

Přesné počítadlo tokenů nevidíš — vyhodnocuj pozorovatelné signály:

1. **Proběhla kompaktace** — v konverzaci je souhrn předchozí části
   („This session is being continued…"). Detaily starší práce existují
   už jen jako parafráze.
2. **Druhá a další kompaktace** — kritický stav, souhrn souhrnu ztrácí
   informace exponenciálně.
3. **Měkké signály:** musel jsi znovu načítat velké soubory, jejichž
   obsah „vypadl"; session pokrývá několik velkých uzavřených témat;
   harness zobrazuje reminder o context managementu.

**Reakce (tři stupně):**

- **Zelená** → v potvrzovací řádce „kontext OK", pracuj normálně.
- **Oranžová** (jedna kompaktace NEBO silné měkké signály) → aktuální
  požadavek dokonči, ale ohlas „kontext ORANŽOVÁ — po tomto úkolu
  doporučím nový chat" a na konec odpovědi přidej předávací balíček.
  Velké NOVÉ téma už tady nezačínej — chovej se jako u červené.
- **Červená** (druhá kompaktace, nebo velké nové téma při oranžové) →
  **nezačínej pracovat**; vysvětli proč, dej předávací balíček a čekej.
  Výjimky: uživatel výslovně řekne „pokračuj i tak"; drobnost na jednu
  odpověď (dotaz, commit hotové práce) dokonči vždy.

**Předávací balíček** — konkrétní, v code-blocku, ke zkopírování do
nového chatu:

```
Pokračuji z předchozí session. Stav:
- Branch: <branch>, poslední commit: <hash> „<message>" (pushnuto ano/ne)
- Hotovo v minulé session: <1–3 odrážky>
- Rozdělané / další krok: <co přesně, kde jsem skončil>
- Klíčové soubory k úkolu: <cesty, případně čísla řádků>
- Rozhodnutí, která nejsou zapsaná v CLAUDE.md ani v kódu: <pokud žádná, vynech>
Úkol: <čím má nová session začít>
```

Zásady balíčku: CLAUDE.md se v novém chatu načte samo — do balíčku patří
jen to, co v něm ani v repu není. Před předáním vše hotové commitni a
pushni (nová session vidí jen repo). Rozhodnutí trvalé platnosti zapiš
rovnou do CLAUDE.md, ať balíček zůstane krátký.

### Potvrzovací řádka (společná pro A i B)

*„✓ Model sedí (Sonnet High na středně náročný úkol) · kontext OK —
pokračuji."* — případně s oranžovým/červeným hlášením místo „kontext OK".

## Jak pracovat na tomto projektu

- Projekt = jednosouborová webová aplikace `index.html` (čtečka pro
  výuku angličtiny). Spouští se otevřením v prohlížeči; produkce je
  GitHub Pages (https://konias12479.github.io/Petrus/), nasazuje ji
  workflow `.github/workflows/pages.yml` při každém pushi do `main`.
  Repozitář musí zůstat **veřejný** — na private repu Pages bez
  placeného plánu nefunguje.
- **Po každé změně ověř, že nic nespadlo** — spusť Playwright test
  headless Chromiem (`/opt/pw-browsers/chromium`) proti lokálnímu
  `python3 -m http.server`; překladová API a CDN v kontejneru nejedou,
  mockuj je přes `page.route()`. Neposílej změnu bez ověření; i drobná
  úprava umí něco rozbít.
- **Edituj postupně a cíleně** — najdi přesnou kotvu (`grep -n`),
  použij cílený edit, neposkytuj celé soubory znovu.
- **Commituj po každé uzavřené funkci**, ne po každém dílčím kroku.
- **Každou dokončenou a ověřenou změnu vždy doveď až do `main`** —
  push větve → založ PR → **rovnou ho mergni**. Na merge se neptej a
  nečekej na vyzvání; uživatel chce vždy merge. Neptej se ani „mám
  založit PR?" — prostě to udělej. Co `main` servíruje
  (Pages/produkce), doplň, až bude jasné.

## Prostředí (platí pro Claude Code na webu)

- **WebFetch/curl na běžné weby nefunguje** — egress proxy povoluje jen
  GitHub a balíčkové registry. Pro rešerše používej **WebSearch** (limit
  ~200 dotazů na session — plánuj úsporně). Veřejné GitHub repozitáře
  jdou klonovat přes git proxy, i když WebFetch na github.com selže.
- Balíčky pro skripty (`jsdom`, `playwright`, …) nejsou v image —
  instaluj **jedním** `npm install … --no-save` (samostatné instalace
  se navzájem odinstalují). Skripty mimo repo spouštěj s
  `NODE_PATH=<repo>/node_modules` — POZOR: platí jen pro CommonJS
  `require`; ESM `import` NODE_PATH ignoruje, pro `.mjs` skripty ve
  scratchpadu udělej `ln -s <repo>/node_modules <scratchpad>/node_modules`.
  Chromium je v `/opt/pw-browsers/chromium` — playwrightu předej
  `executablePath`, nesmí stahovat vlastní build. Python balíčky přes
  `pip install` (PyPI je v povolených registrech) fungují — např.
  Pillow na zpracování obrázků.
- Kontejner je efemérní — co není commitnuté a pushnuté, po session
  zmizí. Dočasné soubory patří do scratchpad adresáře session.
- Egress proxy blokuje i cdnjs a překladová API aplikace — při
  testování v kontejneru je mockuj (`page.route()` v Playwrightu);
  v prohlížeči uživatele fungují normálně.

## Architektura projektu

- **`index.html`** — celá aplikace (HTML + CSS + JS v jednom souboru,
  bez build kroku, UI česky). Pohledy: knihovna → čtečka → slovníček +
  panel slovíčka + zásuvka nastavení vzhledu.
- **Import textů:** .txt nativně; .pdf přes pdf.js a .docx přes
  mammoth.js — obě knihovny se lazy-loadují z cdnjs až při potřebě
  (starý binární .doc podporován není, hlásí se srozumitelná chyba).
- **Překlady (klient, bez API klíče):** primárně neoficiální Google
  endpoint `translate.googleapis.com/translate_a/single?client=gtx`
  (dt=t překlad, dt=bd další významy), fallback MyMemory
  (`api.mymemory.translated.net`, limit ~5000 znaků/den anonymně).
  Výklad + příklady EN: `api.dictionaryapi.dev`. Výslovnost: Web
  Speech API (speechSynthesis). Odpovědi se cachují v localStorage
  (`petrus-tr-cache`, max 400 záznamů).
- **Úložiště:** texty v IndexedDB (db `petrus`, store `texts`,
  záznam `{id,title,addedAt,paragraphs[],pos:{page}}`; knihy ze
  základní knihovny mají navíc `builtin:<id>`); nastavení vzhledu
  `petrus-settings` a slovníček `petrus-words` v localStorage.
- **Základní knihovna:** public domain klasiky v `books/*.txt`
  (zdroj: Project Gutenberg přes GITenberg zrcadla na GitHubu,
  hlavičky/patičky ořezány), seznam `BUILTIN_BOOKS` v index.html;
  karta v knihovně → fetch → import do IndexedDB jako běžný text.
  **Pozor na licence:** přidávat sem jen skutečné public domain texty
  (Gutenberg). Zjednodušené „graded readers" (Oxford Bookworms,
  Penguin, english-e-reader.net apod.) jsou copyrightované — do
  veřejného repa NIKDY; uživatel si je může nahrát sám tlačítkem
  „Nahrát text" (zůstávají jen v jeho prohlížeči).
- **Ilustrace základní knihovny:** původní public domain ilustrace
  (Tenniel/Alice, Denslow/Oz, Paget/Sherlock; Gatsby žádné nemá).
  Zmenšené obrázky (700 px JPEG) v `books/img/<id>/`, manifesty
  `books/illustrations/<id>.json` (`items:[{par,src,alt?,cap?}]`,
  `par` = index odstavce z textToParagraphs). Generuje
  `tools/build_illustrations.py` (potřebuje Pillow — `pip install
  Pillow` v kontejneru funguje) z klonů ilustrovaných edic:
  standardebooks/lewis-carroll_alices-adventures-in-wonderland_john-tenniel,
  GITenberg/The-Wonderful-Wizard-of-Oz_43936 (pozor: zrcadlo #55 obrázky
  NEMÁ, Standard Ebooks Oz taky ne), GITenberg/Adventures-of-Sherlock-Holmes-Illustrated_48320.
  Kotvení: nejbližší odstavec u obrázku v ilustrované edici → fuzzy
  match (normalizace + SequenceMatcher, monotónně vpřed) na náš .txt.
  Čtečka: `paginate` si drží `parIdx`+`first`, `renderPage` vkládá
  `figure.ill` inline PŘED kotevní odstavec a plní boční lišty
  `#ill-rail` (vpravo) + `#ill-rail-left`; `railMode()` = 0/1/2 lišt
  podle volného místa (≈ šířka stránky + 460 / + 800 px; třídy
  `rail-on`/`rail-2` na `#view-reader`). Při lištách se inline figury
  skryjí; víc figur na stránce se střídavě rozdělí vpravo/vlevo; když
  stránka kotvu nemá, lišty ukážou nejbližší předchozí a následující
  ilustraci (jen v lištách, ne v textu) — obraz tak doprovází celou
  kapitolu. V dvoulištovém režimu (`railMode()===2`) se od v1.5.4
  i stránka s jen jedním vlastním obrázkem doplní o nejbližší další
  z knihy, ať druhá lišta nezůstane prázdná zbytečně — bez knihy
  s víc ilustracemi (jen jedna v celé knize) se nic nezdvojuje, druhá
  lišta prostě zůstane prázdná. Od v1.5.6 mají `figure.ill img` (inline
  i v liště) natrvalo stejný „stínohra" filtr jako přechodový overlay —
  `grayscale+contrast` + `mix-blend-mode:multiply` + radiální mask-image
  (jemnější než u `.sp-sil`, ať zůstane čitelný obsah) — místo dřívějšího
  bílého fotorámečku; sjednocuje to vzhled skenů (Tenniel/Denslow/Paget)
  i barevných fotek z Wikimedia Commons u nahraných knih. `#lightbox img`
  má vlastní selektor bez filtru — zvětšený náhled zůstává plnobarevný.
  Klik = lightbox (`#lightbox`), Escape/klik zavírá.
  Přepínač `settings.ills` v zásuvce vzhledu. Knihy s manifestem
  mají v `BUILTIN_BOOKS` příznak `ills:true` (jinak se fetch nedělá).
- **Stínohra kapitol:** při přechodu na stránku s nadpisem kapitoly
  (`isHeading` — vzory `CHAPTER I.`, `ADVENTURE I.`, `1. Titulek`,
  `VII. TITULEK`; jen knihy s ilustracemi) se na ~4,5 s ukáže overlay
  `#shadowplay`: „plátno lucerny" (radiální gradient + flicker) a 1–2
  nejbližší ilustrace kapitoly jako siluety — trik: `grayscale+contrast`
  + `mix-blend-mode:multiply` (bílé pozadí JPEG splyne s plátnem) +
  radiální `mask-image` viněta (rozpustí hrany celoplošných skenů,
  např. Pagetových). Klik/Escape zavírá, `settings.shadow` přepínač,
  `prefers-reduced-motion` stínohru zcela vypne. Spouští se i při
  otevření knihy (titulní karta s názvem, `openReader`). Jemné
  animace: figury v lištách fade-in + pomalé vznášení, lightbox
  pomalý zoom (jen bez reduced-motion). `#frieze` = statická koláž
  ilustrací při pravém okraji knihovny (fixed sloupec, `z-index:-1`
  za obsahem, střídavé natočení, viněta přes mask-image; pod šířku
  1360 px se schová; řídí ho týž `settings.shadow`). Původně to byl
  animovaný průvod siluet po spodním okraji — předěláno na statické
  na přání uživatele (v1.3.2).
- **Obálky nahraných knih (v1.4.0):** aplikace je jen pro soukromou
  potřebu vlastníka — obálky jeho vlastních (koupených) knih se
  dohledávají za běhu v prohlížeči a ukládají do IndexedDB
  (`rec.cover`), do veřejného repa nikdy nic nejde. Automat
  (`autoCover()`, po importu a při startu pro starší záznamy) má dva
  kroky v `findCoverUrl(title, paragraphs)`: (1) **vždy nejdřív**
  zkusí fulltextovou shodu — `pickSnippet()` vybere charakteristickou
  větu z textu (≥50 znaků, ne CAPS nadpis) a hledá ji jako přesnou
  frázi (`"…"`) v Google Books; shoda jednoznačně určí konkrétní
  knihu bez ohledu na to, jak obecný je název souboru. (2) Když fráze
  nikde není (kniha není v Google fulltext indexu), spadne na
  dohledání podle názvu — 10 kandidátů z Google Books (`intitle:`)
  s fallbackem na Open Library, vybírá se **přesná shoda
  normalizovaného názvu** (`normTitle` — jen a-z0-9), ne první
  „nejrelevantnější" výsledek (u krátkých/obecných názvů jako „48"
  byla čistá relevance nespolehlivá — v1.4.1 takhle omylem přišila
  obálku úplně jiné knihy). Bez přesné shody se u názvů kratších než
  8 znaků obálka vůbec nenasadí — radši žádná než špatná; delší
  názvy si první výsledek ponechají. Soubory z e-čteček mívají tvar
  „Název-Autor"/„Název_Autor_Jméno" — `title.split` nejdřív zkusí jen
  segment před pomlčkou (jméno autora přimíchané do `intitle:` dotazu
  hledání kazilo, viz „The_Incredible_Journey-Burnford_Sheila", v1.5.5),
  celý vyčištěný název je fallback. `rec.coverTried` brání
  opakovaným dotazům (u záznamu se automat spustí jen jednou;
  případnou špatnou/chybějící obálku napraví ruční tlačítko 🖼).
  Ručně:
  tlačítko 🖼 na kartě → file picker → zmenšení na 420 px přes canvas
  → JPEG dataURL (funguje offline a přepíše chybný automat). Karta
  bez obálky dál ukazuje název + úryvek. V kontejneru API mockovat
  přes `page.route()`; pozor, kód přepisuje `http:`→`https:` u URL
  z Google Books — mock musí servírovat přes vlastní doménu, ne
  `http://127.0.0.1`.
- **Ilustrace nahraných knih podle obsahu (v1.5.0):** stejný princip
  jako obálky — jen soukromě v prohlížeči, do repa nic. Detekce
  kapitol sdílená pro stínohru i ilustrace: `chapterStarts()`
  nejdřív zkusí „jistý" vzor (`isHeading()` — „CHAPTER ONE", „1.
  Titulek"); najde-li aspoň 2 shody, kniha má tenhle formát a stačí.
  Jinak zkusí holé číslo/římskou číslici na vlastním řádku („1",
  „II"), ale uzná je za kapitolu jen když hned následuje pořádný
  odstavec prózy (≥80 znaků, sám není holé číslo) — jinak by chytla
  i číslovaný obsah/rejstřík v úvodu knihy (reálně pozorováno u
  knihy „48": „Contents / 1 / 2 / 3…" před vlastním textem).
  `state.chapterIdx` (Set indexů) se počítá v `openReader()` a
  nahradil přímé volání `isHeading()` v `shadowPlayFor()` — pro
  vestavěné knihy beze změny (isHeading tam vždy najde ≥2 shod),
  pro nahrané knihy s „holými" kapitolami teď stínohra funguje taky.
  Dlouhá kapitola (`splitChapterSections()`, práh ~4000 znaků ≈ 3–4
  strany) se rozdělí na víc úseků, každý s vlastním obrázkem — krátká
  kapitola zůstává jeden úsek jako dřív (v1.5.3). Sekce jsou jen pro
  ilustrace/lištu; `state.chapterIdx` (spouštěč stínohry) je pořád
  jen ze skutečných začátků kapitol, ne z dílčích úseků — stínohra
  („clona") se schválně nespouští na každém obratu stránky, jen na
  začátku kapitoly. Pro každý úsek `chapterQuery()` vytáhne z textu
  1–2 charakteristická slova a `fetchCommonsImage()` s nimi dohledá
  obrázek přes Wikimedia Commons (`action=query&generator=search`,
  `origin=*` pro CORS, bez API klíče). Priorita hledaných slov (v1.5.2):
  Commons hostuje jen reálné/encyklopedické fotky, ne fanart k
  fiktivním postavám — jméno postavy tam skoro jistě nic nenajde, ale
  reálné místo ano. Proto **nejdřív** místo za předložkou („in
  London" → „London"), pak vlastní jméno uprostřed věty (≥2× výskyt),
  až nakonec frekvenčně nejčastější obsahové slovo mimo stopslova.
  I tak je to best-effort — u knih bez jasných reálných míst/jmen se
  ilustrace nemusí najít vůbec (Commons nic nevrátí, `contentIlls`
  zůstane prázdné pole). Výsledek (max 40 kapitol) se cachuje
  v IndexedDB stejně jako obálky (`rec.contentIllsTried` brání
  opakování); běží líně až při otevření čtečky, ne při startu jako
  obálky. Tlačítko **🔄** v hlavičce čtečky (`btn-reills`, jen
  u nahraných knih, ne u základní knihovny) vynuluje `contentIlls`/
  `contentIllsTried` a zkusí hledání znovu — jediná cesta, jak dát
  knize druhou šanci po vylepšení algoritmu nebo neúspěšném prvním
  pokusu, protože `coverTried`/`contentIllsTried` jinak brání
  opakování navždy. V kontejneru mockovat `commons.wikimedia.org`
  přes `page.route()` — skutečné API zase přes proxy nejde.
- **Logo „Petrus" v hlavičce** (`.brand`) je od v1.4.1 klikatelné —
  chová se jako tlačítko „← Zpět" (`show('library')`), funguje
  odkudkoli (i ze čtečky).
- **Verze aplikace:** `APP_VERSION` v index.html, badge `#ver` vpravo
  dole viditelný na všech obrazovkách (od v1.5.1). **Při každé uživatelsky viditelné změně verzi
  zvyš** (patch drobnost, minor funkce) — uživatel podle ní pozná,
  jestli Pages už servíruje novou verzi.
- **Vykreslení:** odstavce → věty (regex s lookbehind) → slova obalená
  `span.w`; stránkuje se po ~1200 znacích. Klik na slovo otevře panel
  (překlad, další významy, přeložená věta v kontextu, EN definice,
  další výskyty v textu); výběr textu ukáže plovoucí tlačítko
  „Přeložit výběr". Vzhled přes CSS proměnné, témata
  `body[data-theme=light|sepia|dark]`.

## Časté chyby z historie projektu (nedělej znovu)

1. **Pages vracelo 404, protože repo bylo private** (free plán Pages na
   private repu neumí; ani workflow s `enablement: true` ho nezapne —
   „Resource not accessible by integration") → před laděním Pages vždy
   ověř viditelnost repa; repo musí zůstat veřejné.
2. **Proxy v kontejneru blokuje část GitHub API** (zápisy do nastavení
   repa, Pages endpointy) — hlásí 403 „not permitted through this
   proxy". Takové akce musí udělat uživatel ručně v UI, nebo je řeš
   přes GitHub Actions workflow (tam token práva má).
3. **Nasazení Pages umí uvíznout na „Deployment cancelled" pro
   konkrétní commit SHA** — `deploy-pages` nasazení má ID = SHA
   commitu; jakmile GitHub jednou nasazení pro dané SHA zruší (ať už
   kvůli vypršení `deployment_queued`, nebo hned po pár sekundách bez
   zjevného důvodu), další pokusy pro **stejné** SHA rovnou zamítá, i
   po ručním re-run workflow — vidět v logu kroku `deploy-pages` jako
   `Creating Pages deployment... ID: <sha>` → `##[error]Deployment
   cancelled.` **Toto NENÍ výpadek GitHubu** — status page
   (githubstatus.com) může ukazovat vše v pořádku, protože jde o stav
   vázaný na konkrétní SHA, ne o incident služby. Než cokoliv
   diagnostikuješ jako „výpadek Pages", vždy nejdřív ověř skutečný log
   posledního běhu (`deploy-pages` step) přes GitHub API/MCP — teprve
   pokud tam nic nesedí, uvažuj o výpadku. Řešení: nový commit (jiné
   SHA), ne opakovaný re-run stejného běhu.
4. **Existuje i druhý, odlišný vzorec: nasazení uvízne ve frontě i pro
   úplně nové SHA** a po plných 10 minutách (`timeout: 600000` u
   `deploy-pages`) samo skončí timeoutem — v logu `Current status:
   deployment_queued` desítky opakování v řadě, případně chvíli
   střídání s `deployment_in_progress`, pak `##[error]Timeout reached,
   aborting!` → `Canceled deployment`. Na rozdíl od bodu 3 tohle není
   „SHA je spálené" (žádné dřívější `Deployment cancelled` pro to SHA
   nepředcházelo) — jde o skutečné zpomalení GitHub Pages backendu při
   zpracování fronty nasazení, které status page (githubstatus.com)
   nemusí vykazovat jako incident. Ověřený postup: nezkoušet honit
   opakovanými commity v smyčce (další pokus může znovu narazit na
   stejné zpomalení a další 10 minut čekání) — počkat s odstupem
   (desítky minut) a zkusit znovu, nebo nechat uživatele spustit
   nasazení ručně, až degradace pravděpodobně odezní. Potvrzeno v praxi
   (6.8.2026): dva pokusy po sobě skončily timeoutem, další (~13 minut
   po druhém, přes `workflow_dispatch`) už doběhl za ~40 s. Zdroj Pages
   zůstal po celou dobu na „GitHub Actions" beze změny — přepínání na
   „Deploy from a branch" nebylo potřeba, degradace odezněla sama.
   Pokud by odeznít nechtěla, „Deploy from a branch" (Settings → Pages)
   je funkční obchvat, protože nejede přes stejné Deployments API, ale
   je to změna nastavení repa, kterou musí kvůli proxy (bod 2) udělat
   uživatel ručně.
5. **Třetí vzorec: přechodná OIDC chyba při vytváření nasazení** — krok
   `deploy-pages` spadne hned (ne po timeoutu) s chybou typu
   `Failed to create deployment … no keys match the id token` (validace
   OIDC tokenu na straně GitHubu). Není to problém konfigurace repa ani
   workflow — jde o přechodný stav; řešení je prostý re-run téhož běhu
   (na rozdíl od bodu 3 tady SHA „spálené" není). Teprve pokud selže
   opakovaně stejnou chybou, zkoumej `permissions: id-token: write`
   ve workflow.
6. **Širší degradace Actions backendu — tři další přechodné vzorce**
   (pozorováno společně 6.8.2026 odpoledne/večer, vše odeznělo samo):
   (a) **push do main vůbec nezaloží workflow běh** — event se ztratí
   v backlogu, žádný běh „queued" nevznikne; řešení je ruční
   `workflow_dispatch` (přes API/MCP funguje, i když push eventy
   nejedou). (b) **job je zrušen po ~15 minutách bez přidělení
   runneru** — běh skončí `cancelled`, aniž by cokoliv běželo.
   (c) **nasazení visí ve stavu `waiting`** — běh čeká na environment
   `github-pages` desítky minut; NENÍ to protection rule repa (ověřeno
   — environment žádná pravidla nemá), jen zahlcený deployment backend.
   Zaseknutý `waiting` běh navíc nemusí jít zrušit (cancel API vrací
   502) — díky `concurrency: group pages, cancel-in-progress: true`
   ve workflow ho ale vytlačí nový dispatch, ruční cancel není potřeba.
   Společná strategie pro všechny vzorce: nediagnostikuj nastavení
   repa, nespouštěj smyčku commitů — nový `workflow_dispatch`, případně
   počkat desítky minut dle bodu 4.

## Udržuj tento soubor sám — dělej to na konci každého úkolu

Než odpovíš, že je úkol hotový, polož si otázku: *„Zjistil jsem něco,
co by budoucí session potřebovala vědět a v tomto souboru to ještě
není?"* Pokud ano, soubor rovnou uprav a commitni spolu se změnou kódu
— ideálně v tom samém commitu.

**Co si zaslouží zápis:** nový architektonický prvek nebo vzor
k opakovanému použití; rozhodnutí a **proč** (hlavně zamítnuté
alternativy); nově objevený zádrhel v kódu či prostředí, který se může
opakovat; změna terminologie/procesu/datového modelu platná od teď.

**Co si zápis NEzaslouží:** jednorázová kosmetika (stačí commit
message); cokoliv jasně viditelné přímo z kódu; detaily konkrétního
zadání, které se nebude opakovat.

**Jak zapisovat:** uprav existující sekci, nevytvářej duplicitní;
stručně, v odrážkách; jednou za čas sekce zkonsoliduj (smaž, co už
neplatí). Soubor má zůstat čitelný, ne jen růst. Na konci odpovědi
jednou větou zmiň, že jsi CLAUDE.md aktualizoval.
