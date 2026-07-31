/**
 * GroMush — story (homepage scrollytelling)
 *
 * Drives the seven homepage scenes with GSAP + ScrollTrigger (vendored,
 * self-hosted). The page is complete without this file: the CSS default
 * state of every scene is the finished state. This script only *rewinds*
 * elements and scrubs them forward on scroll.
 *
 * Gates, in order:
 *  1. prefers-reduced-motion: reduce  -> do nothing (page stays static)
 *  2. GSAP missing                    -> do nothing
 *  3. Pinned scenes only >= 48rem via gsap.matchMedia (auto-reverts on
 *     resize, so mobile always falls back to the CSS-only behaviour)
 */
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  if (!window.gsap || !window.ScrollTrigger) {
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  /* Everything below may now rearrange layout for animation */
  document.body.classList.add("story-js");

  var mm = gsap.matchMedia();

  /* --- Scene 1: hero — intro plays on every viewport ------------------- */
  var heroScene = document.querySelector('[data-scene="hero"]');
  if (heroScene) {
    var heroInner = heroScene.querySelector(".scene__inner");
    gsap.from(heroInner.children, {
      autoAlpha: 0,
      y: 28,
      duration: 0.9,
      ease: "power2.out",
      stagger: 0.16,
      clearProps: "all"
    });
    gsap.from(heroScene.querySelector(".scroll-cue"), {
      autoAlpha: 0,
      duration: 0.8,
      delay: 1,
      clearProps: "opacity,visibility"
    });
    /* The hero photo settles from a slight zoom */
    gsap.from(heroScene.querySelector(".hero-photo img"), {
      scale: 1.07,
      duration: 5,
      ease: "power1.out"
    });
  }

  /* --- Pinned scenes: desktop only -------------------------------------- */
  mm.add("(min-width: 48rem)", function () {
    initHeroScrub();
    initUnderground();
    initFarm();
    initVarieties();
    initRoute();
    initPlate();
  });

  /* Hero copy drifts away while the underground scene approaches */
  function initHeroScrub() {
    if (!heroScene) {
      return;
    }
    gsap.to(heroScene.querySelector(".scene__inner"), {
      autoAlpha: 0,
      y: -48,
      ease: "none",
      scrollTrigger: {
        trigger: heroScene,
        start: "top top",
        end: "bottom 35%",
        scrub: true
      }
    });
  }

  /* Mycelium threads draw themselves while the copy steps crossfade */
  function initUnderground() {
    var scene = document.querySelector('[data-scene="underground"]');
    if (!scene) {
      return;
    }
    var pin = scene.querySelector(".scene__pin");
    var soil = scene.querySelector(".myc--soil");
    var mains = scene.querySelectorAll(".myc--main");
    var branches = scene.querySelectorAll(".myc--branch");
    var nodes = scene.querySelectorAll(".myc-node, .myc-dot");
    var steps = scene.querySelectorAll(".scene__step");
    var hook = scene.querySelector(".scene__hook");

    /* Rewind: measure each path and hide it behind its own dash */
    scene.querySelectorAll(".myc").forEach(function (path) {
      var length = path.getTotalLength();
      gsap.set(path, { strokeDasharray: length, strokeDashoffset: length });
    });
    gsap.set(nodes, { scale: 0, transformOrigin: "center center" });
    gsap.set(steps, { autoAlpha: 0, y: 24 });
    gsap.set(hook, { autoAlpha: 0, y: 16 });

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: pin,
        pin: pin,
        start: "top top",
        end: "+=180%",
        scrub: 0.8,
        anticipatePin: 1
      }
    });
    tl.to(soil, { strokeDashoffset: 0, duration: 1, ease: "none" }, 0)
      .to(mains, { strokeDashoffset: 0, duration: 4, stagger: 0.35, ease: "none" }, 0.5)
      .to(branches, { strokeDashoffset: 0, duration: 2.5, stagger: 0.25, ease: "none" }, 3)
      .to(nodes, { scale: 1, duration: 0.6, stagger: 0.12, ease: "back.out(2)" }, 3.5)
      .to(steps[0], { autoAlpha: 1, y: 0, duration: 0.8 }, 0.4)
      .to(steps[0], { autoAlpha: 0, duration: 0.6 }, 3.2)
      .to(steps[1], { autoAlpha: 1, y: 0, duration: 0.8 }, 3.8)
      .to(steps[1], { autoAlpha: 0, duration: 0.6 }, 6.2)
      .to(steps[2], { autoAlpha: 1, y: 0, duration: 0.8 }, 6.8)
      .to(hook, { autoAlpha: 1, y: 0, duration: 0.6 }, 7.4)
      .to({}, { duration: 1.2 });
  }

  /* Photo layers crossfade beside the origin-story steps */
  function initFarm() {
    var scene = document.querySelector('[data-scene="farm"]');
    if (!scene) {
      return;
    }
    var pin = scene.querySelector(".scene__pin");
    var items = gsap.utils.toArray(scene.querySelectorAll(".scene__stack-item"));
    var steps = scene.querySelectorAll(".scene__step");
    var sticker = scene.querySelector(".sticker");

    gsap.set(items.slice(1), { autoAlpha: 0 });
    gsap.set(steps, { autoAlpha: 0, y: 24 });

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: pin,
        pin: pin,
        start: "top top",
        end: "+=250%",
        scrub: 0.8,
        anticipatePin: 1
      }
    });
    tl.to(steps[0], { autoAlpha: 1, y: 0, duration: 0.6 }, 0)
      .to(items[1], { autoAlpha: 1, duration: 1 }, 2)
      .to(steps[0], { autoAlpha: 0, duration: 0.6 }, 2)
      .to(steps[1], { autoAlpha: 1, y: 0, duration: 0.8 }, 2.6)
      .to(items[2], { autoAlpha: 1, duration: 1 }, 5)
      .to(steps[1], { autoAlpha: 0, duration: 0.6 }, 5)
      .to(steps[2], { autoAlpha: 1, y: 0, duration: 0.8 }, 5.6)
      .fromTo(sticker,
        { scale: 0, rotation: -20 },
        { scale: 1, rotation: -4, duration: 0.7, ease: "back.out(2)" }, 6.6)
      .to({}, { duration: 1 });
  }

  /* The six varieties parade sideways past the pinned heading */
  function initVarieties() {
    var scene = document.querySelector('[data-scene="varieties"]');
    if (!scene) {
      return;
    }
    var pin = scene.querySelector(".scene__pin");
    var parade = scene.querySelector(".parade");
    var track = scene.querySelector(".parade__track");
    var items = gsap.utils.toArray(scene.querySelectorAll(".parade__item"));

    var distance = function () {
      return Math.max(0, track.scrollWidth - parade.clientWidth);
    };

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: pin,
        pin: pin,
        start: "top top",
        end: "+=200%",
        scrub: 0.6,
        anticipatePin: 1,
        invalidateOnRefresh: true
      }
    });
    /* Tiles stay visible (they are links) — only shifted, never hidden */
    tl.from(items, { y: 60, duration: 0.5, stagger: 0.1, ease: "power1.out" }, 0)
      .to(track, { x: function () { return -distance(); }, ease: "none", duration: 3 }, 0.2);
  }

  /* The van drives its round: route draws ahead, stops pop as it passes,
     with a short pause at Damme — someone gets fresh mushrooms */
  function initRoute() {
    var scene = document.querySelector('[data-scene="route"]');
    if (!scene) {
      return;
    }
    var pin = scene.querySelector(".scene__pin");
    var maskPath = scene.querySelector(".route-mask-path");
    var van = scene.querySelector(".route-van");
    var stops = scene.querySelectorAll(".route-stop");
    var sticker = scene.querySelector(".scene__sticker");
    var stats = scene.querySelectorAll(".stat-row .stat");
    var hook = scene.querySelector(".scene__hook");

    var length = maskPath.getTotalLength();
    gsap.set(maskPath, { strokeDasharray: length, strokeDashoffset: length });
    gsap.set(van, { offsetDistance: "0%" });
    gsap.set(stops, { scale: 0, transformOrigin: "center center" });
    gsap.set(stats, { autoAlpha: 0, y: 28 });
    gsap.set(hook, { autoAlpha: 0, y: 16 });

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: pin,
        pin: pin,
        start: "top top",
        end: "+=250%",
        scrub: 0.8,
        anticipatePin: 1
      }
    });
    tl.to(maskPath, { strokeDashoffset: 0, duration: 7.2, ease: "none" }, 0)
      /* leg 1: kwekerij -> Damme */
      .to(van, { offsetDistance: "50%", duration: 4, ease: "none" }, 0)
      /* pause at Damme (0.6), then leg 2: Damme -> Brugge */
      .to(van, { offsetDistance: "100%", duration: 3.4, ease: "none" }, 4.6)
      .to(stops[0], { scale: 1, duration: 0.5, ease: "back.out(2)" }, 0.1)
      .to(stops[1], { scale: 1, duration: 0.5, ease: "back.out(2)" }, 3.7)
      .to(stops[2], { scale: 1, duration: 0.5, ease: "back.out(2)" }, 7.7)
      .fromTo(sticker,
        { scale: 0, rotation: 20 },
        { scale: 1, rotation: 3, duration: 0.6, ease: "back.out(2)" }, 4)
      .to(stats, { autoAlpha: 1, y: 0, duration: 0.6, stagger: 0.25 }, 0.3)
      .to(hook, { autoAlpha: 1, y: 0, duration: 0.6 }, 7.9)
      .to({}, { duration: 0.8 });
  }

  /* Mild parallax on the dish photos — the scene itself is not pinned */
  function initPlate() {
    var scene = document.querySelector('[data-scene="plate"]');
    if (!scene) {
      return;
    }
    gsap.utils.toArray(scene.querySelectorAll(".plate-mosaic figure")).forEach(function (fig, i) {
      var drift = i % 2 ? 28 : 48;
      gsap.fromTo(fig, { y: drift }, {
        y: -drift,
        ease: "none",
        scrollTrigger: {
          trigger: scene,
          start: "top bottom",
          end: "bottom top",
          scrub: true
        }
      });
    });
  }

  /* --- Image pre-warmer --------------------------------------------------
     Pinned scenes distort lazy-loading distance heuristics, so flip a
     scene's images to eager well before it enters the viewport. */
  gsap.utils.toArray(document.querySelectorAll(".scene")).forEach(function (scene) {
    ScrollTrigger.create({
      trigger: scene,
      start: "top 150%",
      once: true,
      onEnter: function () {
        scene.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
          img.loading = "eager";
        });
      }
    });
  });

  /* Late layout changes shift the pin math — refresh when they settle */
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      ScrollTrigger.refresh();
    });
  }
  window.addEventListener("load", function () {
    ScrollTrigger.refresh();
  });
})();
