/* ==========================================================================
   Shake&Steer — gallery.js
   Lightbox for the gallery page.

   Every thumbnail is a <button class="gallery-item"> wrapping an <img>.
   Clicking one opens the full picture in an overlay with previous / next
   arrows, keyboard support (← → Esc) and a caption.
   ========================================================================== */
(function () {
  "use strict";

  function init() {
    var lightbox = document.querySelector("[data-lightbox]");
    var items = document.querySelectorAll("[data-lightbox-item]");
    if (!lightbox || !items.length) return;

    var image = lightbox.querySelector("[data-lightbox-image]");
    var caption = lightbox.querySelector("[data-lightbox-caption]");
    var counter = lightbox.querySelector("[data-lightbox-count]");
    var btnClose = lightbox.querySelector("[data-lightbox-close]");
    var btnPrev = lightbox.querySelector("[data-lightbox-prev]");
    var btnNext = lightbox.querySelector("[data-lightbox-next]");

    var index = 0;
    var lastFocused = null;

    /** Show the picture at position `i` (wraps around at both ends). */
    function show(i) {
      var total = items.length;
      index = (i + total) % total;

      var button = items[index];
      var thumb = button.querySelector("img");
      // data-full lets you point the lightbox at a bigger file than the
      // thumbnail; if it's missing we simply reuse the thumbnail.
      var full = button.getAttribute("data-full") || thumb.getAttribute("src");

      image.setAttribute("src", full);
      image.setAttribute("alt", thumb.getAttribute("alt") || "");
      caption.textContent = button.getAttribute("data-caption") || "";
      counter.textContent = index + 1 + " / " + total;
    }

    function open(i) {
      lastFocused = document.activeElement;
      show(i);
      lightbox.classList.add("is-open");
      lightbox.removeAttribute("aria-hidden");
      document.body.style.overflow = "hidden"; // stop the page behind scrolling
      btnClose.focus();
    }

    function close() {
      lightbox.classList.remove("is-open");
      lightbox.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      if (lastFocused) lastFocused.focus();
    }

    /* -- Wiring ---------------------------------------------------------- */
    Array.prototype.forEach.call(items, function (button, i) {
      button.addEventListener("click", function () {
        open(i);
      });
    });

    btnClose.addEventListener("click", close);
    btnPrev.addEventListener("click", function () {
      show(index - 1);
    });
    btnNext.addEventListener("click", function () {
      show(index + 1);
    });

    // Click on the dark background (but not the picture) closes the lightbox
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox) close();
    });

    document.addEventListener("keydown", function (event) {
      if (!lightbox.classList.contains("is-open")) return;
      if (event.key === "Escape") close();
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });

    /* -- Touch swipe ----------------------------------------------------- */
    var touchStartX = null;
    lightbox.addEventListener(
      "touchstart",
      function (event) {
        touchStartX = event.changedTouches[0].clientX;
      },
      { passive: true }
    );

    lightbox.addEventListener(
      "touchend",
      function (event) {
        if (touchStartX === null) return;
        var delta = event.changedTouches[0].clientX - touchStartX;
        if (Math.abs(delta) > 50) show(delta > 0 ? index - 1 : index + 1);
        touchStartX = null;
      },
      { passive: true }
    );

    /* -- Captions are translatable, so refresh the open one on language change */
    document.addEventListener("ss:languagechange", function () {
      if (lightbox.classList.contains("is-open")) {
        // Give the translator a tick to update the data attributes first
        window.setTimeout(function () {
          show(index);
        }, 0);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
