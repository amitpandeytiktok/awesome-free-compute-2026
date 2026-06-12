# 🪙 The Free Token-Maxxing Guide (2026)

> A messiah-guide to extracting the **maximum** amount of frontier-model usage —
> tokens *and* compute — for **$0**, **legitimately**.

**Last verified: June 2026.** Free tiers, models, and limits change weekly. Every
number below was cross-checked against an official pricing/docs page or the
auto-generated [`cheahjs/free-llm-api-resources`](https://github.com/cheahjs/free-llm-api-resources)
list; where a provider hides exact caps behind a login or a JS page, it's flagged.

> [!IMPORTANT]
> **Token-maxx, don't token-cheat.** Everything here uses tiers you genuinely
> qualify for. Creating fake/duplicate accounts, cycling cards to re-trigger
> trials, scraping/sharing keys, or scripting around rate limits violates
> provider ToS, gets you banned, and **risks killing the free programs for
> everyone**. The sustainable move is *aggregating many legit sources*, not
> *cheating one source many times*. See [§9](#9-legit-vs-risky).

---

## Contents

- [TL;DR — the messiah stack](#tldr--the-messiah-stack)
- [1. What "frontier" means in 2026](#1-what-frontier-means-in-2026)
- [2. Free frontier in the browser (chat apps)](#2-free-frontier-in-the-browser-chat-apps)
- [3. Free LLM APIs — the token buffet](#3-free-llm-apis--the-token-buffet)
- [4. Free coding assistants + the BYO-key power move](#4-free-coding-assistants--the-byo-key-power-move)
- [5. Trial credits — one-time fuel](#5-trial-credits--one-time-fuel)
- [6. Self-host OSS for "unlimited" tokens](#6-self-host-oss-for-unlimited-tokens)
- [7. The orchestration layer (wire it together)](#7-the-orchestration-layer-wire-it-together)
- [8. Quota-stretching: caching & batching](#8-quota-stretching-caching--batching)
- [9. Legit vs risky](#9-legit-vs-risky)
- [10. The stacking playbook](#10-the-stacking-playbook)
- [11. The China play 🇨🇳 — cheapest tokens + free media](#11-the-china-play----cheapest-tokens--free-media)
  - [11.1 "100M tokens for ~$1" — the cache-hit trick](#111-100m-tokens-for-1--the-cache-hit-trick)
  - [11.2 Ultra-cheap "coding plan" subscriptions](#112-ultra-cheap-coding-plan-subscriptions)
  - [11.3 Free Chinese model tiers (text + multimodal)](#113-free-chinese-model-tiers-text--multimodal)
  - [11.4 Free image generation](#114-free-image-generation)
  - [11.5 Free video generation (for music videos)](#115-free-video-generation-for-music-videos)
  - [11.6 China caveats](#116-china-caveats)
- [Living lists to bookmark](#living-lists-to-bookmark)
- [Sources](#sources)

---

## TL;DR — the messiah stack

For a solo creator / power user who wants frontier quality at $0:

| Need | Use | Why |
|---|---|---|
| 🧠 **Best free frontier brain** | **Google AI Studio** (browser) + free Gemini API key | The *only* place you get true frontier (Gemini 3 Pro / 3.1 Pro) free, ~1M context, multimodal. Price = your data trains Google. |
| ⚡ **Fastest free tokens** | **Cerebras** (`gpt-oss-120b` ~3000 tok/s) | 1,000,000 tokens/day free, blazing fast. |
| 💻 **Free coding** | **Gemini Code Assist** (~180k completions/mo) + **Gemini CLI** (1,000 agent req/day) | ~90× Copilot Free's completion cap. |
| 🤖 **Free agentic coding** | **Cline / Aider** + a free key (Gemini-free → Groq-free → OpenRouter `:free`) | Model-agnostic OSS agent on free backends = $0. |
| 🔁 **Recurring free GPU** | **Modal** ($5/mo free, **$30/mo** with a card on file) | Best standing serverless-GPU allowance; resets monthly. |
| ♾️ **Truly unlimited** | **Local** (Ollama / LM Studio on Apple Silicon) | Bounded only by your hardware, ToS-clean, private. |
| 🧰 **Glue** | **LiteLLM** or **OpenRouter** as one endpoint, fallback chain | Route local → free → `:free` → cheap-paid automatically. |
| 🇨🇳 **Near-free tokens** | **DeepSeek / Doubao** cache-hit input | ~**100–350M cached input tokens per $1** ([§11.1](#111-100m-tokens-for-1--the-cache-hit-trick)). |
| 🎬 **Free commercial video/image** | **Open weights**: Wan 2.2 / CogVideoX-2B / Kolors on free GPU | No watermark, commercial-OK, $0 ([§11.5](#115-free-video-generation-for-music-videos)). |

**One-liner:** *Chat & long-context → AI Studio. Coding → Gemini Code Assist + CLI.
Agentic/overflow → Cline with Gemini-free + Groq-free + OpenRouter `:free`. Bulk →
local models. Glue it with LiteLLM and lean on prompt caching + batch APIs.*

---

## 1. What "frontier" means in 2026

As of mid-2026, the frontier tier is roughly **GPT-5.5 / Gemini 3.1 Pro / Claude
Opus 4.8**. Free tiers usually hand you the *mid* model of the current generation
(Flash / mini / Sonnet / Haiku) with limited or metered access to the very top
model. The two big exceptions where you can touch a genuine frontier model for
free: **Google AI Studio** (Gemini 3 Pro / 3.1 Pro in the browser) and, briefly,
**trial credits / student offers**.

---

## 2. Free frontier in the browser (chat apps)

The zero-setup layer. Most give a frontier-ish model with **dynamic, unpublished
caps** that silently downgrade you after a threshold.

| App | Free model | Free limit | Notes |
|---|---|---|---|
| **Google AI Studio** 🥇 | **Gemini 3 Pro / 3.1 Pro** (frontier) | Very generous browser use; "rate limits may apply" | Best free frontier. Free-tier data **used for training**. |
| **Gemini app** | Gemini 3 Flash (limited 3 Pro / Deep Think) | Daily caps (unpublished); ~2-month AI Pro trial offered | — |
| **ChatGPT Free** | GPT-5.x ("auto"), downgrades to mini after cap | Dynamic, unpublished; **now shows ads** | Keep threads short to avoid re-sending context. |
| **Claude.ai Free** | **Sonnet 4.5** (Opus is paid) | Rolling ~5-hr window cap (unpublished) | Web search included. |
| **Microsoft Copilot** | GPT-5-class | Generous; light peak throttling | Best free "GPT-5 chat" fallback. |
| **Perplexity Free** | Frontier in "Pro Search" | Unlimited quick + a few Pro searches/day (~3–5, unverified) | Best for **cited** web answers. |
| **Duck.ai** (DuckDuckGo) | GPT-5 mini, Claude Haiku 4.5, Llama 4 Scout, gpt-oss-120b | Free, rate-limited | **Private, no account.** |
| **DeepSeek / Qwen / Kimi / Le Chat** | V3.x/R1 · Qwen3 · K2 · Mistral-large-class | Generous free | Strongest "generous free" non-US chat for bulk work. |
| **Meta AI** | Llama 4 | Free (WhatsApp/IG/web) | Region-limited. |

> **Maximize:** do long-context, multimodal, and reasoning-heavy work in **AI
> Studio** instead of burning capped ChatGPT/Claude messages. Caps on rows without
> a published number are approximate.

---

## 3. Free LLM APIs — the token buffet

Perpetual (or near-perpetual) free API tiers. Numbers verified against
`cheahjs/free-llm-api-resources` and provider docs, June 2026.

| Provider | Top free model(s) | Free limit | Card? | Notes |
|---|---|---|---|---|
| **Google AI Studio / Gemini API** 🥇 | Gemini 3.5 Flash, 3 Flash, 2.5 Flash | 250k TPM · 20 RPD · 5 RPM (3.1 Flash-Lite: **500 RPD**); Gemma 3: **14,400 RPD** | No | Best free access to a top closed model. Data trains Google. |
| **Cerebras** ⚡ | `gpt-oss-120b`, Llama 3.1 8B | 30 RPM · 60k TPM · **1,000,000 tokens/day** | No | ~3000 tok/s — fastest free tokens. |
| **Groq** ⚡ | Llama 3.3 70B, gpt-oss-120b, Qwen3-32B | Per-model, e.g. Llama 3.3 70B = 1,000 RPD; Llama 3.1 8B = **14,400 RPD** | No | Very fast; verify caps at `/settings/limits`. |
| **OpenRouter** | Many `:free` slugs (gpt-oss-120b, Qwen3-Coder, GLM-4.5-Air, Kimi, Nemotron 3…) | 20 RPM · 50 RPD (**→ 1,000 RPD** with a $10 lifetime top-up); shared quota | No (for 50/day) | Best rotating buffet + built-in fallbacks. |
| **Mistral La Plateforme** | Open + proprietary Mistral | 1 req/s · 500k TPM · **1,000,000,000 tokens/month** | Phone | Free "Experiment" plan **requires opting into data training**. |
| **Cloudflare Workers AI** | Llama 3.3 70B, gpt-oss-120b, GLM-4.7-flash, Kimi K2.6 | **10,000 neurons/day** | No | Great background trickle; 70B outputs burn neurons fast. |
| **Cohere** | command-a-* (incl. reasoning/vision) | 20 RPM · **1,000 requests/month** (shared) | No | Genuinely free eval keys, low cap. |
| **GitHub Models** | GPT-5, o3/o4-mini, Grok 3, DeepSeek-R1, Llama 4, Phi-4 | Tiny, tied to Copilot tier (Free ≈ 15 RPM/150 RPD) | No | Best *legal* way to sample closed top models. |
| **NVIDIA NIM** | Nemotron, Llama, many open | 40 RPM | Phone | Context-limited; good for POCs. |
| **HF Inference Providers** | Routes to Groq/Cerebras/Together/etc. | **$0.10/mo** credits (PRO $2/mo) | No | Universal fallback, tiny budget. |
| **Vercel AI Gateway** | Routes to many providers | **$5/mo** | No | One key, many models. |

**Best picks:** Gemini (quality) → Cerebras (speed + volume) → Groq (speed) →
OpenRouter `:free` (variety/overflow) → Cloudflare (automation trickle).

**Not really free in 2026:** Together (min $5 purchase), DeepSeek direct
(balance-based), Fireworks (payment profile). Treat as cheap-paid, not free.

---

## 4. Free coding assistants + the BYO-key power move

| Tool | Free model | Free limit | Notes |
|---|---|---|---|
| **Gemini Code Assist** (individual) 🥇 | Gemini 2.5/3-class, 128k context | **~180,000 completions/month** ("90× other free assistants") | Most generous completions by far. VS Code + JetBrains. |
| **Gemini CLI** | Gemini 3 (Flash+Pro), 1M context | **60 RPM · 1,000 agent requests/day** (personal account) | Open-source (Apache-2.0). |
| **GitHub Copilot Free** | GPT-5-class / Claude / Gemini (shared) | **2,000 completions/mo** + limited chat/agent | Agent mode, MCP, Copilot CLI. ⚠️ New Pro/Pro+/Max/**Student** signups **paused Apr 20 2026**. |
| **Cline** / **Roo Code** (OSS) | **Any** (BYO key) | Unlimited if you BYO a free key | Gemini, OpenRouter 200+, Groq/Cerebras, local Ollama/LM Studio. |
| **Aider** (OSS CLI) | **Any** (BYO key) | Unlimited (BYO) | Great with Gemini-free / DeepSeek. |
| **Continue.dev** (OSS) | **Any** (BYO key) | Free (BYO) | ⚠️ Repo now **read-only / maintenance-freeze** — prefer Cline/Roo. |
| **Zed** | Limited hosted + **BYO key** | Limited free hosted prompts; unlimited w/ own key | Top models are Pro-only. |

### The power move: bring-your-own free key → $0 agentic coding

Run an OSS agent (**Cline / Aider / Roo / Gemini CLI**) and point it at a **free
API tier**:

1. **Quality:** Gemini free key — [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
   Free "Gemini 3-class"; CLI gives 60 RPM / 1,000 req/day. *(Prompts may train Google.)*
2. **Speed:** Groq free — fast Llama / gpt-oss / Qwen.
3. **Overflow:** OpenRouter `:free` — a free DeepSeek/Qwen/Llama variant when the others cap out.

**Recommended free stack:** **Cline (or Aider) + Gemini-free**, with **Groq-free**
secondary and **OpenRouter `:free`** as overflow. Add MCP servers for tools.

---

## 5. Trial credits — one-time fuel

Use once, on one real account, as intended. (From `cheahjs/free-llm-api-resources`.)

| Provider | Free credit | Notes |
|---|---|---|
| **Modal** | **$5/mo** free, **$30/mo** with a payment method on file | Best recurring serverless GPU/CPU; pay-per-second. |
| **Baseten** | $30 | Pay by compute time. |
| **NLP Cloud** | $15 | Phone verification. |
| **AI21** / **Upstage** | $10 / 3 months each | Jamba · Solar models. |
| **SambaNova Cloud** | $5 / 3 months | DeepSeek V3.x, Llama 4 Maverick, gpt-oss-120b. (A no-card free tier ~20 req/day/model also exists.) |
| **Scaleway** | 1,000,000 free tokens | Llama 3.3 70B, Qwen3, Mistral, gpt-oss-120b. |
| **Alibaba Model Studio** (Intl) | 1,000,000 tokens/model | Qwen open + proprietary; activate Intl/Singapore mode. |
| **Inference.net** | $1 (+$25 on survey) | Various open models. |
| **Fireworks / Nebius / Hyperbolic** | $1 each | Various open models. |
| **Novita** | $0.50 for 1 year | Various open models. |

> For **cloud credits** ($300 GCP, $200 Azure, AWS's new $100+$100, Oracle $300),
> and **student/startup** programs (GitHub Student Pack, Google for Startups up to
> $350k, AWS Activate up to $200k), see the main
> [README §6](./README.md#6-trial-credits--student--startup-programs).

---

## 6. Self-host OSS for "unlimited" tokens

When you run the model, tokens are free (bounded by hardware). All of these speak
the **OpenAI-compatible API**, so they slot behind the same client code / hub.

| Runtime | Endpoint | Best for |
|---|---|---|
| **Ollama** | `http://localhost:11434/v1` | Easiest local; Mac-native. |
| **LM Studio** | `http://localhost:1234/v1` | GUI + Responses API (works with Codex). |
| **llama.cpp** | `llama-server` | Lightweight C/C++, GGUF quant on CPU/GPU. |
| **vLLM** | `vllm serve <model>` | High-throughput serving, prefix caching; runs on Apple Silicon. |

**Hardware reality:** Apple Silicon **unified memory** lets an M-series Mac address
lots of RAM as effective "VRAM," which is why it's the popular local-LLM choice. A
16–24 GB machine comfortably runs 8–14B models (Llama 3 8B, Qwen3-14B,
DeepSeek-R1-Distill); 32B+ needs more.

**Free GPU to host bigger models / media:** Hugging Face Spaces (free high-VRAM
GPU time via ZeroGPU), Kaggle (30 GPU-hrs/week), Modal ($30/mo). Full details and
the GPU→model map are in the main [README §2–§3](./README.md#2-free-gpu-notebooks--sessions).
Oracle's **Always-Free ARM** (4 OCPU / 24 GB) makes a perfect 24/7 CPU LLM backend
via `llama.cpp` (8B at ~5–10 tok/s, permanent).

---

## 7. The orchestration layer (wire it together)

The whole stack is glued by the **OpenAI Chat Completions schema** — change only
`base_url` + `api_key` to repoint any client. Pick one hub:

- **OpenRouter** (hosted, zero-ops): `:free` models, a `models: [...]` array for
  automatic fallback, and `provider` routing (`sort`, `data_collection:"deny"`, ZDR).
- **LiteLLM** (self-hosted proxy, `http://0.0.0.0:4000`): unify 100+ providers,
  **load-balance multiple free keys *you legitimately own*** under one `model_name`,
  fallback across model groups, and **hard-enforce RPM** (`enforce_model_rate_limits`,
  + Redis for multi-instance) so you degrade gracefully instead of getting 429-banned.

```
   Apps / coding tools (Aider · Cline · Roo · your scripts)   ── all speak OpenAI API
                              │
                              ▼
          ┌──────────────────────────────────────────┐
          │  ONE HUB:  LiteLLM proxy  — or — OpenRouter │
          └───────┬───────────────────────┬────────────┘
   routing /      │                       │   :free models, provider routing,
   fallback /     │                       │   model-array fallbacks
   load-balance   ▼                       ▼
   ┌────────────┬───────────────┬───────────────┬──────────────────────────┐
   │ Free tiers │ Trial-credit  │ Your OTHER    │ LOCAL (unlimited):        │
   │ (Gemini,   │ providers     │ legit free    │ Ollama, LM Studio,        │
   │ Groq, …)   │ (Modal, …)    │ keys (yours)  │ llama.cpp, vLLM           │
   └────────────┴───────────────┴───────────────┴──────────────────────────┘
```

**Tiered fallback chain (cheapest-first):** local model → free hosted tier
(Groq/Gemini/Cerebras) → OpenRouter `:free` → small paid model as last resort.

---

## 8. Quota-stretching: caching & batching

Make each free token go further:

- **Prompt caching** (reuse a fixed prefix cheaply):
  - **Anthropic** — `cache_control: {type:"ephemeral"}`; **cache reads ≈10% of base input** (~90% off).
  - **Gemini** — *implicit* caching auto-on for 2.5+; *explicit* via `caches.create()` (guaranteed savings). Put stable content **at the start** of the prompt.
  - **DeepSeek** — disk caching **on by default**, no code changes (`prompt_cache_hit_tokens` in usage).
- **Batch APIs (50% off + higher limits)** for non-interactive jobs: **OpenAI Batch**
  (24-hr turnaround) and **Anthropic Message Batches** (most finish < 1 hr).
- **Trim & stabilize:** keep a stable system-prompt prefix (maximizes cache hits +
  batch efficiency), summarize old turns, pin `num_ctx` locally to avoid silent
  truncation/OOM.

---

## 9. Legit vs risky

### ✅ Clearly legit & sustainable
Official free tiers (AI Studio, Groq, Cerebras, Cohere, NIM, Mistral, Cloudflare,
GitHub Models) · trial credits used as intended on one real account · OpenRouter
`:free` · OSS self-hosting · student/startup programs you actually qualify for.

> **Legit ≠ private.** Many free tiers **train on your inputs** (Google AI Studio
> free, Mistral's free Experiment plan, etc.). **Never paste secrets, proprietary,
> or sensitive code into a free tier.**

### ⚠️ Grey / risky — flagged, **not** endorsed (no how-to)

| Practice | Why it's risky | Consequence |
|---|---|---|
| **gpt4free-style reverse proxies** | Scrape/automate vendor chatbots (HAR/cookies) — violates source ToS | Constant breakage, takedowns, no privacy/reliability |
| **Multi-accounting / fake accounts** | Circumvents the per-account caps that keep free tiers alive | Bans/termination |
| **Card cycling to re-trigger trials** | Defeats trial eligibility; crosses payment terms | Payment bans, possible fraud liability |
| **Sharing / scraping API keys** | Keys are credentials; unauthorized use | Revocation; owner eats the bill; legal exposure |
| **Bypassing rate limits** | Contravenes technical controls | 429 → hard ban; **collateral damage to the whole community** |

---

## 10. The stacking playbook

A realistic $0 routine for a solo AI creator:

1. **Daily driver:** Google **AI Studio** for ideation/long-context/multimodal;
   **Gemini Code Assist + CLI** for coding.
2. **Agentic coding:** **Cline/Aider** → Gemini-free → Groq-free → OpenRouter `:free`,
   behind **LiteLLM** with per-key RPM caps + fallbacks.
3. **Bulk / iterative grunt work:** **local** Ollama/LM Studio (lint fixes, drafts).
4. **Speed bursts:** **Cerebras** (1M tok/day) / **Groq**.
5. **GPU jobs (media, fine-tunes):** **Modal** ($30/mo) for serverless bursts;
   **Kaggle** (30 h/wk) for long headless runs; **Oracle A1** as a free 24/7 backend.
6. **Stretch quotas:** prompt caching (~90% off) + batch APIs (50% off) on stable prompts.
7. **One-time fuel:** spend trial credits (Modal/Baseten/SambaNova/Scaleway…) on
   real deployable workloads; claim **GitHub Student Pack** / startup programs if eligible.
8. **Hygiene:** set budgets, disable auto-recharge, delete idle GPU/volumes, and
   never feed secrets to a training-on free tier.

---

## 11. The China play 🇨🇳 — cheapest tokens + free media

Chinese labs are in an all-out price/feature war, which is *fantastic* for a
token-maxxer. Three things stand out: **near-free token pricing** via context
caching, **flat coding subscriptions** at a fraction of Claude's price, and
**genuinely free image/video** (especially via **open weights**). The trade-offs
— data jurisdiction, watermarks, ToS — are real; see [§11.6](#116-china-caveats).

> **Versions move fast.** As of June 2026 the current models are GLM-5.1 / 4.7,
> Kimi K2.7, MiniMax M3, DeepSeek V4, Kling 3.0, Hailuo 2.3, Seedance 2.0,
> CogVideoX-3, Wan 2.2, HunyuanVideo 1.5. Re-verify names before relying on them.

### 11.1 "100M tokens for ~$1" — the cache-hit trick

The viral claim is **real, but only for *input* tokens served from cache** — not
output. The mechanism is **context caching**: a provider bills a repeated prompt
prefix (system prompt, long doc, codebase, chat history) at ~1–2% of the normal
price. Agentic coding naturally creates this, because every tool-call resends the
same growing context. *(DeepSeek prices verified on its official pricing page,
2026-06-12; the prefix cache is automatic — it only matches an identical prefix
from token 0.)*

| Provider · model | Cache-**hit** input /1M | Cache-**miss** input /1M | Output /1M | **$1 buys (cache-hit input)** |
|---|---:|---:|---:|---:|
| **DeepSeek V4 Flash** | **$0.0028** | $0.14 | $0.28 | **≈ 357M tokens** |
| **DeepSeek V4 Pro** | **$0.003625** | $0.435 | $0.87 | **≈ 276M tokens** |
| **ByteDance Doubao** seed-1.6-flash | ≈$0.0042 (¥0.03) | ≈$0.021 (¥0.15) | ≈$0.21 (¥1.50) | **≈ 239M tokens** |
| Doubao seed-1.6-flash **batch** | ≈$0.0042 | ≈$0.0105 (¥0.075) | ≈$0.10 | input ≈ 96M / $1 |
| DeepSeek (2024 cache launch price) | $0.014 | $0.14 | — | ≈ 71M tokens |

**Where the meme came from:** Hacker News users (May 2026) reported running
**DeepSeek V4 Pro + opencode** and burning **~100M tokens for ~$2** in a day,
"majority cache tokens." Plausible against official pricing **with a high
cache-hit ratio and limited output**.

**The honest version:** *fresh* input is ~$0.14/M (≈7M/$1) and **output is
100–300× the cache-hit price**, so a real mixed bill is higher. Mechanisms that
actually work: **automatic context cache** (DeepSeek, Doubao, Kimi) + **batch
APIs** (~50–60% off, non-real-time). ⚠️ A specific **off-peak discount** could
*not* be confirmed on DeepSeek's live 2026 page (it existed historically) — treat
off-peak as unverified.

### 11.2 Ultra-cheap "coding plan" subscriptions

Chinese labs sell flat monthly coding plans that undercut Claude Code massively.
The wiring is **officially supported, not a hack**: most expose an
**Anthropic-compatible endpoint**, so you point Claude Code / Cline / Roo at it:

```jsonc
// ~/.claude/settings.json  (Z.ai GLM example, per docs.z.ai)
{ "env": {
  "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
  "ANTHROPIC_AUTH_TOKEN": "<your_key>",
  "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.1",
  "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7"
}}
```

| Plan | Price (2026) | Model(s) | Rough quota | Notes |
|---|---|---|---|---|
| **Z.ai GLM Coding Plan – Lite** | **~$18/mo** advertised (launched ~$3/mo late 2025) ⚠️verify live | GLM-5.1 / 4.7 / 4.5-Air | ~80 prompts/5h, ~400/wk; *"≈3× Claude Pro usage"* | Flagship; widest tool support. ToS = supported tools only. |
| **MiniMax Token Plan** (ex-"Coding Plan") | **$20 / $50 / $120** | MiniMax-M3 (+multimodal) | 5-hr + weekly windows | Bundles coding **and** image/video/music under one quota. |
| **Moonshot Kimi K2.7 Code** | PAYG: **$0.19 / $0.95 / $4.00** per 1M (hit/miss/out) | kimi-k2.7-code, 256K ctx | spend-budget caps | Strong agentic coder; no cheap flat sub. |
| **DeepSeek V4** | PAYG: **$0.14 / $0.28** (flash) per 1M | deepseek-v4-flash/pro | — | Cheapest credible Claude-Code backend. |
| *Anthropic Claude* (baseline) | ~$20 Pro / ~$100–200 Max | Claude | — | The thing they're undercutting. |
| *GitHub Copilot* (baseline) | $10 / $39 / $100 | GPT/Claude/Gemini | — | — |

⚠️ **Alibaba Qwen's free coding tier was discontinued 2026-04-15** (1,000→100→0
req/day); Qwen Code now needs a paid plan or BYO key.

### 11.3 Free Chinese model tiers (text + multimodal)

| Provider | Genuinely-free API | Free chat app | Open weights | Intl friction |
|---|---|---|---|---|
| **Zhipu GLM / Z.ai** 🥇 | **`glm-4.7-flash`, `glm-4.5-flash`, `glm-4-flash`** (text); **`glm-4v-flash`, `glm-4.6v-flash`** (vision); **`cogview-3-flash`** (image) — all $0 ⚠️rate limits login-gated | chat.z.ai | GLM-4.5/4.7 (4.5 = MIT) | **Low** — Z.ai takes intl email/cards |
| **Tencent Hunyuan** | **1,000,000 tokens free, valid 1 year** (Tencent Cloud) | yuanbao.tencent.com | Hunyuan-A13B (13B active, 256K ctx) | Med — Cloud acct verification |
| **Alibaba Qwen** | Model Studio Intl: **1M tokens/model, 90 days, Singapore region** (enable "Free Quota Only" to avoid overage) | chat.qwen.ai | Qwen3 (Apache-2.0) | Med |
| **DeepSeek** | No free API (cheap PAYG) | chat.deepseek.com | DeepSeek-V3 / R1 | Low |
| **Moonshot Kimi** | No free API | kimi.com | Kimi K2 (huge) | Low |
| **ByteDance Doubao** | Ark trial credits only | doubao.com | — | High (CN-first) |

**🏆 The standout: Zhipu's `*-Flash` family** — the only major Chinese lab with a
genuinely $0 API spanning **text, vision, and image** (and historically video).
Sign up on the international **Z.ai** portal (intl email/card OK).

**Best $0 self-host weights** (run free on free GPU — see [§6](#6-self-host-oss-for-unlimited-tokens)):
Qwen3, DeepSeek-V3/R1, GLM-4.5/4.7, Hunyuan-A13B, ERNIE 4.5, Kimi K2, Yi, MiniMax-M1.

### 11.4 Free image generation

| Model | Provider | Free path | Watermark / commercial | Open weights | Friction |
|---|---|---|---|---|---|
| **CogView-3-Flash** 🥇 | Zhipu | **Free via API** (Z.ai) ⚠️limits login-gated | **None / commercial OK** | ❌ | Low |
| **Kolors (可图)** 🥇 | Kuaishou | **Open weights** (self-host) + Kling app | **None / commercial** (<300M MAU) | ✅ | Zero (self-host) |
| **Hunyuan-DiT** | Tencent | **Open weights** (self-host) | **None / commercial** (<100M MAU) | ✅ | Zero (self-host) |
| **Dreamina / Seedream** | ByteDance | App ~60 credits/day | **Watermark / personal only** | ❌ | Low (Google login) |
| **Tongyi Wanxiang** | Alibaba | App (free) / API trial | App watermark; API commercial | ❌ | High (app needs +86) |
| **ERNIE-ViLG** | Baidu | App ~50 signup credits | Watermark / personal | ❌ | Extreme (+86, real-name) |

**Verdict:** self-host **Kolors** (top quality, clean license, runs on free GPU)
or hit the **CogView-3-Flash API** (no server needed) for commercial-grade cover
art and thumbnails at $0.

### 11.5 Free video generation (for music videos)

**The key insight: free *app* tiers almost all watermark and forbid commercial
use — so for monetized music videos, the free *and* legally-clean path is
OPEN WEIGHTS, run free on free GPU** (HF ZeroGPU / Kaggle / Colab / Modal) via
ComfyUI or Diffusers.

**🔓 Self-host open weights — free, no watermark, commercial:**

| Model | Best free-GPU fit | VRAM (quantized) | Clip / res | License |
|---|---|---|---|---|
| **CogVideoX-2B** 🥇 lowest barrier | **Free Colab T4** | **~4 GB** | 6s · 720×480 | **Apache-2.0** |
| **CogVideoX-5B / 1.5-5B** | Kaggle, HF ZeroGPU | ~5–10 GB | up to **10s · 1360×768** | commercial OK |
| **Wan 2.2 TI2V-5B** 🥇 best license | **HF ZeroGPU Space**, RTX 4090 | ~16–24 GB | **720p · 24fps**, T2V+I2V | **Apache-2.0** |
| **HunyuanVideo 1.5** | HF ZeroGPU / Modal; GGUF on 12–16 GB | 12–24 GB (FP8/GGUF) | 5s · 720p | commercial **except EU/UK/KR** |
| Step-Video-T2V | (multi-GPU only) | ~78 GB | ~8.5s | heavy — skip on free |

**📱 Free app tiers (easy, but watermark + personal/non-commercial — good for drafts):**

| App | Free allowance | Free output | Notes |
|---|---|---|---|
| **Kling AI** (kling.ai) 🥇 | **66 credits/day** (≈1–3 clips) | 5s · 720p | Best quality free app; T2V+I2V+Motion Control. Free queue can wait hours. |
| **Hailuo** (hailuoai.video) | daily bonus (≈2–3/day) ⚠️ | 6s · 768p · 24fps | 15 cinematic camera commands. Pair with MiniMax **Music** API for an original track. |
| **Vidu / PixVerse** | monthly/daily credits ⚠️unverified | varies | Vidu = character-reference (consistent characters across a video). |

**Verdict for music videos:**
1. **🥇 Wan 2.2 TI2V-5B** (self-host) — cleanest license (Apache-2.0), 720p/24fps,
   runs on a free **HF ZeroGPU** Space or a 4090. Publishable & monetizable.
2. **🥇 CogVideoX-2B** (self-host) — **runs on a free Colab T4**; churn many short
   clips to cut to a beat.
3. **Kling / Hailuo** free apps — fast drafts & storyboards (watermarked).
4. **Cheapest paid fallback:** Zhipu **CogVideoX-3 API ~$0.20/video** (4K/60fps/audio).

⚠️ **"CogVideoX-Flash free"** is **not confirmed for 2026** — there's no free video
model on international Z.ai (CogVideoX-3 is paid). The free Flash video tier was a
Chinese-BigModel feature and may be retired; **verify before relying on it.**

### 11.6 China caveats

- **Data jurisdiction:** these run under PRC jurisdiction and **inputs may be used
  to train** models. Don't send secrets, proprietary, or regulated code/codebases.
- **Watermark + non-commercial on free app tiers:** for anything you'll monetize
  (incl. YouTube music videos), use **open weights** (Wan / CogVideoX / Hunyuan /
  Kolors) — free *and* commercially clean.
- **Don't prompt copyrighted characters:** Disney/Universal/Warner sued MiniMax
  (Sept 2025) over Hailuo reproducing IP. Generate original characters only.
- **ToS:** Z.ai's coding plan restricts use to officially supported tools and is
  individual-use only (repeated violations → ban). One legit account per service —
  Anthropic publicly accused MiniMax (Feb 2026) of using thousands of fraudulent
  accounts; don't be a cautionary tale.
- **Geopolitics/availability:** some orgs prohibit sending code to Chinese
  endpoints; access and pricing can change (Qwen's free tier vanished; GLM's entry
  price rose). Verify current terms before committing.

---

## Living lists to bookmark

- **[`cheahjs/free-llm-api-resources`](https://github.com/cheahjs/free-llm-api-resources)** —
  *the* auto-generated, **legit-only** list of free LLM API tiers + trial credits.
- **[`ripienaar/free-for-dev`](https://github.com/ripienaar/free-for-dev)** —
  huge general free-tier catalog for developers (incl. AI/ML).

---

## Sources

Compiled June 2026 from a multi-model research sweep (GPT-5.5, Claude Opus 4.8,
Gemini 3.1 Pro), with every number cross-checked against primary docs:

- Free LLM tiers & limits: `github.com/cheahjs/free-llm-api-resources`
- Gemini API pricing / rate limits: `ai.google.dev/gemini-api/docs/pricing`, `/rate-limits`
- Gemini Code Assist: `blog.google/.../gemini-code-assist-free/`, `developers.google.com/gemini-code-assist/resources/quotas`
- Gemini CLI: `github.com/google-gemini/gemini-cli`
- GitHub Copilot Free + signup pause: `docs.github.com/copilot/get-started/plans`
- OpenRouter: `openrouter.ai/docs` (free variants, fallbacks, provider routing)
- LiteLLM: `docs.litellm.ai/docs/proxy/load_balancing`, `/reliability`
- Cerebras: `inference-docs.cerebras.ai`; Groq: `console.groq.com/docs/rate-limits`
- Cloudflare Workers AI: `developers.cloudflare.com/workers-ai/platform/pricing`
- Prompt caching / batch: `platform.claude.com/docs`, `ai.google.dev/gemini-api/docs/caching`, `developers.openai.com/api/docs/guides/batch`
- Local runtimes: `ollama.com`, `lmstudio.ai`, `github.com/ggml-org/llama.cpp`, `github.com/vllm-project/vllm`
- Modal pricing: `modal.com/pricing`
- **China — token pricing:** `api-docs.deepseek.com/quick_start/pricing`, `/news/news0802` (context cache), `/news/news250929` (V3.2 DSA), `volcengine.com/docs/82379/1544106` (Doubao)
- **China — coding plans:** `docs.z.ai/devpack`, `platform.minimax.io/docs/token-plan`, `platform.kimi.ai/docs/pricing`, `api-docs.deepseek.com/guides/anthropic_api`
- **China — free model tiers:** `docs.bigmodel.cn/cn/guide/models/free/*` (GLM/CogView/CogVideoX Flash), `cloud.tencent.com/document/product/1729/97731` (Hunyuan 1M/yr), `alibabacloud.com/help/en/model-studio/new-free-quota`
- **China — image/video (open weights):** `github.com/Kwai-Kolors/Kolors`, `github.com/Tencent/HunyuanDiT`, `github.com/Wan-Video/Wan2.2`, `github.com/THUDM/CogVideo`, `github.com/Tencent-Hunyuan/HunyuanVideo`; apps: `kling.ai`, `hailuoai.video`

*Numbers are point-in-time (June 2026) and change frequently — verify before relying on them. Corrections via PR welcome.*
