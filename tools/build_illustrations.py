#!/usr/bin/env python3
"""Vygeneruje books/illustrations/<id>.json a zmenšené obrázky books/img/<id>/
z klonů ilustrovaných edic (Standard Ebooks Alice, GITenberg Oz #43936,
GITenberg Sherlock #48320).

Použití:
  python3 tools/build_illustrations.py <dir-se-alice> <dir-oz-43936> <dir-sherlock-48320>

Kotvení: pro každou ilustraci se vezme text nejbližšího odstavce v ilustrované
edici a najde se odpovídající odstavec v books/*.txt (stejné dělení odstavců
jako textToParagraphs v index.html). Ilustrace bez spolehlivé kotvy se vynechá
a vypíše se varování.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
MAX_W = 700
JPEG_Q = 80


def text_to_paragraphs(text):
    # zrcadlí textToParagraphs() z index.html
    parts = re.split(r"\n\s*\n+", text.replace("\r\n", "\n"))
    out = []
    for p in parts:
        p = re.sub(r"\s*\n\s*", " ", p)
        p = re.sub(r"\s+", " ", p).strip()
        if p:
            out.append(p)
    return out


def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_tags(html):
    html = re.sub(r"<[^>]+>", " ", html)
    html = (html.replace("&nbsp;", " ").replace("&amp;", "&")
            .replace("&quot;", '"').replace("&#39;", "'")
            .replace("&mdash;", "—").replace("&ldquo;", '"').replace("&rdquo;", '"'))
    return re.sub(r"\s+", " ", html).strip()


def find_anchor(paras_norm, anchor, start):
    """Najdi index odstavce odpovídající kotvě; hledá se od `start` dopředu
    (ilustrace jdou v pořadí textu), s malou tolerancí zpět."""
    a = norm(anchor)
    if len(a) < 20:
        return None, 0.0
    probe = " ".join(a.split()[:12])
    lo = max(0, start - 3)
    best_i, best_r = None, 0.0
    for i in range(lo, len(paras_norm)):
        p = paras_norm[i]
        if probe and probe in p:
            return i, 1.0
        r = SequenceMatcher(None, p[:400], a[:400]).ratio()
        if r > best_r:
            best_i, best_r = i, r
    if best_r >= 0.55:
        return best_i, best_r
    return None, best_r


def resize_save(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=JPEG_Q, progressive=True, optimize=True)


def extract_alice(d):
    """Standard Ebooks: <figure id="illustration-N"><img alt=... src=.../figure>,
    kotva = následující <p>."""
    items = []
    text_dir = d / "src/epub/text"
    for n in range(1, 13):
        html = (text_dir / f"chapter-{n}.xhtml").read_text(encoding="utf-8")
        for m in re.finditer(
            r'<figure[^>]*? id="(illustration-\d+)">\s*<img alt="([^"]*)"[^>]*>\s*</figure>(.*?)(?=<figure|\Z)',
            html, re.S,
        ):
            fig_id, alt, rest = m.group(1), m.group(2), m.group(3)
            pm = re.search(r"<p[^>]*>(.*?)</p>", rest, re.S)
            if not pm:
                continue
            items.append({
                "img": d / "images" / f"{fig_id}.png",
                "name": fig_id,
                "anchor": strip_tags(pm.group(1)),
                "alt": alt, "cap": None,
            })
    return items


def extract_oz(d):
    """GITenberg #43936: <img src="images/iNNN..jpg" alt=... title=... height=H width=W>,
    jen dost velké obrázky; kotva = následující <p>."""
    html = (d / "43936-h" / "43936-h.htm").read_text(encoding="utf-8", errors="replace")
    skip_alts = {"copyright", "dedication", "wizard of oz", "toto", "scarecrow"}
    items = []
    for m in re.finditer(
        r'<img src="images/(i\d+[^"]*?)\.jpg" alt="([^"]*)"[^>]*?'
        r'height="(\d+)" width="(\d+)"[^>]*>', html
    ):
        name, alt, h, w = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
        if min(h, w) < 300 or alt.strip().lower() in skip_alts:
            continue
        rest = html[m.end():m.end() + 8000]
        pm = re.search(r"<p[^>]*>(.*?)</p>", rest, re.S)
        if not pm:
            continue
        anchor = strip_tags(pm.group(1))
        items.append({
            "img": d / "43936-h" / "images" / f"{name}.jpg",
            "name": name.replace("_edit", ""),
            "anchor": anchor, "alt": alt,
            "cap": None,
        })
    return items


def extract_sherlock(d):
    """GITenberg #48320: <div class="figcenter ..."><img src="images/illusNNNa.jpg">
    <div class="caption">…</div></div>, kotva = předchozí <p> (obrázek je u citované
    scény), fallback následující <p>."""
    html = (d / "48320-h" / "48320-h.htm").read_text(encoding="utf-8", errors="replace")
    items = []
    for m in re.finditer(
        r'<div class="figcenter[^"]*">.*?<img src="images/(illus\w+)\.jpg"[^>]*>'
        r'(?:.*?<div class="caption">(.*?)</div>)?\s*</div>', html, re.S,
    ):
        name, cap = m.group(1), m.group(2)
        before = html[:m.start()]
        prev = re.findall(r"<p[^>]*>(.*?)</p>", before[-8000:], re.S)
        rest = html[m.end():m.end() + 8000]
        nxt = re.search(r"<p[^>]*>(.*?)</p>", rest, re.S)
        anchors = []
        if prev:
            anchors.append(strip_tags(prev[-1]))
        if nxt:
            anchors.append(strip_tags(nxt.group(1)))
        cap_txt = strip_tags(cap) if cap else None
        items.append({
            "img": d / "48320-h" / "images" / f"{name}.jpg",
            "name": name, "anchor": anchors, "alt": cap_txt or "",
            "cap": cap_txt,
        })
    return items


def build(book_id, txt_file, items):
    paras = text_to_paragraphs((REPO / txt_file).read_text(encoding="utf-8"))
    paras_norm = [norm(p) for p in paras]
    out, last, dropped = [], 0, 0
    for it in items:
        anchors = it["anchor"] if isinstance(it["anchor"], list) else [it["anchor"]]
        idx, score = None, 0.0
        for a in anchors:
            idx, score = find_anchor(paras_norm, a, last)
            if idx is not None:
                break
        if idx is None:
            dropped += 1
            print(f"  ! {book_id}/{it['name']}: kotva nenalezena "
                  f"(score {score:.2f}): {anchors[0][:70]}…")
            continue
        last = max(last, idx)
        rel = f"books/img/{book_id}/{it['name']}.jpg"
        resize_save(it["img"], REPO / rel)
        entry = {"par": idx, "src": rel}
        if it["cap"]:
            entry["cap"] = it["cap"]
        if it["alt"]:
            entry["alt"] = it["alt"]
        out.append(entry)
    out.sort(key=lambda e: e["par"])
    dst = REPO / "books" / "illustrations" / f"{book_id}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps({"items": out}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(f"{book_id}: {len(out)} ilustrací namapováno, {dropped} vynecháno "
          f"→ {dst.relative_to(REPO)}")


def main():
    se_alice, oz, sherlock = (Path(p) for p in sys.argv[1:4])
    build("alice", "books/alice-in-wonderland.txt", extract_alice(se_alice))
    build("oz", "books/wizard-of-oz.txt", extract_oz(oz))
    build("sherlock", "books/sherlock-holmes.txt", extract_sherlock(sherlock))


if __name__ == "__main__":
    main()
