// POST /api/chat: the Athlon Rub assistant.
//
// Streams newline-delimited JSON events back to the widget:
//   {"t":"d","v":"text delta"}   {"t":"done"}   {"t":"e","v":"error message"}
//
// Credentials: ANTHROPIC_API_KEY (Vercel env, encrypted). Nothing the shopper
// types is stored or logged; only token usage is logged, for cost tracking.

import Anthropic from "@anthropic-ai/sdk";
import { SYSTEM_PROMPT } from "../lib/assistant-prompt.js";

const MODEL = "claude-opus-5-5";
const client = new Anthropic();

// Abuse limits: this endpoint spends real money.
const MAX_MESSAGES = 40;          // per conversation sent to the model
const MAX_MESSAGE_CHARS = 1500;   // per shopper message
const MAX_TOTAL_CHARS = 40000;    // whole history
const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_MAX = 30;              // requests per IP per window (best effort, per instance)
const hits = new Map();

const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || "https://athlonrub.com,https://www.athlonrub.com")
  .split(",").map((s) => s.trim()).filter(Boolean);

const json = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });

function originAllowed(request) {
  const origin = request.headers.get("origin");
  if (!origin) return false;
  try {
    const o = new URL(origin);
    const host = request.headers.get("x-forwarded-host") || request.headers.get("host");
    if (o.host === host) return true;
    if (o.hostname === "localhost" || o.hostname === "127.0.0.1") return true;
    return ALLOWED_ORIGINS.includes(o.origin);
  } catch {
    return false;
  }
}

function rateLimited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) for (const [k, v] of hits) if (now - v[v.length - 1] > RATE_WINDOW_MS) hits.delete(k);
  return recent.length > RATE_MAX;
}

// Keep only well-formed user/assistant text turns, starting with a user turn.
function cleanHistory(raw) {
  if (!Array.isArray(raw)) return null;
  const out = [];
  for (const m of raw.slice(-MAX_MESSAGES)) {
    if (!m || (m.role !== "user" && m.role !== "assistant") || typeof m.content !== "string") continue;
    const content = m.content.trim().slice(0, m.role === "user" ? MAX_MESSAGE_CHARS : 6000);
    if (!content) continue;
    if (out.length && out[out.length - 1].role === m.role) out[out.length - 1].content += "\n\n" + content;
    else out.push({ role: m.role, content });
  }
  while (out.length && out[0].role !== "user") out.shift();
  if (!out.length || out[out.length - 1].role !== "user") return null;
  let total = out.reduce((n, m) => n + m.content.length, 0);
  while (total > MAX_TOTAL_CHARS && out.length > 1) total -= out.shift().content.length;
  while (out.length && out[0].role !== "user") out.shift();
  return out.length ? out : null;
}

function pageNote(page) {
  if (!page || typeof page !== "object") return null;
  const path = typeof page.path === "string" ? page.path.slice(0, 200).replace(/[^\w\-/.]/g, "") : "";
  const title = typeof page.title === "string" ? page.title.slice(0, 160).replace(/[<>]/g, "") : "";
  if (!path) return null;
  return `Context from the website, not from the shopper: they are currently viewing "${title}" (${path}). Use it only if relevant.`;
}

export function GET() {
  return json(405, { error: "Use POST" });
}

export async function POST(request) {
  if (!originAllowed(request)) return json(403, { error: "Forbidden" });
  const ip = (request.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "local";
  if (rateLimited(ip)) return json(429, { error: "You're sending messages quickly. Give it a minute and try again." });

  let payload;
  try {
    payload = await request.json();
  } catch {
    return json(400, { error: "Invalid request" });
  }
  const history = cleanHistory(payload?.messages);
  if (!history) return json(400, { error: "Invalid conversation" });

  // Page context goes in as a mid-conversation system message after the last
  // user turn, so the cached system prompt prefix stays byte-identical.
  const note = pageNote(payload?.page);
  const messages = note ? [...history, { role: "system", content: note }] : history;

  const encoder = new TextEncoder();
  const body = new ReadableStream({
    async start(controller) {
      const send = (obj) => controller.enqueue(encoder.encode(JSON.stringify(obj) + "\n"));
      let wroteText = false;
      try {
        const stream = client.beta.messages.stream(
          {
            model: MODEL,
            max_tokens: 8000,
            betas: ["server-side-fallback-2026-07-01"],
            fallbacks: "default",
            output_config: { effort: "low" },
            system: [{ type: "text", text: SYSTEM_PROMPT, cache_control: { type: "ephemeral" } }],
            messages,
          },
          { signal: request.signal },
        );
        stream.on("text", (delta) => {
          wroteText = true;
          send({ t: "d", v: delta });
        });
        const final = await stream.finalMessage();
        if (final.stop_reason === "refusal") {
          send({ t: "d", v: (wroteText ? "\n\n" : "") + "Sorry, I can't help with that one. Ask me anything about Athlon Rub, sizing or a warm-up for your sport." });
        } else if (final.stop_reason === "max_tokens") {
          send({ t: "d", v: "\n\nThat ran long, so I stopped there. Ask me to continue if you'd like the rest." });
        }
        const u = final.usage || {};
        console.log(JSON.stringify({
          event: "assistant_reply", model: final.model, stop: final.stop_reason, turns: history.length,
          input: u.input_tokens, cache_read: u.cache_read_input_tokens, cache_write: u.cache_creation_input_tokens, output: u.output_tokens,
        }));
        send({ t: "done" });
      } catch (err) {
        let msg = "Something went wrong on our side. Please try again, or email info@athlonrub.com.";
        if (err instanceof Anthropic.RateLimitError) msg = "The assistant is busy right now. Please try again in a moment.";
        else if (err instanceof Anthropic.AuthenticationError) msg = "The assistant isn't configured yet. Please email info@athlonrub.com.";
        else if (err instanceof Anthropic.APIUserAbortError) msg = "";
        else if (err instanceof Anthropic.APIError) console.error("anthropic_error", err.status, err.message);
        else console.error("assistant_error", err?.message);
        if (msg) send({ t: "e", v: msg });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(body, {
    headers: { "Content-Type": "application/x-ndjson; charset=utf-8", "Cache-Control": "no-store", "X-Accel-Buffering": "no" },
  });
}
