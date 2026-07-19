/**
 * GroMush — site behaviour
 * Mobile navigation, scroll reveals and hero scroll-fade.
 * All motion respects prefers-reduced-motion.
 */
(function () {
  "use strict";

  /* Mobile nav toggle */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* Couverts-kiezer: klik een bereik en zie de aanbevolen formule */
  var coversOptions = document.querySelectorAll(".covers__option");
  if (coversOptions.length) {
    var coversLink = document.querySelector(".covers__link");
    coversOptions.forEach(function (option) {
      var range = option.querySelector(".covers__range");
      if (!range) {
        return;
      }
      range.addEventListener("click", function () {
        coversOptions.forEach(function (other) {
          other.classList.remove("is-active");
          var otherRange = other.querySelector(".covers__range");
          if (otherRange) {
            otherRange.setAttribute("aria-pressed", "false");
          }
        });
        option.classList.add("is-active");
        range.setAttribute("aria-pressed", "true");
        if (coversLink) {
          var formule = option.getAttribute("data-formule");
          var doel = option.getAttribute("data-doel");
          if (formule) {
            coversLink.textContent = "Bekijk " + formule;
          }
          if (doel) {
            coversLink.setAttribute("href", doel);
          }
        }
      });
    });
  }

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    return;
  }

  /* Reveal-on-scroll (photos slide in from the side, blocks fade up) */
  var revealed = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealed.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.18, rootMargin: "0px 0px -8% 0px" }
    );
    revealed.forEach(function (el) {
      io.observe(el);
    });
  } else {
    revealed.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* Hero copy gently fades away while scrolling */
  var heroInner = document.querySelector(".hero__inner");
  if (heroInner) {
    var ticking = false;
    var fade = function () {
      var y = window.scrollY;
      var range = window.innerHeight * 0.6;
      var opacity = Math.max(0, 1 - y / range);
      heroInner.style.opacity = opacity.toFixed(3);
      heroInner.style.transform = "translateY(" + (y * 0.12).toFixed(1) + "px)";
      ticking = false;
    };
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(fade);
          ticking = true;
        }
      },
      { passive: true }
    );
  }
})();
