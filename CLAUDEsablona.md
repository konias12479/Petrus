# {NÁZEV PROJEKTU} — kontext pro Claude Code

> Šablona obecných pravidel (převzato z projektu OLPE, 08/2026).
> Místa ve složených závorkách {…} doplňte podle projektu; sekce
> označené „doplňte později" klidně nechte prázdné a nechte je Clauda
> průběžně plnit podle pravidla „Udržuj tento soubor sám" na konci.

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
3. **Pokud nesedí:** napiš krátké doporučení přepnout (model nejde
   přepnout programově — přepíná uživatel v UI) a **nepokračuj
   v práci**, dokud uživatel nepotvrdí nebo nenapíše „pokračuj i tak".
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

- {Doplňte: jak se projekt spouští — build/bez buildu, jak zobrazit
  výsledek, co je „hotovo".}
- **Po každé změně ověř, že nic nespadlo** — {doplňte konkrétní
  příkazy: syntax check, testy, lint}. Neposílej změnu bez ověření;
  i drobná úprava umí něco rozbít.
- **Edituj postupně a cíleně** — najdi přesnou kotvu (`grep -n`),
  použij cílený edit, neposkytuj celé soubory znovu.
- **Commituj po každé uzavřené funkci**, ne po každém dílčím kroku.
- **Každou dokončenou a ověřenou změnu vždy doveď až do `main`**
  (push větve → PR → merge, bez čekání na vyzvání). {Doplňte, co `main`
  servíruje — např. GitHub Pages / produkci — dokud změna není
  mergnutá, uživatel/zákazník ji nevidí.}

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

## Architektura projektu

{Doplňte později — strukturu, klíčové soubory, datový model, konvence
pojmenování. Nechte Clauda sekci plnit průběžně dle pravidla níže.}

## Časté chyby z historie projektu (nedělej znovu)

{Zatím prázdné — plní se průběžně. Formát: číslovaný seznam, vzorec
**co se stalo → jaké je pravidlo do budoucna**.}

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
