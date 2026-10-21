from pathlib import Path

from html import escape

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "blog"

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


if __name__ == "__main__":
    main()