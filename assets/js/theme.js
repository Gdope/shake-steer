/* ==========================================================================
   Shake&Steer — theme.js
   Dark / light mode. Dark is the default; the choice is stored in
   localStorage so it sticks between visits and across pages.

   This file is loaded in <head> WITHOUT "defer" on purpose: it must run
   before the page paints, otherwise light-mode users would see a dark flash.
   ========================================================================== */
(function () {
  "use strict";

  var STORAGE_KEY = "shakeandsteer:theme";
  var DEFAULT_THEME = "dark"; // <- change to "light" to flip the default

  /** Read the saved theme, falling back to the default. */
  function getSavedTheme() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === "dark" || saved === "light") return saved;
    } catch (e) {
      /* localStorage can be blocked (private mode) — ignore and use default */
    }
    return DEFAULT_THEME;
  }

  /** Apply a theme to the document and remember it. */
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      /* nothing we can do — the theme still applies for this page view */
    }
  }

  // 1. Apply immediately, before the first paint.
  applyTheme(getSavedTheme());

  // 2. Wire up the toggle button once the header exists in the DOM.
  document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll("[data-theme-toggle]");

    Array.prototype.forEach.call(buttons, function (button) {
      button.addEventListener("click", function () {
        var current = document.documentElement.getAttribute("data-theme");
        applyTheme(current === "light" ? "dark" : "light");
      });
    });
  });

  // Expose a tiny API in case you want to switch themes from elsewhere.
  window.SSTheme = { apply: applyTheme, get: getSavedTheme };
})();
