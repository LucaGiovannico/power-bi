/* BUSINESS PLAN IT: gesture along the landscape dashboard axis.
   No MutationObserver, no timers, no polling. */
(() => {
  "use strict";

  function init() {
    const box = document.querySelector(".dashboard-lightbox");
    const image = box?.querySelector(".dashboard-lightbox__image");
    const previous = box?.querySelector(".dashboard-lightbox__arrow--left");
    const next = box?.querySelector(".dashboard-lightbox__arrow--right");
    const slides = [...document.querySelectorAll(".dashboard__image")];
    if (!box || !image || !previous || !next || !slides.length) return;

    let counter = box.querySelector(".dashboard-lightbox__counter");
    if (!counter) {
      counter = document.createElement("span");
      counter.className = "dashboard-lightbox__counter";
    }
    counter.setAttribute("aria-live", "polite");
    if (counter.parentElement !== box) box.appendChild(counter);

    const mobilePortrait = () => window.matchMedia(
      "(max-width: 767px) and (orientation: portrait)"
    ).matches;
    const isOpen = () => box.classList.contains("is-open");
    const url = (s) => s ? new URL(s, document.baseURI).href : "";

    function updateCounter() {
      const selected = url(image.getAttribute("src"));
      const idx = slides.findIndex((slide) =>
        url(slide.dataset.full || slide.getAttribute("src")) === selected
      );
      counter.textContent = `${idx < 0 ? 1 : idx + 1}/${slides.length}`;
    }

    image.addEventListener("load", updateCounter);
    slides.forEach((slide) => slide.addEventListener("click", updateCounter));
    previous.addEventListener("click", updateCounter);
    next.addEventListener("click", updateCounter);
    updateCounter();

    let start = null;
    let mouseStart = null;

    // Il gesto richiesto è verso il contatore precedente (in basso sul
    // telefono verticale) o nella direzione opposta (in alto).
    function move(x1, y1, x2, y2) {
      const dx = x2 - x1;
      const dy = y2 - y1;
      if (Math.abs(dy) < 60 || Math.abs(dy) < Math.abs(dx) * 1.4) return false;
      (dy > 0 ? next : previous).click();
      updateCounter();
      return true;
    }

    box.addEventListener("touchstart", (event) => {
      if (!mobilePortrait() || !isOpen() || event.touches.length !== 1) {
        start = null;
        return;
      }
      const t = event.touches[0];
      start = [t.clientX, t.clientY];
    }, {capture: true, passive: true});

    box.addEventListener("touchend", (event) => {
      if (!mobilePortrait() || !isOpen()) { start = null; return; }
      // Impedisce alla lightbox originale di eseguire anche lo swipe X.
      event.stopImmediatePropagation();
      const from = start;
      start = null;
      if (!from || event.changedTouches.length !== 1) return;
      const t = event.changedTouches[0];
      if (move(from[0], from[1], t.clientX, t.clientY)) {
        event.preventDefault();
      }
    }, {capture: true, passive: false});

    box.addEventListener("touchcancel", () => { start = null; }, {
      capture: true, passive: true
    });

    // Simulatore mobile di Safari: anche il trascinamento con mouse.
    box.addEventListener("pointerdown", (event) => {
      if (event.pointerType !== "mouse" || !mobilePortrait() || !isOpen() ||
          event.target.closest("button")) return;
      mouseStart = [event.clientX, event.clientY];
    });
    box.addEventListener("pointerup", (event) => {
      const from = mouseStart;
      mouseStart = null;
      if (!from || event.pointerType !== "mouse" || !mobilePortrait() || !isOpen()) return;
      move(from[0], from[1], event.clientX, event.clientY);
    });
    image.addEventListener("dragstart", (event) => event.preventDefault());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, {once: true});
  } else {
    init();
  }
})();
