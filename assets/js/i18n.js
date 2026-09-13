/* ==========================================================================
   Shake&Steer — i18n.js
   Five-language support: English, Serbian, Russian, German, Chinese.

   HOW IT WORKS
   ------------
   1. Every translatable element in the HTML carries a `data-i18n="key"`
      attribute, e.g.  <h2 data-i18n="home.services.title">Our services</h2>
   2. The English text stays written in the HTML. That is the fallback: if
      JavaScript is off — or you opened the file straight from your hard drive
      with file:// — the site still reads perfectly in English.
   3. When a language is chosen, this script fetches /i18n/<code>.json and
      swaps the text in.

   VARIANTS
   --------
   data-i18n="key"                  -> replaces the element's text
   data-i18n-html="key"             -> replaces the element's HTML (use when
                                       the translation contains <em>, <br>…)
   data-i18n-attr="alt:key, title:key"
                                    -> replaces one or more attributes

   TO TRANSLATE NEW TEXT: add a data-i18n attribute in the HTML, then add the
   same key to all five files in the /i18n/ folder.
   ========================================================================== */
(function () {
  "use strict";

  var STORAGE_KEY = "shakeandsteer:lang";
  var DEFAULT_LANG = "en";

  /* The languages offered in the header switcher.
     `dir` is here for the future — none of these five are right-to-left. */
  var LANGUAGES = [
    { code: "en", label: "EN", name: "English" },
    { code: "sr", label: "SR", name: "Srpski" },
    { code: "ru", label: "RU", name: "Русский" },
    { code: "de", label: "DE", name: "Deutsch" },
    { code: "zh", label: "中文", name: "中文" }
  ];

  var cache = {}; // downloaded dictionaries, keyed by language code
  var currentLang = DEFAULT_LANG;

  /* ---------------------------------------------------------------------
     Helpers
     --------------------------------------------------------------------- */

  /** Is `code` one of the languages we ship? */
  function isSupported(code) {
    for (var i = 0; i < LANGUAGES.length; i++) {
      if (LANGUAGES[i].code === code) return true;
    }
    return false;
  }

  /** The language to start with: saved choice > browser language > English. */
  function detectLang() {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved && isSupported(saved)) return saved;
    } catch (e) {
      /* storage blocked — fall through */
    }
    return DEFAULT_LANG;
  }

  /** Look up "a.b.c" inside a nested dictionary object. */
  function lookup(dict, key) {
    var parts = key.split(".");
    var value = dict;
    for (var i = 0; i < parts.length; i++) {
      if (value === null || typeof value !== "object") return undefined;
      value = value[parts[i]];
    }
    return typeof value === "string" ? value : undefined;
  }

  /* ---------------------------------------------------------------------
     Applying a dictionary to the page
     --------------------------------------------------------------------- */
  function translate(dict, lang) {
    // Plain text nodes
    var nodes = document.querySelectorAll("[data-i18n]");
    Array.prototype.forEach.call(nodes, function (el) {
      var text = lookup(dict, el.getAttribute("data-i18n"));
      if (text !== undefined) el.textContent = text;
    });

    // Rich text (may contain inline markup)
    var htmlNodes = document.querySelectorAll("[data-i18n-html]");
    Array.prototype.forEach.call(htmlNodes, function (el) {
      var html = lookup(dict, el.getAttribute("data-i18n-html"));
      if (html !== undefined) el.innerHTML = html;
    });

    // Attributes, e.g. data-i18n-attr="alt:gallery.1.alt, title:nav.home"
    var attrNodes = document.querySelectorAll("[data-i18n-attr]");
    Array.prototype.forEach.call(attrNodes, function (el) {
      el.getAttribute("data-i18n-attr")
        .split(",")
        .forEach(function (pair) {
          var bits = pair.split(":");
          if (bits.length !== 2) return;
          var attr = bits[0].trim();
          var value = lookup(dict, bits[1].trim());
          if (value !== undefined) el.setAttribute(attr, value);
        });
    });

    // Tell the browser (and screen readers) which language the page is in
    document.documentElement.setAttribute("lang", lang);

    // Keep the switcher in sync
    var selects = document.querySelectorAll("[data-lang-switch]");
    Array.prototype.forEach.call(selects, function (select) {
      select.value = lang;
    });

    // Let other scripts react (menu.js swaps the PDF link, for example)
    document.dispatchEvent(
      new CustomEvent("ss:languagechange", { detail: { lang: lang, dict: dict } })
    );
  }

  /* ---------------------------------------------------------------------
     Loading a language file
     --------------------------------------------------------------------- */
  function setLanguage(lang, options) {
    if (!isSupported(lang)) lang = DEFAULT_LANG;
    currentLang = lang;

    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* storage blocked — the choice just won't persist */
    }

    if (cache[lang]) {
      translate(cache[lang], lang);
      return Promise.resolve(cache[lang]);
    }

    // The i18n folder sits next to the HTML pages, so a relative path works.
    return fetch("i18n/" + lang + ".json", { cache: "no-cache" })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(function (dict) {
        cache[lang] = dict;
        translate(dict, lang);
        return dict;
      })
      .catch(function (error) {
        // Most common cause: the page was opened with file:// instead of a
        // web server, which browsers block for security reasons.
        if (location.protocol === "file:") {
          console.warn(
            "[Shake&Steer] Translations can't load from file:// — the page " +
              "stays in English. Run a local server to test other languages:\n" +
              "    python -m http.server 8000\n" +
              "then open http://localhost:8000"
          );
        } else {
          console.error("[Shake&Steer] Could not load i18n/" + lang + ".json", error);
        }
        // Silent fallback: the English text already in the HTML stays put.
        if (options && options.onError) options.onError(error);
      });
  }

  /* ---------------------------------------------------------------------
     Build the switcher and start up
     --------------------------------------------------------------------- */
  function initSwitchers() {
    var selects = document.querySelectorAll("[data-lang-switch]");

    Array.prototype.forEach.call(selects, function (select) {
      // Fill the <select> from the LANGUAGES list above
      select.innerHTML = "";
      LANGUAGES.forEach(function (lang) {
        var option = document.createElement("option");
        option.value = lang.code;
        option.textContent = lang.label;
        option.title = lang.name;
        select.appendChild(option);
      });

      select.value = currentLang;
      select.addEventListener("change", function () {
        setLanguage(select.value);
      });
    });
  }

  function init() {
    currentLang = detectLang();
    initSwitchers();
    // English is already in the HTML — only fetch when something else is picked.
    if (currentLang !== DEFAULT_LANG) {
      setLanguage(currentLang);
    } else {
      document.documentElement.setAttribute("lang", "en");
      document.dispatchEvent(
        new CustomEvent("ss:languagechange", { detail: { lang: "en", dict: null } })
      );
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Small public API
  window.SSi18n = {
    languages: LANGUAGES,
    set: setLanguage,
    get: function () {
      return currentLang;
    }
  };
})();
