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
  `NODE_PATH=<repo>/node_modules`. Chromium je v
  `/opt/pw-browsers/chromium` — playwrightu předej `executablePath`,
  nesmí stahovat vlastní build.
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
  záznam `{id,title,addedAt,paragraphs[],pos:{page}}`); nastavení
  vzhledu `petrus-settings` a slovníček `petrus-words` v localStorage.
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
