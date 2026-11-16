/* Athlon Rub v3 storefront behaviour. No dependencies.
   Preview bag: stored locally, checkout goes to athlonrub.com through a Shopify
   cart permalink (/cart/{variant}:{qty},...), so real orders work from the preview.
   Shopify port: swap Bag for /cart/add.js, /cart/change.js and /cart.js. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const money = (c) => "$" + (c / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const store = {
    get(k, f) { try { return JSON.parse(localStorage.getItem(k)) ?? f; } catch { return f; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  const STORE_URL = "https://athlonrub.com";

  /* Announcement rotation */
  const ann = $$("[data-announce] .announce__item");
  if (ann.length > 1 && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let i = 0;
    setInterval(() => {
      ann[i].classList.remove("is-active"); ann[i].setAttribute("aria-hidden", "true");
      i = (i + 1) % ann.length;
      ann[i].classList.add("is-active"); ann[i].removeAttribute("aria-hidden");
    }, 4500);
  }

  /* Drawers */
  const overlay = $("[data-overlay]");
  let lastFocus = null;
  function openDrawer(name) {
    const d = $(`[data-drawer="${name}"]`);
    if (!d) return;
    lastFocus = document.activeElement;
    $$("[data-drawer].is-open").forEach((x) => closeDrawer(x, false));
    d.classList.add("is-open"); d.setAttribute("aria-hidden", "false");
    overlay.classList.add("is-open");
    document.body.style.overflow = "hidden";
    $$(`[data-open="${name}"]`).forEach((b) => b.setAttribute("aria-expanded", "true"));
    setTimeout(() => (d.querySelector("[data-close]") || d).focus(), 50);
  }
  function closeDrawer(d, restore = true) {
    d.classList.remove("is-open"); d.setAttribute("aria-hidden", "true");
    $$(`[data-open="${d.dataset.drawer}"]`).forEach((b) => b.setAttribute("aria-expanded", "false"));
    if (!$("[data-drawer].is-open")) { overlay.classList.remove("is-open"); document.body.style.overflow = ""; }
    if (restore && lastFocus) lastFocus.focus();
  }
  document.addEventListener("click", (e) => {
    const o = e.target.closest("[data-open]");
    if (o) { e.preventDefault(); openDrawer(o.dataset.open); return; }
    const c = e.target.closest("[data-close]");
    if (c) closeDrawer(c.closest("[data-drawer]"));
  });
  overlay?.addEventListener("click", () => $$("[data-drawer].is-open").forEach((d) => closeDrawer(d)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") $$("[data-drawer].is-open").forEach((d) => closeDrawer(d));
    if (e.key === "Tab") {
      const d = $("[data-drawer].is-open");
      if (!d) return;
      const f = $$("a[href], button:not([disabled]), input, summary, [tabindex]:not([tabindex='-1'])", d).filter((x) => x.offsetParent !== null);
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* Bag */
  const Bag = {
    items: store.get("ar-bag", []),
    save() { store.set("ar-bag", this.items); render(); },
    add(item, qty = 1) {
      const ex = this.items.find((i) => i.variant === item.variant);
      if (ex) ex.qty = Math.min(ex.qty + qty, 99); else this.items.push({ ...item, qty });
      this.save();
    },
    set(variant, qty) {
      this.items = this.items.map((i) => (i.variant === variant ? { ...i, qty } : i)).filter((i) => i.qty > 0);
      this.save();
    },
    count() { return this.items.reduce((n, i) => n + i.qty, 0); },
    total() { return this.items.reduce((n, i) => n + i.qty * i.price, 0); },
    permalink() { return `${STORE_URL}/cart/` + this.items.map((i) => `${i.variant}:${i.qty}`).join(","); },
  };

  const lines = $("[data-cart-lines]");
  function render() {
    const n = Bag.count();
    $$("[data-cart-count]").forEach((el) => { el.textContent = n; el.dataset.count = n; });
    const txt = $("[data-cart-count-text]"); if (txt) txt.textContent = n ? `(${n})` : "";
    if (!lines) return;
    lines.innerHTML = Bag.items.map((i) => `
      <li class="cart-line">
        <div class="cart-line__img"><img src="${i.image}" alt="" width="40" height="76"></div>
        <div>
          <p class="cart-line__title">${i.title}</p>
          <p class="cart-line__meta">${i.size}</p>
          <div class="qty" role="group" aria-label="Quantity for ${i.title}">
            <button type="button" data-qty="${i.variant}" data-delta="-1" aria-label="Decrease">−</button>
            <span>${i.qty}</span>
            <button type="button" data-qty="${i.variant}" data-delta="1" aria-label="Increase">+</button>
          </div>
        </div>
        <p class="cart-line__price">${money(i.price * i.qty)}</p>
      </li>`).join("");
    $("[data-cart-empty]").hidden = n > 0;
    $("[data-cart-foot]").hidden = n === 0;
    $("[data-cart-subtotal]").textContent = money(Bag.total());
    const co = $("[data-checkout]"); if (co) co.href = n ? Bag.permalink() : `${STORE_URL}/cart`;
    const meter = $("[data-ship-meter]");
    if (meter) {
      const t = Number(meter.dataset.threshold), tot = Bag.total();
      $("[data-ship-fill]").style.width = Math.min(100, (tot / t) * 100) + "%";
      $("[data-ship-text]").innerHTML = tot >= t
        ? "<strong>You have unlocked free shipping.</strong>"
        : n ? `You are <strong>${money(t - tot)}</strong> away from free shipping.` : `Free shipping on orders over ${money(t).replace(".00", "")}`;
    }
  }
  lines?.addEventListener("click", (e) => {
    const b = e.target.closest("[data-qty]"); if (!b) return;
    const v = Number(b.dataset.qty), it = Bag.items.find((i) => i.variant === v);
    if (it) Bag.set(v, it.qty + Number(b.dataset.delta));
  });

  const toast = $("[data-toast]");
  let toastT;
  function say(msg) {
    if (!toast) return;
    toast.textContent = msg; toast.classList.add("is-visible");
    clearTimeout(toastT); toastT = setTimeout(() => toast.classList.remove("is-visible"), 2400);
  }

  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-add]"); if (!b) return;
    const qtyInput = b.closest("[data-buy]")?.querySelector("[data-qty-input]");
    const qty = Math.max(1, Number(qtyInput?.value || 1));
    Bag.add({ variant: Number(b.dataset.variant), handle: b.dataset.handle, title: b.dataset.title, size: b.dataset.size, price: Number(b.dataset.price), image: b.dataset.image }, qty);
    say(`${b.dataset.title} added to your bag`);
    openDrawer("cart");
  });
  render();

  /* Quantity stepper on product page */
  $$("[data-stepper]").forEach((g) => {
    const input = $("[data-qty-input]", g);
    g.addEventListener("click", (e) => {
      const b = e.target.closest("[data-step]"); if (!b) return;
      input.value = Math.max(1, Math.min(99, Number(input.value || 1) + Number(b.dataset.step)));
    });
  });

  /* Product gallery */
  $$("[data-gallery]").forEach((g) => {
    const slides = $$(".gallery__slide", g), thumbs = $$(".gallery__thumb", g);
    thumbs.forEach((t, i) => t.addEventListener("click", () => {
      slides.forEach((s, j) => s.classList.toggle("is-active", i === j));
      thumbs.forEach((x, j) => x.setAttribute("aria-current", i === j ? "true" : "false"));
    }));
  });

  /* Sticky buy bar */
  const buy = $("[data-buy]"), sticky = $("[data-sticky-buy]");
  if (buy && sticky && "IntersectionObserver" in window) {
    new IntersectionObserver(([en]) => sticky.classList.toggle("is-visible", !en.isIntersecting && en.boundingClientRect.top < 0)).observe(buy);
  }

  /* Collection filters */
  $$("[data-filters]").forEach((bar) => {
    const grid = $(bar.dataset.filters);
    bar.addEventListener("click", (e) => {
      const b = e.target.closest("[data-filter]"); if (!b) return;
      $$("[data-filter]", bar).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      $$("[data-type]", grid).forEach((c) => { c.hidden = b.dataset.filter !== "all" && c.dataset.type !== b.dataset.filter; });
    });
  });
  if (location.hash === "#bundles") $('[data-filter="bundle"]')?.click();

  /* Newsletter (preview): no data leaves the page until Shopify customer signup is wired */
  $$("[data-signup]").forEach((f) => f.addEventListener("submit", (e) => {
    e.preventDefault();
    const em = f.querySelector("input[type=email]"), msg = f.querySelector("[data-signup-msg]");
    if (!em.value || !em.checkValidity()) { msg.textContent = "Enter a valid email address."; em.focus(); return; }
    msg.textContent = "Thanks. Signup goes live with the Shopify store.";
    f.reset();
  }));

  /* QA screenshot mode (?shot): everything visible, images eager */
  const SHOT = new URLSearchParams(location.search).has("shot");
  if (SHOT) $$("img[loading=lazy]").forEach((i) => (i.loading = "eager"));

  /* Reveal on scroll */
  const rev = $$("[data-reveal]");
  if (!SHOT && "IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const io = new IntersectionObserver((ens) => ens.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rev.forEach((el) => io.observe(el));
  } else rev.forEach((el) => el.classList.add("is-in"));
})();
