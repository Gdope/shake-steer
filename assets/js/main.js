/* ==========================================================================
   Shake&Steer — main.js
   Shared page behaviour:
     1. Sticky header state
     2. Mobile navigation drawer
     3. Scroll-reveal animations
     4. Current year in the footer
     5. Menu PDF link follows the selected language
   ========================================================================== */
(function () {
  "use strict";

  /* ---------------------------------------------------------------------
     1. HEADER — add .is-stuck once the visitor scrolls away from the top
     --------------------------------------------------------------------- */
  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;

    var ticking = false;

    function update() {
      header.classList.toggle("is-stuck", window.scrollY > 20);
      ticking = false;
    }

    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(update);
          ticking = true;
        }
      },
      { passive: true }
    );

    update();
  }

  /* ---------------------------------------------------------------------
     2. MOBILE NAVIGATION
     --------------------------------------------------------------------- */
  function initNav() {
    var header = document.querySelector(".site-header");
    var toggle = document.querySelector("[data-nav-toggle]");
    var nav = document.querySelector("[data-nav]");
    if (!header || !toggle || !nav) return;

    function setOpen(open) {
      header.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    }

    toggle.addEventListener("click", function () {
      setOpen(!header.classList.contains("is-open"));
    });

    // Close when a link is tapped
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) setOpen(false);
    });

    // Close on Escape
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false);
    });

    // Close when the window grows back to desktop width
    window.addEventListener("resize", function () {
      if (window.innerWidth > 900) setOpen(false);
    });
  }

  /* ---------------------------------------------------------------------
     3. SCROLL REVEAL
     Elements with class="reveal" fade up when they enter the viewport.
     Children of a [data-reveal-group] get a small staggered delay.
     --------------------------------------------------------------------- */
  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    // No IntersectionObserver (very old browser)? Just show everything.
    if (!("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(items, function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    // Stagger: each .reveal inside a group waits a little longer than the last
    var groups = document.querySelectorAll("[data-reveal-group]");
    Array.prototype.forEach.call(groups, function (group) {
      var step = parseInt(group.getAttribute("data-reveal-group"), 10) || 90;
      Array.prototype.forEach.call(
        group.querySelectorAll(".reveal"),
        function (el, index) {
          el.style.setProperty("--reveal-delay", index * step + "ms");
        }
      );
    });

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target); // animate once, then forget
        });
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.08 }
    );

    Array.prototype.forEach.call(items, function (el) {
      observer.observe(el);
    });
  }

  /* ---------------------------------------------------------------------
     4. FOOTER YEAR — keeps the copyright line current by itself
     --------------------------------------------------------------------- */
  function initYear() {
    var nodes = document.querySelectorAll("[data-year]");
    var year = String(new Date().getFullYear());
    Array.prototype.forEach.call(nodes, function (el) {
      el.textContent = year;
    });
  }

  /* ---------------------------------------------------------------------
     5. MENU PDF — point the download button at the right language file.
     We ship two PDFs (English and Serbian). Serbian visitors get the
     Serbian one; every other language gets English.
     --------------------------------------------------------------------- */
  function initPdfLinks() {
    var links = document.querySelectorAll("[data-pdf-link]");
    if (!links.length) return;

    function update(lang) {
      var isSerbian = lang === "sr";
      Array.prototype.forEach.call(links, function (link) {
        var file = isSerbian
          ? link.getAttribute("data-pdf-sr")
          : link.getAttribute("data-pdf-en");
        if (file) {
          link.setAttribute("href", file);
          link.setAttribute("download", file.split("/").pop());
        }
      });
    }

    document.addEventListener("ss:languagechange", function (event) {
      update(event.detail.lang);
    });

    update(window.SSi18n ? window.SSi18n.get() : "en");
  }

  /* --------------------------------------------------------------------- */
  function init() {
    initHeader();
    initNav();
    initReveal();
    initYear();
    initPdfLinks();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
