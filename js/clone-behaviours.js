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
