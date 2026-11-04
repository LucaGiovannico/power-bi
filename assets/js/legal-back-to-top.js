document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("back__to-top");
  if (!button) return;

  function updateButton() {
    button.classList.toggle("show", window.scrollY > 500);
  }

  window.addEventListener("scroll", updateButton, {
    passive: true
  });

  button.addEventListener("click", () => {
    const reducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    window.scrollTo({
      top: 0,
      behavior: reducedMotion ? "auto" : "smooth"
    });
  });

  updateButton();
});
