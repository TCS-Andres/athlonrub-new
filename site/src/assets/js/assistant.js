/* Athlon Rub assistant widget. No dependencies.
   Talks to /api/chat (NDJSON stream), renders a safe markdown subset and
   [[product:handle]] markers as product cards whose "Add to bag" buttons reuse
   the storefront bag in main.js, and [[video:key]] / [[video:key@m:ss]] markers as
   video cards that play inline (youtube-nocookie) only after a click. The conversation lives in sessionStorage so it
   follows the shopper across pages and is gone when the tab closes. */
(() => {
  const root = document.querySelector("[data-assistant]");
  if (!root) return;
  const $ = (s) => root.querySelector(s);
  const panel = $("#assistant-panel");
  const toggle = $("[data-assistant-toggle]");
  const log = $("[data-assistant-log]");
  const form = $("[data-assistant-form]");
  const input = $("[data-assistant-input]");
  const sendBtn = $("[data-assistant-send]");
  const chips = $("[data-assistant-chips]");
  const endpoint = root.dataset.endpoint || "/api/chat";
  const KEY = "ar-assistant";

  let products = [];
  try { products = JSON.parse(document.getElementById("assistant-products").textContent); } catch {}
  const byHandle = Object.fromEntries(products.map((p) => [p.handle, p]));
  let videos = [];
  try { videos = JSON.parse(document.getElementById("assistant-videos").textContent); } catch {}
  const byVideo = Object.fromEntries(videos.map((v) => [v.key, v]));

  const GREETING = "Hey, I'm the Athlon Rub assistant. I can help you pick the right size, explain how to use it, or build a warm-up for your sport. What do you train?";
  const store = {
    get() { try { return JSON.parse(sessionStorage.getItem(KEY)) || { messages: [], open: false }; } catch { return { messages: [], open: false }; } },
    set(v) { try { sessionStorage.setItem(KEY, JSON.stringify(v)); } catch {} },
  };
  let state = store.get();
  let busy = false;
  let controller = null;

  const money = (c) => "$" + (c / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  function card(handle) {
    const p = byHandle[handle];
    if (!p) return "";
    const img = p.image || `/assets/img/products/${p.cutout}.webp`;
    return `<div class="a-card">
      <a class="a-card__img" href="/products/${p.handle}/"><img src="${img}" alt="" loading="lazy"></a>
      <div class="a-card__body">
        <a class="a-card__title" href="/products/${p.handle}/">${esc(p.title)}</a>
        <span class="a-card__meta">${esc(p.size)}</span>
        <span class="a-card__price">${money(p.price)}${p.compare_at_price ? ` <s>${money(p.compare_at_price)}</s>` : ""}</span>
      </div>
      <button type="button" class="btn btn--sm" data-add data-variant="${p.variant_id}" data-handle="${p.handle}" data-title="${esc(p.title)}" data-size="${esc(p.size)}" data-price="${p.price}" data-image="${img}">Add</button>
    </div>`;
  }

  const toSec = (t) => t.split(":").reduce((a, n) => a * 60 + Number(n), 0);
  function videoCard(key, t) {
    const v = byVideo[key];
    if (!v) return "";
    const chap = t ? (v.chapters || []).find((c) => c.t === t) : null;
    const start = chap ? toSec(chap.t) : 0;
    const href = `https://www.youtube.com/watch?v=${v.id}${start ? `&t=${start}s` : ""}`;
    const meta = chap ? `From ${chap.t}: ${esc(chap.label)}` : esc(v.who);
    return `<div class="a-video" data-video="${v.id}" data-start="${start}">
      <button type="button" class="a-video__play" aria-label="Play video: ${esc(v.title)}">
        <img src="https://i.ytimg.com/vi/${v.id}/mqdefault.jpg" alt="" loading="lazy" width="320" height="180">
        <span class="a-video__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13l11-6.5z"/></svg></span>
        <span class="a-video__len">${esc(chap ? chap.t : v.length)}</span>
      </button>
      <div class="a-video__body">
        <span class="a-video__title">${esc(v.title)}</span>
        <span class="a-video__meta">${meta} · <a href="${href}" target="_blank" rel="noopener">YouTube</a></span>
      </div>
    </div>`;
  }

  function safeHref(url) {
    if (/^\/(?!\/)[\w\-/.#?=&]*$/.test(url)) return url;
    if (/^https:\/\/(www\.)?athlonrub\.com(\/[\w\-/.#?=&]*)?$/.test(url)) return url;
    if (/^mailto:[\w.+-]+@[\w.-]+$/.test(url)) return url;
    return null;
  }

  function inline(s) {
    s = esc(s);
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, t, u) => {
      const h = safeHref(u.replace(/&amp;/g, "&"));
      return h ? `<a href="${esc(h)}">${t}</a>` : t;
    });
    s = s.replace(/\b([\w.+-]+@athlonrub\.com)\b/g, '<a href="mailto:$1">$1</a>');
    return s;
  }

  // Safe markdown subset: paragraphs, **bold**, links, "- " and "1." lists, product and video cards.
  function render(text, streaming) {
    if (streaming) text = text.replace(/\[\[[^\]]*$/, "");
    const out = [];
    let list = null;
    const close = () => { if (list) { out.push(`</${list}>`); list = null; } };
    for (const raw of text.split("\n")) {
      const line = raw.trim();
      const prod = line.match(/^\[\[product:([\w-]+)\]\]$/);
      if (prod) { close(); out.push(card(prod[1])); continue; }
      const vid = line.match(/^\[\[video:([\w-]+)(?:@(\d{1,2}:\d{2}))?\]\]$/);
      if (vid) { close(); out.push(videoCard(vid[1], vid[2])); continue; }
      const ul = line.match(/^[-*]\s+(.*)$/);
      const ol = line.match(/^(\d+)[.)]\s+(.*)$/);
      if (ul || ol) {
        const kind = ul ? "ul" : "ol";
        // A numbered list interrupted by bullets keeps counting from the model's own number.
        if (list !== kind) { close(); out.push(kind === "ol" && ol[1] !== "1" ? `<ol start="${Number(ol[1])}">` : `<${kind}>`); list = kind; }
        out.push(`<li>${inline(ul ? ul[1] : ol[2])}</li>`);
        continue;
      }
      close();
      if (line) out.push(`<p>${inline(line)}</p>`);
    }
    close();
    return out.join("");
  }

  function bubble(role, html, extra = "") {
    const el = document.createElement("div");
    el.className = `a-msg a-msg--${role} ${extra}`.trim();
    el.innerHTML = html;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  function draw() {
    log.innerHTML = "";
    bubble("bot", render(GREETING));
    // Suggestions sit right under the greeting until the first message.
    if (!state.messages.length) log.appendChild(chips);
    for (const m of state.messages) bubble(m.role === "user" ? "user" : "bot", m.role === "user" ? `<p>${esc(m.content)}</p>` : render(m.content));
    chips.hidden = state.messages.length > 0;
  }

  function setOpen(open) {
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    root.classList.toggle("is-open", open);
    state.open = open; store.set(state);
    if (open) { autosize(); log.scrollTop = log.scrollHeight; setTimeout(() => input.focus(), 30); }
  }

  async function send(text) {
    text = text.trim();
    if (!text || busy) return;
    busy = true; sendBtn.disabled = true;
    state.messages.push({ role: "user", content: text.slice(0, 1500) });
    store.set(state);
    chips.hidden = true;
    bubble("user", `<p>${esc(text)}</p>`);
    input.value = ""; autosize();
    const el = bubble("bot", '<span class="a-typing" aria-label="Assistant is typing"><i></i><i></i><i></i></span>');
    let reply = "", raf = 0, error = "";
    const paint = () => { raf = 0; el.innerHTML = render(reply, true) || el.innerHTML; log.scrollTop = log.scrollHeight; };
    controller = new AbortController();
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: state.messages, page: { path: location.pathname, title: document.title } }),
        signal: controller.signal,
      });
      if (!res.ok || !res.body) {
        let msg = "Something went wrong. Please try again.";
        try { msg = (await res.json()).error || msg; } catch {}
        throw new Error(msg);
      }
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let i;
        while ((i = buf.indexOf("\n")) >= 0) {
          const line = buf.slice(0, i); buf = buf.slice(i + 1);
          if (!line) continue;
          const ev = JSON.parse(line);
          if (ev.t === "d") { reply += ev.v; if (!raf) raf = requestAnimationFrame(paint); }
          else if (ev.t === "e") error = ev.v;
        }
      }
    } catch (e) {
      if (e.name !== "AbortError") error = e.message || "Connection lost. Please try again.";
    }
    cancelAnimationFrame(raf);
    if (reply) {
      el.innerHTML = render(reply);
      state.messages.push({ role: "assistant", content: reply });
    } else {
      el.remove();
      state.messages.pop(); // let the shopper retry the same question
    }
    if (error) bubble("bot", `<p>${esc(error)}</p>`, "a-msg--error");
    store.set(state);
    busy = false; sendBtn.disabled = false; controller = null;
    log.scrollTop = log.scrollHeight;
    input.focus();
  }

  // Grow with the message up to 5 lines; only then allow scrolling.
  function autosize() {
    input.style.height = "40px";
    const h = input.value ? Math.min(input.scrollHeight, 128) : 40;
    input.style.height = h + "px";
    input.style.overflowY = input.scrollHeight > 128 ? "auto" : "hidden";
  }

  toggle.addEventListener("click", () => setOpen(panel.hidden));
  $("[data-assistant-close]").addEventListener("click", () => { setOpen(false); toggle.focus(); });
  $("[data-assistant-reset]").addEventListener("click", () => {
    controller?.abort();
    state = { messages: [], open: true }; store.set(state); draw(); input.focus();
  });
  root.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) { setOpen(false); toggle.focus(); } });
  form.addEventListener("submit", (e) => { e.preventDefault(); send(input.value); });
  input.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(input.value); } });
  input.addEventListener("input", autosize);
  // Video cards: swap the thumbnail for the player only when the shopper asks for it.
  log.addEventListener("click", (e) => {
    const b = e.target.closest(".a-video__play");
    if (!b) return;
    const box = b.closest("[data-video]");
    const f = document.createElement("iframe");
    f.src = `https://www.youtube-nocookie.com/embed/${box.dataset.video}?autoplay=1&rel=0&playsinline=1${Number(box.dataset.start) ? `&start=${box.dataset.start}` : ""}`;
    f.title = b.getAttribute("aria-label").replace(/^Play video: /, "");
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    f.className = "a-video__frame";
    b.replaceWith(f);
  });
  chips.addEventListener("click", (e) => { const b = e.target.closest("[data-prompt]"); if (b) send(b.dataset.prompt); });
  // "Ask" links anywhere on the site: <a data-ask="Build me a warm-up for soccer">
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-ask]");
    if (!a) return;
    e.preventDefault(); setOpen(true); send(a.dataset.ask);
  });

  draw();
  if (state.open && window.matchMedia("(min-width: 640px)").matches) setOpen(true);
})();
