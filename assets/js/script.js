
(() => {
  "use strict";

  /* ============================= */
  /* LANGUAGE SELECTOR */
  /* ============================= */

  function getLanguageSelectorFromEvent(event) {
    if (event && event.currentTarget) {
      const selector = event.currentTarget.closest(".language-selector");
      if (selector) return selector;
    }

    return document.querySelector(".language-selector");
  }

  function closeLanguageMenus(exceptSelector = null) {
    document.querySelectorAll(".language-selector").forEach((selector) => {
      if (selector === exceptSelector) return;

      const menu =
        selector.querySelector(".language-selector__menu") ||
        document.getElementById("languageMenu");
      const button = selector.querySelector(".language-selector__button");

      if (menu) {
        menu.classList.remove("show");
      }

      if (button) {
        button.setAttribute("aria-expanded", "false");
      }
    });
  }

  function toggleLanguageMenu(event) {
    if (event) {
      event.stopPropagation();
    }

    const selector = getLanguageSelectorFromEvent(event);
    if (!selector) return;

    const menu =
      selector.querySelector(".language-selector__menu") ||
      document.getElementById("languageMenu");
    const button = selector.querySelector(".language-selector__button");

    if (!menu) return;

    closeLanguageMenus(selector);

    const isOpen = menu.classList.toggle("show");

    if (button) {
      button.setAttribute("aria-expanded", String(isOpen));
    }
  }

  function setLanguage(lang) {
    const selector = document.querySelector(".language-selector");

    /* Pagine che definiscono gli URL tramite data-it / data-en */
    const targetUrl = selector ? selector.dataset[lang] : null;

    if (targetUrl) {
      window.location.href = targetUrl;
      return;
    }

    /* Fallback compatibile con il primo JS originale */
    const fallbackUrls = {
      it: "index.html",
      en: "index-en.html",
    };

    if (fallbackUrls[lang]) {
      window.location.href = fallbackUrls[lang];
      return;
    }

    console.warn(`No URL found for language: ${lang}`);
  }

  /* Mantiene disponibili le funzioni per eventuali onclick nell'HTML */
  window.toggleLanguageMenu = toggleLanguageMenu;
  window.setLanguage = setLanguage;

  /* ============================= */
  /* INITIALIZATION */
  /* ============================= */

  function init() {
    /* ============================= */
    /* HASH SCROLL RESTORATION */
    /* ============================= */

    function scrollToHashSection() {
      const hash = window.location.hash;
      if (!hash) return;

      let target = null;

      try {
        target = document.querySelector(hash);
      } catch (error) {
        console.warn("Hash selector non valido:", hash);
        return;
      }

      if (!target) return;

      const navbar = document.querySelector(".navbar");
      const navbarHeight = navbar ? navbar.offsetHeight : 0;

      const targetPosition =
        target.getBoundingClientRect().top + window.scrollY - navbarHeight;

      window.scrollTo({
        top: targetPosition,
        behavior: "auto",
      });
    }

    function restoreHashPosition() {
      if (!window.location.hash) return;

      if ("scrollRestoration" in history) {
        history.scrollRestoration = "manual";
      }

      scrollToHashSection();

      /* Ripete il posizionamento dopo font, immagini e ripristino browser */
      window.setTimeout(scrollToHashSection, 100);
      window.setTimeout(scrollToHashSection, 400);
      window.setTimeout(scrollToHashSection, 1000);
    }

    restoreHashPosition();
    window.addEventListener("load", restoreHashPosition);
    window.addEventListener("pageshow", restoreHashPosition);

    /* Chiude il menu lingua cliccando fuori dal selettore */
    document.addEventListener("click", (event) => {
      document.querySelectorAll(".language-selector").forEach((selector) => {
        if (selector.contains(event.target)) return;

        const menu =
          selector.querySelector(".language-selector__menu") ||
          document.getElementById("languageMenu");
        const button = selector.querySelector(".language-selector__button");

        if (menu) {
          menu.classList.remove("show");
        }

        if (button) {
          button.setAttribute("aria-expanded", "false");
        }
      });
    });

    /* ============================= */
    /* DASHBOARD CAROUSEL */
    /* ============================= */

    const carouselTrack = document.querySelector(".carousel__track");
    const dashboardImages = Array.from(
      document.querySelectorAll(".dashboard__image")
    );
    const carouselPrevButton = document.querySelector(".carousel__arrow--left");
    const carouselNextButton = document.querySelector(
      ".carousel__arrow--right"
    );

    let carouselIndex = 0;

    function updateCarousel() {
      if (!carouselTrack || dashboardImages.length === 0) return;

      carouselTrack.style.transform = `translateX(-${carouselIndex * 100}%)`;
    }

    function showPreviousSlide() {
      if (dashboardImages.length === 0) return;

      carouselIndex =
        carouselIndex === 0 ? dashboardImages.length - 1 : carouselIndex - 1;

      updateCarousel();
    }

    function showNextSlide() {
      if (dashboardImages.length === 0) return;

      carouselIndex =
        carouselIndex === dashboardImages.length - 1 ? 0 : carouselIndex + 1;

      updateCarousel();
    }

    if (carouselPrevButton) {
      carouselPrevButton.addEventListener("click", showPreviousSlide);
    }

    if (carouselNextButton) {
      carouselNextButton.addEventListener("click", showNextSlide);
    }

    /* ============================= */
    /* DASHBOARD CAROUSEL SWIPE */
    /* ============================= */

    const swipeThreshold = 45;
    let carouselTouchStartX = 0;
    let carouselTouchEndX = 0;

    function handleCarouselSwipe() {
      const swipeDistance = carouselTouchEndX - carouselTouchStartX;

      if (Math.abs(swipeDistance) < swipeThreshold) return;

      if (swipeDistance < 0) {
        showNextSlide();
      } else {
        showPreviousSlide();
      }
    }

    if (carouselTrack) {
      carouselTrack.addEventListener(
        "touchstart",
        (event) => {
          carouselTouchStartX = event.changedTouches[0].screenX;
        },
        { passive: true }
      );

      carouselTrack.addEventListener(
        "touchend",
        (event) => {
          carouselTouchEndX = event.changedTouches[0].screenX;
          handleCarouselSwipe();
        },
        { passive: true }
      );
    }

    /* ============================= */
    /* DASHBOARD LIGHTBOX */
    /* ============================= */

    const lightbox = document.querySelector(".dashboard-lightbox");
    const lightboxImage = document.querySelector(".dashboard-lightbox__image");
    const lightboxCloseButton = document.querySelector(
      ".dashboard-lightbox__close"
    );
    const lightboxPrevButton = document.querySelector(
      ".dashboard-lightbox__arrow--left"
    );
    const lightboxNextButton = document.querySelector(
      ".dashboard-lightbox__arrow--right"
    );

    let currentDashboardIndex = 0;

    function setLightboxImage(index) {
      if (!lightboxImage || dashboardImages.length === 0) return;

      currentDashboardIndex = index;

      const image = dashboardImages[currentDashboardIndex];
      const fullImageSrc = image.dataset.full || image.src;
      const imageAlt = image.alt || "Dashboard preview";

      lightboxImage.src = fullImageSrc;
      lightboxImage.alt = imageAlt;
    }

    function openDashboardLightbox(index) {
      if (!lightbox || !lightboxImage || dashboardImages.length === 0) return;

      setLightboxImage(index);

      lightbox.classList.add("is-open");
      lightbox.setAttribute("aria-hidden", "false");
      document.body.classList.add("lightbox-open");

      if (lightboxCloseButton) {
        lightboxCloseButton.focus();
      }
    }

    function closeDashboardLightbox() {
      if (!lightbox || !lightboxImage) return;

      lightbox.classList.remove("is-open");
      lightbox.setAttribute("aria-hidden", "true");
      document.body.classList.remove("lightbox-open");

      lightboxImage.src = "";
      lightboxImage.alt = "";
    }

    function showPreviousDashboard() {
      if (dashboardImages.length === 0) return;

      const previousIndex =
        currentDashboardIndex === 0
          ? dashboardImages.length - 1
          : currentDashboardIndex - 1;

      setLightboxImage(previousIndex);
    }

    function showNextDashboard() {
      if (dashboardImages.length === 0) return;

      const nextIndex =
        currentDashboardIndex === dashboardImages.length - 1
          ? 0
          : currentDashboardIndex + 1;

      setLightboxImage(nextIndex);
    }

    dashboardImages.forEach((image, index) => {
      image.addEventListener("click", () => {
        openDashboardLightbox(index);
      });

      image.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openDashboardLightbox(index);
        }
      });
    });

    if (lightboxCloseButton) {
      lightboxCloseButton.addEventListener("click", closeDashboardLightbox);
    }

    if (lightboxPrevButton) {
      lightboxPrevButton.addEventListener("click", showPreviousDashboard);
    }

    if (lightboxNextButton) {
      lightboxNextButton.addEventListener("click", showNextDashboard);
    }

    if (lightbox) {
      lightbox.addEventListener("click", (event) => {
        if (event.target === lightbox) {
          closeDashboardLightbox();
        }
      });
    }

    /* ============================= */
    /* DASHBOARD LIGHTBOX SWIPE */
    /* ============================= */

    let lightboxTouchStartX = 0;
    let lightboxTouchEndX = 0;

    function handleLightboxSwipe() {
      const swipeDistance = lightboxTouchEndX - lightboxTouchStartX;

      if (Math.abs(swipeDistance) < swipeThreshold) return;

      if (swipeDistance < 0) {
        showNextDashboard();
      } else {
        showPreviousDashboard();
      }
    }

    if (lightbox) {
      lightbox.addEventListener(
        "touchstart",
        (event) => {
          lightboxTouchStartX = event.changedTouches[0].screenX;
        },
        { passive: true }
      );

      lightbox.addEventListener(
        "touchend",
        (event) => {
          lightboxTouchEndX = event.changedTouches[0].screenX;
          handleLightboxSwipe();
        },
        { passive: true }
      );
    }

    /* ============================= */
    /* COUNTER ANIMATION */
    /* ============================= */

    const counters = document.querySelectorAll(".js-counter");

    function animateCounter(counter) {
      const target = Number(counter.dataset.target);
      const prefix = counter.dataset.prefix || "";
      const suffix = counter.dataset.suffix || "";

      if (!Number.isFinite(target)) {
        console.error("Valore data-target non valido:", counter);
        return;
      }

      const duration = 1200;
      const startTime = performance.now();

      function updateCounter(currentTime) {
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        const easedProgress = 1 - Math.pow(1 - progress, 3);
        const currentValue = Math.round(target * easedProgress);

        counter.textContent = `${prefix}${currentValue}${suffix}`;

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        }
      }

      requestAnimationFrame(updateCounter);
    }

    if (counters.length > 0 && "IntersectionObserver" in window) {
      const counterObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            animateCounter(entry.target);
            observer.unobserve(entry.target);
          });
        },
        {
          threshold: 0.35,
        }
      );

      counters.forEach((counter) => {
        counterObserver.observe(counter);
      });
    } else if (counters.length > 0) {
      counters.forEach(animateCounter);
    }

    /* ============================= */
    /* CONTACT FORM MODAL */
    /* ============================= */

    const contactFormModal = document.getElementById("contactFormModal");
    const closeContactFormOverlay = document.getElementById("closeContactForm");
    const closeContactFormButton = document.getElementById(
      "closeContactFormButton"
    );

    let lastFocusedElementBeforeModal = null;

    function openContactForm() {
      if (!contactFormModal) return;

      lastFocusedElementBeforeModal = document.activeElement;

      contactFormModal.classList.add("show");
      contactFormModal.setAttribute("aria-hidden", "false");
      document.body.classList.add("lightbox-open");

      window.requestAnimationFrame(() => {
        const firstField = contactFormModal.querySelector(
          "input:not([type='hidden']), select, textarea, button"
        );

        if (firstField) {
          firstField.focus();
        }
      });
    }

    function closeContactForm() {
      if (!contactFormModal) return;

      contactFormModal.classList.remove("show");
      contactFormModal.setAttribute("aria-hidden", "true");
      document.body.classList.remove("lightbox-open");

      if (
        lastFocusedElementBeforeModal &&
        typeof lastFocusedElementBeforeModal.focus === "function"
      ) {
        lastFocusedElementBeforeModal.focus();
      }

      lastFocusedElementBeforeModal = null;
    }

    document
      .querySelectorAll("#openContactForm, .js-open-contact-form")
      .forEach((button) => {
        button.addEventListener("click", openContactForm);
      });

    if (closeContactFormOverlay) {
      closeContactFormOverlay.addEventListener("click", closeContactForm);
    }

    if (closeContactFormButton) {
      closeContactFormButton.addEventListener("click", closeContactForm);
    }

    /* ============================= */
    /* CONTACT FORM SUBMISSION */
    /* ============================= */

const contactForm = document.getElementById("contactForm");
const formSuccessMessage = document.getElementById("formSuccessMessage");

const pageLanguage = document.documentElement.lang
  .toLowerCase()
  .startsWith("en")
  ? "en"
  : "it";

const formText = {
  it: {
    loading: "Invio in corso...",
    success: "Richiesta inviata",
    retry: "Riprova",
    error:
      "Non è stato possibile inviare la richiesta. Riprova tra poco oppure contattami via email.",
  },
  en: {
    loading: "Sending...",
    success: "Request sent",
    retry: "Try again",
    error:
      "Your request could not be sent. Please try again shortly or contact me by email.",
  },
};

const currentFormText = formText[pageLanguage];

let formErrorMessage = document.getElementById("formErrorMessage");

if (contactForm && !formErrorMessage) {
  formErrorMessage = document.createElement("p");
  formErrorMessage.id = "formErrorMessage";
  formErrorMessage.className = "form-error-message";
  formErrorMessage.setAttribute("role", "alert");
  formErrorMessage.setAttribute("aria-live", "assertive");
  formErrorMessage.textContent = currentFormText.error;

  if (formSuccessMessage) {
    formSuccessMessage.insertAdjacentElement("afterend", formErrorMessage);
  } else {
    contactForm.appendChild(formErrorMessage);
  }
}

if (contactForm) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(contactForm);
    const submitButton = contactForm.querySelector("button[type='submit']");
    const originalButtonText = submitButton
      ? submitButton.textContent.trim()
      : "";

    if (formSuccessMessage) {
      formSuccessMessage.style.display = "none";
    }

    if (formErrorMessage) {
      formErrorMessage.style.display = "none";
    }

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = currentFormText.loading;
    }

    try {
      const response = await fetch(contactForm.action, {
        method: contactForm.method || "POST",
        body: formData,
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Form submission failed");
      }

      contactForm.reset();

      if (formSuccessMessage) {
        formSuccessMessage.style.display = "block";
      }

      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
      }
    } catch (error) {
      console.error("Contact form submission error:", error);

      if (formErrorMessage) {
        formErrorMessage.style.display = "block";
      }

      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent =
          originalButtonText || currentFormText.retry;
      }
    }
  });
}
    /* ============================== */
    /* SCROLL BUTTON: DOWN / UP */
    /* ============================== */

    const backToTopButton =
      document.getElementById("back__to-top") ||
      document.getElementById("backToTop");

    function updateScrollButton() {
      if (!backToTopButton) return;

      const scrollPosition = window.scrollY;
      const viewportHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      const maxScroll = documentHeight - viewportHeight;
      const middleOfPage = maxScroll / 2;

      const shouldShow = scrollPosition > 500;
      const isPastMiddle = scrollPosition >= middleOfPage;

      backToTopButton.classList.toggle("show", shouldShow);
      backToTopButton.classList.toggle("is-visible", shouldShow);

      if (isPastMiddle) {
        backToTopButton.textContent = "↥";
        backToTopButton.setAttribute("aria-label", "Torna all’inizio");
        backToTopButton.dataset.direction = "up";
      } else {
        backToTopButton.textContent = "↧";
        backToTopButton.setAttribute(
          "aria-label",
          "Vai alla fine della pagina"
        );
        backToTopButton.dataset.direction = "down";
      }
    }

    if (backToTopButton) {
      window.addEventListener("scroll", updateScrollButton, {
        passive: true,
      });

      window.addEventListener("resize", updateScrollButton);

      backToTopButton.addEventListener("click", () => {
        const direction = backToTopButton.dataset.direction;

        if (direction === "up") {
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        } else {
          window.scrollTo({
            top: document.documentElement.scrollHeight,
            behavior: "smooth",
          });
        }
      });

      updateScrollButton();
    }

    /* ============================= */
    /* SERVICE FAQ ACCORDION */
    /* ============================= */

    const serviceFaqQuestions = Array.from(
      document.querySelectorAll(".service-faq__question")
    );

    function closeServiceFaq(question) {
      const answerId = question.getAttribute("aria-controls");
      const answer = answerId ? document.getElementById(answerId) : null;
      const item = question.closest(".service-faq__item");

      question.setAttribute("aria-expanded", "false");

      if (answer) {
        answer.hidden = true;
      }

      if (item) {
        item.classList.remove("is-open");
      }
    }

    function openServiceFaq(question) {
      const answerId = question.getAttribute("aria-controls");
      const answer = answerId ? document.getElementById(answerId) : null;
      const item = question.closest(".service-faq__item");

      question.setAttribute("aria-expanded", "true");

      if (answer) {
        answer.hidden = false;
      }

      if (item) {
        item.classList.add("is-open");
      }
    }

    function toggleServiceFaq(question) {
      const isOpen = question.getAttribute("aria-expanded") === "true";

      serviceFaqQuestions.forEach((otherQuestion) => {
        if (otherQuestion !== question) {
          closeServiceFaq(otherQuestion);
        }
      });

      if (isOpen) {
        closeServiceFaq(question);
      } else {
        openServiceFaq(question);
      }
    }

    serviceFaqQuestions.forEach((question) => {
      question.addEventListener("click", () => {
        toggleServiceFaq(question);
      });
    });

    /* ============================= */
    /* GLOBAL KEYBOARD HANDLER */
    /* ============================= */

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeLanguageMenus();

        if (lightbox && lightbox.classList.contains("is-open")) {
          closeDashboardLightbox();
        }

        if (contactFormModal && contactFormModal.classList.contains("show")) {
          closeContactForm();
        }

        serviceFaqQuestions.forEach((question) => {
          if (question.getAttribute("aria-expanded") === "true") {
            closeServiceFaq(question);
          }
        });

        return;
      }

      if (!lightbox || !lightbox.classList.contains("is-open")) return;

      if (event.key === "ArrowLeft") {
        showPreviousDashboard();
      }

      if (event.key === "ArrowRight") {
        showNextDashboard();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
