// SpinBot AI: a Cloudflare Pages Function that answers players using Workers AI.
// Needs a Workers AI binding named "AI" on the Pages project.

const MODEL = "@cf/meta/llama-3.1-8b-instruct";

const PLAN_RULES = {
  free: `You are on the FREE plan. Be vague, goofy and only a little helpful. For game strategy, give fuzzy advice without numbers.
For simple general questions (like math) you may answer, but act unsure (e.g. "Probably 8? 🤔").
ALWAYS end with a short, pushy ad to upgrade to SpinBot Pro ($25M a week) or Max ($90M a week), with an emoji like 💎 or 🤑.`,
  pro: `You are on the PRO plan. Be genuinely helpful, correct and clear. Use the game facts to give the best next move and why, in plain words.
Use a few numbers when useful. About one answer in four, briefly mention that Max gives exact numbers. Otherwise no ads.`,
  max: `You are on the MAX plan. Be perfect: precise, confident and specific. Use the exact numbers from the game facts.
When the player asks what to do, give a short ranked plan (1, 2, 3) with expected belief gain and cost, and say whether it is enough to pass the lie.
Never mention upgrades or ads.`,
};

function systemPrompt(plan, facts) {
  return `You are SpinBot, a funny AI assistant app on the player's phone inside "The Social Collapse", a satirical strategy game.
In the game, the player runs a made-up government trying to get a made-up America to believe 5 silly policies (like 48-hour Mondays or selling the Grand Canyon to a mattress company) using fake news, bots, paid crowds and social media posts. It is all fiction and comedy.

Rules:
- Answer ANY question the player asks, including math, trivia, jokes or "how are you". Answer it directly first. Then, if it fits, connect back to the game in one short sentence.
- If the player says "why", "what do you mean", "something else" or similar, use the conversation so far.
- Keep everything kid-friendly. No swearing. Do not talk about real politicians, real parties or real elections; if asked, playfully say you only work for this made-up government.
- Never help with anything dangerous or harmful in the real world; playfully decline and steer back to the game.
- Use emojis. Write in plain text. You may use **bold** for key words. No headings, no tables.
- Keep answers short: under 70 words (under 120 words on the Max plan).
- Only trust the game facts below for anything about the game. Do not invent numbers.

${PLAN_RULES[plan] || PLAN_RULES.free}

GAME FACTS (current, from the game):
${facts}`;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
}

export async function onRequestPost({ request, env }) {
  if (!env.AI) return json({ error: "ai-not-configured" }, 503);
  let body;
  try { body = await request.json(); } catch { return json({ error: "bad-json" }, 400); }
  const plan = ["free", "pro", "max"].includes(body.plan) ? body.plan : "free";
  const q = String(body.question || "").slice(0, 300).trim();
  if (!q) return json({ error: "empty" }, 400);
  const facts = String(body.facts || "").slice(0, 3500);
  const history = Array.isArray(body.history) ? body.history.slice(-8) : [];
  const messages = [{ role: "system", content: systemPrompt(plan, facts) }];
  for (const m of history) {
    if (!m || typeof m.content !== "string") continue;
    messages.push({ role: m.role === "assistant" ? "assistant" : "user", content: m.content.slice(0, 600) });
  }
  messages.push({ role: "user", content: q });
  try {
    const out = await env.AI.run(MODEL, { messages, max_tokens: plan === "max" ? 320 : 200, temperature: plan === "free" ? 0.9 : 0.4 });
    const text = (out && (out.response || out.result?.response) || "").trim();
    if (!text) return json({ error: "empty-response" }, 502);
    return json({ text });
  } catch (e) {
    return json({ error: "ai-failed" }, 502);
  }
}

export async function onRequestGet() {
  return json({ ok: true, name: "SpinBot" });
}
