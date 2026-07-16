/**
 * GroMush — design-system gedrag
 * Kopieerknoppen bij codeblokken en een replay-knop voor de scroll-reveals.
 * Progressieve verrijking: zonder JS blijven de snippets gewoon leesbaar.
 */
(function () {
  "use strict";

  /* Kopieerknop bij elk codeblok */
  var blocks = document.querySelectorAll(".ds-code");
  blocks.forEach(function (block) {
    var code = block.querySelector("code");
    if (!code || !navigator.clipboard) {
      return;
    }
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "ds-copy";
    btn.textContent = "Kopieer";
    btn.setAttribute("aria-label", "Kopieer dit codevoorbeeld");
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(code.textContent.trim()).then(function () {
        btn.textContent = "Gekopieerd";
        btn.classList.add("is-copied");
        window.setTimeout(function () {
          btn.textContent = "Kopieer";
          btn.classList.remove("is-copied");
        }, 2000);
      });
    });
    block.appendChild(btn);
  });

  /* Reveal-demo opnieuw afspelen */
  var replay = document.querySelector(".ds-replay");
  var demo = document.getElementById("reveal-demo");
  if (replay && demo) {
    replay.addEventListener("click", function () {
      var items = demo.querySelectorAll("[data-reveal]");
      items.forEach(function (el) {
        el.classList.remove("is-visible");
      });
      window.setTimeout(function () {
        items.forEach(function (el) {
          el.classList.add("is-visible");
        });
      }, 400);
    });
  }
})();
