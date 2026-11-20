/* BLOG ARTICLE BACK TO TOP - DOM REPAIR */
(() => {
  "use strict";
  const buttonIT = "<button\n      id=\"blog-article-back-to-top\"\n      class=\"back__to-top\"\n      type=\"button\"\n      aria-label=\"Torna all'inizio\"\n    >\n      ↥\n    </button>";
  const buttonEN = "<button\n      id=\"blog-article-back-to-top\"\n      class=\"back__to-top\"\n      type=\"button\"\n      aria-label=\"Torna all'inizio\"\n    >\n      ↥\n    </button>";
  const CLASS = "blog-article-back-to-top";

  function init() {
    let button = document.querySelector("button." + CLASS);
    if (!button) {
      const language = (document.documentElement.lang || "it").toLowerCase();
      const template = document.createElement("template");
      template.innerHTML = (language.startsWith("en") ? buttonEN : buttonIT).trim();
      button = template.content.firstElementChild;
      if (!button || button.tagName !== "BUTTON") {
        console.error("Back to top: modello pulsante non valido");
        return;
      }
      document.body.appendChild(button);
    }
    if (button.dataset.blogTopReady === "true") return;
    button.dataset.blogTopReady = "true";
    button.hidden = false;
    button.type = "button";
    button.style.setProperty("display", "flex", "important");
    button.style.setProperty("position", "fixed", "important");
    button.style.setProperty("z-index", "9999", "important");

    function update() {
      const mobile = window.innerWidth <= 768;
      button.style.setProperty("right", mobile ? "16px" : "24px", "important");
      button.style.setProperty("bottom", mobile ? "16px" : "24px", "important");
      const threshold = Math.max(320, Math.round(window.innerHeight * 0.55));
      const show = window.scrollY >= threshold;
      button.classList.toggle("is-visible", show);
      button.style.setProperty("opacity", show ? "1" : "0", "important");
      button.style.setProperty("visibility", show ? "visible" : "hidden", "important");
      button.style.setProperty("pointer-events", show ? "auto" : "none", "important");
      button.tabIndex = show ? 0 : -1;
      button.setAttribute("aria-hidden", show ? "false" : "true");
    }
    button.addEventListener("click", () => {
      const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({top: 0, behavior: reduced ? "auto" : "smooth"});
    });
    window.addEventListener("scroll", update, {passive: true});
    window.addEventListener("resize", update, {passive: true});
    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, {once: true});
  } else {
    init();
  }
})();
