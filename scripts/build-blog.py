from pathlib import Path

from html import escape

import re

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "blog"

BLOG_DIR = ROOT / "blog"
TEMPLATE_IT = ROOT / "templates" / "blog-article-it.html"
TEMPLATE_EN = ROOT / "templates" / "blog-article-en.html"

TEMPLATE_ARCHIVE_IT = (
    ROOT
    / "templates"
    / "blog-archive-it.html"
)

TEMPLATE_ARCHIVE_EN = (
    ROOT
    / "templates"
    / "blog-archive-en.html"
)

ARCHIVE_OUTPUT_IT = (
    ROOT
    / "blog"
    / "articoli.html"
)

ARCHIVE_OUTPUT_EN = (
    ROOT
    / "blog"
    / "articles.html"
)

BLOG_INDEX_IT = ROOT / "blog" / "index.html"
BLOG_INDEX_EN = ROOT / "blog" / "index-en.html"

BLOG_ARTICLES_START = "<!-- BLOG_ARTICLES_START -->"
BLOG_ARTICLES_END = "<!-- BLOG_ARTICLES_END -->"

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

    lang = str(meta["lang"])

    labels = {
        "it": {
            "reading": "MIN DI LETTURA",
            "read_article": "Leggi l'articolo",
        },
        "en": {
            "reading": "MIN READ",
            "read_article": "Read the article",
        },
    }

    if lang not in labels:
        raise ValueError(
            f"{article['path']}: lingua card non supportata: {lang}"
        )

    current = labels[lang]

    title = escape(str(meta["card_title"]))
    description = escape(str(meta["card_description"]))
    category = escape(str(meta["category"]))
    image = escape(str(meta["image"]), quote=True)
    image_alt = escape(str(meta["image_alt"]), quote=True)
    reading_time = meta["reading_time"]

    filename = article_filename(meta)
    article_url = f"./{filename}"

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
  <article class="article-card article-card--featured article-card--clickable">

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
      <span>{reading_time} {current["reading"]}</span>
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

    <span class="article-status">
      {current["read_article"]}
    </span>

  </div>

</article>"""

    image_class = "article-card__image"

    if image_fit == "contain":
        image_class += " article-card__image--contain"

    return f"""\
<article class="article-card article-card--clickable">

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
      <span>{reading_time} {current["reading"]}</span>
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

    <span class="article-status">
      {current["read_article"]}
    </span>

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
        r"`([^`]+)`",
        r'<code class="blog-article__inline-code">\1</code>',
        text,
    )

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

    in_code_block = False
    code_language = ""
    code_lines = []

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

    def flush_code():
        nonlocal code_lines
        nonlocal code_language

        code = escape(
            "\n".join(code_lines)
        )

        language_class = ""

        if code_language:
            language_class = (
                f' class="language-{escape(code_language.lower())}"'
            )

        html_parts.append(
            '<pre class="blog-article__code">'
            f'<code{language_class}>{code}</code>'
            '</pre>'
        )

        code_lines = []
        code_language = ""

    for raw_line in lines:
        stripped = raw_line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()

            if not in_code_block:
                in_code_block = True
                code_language = (
                    stripped[3:].strip()
                )
                code_lines = []
            else:
                flush_code()
                in_code_block = False

            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        line = stripped

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
                "Il corpo Markdown non deve contenere "
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

    if in_code_block:
        raise ValueError(
            "Blocco di codice Markdown non chiuso"
        )

    flush_paragraph()
    flush_list()

    return "\n\n".join(html_parts)


def enhance_article_layout(html, lang):
    """
    Migliora automaticamente il layout dell'articolo
    in base alla lingua.
    """

    labels = {
        "it": {
            "context": "Il contesto",
            "impact_label": "Nella pratica",
            "impact_title":
                "Cosa cambia davvero nel lavoro quotidiano",
            "summary": "In sintesi",
        },
        "en": {
            "context": "Context",
            "impact_label": "In practice",
            "impact_title":
                "What actually changes in everyday work",
            "summary": "In summary",
        },
    }

    if lang not in labels:
        raise ValueError(
            f"Lingua articolo non supportata: {lang}"
        )

    current = labels[lang]

    numbered_pattern = re.compile(
        r"(<h2>(\d+)\.\s.*?</h2>.*?)(?=<h2>|$)",
        re.DOTALL,
    )

    matches = list(
        numbered_pattern.finditer(html)
    )

    if matches:
        intro_html = html[
            :matches[0].start()
        ].strip()

        after = html[
            matches[-1].end():
        ].strip()

        if intro_html:
            before = (
                '<section class="blog-article__lead">\n'
                '  <span class="blog-article__lead-label">'
                f'{current["context"]}'
                '</span>\n'
                f'{intro_html}\n'
                '</section>\n\n'
            )
        else:
            before = ""

        cards = []

        for match in matches:
            section_html = (
                match.group(1).strip()
            )

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

    impact_title = re.escape(
        current["impact_title"]
    )

    summary_title = re.escape(
        current["summary"]
    )

    impact_pattern = re.compile(
        rf"<h2>{impact_title}</h2>"
        rf"(.*?)(?=<h2>{summary_title}</h2>|$)",
        re.DOTALL,
    )

    html = impact_pattern.sub(
        lambda match: (
            '<section class="blog-article__impact">\n'
            '  <div class="blog-article__impact-heading">\n'
            '    <span class="blog-article__impact-label">'
            f'{current["impact_label"]}'
            '</span>\n'
            f'    <h2>{current["impact_title"]}</h2>\n'
            '  </div>\n'
            '  <div class="blog-article__impact-body">\n'
            f'{match.group(1).strip()}\n'
            '  </div>\n'
            '</section>\n\n'
        ),
        html,
    )

    summary_pattern = re.compile(
        rf"<h2>{summary_title}</h2>(.*)$",
        re.DOTALL,
    )

    html = summary_pattern.sub(
        lambda match: (
            '<section class="blog-article__summary">\n'
            '  <span class="blog-article__summary-label">'
            f'{current["summary"]}'
            '</span>\n'
            f'  <h2>{current["summary"]}</h2>\n'
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


def format_date_en(date_value):
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    year, month, day = map(
        int,
        str(date_value).split("-"),
    )

    return (
        f"{months[month]} {day}, {year}"
    )


def article_filename(meta):
    lang = str(meta["lang"])
    slug = str(meta["slug"])

    if lang == "it":
        return f"{slug}.html"

    if lang == "en":
        return f"{slug}-en.html"

    raise ValueError(
        f"Lingua articolo non supportata: {lang}"
    )


def render_article_page(article):
    meta = article["metadata"]
    lang = str(meta["lang"])

    templates = {
        "it": TEMPLATE_IT,
        "en": TEMPLATE_EN,
    }

    if lang not in templates:
        raise ValueError(
            f"{article['path']}: "
            f"lingua non supportata: {lang}"
        )

    template = templates[lang].read_text(
        encoding="utf-8"
    )

    title = str(meta["title"])

    filename = article_filename(meta)

    canonical_url = (
        f"{SITE_URL}/blog/{filename}"
    )

    seo_title = (
        f"{title} | Dina Fiorentino"
    )

    lang_it_url = (
        f"./{meta['slug']}.html"
    )

    lang_en_url = (
        f"./{meta['slug']}-en.html"
    )

    it_url = (
    f"{SITE_URL}/blog/{meta['slug']}.html"
)

    en_url = (
        f"{SITE_URL}/blog/{meta['slug']}-en.html"
    )

    hreflang_alternates = f"""\
    <link
      rel="alternate"
      hreflang="it"
      href="{it_url}"
    />
    <link
      rel="alternate"
      hreflang="en"
      href="{en_url}"
    />
    <link
      rel="alternate"
      hreflang="x-default"
      href="{it_url}"
    />"""

    if lang == "it":
        formatted_date = format_date_it(
            meta["date"]
        )
    else:
        formatted_date = format_date_en(
            meta["date"]
        )

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
        "{{LANG_IT_URL}}": escape(
            lang_it_url,
            quote=True,
        ),
        "{{LANG_EN_URL}}": escape(
            lang_en_url,
            quote=True,
        ),
        "{{CATEGORY}}": escape(
            str(meta["category"])
        ),
        "{{DATE}}": escape(
            formatted_date
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
                    article["body"]
                ),
                lang,
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
        / article_filename(meta)
    )

    page = render_article_page(
        article
    )

    output_path.write_text(
        page,
        encoding="utf-8",
    )

    return output_path

def update_blog_index_it(articles):
    home_articles = select_home_articles(
        articles,
        "it",
        limit=3,
    )

    if not home_articles:
        print("Nessun articolo IT pubblicato: Home Blog non aggiornata.")
        return

    cards = []

    for position, article in enumerate(
        home_articles,
        start=1,
    ):
        cards.append(
            render_card(
                article,
                featured_layout=(position == 1),
            )
        )

    # Finché non abbiamo 3 articoli reali,
    # manteniamo i placeholder esistenti.
    if len(cards) < 2:
        cards.append("""\
<article class="article-card">

  <div class="article-card__visual article-card__visual--dax">

    <span class="dax-badge">
      DAX
    </span>

    <div class="dax-code">
      <span>Sales Category A =</span>
      <span>CALCULATE(</span>
      <span>&nbsp;&nbsp;[Sales],</span>
      <span>&nbsp;&nbsp;FILTER(</span>
      <span>&nbsp;&nbsp;&nbsp;&nbsp;ALL('Product'),</span>
      <span>&nbsp;&nbsp;&nbsp;&nbsp;'Product'[Category] = "A"</span>
      <span>&nbsp;&nbsp;)</span>
      <span>)</span>
    </div>

  </div>

  <div class="article-card__body">

    <div class="article-meta">
      <span>DAX</span>
      <span>7 MIN DI LETTURA</span>
    </div>

    <h3>
      5 formule DAX da conoscere davvero
    </h3>

    <p>
      Una raccolta pratica di funzioni e pattern
      utili che ricorrono spesso nei modelli Power BI.
    </p>

    <span class="article-status">
      Prossimamente
    </span>

  </div>

</article>""")

    if len(cards) < 3:
        cards.append("""\
<article class="article-card">

  <div class="article-card__visual article-card__visual--story-image">

    <picture>
      <img
        class="article-card__story-image"
        src="../assets/images/blog/hero-data-storytelling.png"
        alt="Visual di data storytelling"
        loading="lazy"
        decoding="async"
      />
    </picture>

  </div>

  <div class="article-card__body">

    <div class="article-meta">
      <span>DATA STORYTELLING</span>
      <span>6 MIN DI LETTURA</span>
    </div>

    <h3>
      Data storytelling:
      un buon grafico non basta
    </h3>

    <p>
      Come costruire una narrazione visiva efficace
      per aiutare chi guarda a capire cosa sta
      succedendo e perché.
    </p>

    <span class="article-status">
      Prossimamente
    </span>

  </div>

</article>""")

    html = BLOG_INDEX_IT.read_text(
        encoding="utf-8"
    )

    if BLOG_ARTICLES_START not in html:
        raise ValueError(
            "Marker BLOG_ARTICLES_START non trovato in blog/index.html"
        )

    if BLOG_ARTICLES_END not in html:
        raise ValueError(
            "Marker BLOG_ARTICLES_END non trovato in blog/index.html"
        )

    start_index = (
        html.index(BLOG_ARTICLES_START)
        + len(BLOG_ARTICLES_START)
    )

    end_index = html.index(
        BLOG_ARTICLES_END,
        start_index,
    )

    generated_cards = (
        "\n\n"
        + "\n\n".join(cards)
        + "\n\n            "
    )

    updated_html = (
        html[:start_index]
        + generated_cards
        + html[end_index:]
    )

    BLOG_INDEX_IT.write_text(
        updated_html,
        encoding="utf-8",
    )

    print("✓ blog/index.html aggiornato automaticamente")

def update_blog_index_en(articles):
    home_articles = select_home_articles(
        articles,
        "en",
        limit=3,
    )

    if not home_articles:
        print(
            "No published EN articles: "
            "English Blog Home not updated."
        )
        return

    cards = []

    for position, article in enumerate(
        home_articles,
        start=1,
    ):
        cards.append(
            render_card(
                article,
                featured_layout=(position == 1),
            )
        )

    # Keep the two existing editorial placeholders
    # until real EN articles are available.
    if len(cards) < 2:
        cards.append("""\
<article class="article-card">

  <div class="article-card__visual article-card__visual--dax">

    <span class="dax-badge">
      DAX
    </span>

    <div class="dax-code">
      <span>Sales Category A =</span>
      <span>CALCULATE(</span>
      <span>&nbsp;&nbsp;[Sales],</span>
      <span>&nbsp;&nbsp;FILTER(</span>
      <span>&nbsp;&nbsp;&nbsp;&nbsp;ALL('Product'),</span>
      <span>&nbsp;&nbsp;&nbsp;&nbsp;'Product'[Category] = "A"</span>
      <span>&nbsp;&nbsp;)</span>
      <span>)</span>
    </div>

  </div>

  <div class="article-card__body">

    <div class="article-meta">
      <span>DAX</span>
      <span>7 MIN READ</span>
    </div>

    <h3>
      5 DAX formulas worth knowing
    </h3>

    <p>
      A practical collection of useful functions and patterns
      that frequently appear in Power BI models.
    </p>

    <span class="article-status">
      Coming soon
    </span>

  </div>

</article>""")

    if len(cards) < 3:
        cards.append("""\
<article class="article-card">

  <div class="article-card__visual article-card__visual--story-image">

    <picture>
      <img
        class="article-card__story-image"
        src="../assets/images/blog/hero-data-storytelling.png"
        alt="Data storytelling editorial visual"
        loading="lazy"
        decoding="async"
      />
    </picture>

  </div>

  <div class="article-card__body">

    <div class="article-meta">
      <span>DATA STORYTELLING</span>
      <span>6 MIN READ</span>
    </div>

    <h3>
      Data storytelling:
      a good chart is not enough
    </h3>

    <p>
      How to build an effective visual narrative
      that helps people understand what is happening
      and why.
    </p>

    <span class="article-status">
      Coming soon
    </span>

  </div>

</article>""")

    html = BLOG_INDEX_EN.read_text(
        encoding="utf-8"
    )

    if BLOG_ARTICLES_START not in html:
        raise ValueError(
            "BLOG_ARTICLES_START marker not found "
            "in blog/index-en.html"
        )

    if BLOG_ARTICLES_END not in html:
        raise ValueError(
            "BLOG_ARTICLES_END marker not found "
            "in blog/index-en.html"
        )

    start_index = (
        html.index(BLOG_ARTICLES_START)
        + len(BLOG_ARTICLES_START)
    )

    end_index = html.index(
        BLOG_ARTICLES_END,
        start_index,
    )

    generated_cards = (
        "\n\n"
        + "\n\n".join(cards)
        + "\n\n            "
    )

    updated_html = (
        html[:start_index]
        + generated_cards
        + html[end_index:]
    )

    BLOG_INDEX_EN.write_text(
        updated_html,
        encoding="utf-8",
    )

    print(
        "✓ blog/index-en.html updated automatically"
    )


def generate_archive_it(articles):
    published = get_published_articles(
        articles,
        "it",
    )

    template = TEMPLATE_ARCHIVE_IT.read_text(
        encoding="utf-8"
    )

    if published:
        cards = [
            render_card(
                article,
                featured_layout=False,
            )
            for article in published
        ]

        archive_html = (
            "\n\n".join(cards)
        )

    else:
        archive_html = """\
<p class="blog-archive__empty">
  Nessun articolo pubblicato al momento.
</p>"""

    page = template.replace(
        "{{ARCHIVE_ARTICLES}}",
        archive_html,
    )

    remaining = re.findall(
        r"\{\{[A-Z_]+\}\}",
        page,
    )

    if remaining:
        raise ValueError(
            "Placeholder archivio non sostituiti: "
            + ", ".join(
                sorted(set(remaining))
            )
        )

    ARCHIVE_OUTPUT_IT.write_text(
        page,
        encoding="utf-8",
    )

    print(
        "✓ blog/articoli.html generato automaticamente"
    )

def generate_archive_en(articles):
    published = get_published_articles(
        articles,
        "en",
    )

    template = TEMPLATE_ARCHIVE_EN.read_text(
        encoding="utf-8"
    )

    if published:
        cards = [
            render_card(
                article,
                featured_layout=False,
            )
            for article in published
        ]

        archive_html = (
            "\n\n".join(cards)
        )

    else:
        archive_html = """\
<p class="blog-archive__empty">
  No articles published yet.
</p>"""

    page = template.replace(
        "{{ARCHIVE_ARTICLES}}",
        archive_html,
    )

    remaining = re.findall(
        r"\{\{[A-Z_]+\}\}",
        page,
    )

    if remaining:
        raise ValueError(
            "Unreplaced archive placeholders: "
            + ", ".join(
                sorted(set(remaining))
            )
        )

    ARCHIVE_OUTPUT_EN.write_text(
        page,
        encoding="utf-8",
    )

    print(
        "✓ blog/articles.html generated automatically"
    )


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
    print("PAGINE ARTICOLO GENERATE")
    print("=" * 60)
    print()

    for article in articles:
        meta = article["metadata"]

        if (
            meta["published"]
            and meta["lang"] in {"it", "en"}
        ):
            output_path = write_article_page(
                article
            )

            print(
                f"✓ {output_path.relative_to(ROOT)}"
            )

    print()
    print("=" * 60)
    print("HOME BLOG")
    print("=" * 60)
    print()

    update_blog_index_it(articles)
    update_blog_index_en(articles)

    print()
    print("=" * 60)
    print("ARCHIVIO BLOG")
    print("=" * 60)
    print()

    generate_archive_it(articles)
    generate_archive_en(articles)

if __name__ == "__main__":
    main()