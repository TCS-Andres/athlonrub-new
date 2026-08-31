/* Clone-side behaviours. The theme's own bundles do the real work; this file
   only replaces what the Shopify platform normally provides.

   1. Trigger-position drift: scroll positions computed at load go stale when
      images finish decoding and shift the layout. GSAP's ScrollTrigger lives
      inside the theme's webpack bundle (no global), so we refresh it the way it
      listens for — a debounced resize — whenever document height changes.
   2. The theme's non-GSAP reveal (.animate-in -> .is-animated) runs off a
      scroll listener, so nudge it on the same cadence. */
(function () {
  var lastH = 0, t = 0;
  function nudge() {
    clearTimeout(t);
    t = setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
      window.dispatchEvent(new Event('scroll'));
    }, 120);
  }
  function watch() {
    if (!('ResizeObserver' in window)) return;
    new ResizeObserver(function () {
      var h = document.documentElement.scrollHeight;
      if (h === lastH) return;
      lastH = h; nudge();
    }).observe(document.body);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', watch);
  else watch();
  window.addEventListener('load', nudge);

  /* Cart / search endpoints don't exist on a static clone. Swallow those calls
     so a rejected promise doesn't abort a theme init that runs after it. */
  var LOCAL_404 = /\/cart(\.js|\/)|\/search\/suggest|\/recommendations\//;
  var _fetch = window.fetch;
  window.fetch = function (input) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    if (LOCAL_404.test(url)) {
      return Promise.resolve(new Response('{"items":[],"item_count":0,"total_price":0}',
        { status: 200, headers: { 'Content-Type': 'application/json' } }));
    }
    return _fetch.apply(this, arguments);
  };
})();

/* Mobile carousels: one slide per swipe.
   The theme configures these at slidesPerView 2.1 (categories) and 1.25
   (ingredients, reviews), so a phone shows a card and a half and every card is
   clipped at one edge. CSS cannot fix this — Swiper writes the slide widths
   inline — so retune the live instances and let Swiper recompute. */
(function () {
  var MOBILE = 767;
  function tune() {
    var mobile = window.innerWidth <= MOBILE;
    document.querySelectorAll('.swiper').forEach(function (el) {
      var sw = el.swiper;
      if (!sw || !sw.params) return;
      if (el.closest('.hero')) return;                 // hero is already 1-up
      if (sw.__athlonBase === undefined) {
        sw.__athlonBase = { spv: sw.params.slidesPerView, sb: sw.params.spaceBetween, cs: sw.params.centeredSlides };
      }
      var want = mobile ? 1 : sw.__athlonBase.spv;
      var gap = mobile ? 14 : sw.__athlonBase.sb;
      var centred = mobile ? false : sw.__athlonBase.cs;
      if (sw.params.slidesPerView === want && sw.params.spaceBetween === gap) return;
      sw.params.slidesPerView = want;
      sw.params.spaceBetween = gap;
      sw.params.centeredSlides = centred;
      try { sw.update(); } catch (e) {}
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(tune, 400); });
  else setTimeout(tune, 400);
  window.addEventListener('load', function () { setTimeout(tune, 300); });
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(tune, 200); });
})();
