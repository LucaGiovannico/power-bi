from pathlib import Path

from html import escape

import re

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "blog"

BLOG_DIR = ROOT / "blog"
TEMPLATE_IT = ROOT / "templates" / "blog-article-it.html"

SITE_URL = "https://www.dinafiorentino.com"

REQUIRED_FIELDS = {
    "slug",
    "lang",
    "title",
    "card_title",
    "description",
    "card_description",
    "category",
    "date",
    "reading_time",
    "image",
    "image_alt",
    "featured",
    "published",
}


def parse_value(value):
    value = value.strip()

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    if value.isdigit():
        return int(value)

    return value


def parse_article(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError(
            f"{path}: front matter iniziale mancante"
        )

    try:
        end_index = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        raise ValueError(
            f"{path}: front matter non chiuso"
        )

    metadata = {}

    for line in lines[1:end_index]:
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            raise ValueError(
                f"{path}: riga metadati non valida: {line}"
            )

        key, value = line.split(":", 1)

        metadata[key.strip()] = parse_value(value)

    missing = REQUIRED_FIELDS - metadata.keys()

    if missing:
        raise ValueError(
            f"{path}: campi mancanti: "
            + ", ".join(sorted(missing))
        )

    body = "\n".join(lines[end_index + 1:]).strip()

    if not body:
        raise ValueError(
            f"{path}: corpo articolo vuoto"
        )

    return {
        "path": path,
        "metadata": metadata,
        "body": body,
    }

def render_card(article, featured_layout=False):
    meta = article["metadata"]

    title = escape(str(meta["card_title"]))
    description = escape(str(meta["card_description"]))
    category = escape(str(meta["category"]))
    image = escape(str(meta["image"]), quote=True)
    image_alt = escape(str(meta["image_alt"]), quote=True)
    slug = escape(str(meta["slug"]), quote=True)
    reading_time = meta["reading_time"]

    article_url = f"./{slug}.html"

    image_fit = str(
        meta.get("image_fit", "cover")
    ).lower()

    if image_fit not in {"cover", "contain"}:
        raise ValueError(
            f"{article['path']}: image_fit deve essere "
            "'cover' oppure 'contain'"
        )

    if featured_layout:
        return f"""\
<article class="article-card article-card--featured">

  <div class="featured-visual featured-visual--image">

    <img
      class="featured-visual__image"
      src="{image}"
      alt="{image_alt}"
      loading="lazy"
      decoding="async"
    />

  </div>

  <div class="article-card__body">

    <div class="article-meta">
      <span>{category}</span>
      <span>{reading_time} MIN DI LETTURA</span>
    </div>

    <h3>
      <a
        class="article-title-link"
        href="{article_url}"
      >
        {title}
      </a>
    </h3>

    <p>
      {description}
    </p>

    <a
      class="article-status article-status--link"
      href="{article_url}"
    >
      Leggi l'articolo
    </a>

  </div>

</article>"""

    image_class = "article-card__image"

    if image_fit == "contain":
        image_class += " article-card__image--contain"

    return f"""\
<article class="article-card">

  <div class="article-card__visual article-card__visual--image">

    <img
      class="{image_class}"
      src="{image}"
      alt="{image_alt}"
      loading="lazy"
      decoding="async"
    />

  </div>

  <div class="article-card__body">

    <div class="article-meta">
      <span>{category}</span>
      <span>{reading_time} MIN DI LETTURA</span>
    </div>

    <h3>
      <a
        class="article-title-link"
        href="{article_url}"
      >
        {title}
      </a>
    </h3>

    <p>
      {description}
    </p>

    <a
      class="article-status article-status--link"
      href="{article_url}"
    >
      Leggi l'articolo
    </a>

  </div>

</article>"""

def get_published_articles(articles, lang):
    published = [
        article
        for article in articles
        if article["metadata"]["published"]
        and article["metadata"]["lang"] == lang
    ]

    return sorted(
        published,
        key=lambda article: article["metadata"]["date"],
        reverse=True,
    )


def select_home_articles(articles, lang, limit=3):
    published = get_published_articles(
        articles,
        lang,
    )

    featured_articles = [
        article
        for article in published
        if article["metadata"]["featured"]
    ]

    if len(featured_articles) > 1:
        raise ValueError(
            f"Più di un articolo featured per la lingua '{lang}'"
        )

    selected = []

    if featured_articles:
        featured = featured_articles[0]
        selected.append(featured)

        published = [
            article
            for article in published
            if article is not featured
        ]

    selected.extend(published)

    return selected[:limit]

def render_inline_markdown(text):
    text = escape(text)

    text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        text,
    )

    text = re.sub(
        r"\*(.+?)\*",
        r"<em>\1</em>",
        text,
    )

    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )

    return text


def render_markdown(body):
    lines = body.splitlines()

    html_parts = []
    paragraph = []
    list_items = []

    def flush_paragraph():
        nonlocal paragraph

        if paragraph:
            text = " ".join(
                line.strip()
                for line in paragraph
            )

            html_parts.append(
                f"<p>{render_inline_markdown(text)}</p>"
            )

            paragraph = []

    def flush_list():
        nonlocal list_items

        if list_items:
            items = "\n".join(
                f"  <li>{render_inline_markdown(item)}</li>"
                for item in list_items
            )

            html_parts.append(
                "<ul>\n"
                f"{items}\n"
                "</ul>"
            )

            list_items = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            flush_paragraph()
            flush_list()
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()

            html_parts.append(
                f"<h3>{render_inline_markdown(line[4:])}</h3>"
            )

            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()

            html_parts.append(
                f"<h2>{render_inline_markdown(line[3:])}</h2>"
            )

            continue

        if line.startswith("# "):
            raise ValueError(
                "Il corpo dell'articolo non deve contenere "
                "un H1: il titolo viene generato dal template."
            )

        if line.startswith("- "):
            flush_paragraph()

            list_items.append(
                line[2:].strip()
            )

            continue

        flush_list()
        paragraph.append(line)

    flush_paragraph()
    flush_list()

    return "\n\n".join(html_parts)

def enhance_article_layout(html):
    """
    Migliora automaticamente il layout dell'articolo:
    - introduzione iniziale -> box "Il contesto"
    - sezioni numerate 1-6 -> griglia/card
    - sezione "In sintesi" -> box evidenziato
    """

    numbered_pattern = re.compile(
        r"(<h2>([1-6])\.\s.*?</h2>.*?)(?=<h2>|$)",
        re.DOTALL,
    )

    matches = list(
        numbered_pattern.finditer(html)
    )

    if len(matches) == 6:
        intro_html = html[:matches[0].start()].strip()
        after = html[matches[-1].end():].strip()

        if intro_html:
            before = (
                '<section class="blog-article__lead">\n'
                '  <span class="blog-article__lead-label">'
                'Il contesto'
                '</span>\n'
                f'{intro_html}\n'
                '</section>\n\n'
            )
        else:
            before = ""

        cards = []

        for match in matches:
            section_html = match.group(1).strip()

            cards.append(
                '<section class="blog-article__section-card">\n'
                f'{section_html}\n'
                '</section>'
            )

        html = (
            before
            + '<div class="blog-article__sections-grid">\n'
            + '\n\n'.join(cards)
            + '\n</div>\n\n'
            + after
        )

    impact_pattern = re.compile(
        r"<h2>Cosa cambia davvero nel lavoro quotidiano</h2>"
        r"(.*?)(?=<h2>In sintesi</h2>|$)",
        re.DOTALL,
    )

    html = impact_pattern.sub(
        lambda match: (
            '<section class="blog-article__impact">\n'
            '  <div class="blog-article__impact-heading">\n'
            '    <span class="blog-article__impact-label">'
            'Nella pratica'
            '</span>\n'
            '    <h2>Cosa cambia davvero nel lavoro quotidiano</h2>\n'
            '  </div>\n'
            '  <div class="blog-article__impact-body">\n'
            f'{match.group(1).strip()}\n'
            '  </div>\n'
            '</section>\n\n'
        ),
        html,
    )

    summary_pattern = re.compile(
        r"<h2>In sintesi</h2>(.*)$",
        re.DOTALL,
    )

    html = summary_pattern.sub(
        lambda match: (
            '<section class="blog-article__summary">\n'
            '  <span class="blog-article__summary-label">'
            'In sintesi'
            '</span>\n'
            '  <h2>In sintesi</h2>\n'
            f'{match.group(1).strip()}\n'
            '</section>'
        ),
        html,
    )

    return html

def format_date_it(date_value):
    months = {
        1: "gennaio",
        2: "febbraio",
        3: "marzo",
        4: "aprile",
        5: "maggio",
        6: "giugno",
        7: "luglio",
        8: "agosto",
        9: "settembre",
        10: "ottobre",
        11: "novembre",
        12: "dicembre",
    }

    year, month, day = map(
        int,
        str(date_value).split("-"),
    )

    return (
        f"{day} {months[month]} {year}"
    )


def render_article_page(article):
    meta = article["metadata"]

    if meta["lang"] != "it":
        raise ValueError(
            f"{article['path']}: template italiano "
            "usato con articolo non italiano"
        )

    template = TEMPLATE_IT.read_text(
        encoding="utf-8"
    )

    slug = str(meta["slug"])
    title = str(meta["title"])

    canonical_url = (
        f"{SITE_URL}/blog/{slug}.html"
    )

    seo_title = (
        f"{title} | Dina Fiorentino"
    )

    hreflang_alternates = f"""\
<link
  rel="alternate"
  hreflang="it"
  href="{canonical_url}"
/>"""

    replacements = {
        "{{SEO_TITLE}}": escape(
            seo_title
        ),
        "{{DESCRIPTION}}": escape(
            str(meta["description"]),
            quote=True,
        ),
        "{{CANONICAL_URL}}": escape(
            canonical_url,
            quote=True,
        ),
        "{{HREFLANG_ALTERNATES}}":
            hreflang_alternates,
        "{{CATEGORY}}": escape(
            str(meta["category"])
        ),
        "{{DATE}}": escape(
            format_date_it(meta["date"])
        ),
        "{{READING_TIME}}": escape(
            str(meta["reading_time"])
        ),
        "{{TITLE}}": escape(
            title
        ),
        "{{IMAGE}}": escape(
            str(meta["image"]),
            quote=True,
        ),
        "{{IMAGE_ALT}}": escape(
            str(meta["image_alt"]),
            quote=True,
        ),
        "{{ARTICLE_BODY}}":
            enhance_article_layout(
            render_markdown(
                article["body"])
        ),
        }

    page = template

    for placeholder, value in replacements.items():
        page = page.replace(
            placeholder,
            value,
        )

    remaining = re.findall(
        r"\{\{[A-Z_]+\}\}",
        page,
    )

    if remaining:
        raise ValueError(
            "Placeholder non sostituiti: "
            + ", ".join(
                sorted(set(remaining))
            )
        )

    return page

def write_article_page(article):
    meta = article["metadata"]

    output_path = (
        BLOG_DIR
        / f"{meta['slug']}.html"
    )

    page = render_article_page(
        article
    )

    output_path.write_text(
        page,
        encoding="utf-8",
    )

    return output_path

def main():
    article_paths = sorted(
        CONTENT_DIR.glob("*/*.md")
    )

    if not article_paths:
        print("Nessun articolo trovato.")
        return

    articles = [
        parse_article(path)
        for path in article_paths
    ]

    print(
        f"Articoli trovati: {len(articles)}\n"
    )

    for article in articles:
        path = article["path"]
        meta = article["metadata"]

        print(f"✓ {path.relative_to(ROOT)}")
        print(f"  Titolo: {meta['title']}")
        print(f"  Lingua: {meta['lang']}")
        print(f"  Data: {meta['date']}")
        print(f"  Categoria: {meta['category']}")
        print(f"  Lettura: {meta['reading_time']} min")
        print(f"  Featured: {meta['featured']}")
        print(f"  Pubblicato: {meta['published']}")
        print()

    home_articles = select_home_articles(
        articles,
        "it",
    )

    if home_articles:
        print("=" * 60)
        print("ARTICOLI SELEZIONATI PER LA HOME BLOG")
        print("=" * 60)
        print()

        for position, article in enumerate(
            home_articles,
            start=1,
        ):
            meta = article["metadata"]

            print(
                f"{position}. "
                f"{meta['title']} "
                f"— {meta['date']} "
                f"— featured={meta['featured']}"
            )

        print()
        print("=" * 60)
        print("ANTEPRIMA DELLE 3 CARD")
        print("=" * 60)
        print()

        for position, article in enumerate(
            home_articles,
            start=1,
        ):
            print(
                render_card(
                    article,
                    featured_layout=(position == 1),
                )
            )

            print()

    print()
    print("=" * 60)
    print("PAGINE ARTICOLO GENERATE")
    print("=" * 60)
    print()

    for article in articles:
        meta = article["metadata"]

        if (
            meta["published"]
            and meta["lang"] == "it"
        ):
            output_path = write_article_page(
                article
            )

            print(
                f"✓ {output_path.relative_to(ROOT)}"
            )

if __name__ == "__main__":
    main()