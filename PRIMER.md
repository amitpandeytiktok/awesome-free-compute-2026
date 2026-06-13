# 🧠 AI & Tokens 101 — the primer

> New here? This is the plain-English backstory behind every other guide on this site:
> what a "token" actually is, why so much AI compute is **free**, and how we got to a 2026
> where you can run a studio-grade creative + dev stack for **$0**.

## Contents

- [What is a token?](#what-is-a-token)
- [Why is any of this free?](#why-is-any-of-this-free)
- [A short history (2022 → 2026)](#a-short-history-2022--2026)
- [The four ways to pay $0](#the-four-ways-to-pay-0)
- [The one thing that bites creators: licensing](#the-one-thing-that-bites-creators-licensing)
- [Glossary](#glossary)

---

## What is a token?

A **token** is the unit language models read and write. It's *roughly* ¾ of a word — a
chunk of characters the model treats as one step. "Unbelievable" might be 3 tokens
(`un` + `believ` + `able`); a space, an emoji, or a CJK character can each be their own.

Two rules of thumb that explain almost all AI pricing:

- **~1 token ≈ 4 characters ≈ 0.75 words** in English. 1,000 tokens ≈ 750 words.
- You pay for **input tokens** (your prompt + context) **and output tokens** (the reply),
  usually at different rates, **per million tokens** (often written *$/Mtok*).

So a "128k context window" means the model can hold ~96,000 words of prompt at once, and a
bill of "$0.50 / 1M input" means a 10,000-token prompt costs half a cent. Everything else
— caching, batching, the "100M tokens for $1" tricks — is just **moving where those
tokens are counted and how often they're recomputed.** (The
[Token-Maxxing guide](./TOKEN-MAXXING.md) is the deep dive.)

> 💡 Images, audio, and video get "tokenized" too — a few hundred tokens per image tile, a
> chunk per second of audio. Same meter, different media.

---

## Why is any of this free?

It feels too good to be true, so it's worth knowing the actual incentives. "Free" AI
compute exists for five honest reasons:

1. **Land-grab.** Cloud and model vendors give away credits to win developers before the
   market settles. Free tiers are a customer-acquisition cost, not charity.
2. **Open weights.** Labs (Meta, Mistral, Qwen, DeepSeek, Black Forest Labs, Stability,
   Tencent) release model weights publicly. Once weights are open, *anyone* can run them
   on free or cheap hardware — the marginal cost of inference collapses.
3. **Spare capacity.** Research programs (Google's TPU Research Cloud, Kaggle, Colab) and
   serverless platforms hand out idle GPU/TPU time to seed an ecosystem.
4. **Loss-leader pricing.** Aggressive players — especially Chinese labs in 2025–26 — price
   tokens near cost (or below) and lean on **prompt caching** to make repeat work nearly
   free.
5. **Your own hardware.** A modern laptop — *especially Apple Silicon with unified memory*
   — can run real models locally. Local inference is unmetered and private: the truest $0.

The catch is never the price — it's **quotas, idle-sleep, data-sharing, and licensing.**
This site exists to map exactly those.

---

## A short history (2022 → 2026)

| When | What happened | Why it mattered |
|---|---|---|
| **Nov 2022** | ChatGPT launches | LLMs go mainstream; "tokens" enters the vocabulary |
| **Feb–Jul 2023** | LLaMA leaks → **Llama 2** open weights; Stable Diffusion booms | the open-weights era begins; local AI becomes real |
| **2023** | Whisper, Colab/Kaggle free GPUs, HF Hub | free transcription + free notebooks = a $0 starter stack |
| **2024** | Token prices **fall ~10×**; Mixtral/Qwen/Gemma; serverless GPU (Modal-class); FLUX | open models rival closed ones; per-token cost becomes trivial |
| **Late 2024** | Free perpetual tiers start dying (Fly.io, PlanetScale Hobby) | the "free backend" map gets redrawn — see the [Ship-It Stack](./STACK.md) |
| **2025** | **DeepSeek** + Chinese labs: cache-hit pricing, "100M tokens for ~$1"; ACE-Step, open TTS/voice cloning | the cheapest tokens on earth + free music/voice generation |
| **2026** | Open image/video/3D mature; MCP becomes the agent "tool bus"; Apple Silicon is a credible local rig | a full creator **+** dev stack runs at $0 — if you know the map |

The throughline: **every year, more of the stack falls to $0** — first tokens, then audio,
then finishing, then the backend. What stays scarce is *trustworthy information about which
free option is actually free, actually good, and actually safe to monetize.*

---

## The four ways to pay $0

Every resource on this site is one of these. Mix them with the
[stacking playbook](./TOKEN-MAXXING.md#10-the-stacking-playbook):

1. **Free tiers** — recurring monthly allowances (Gemini API, Groq, Cloudflare, Neon). Best
   for steady low-volume use; watch the quota and the idle-sleep.
2. **Trial credits** — one-time fuel ($300 GCP, $200 Azure, $25 Predibase). Best for a
   burst of heavy work; they expire.
3. **Open weights, self-hosted** — run the model yourself on free GPU (Kaggle/Colab) or
   local (Ollama, ComfyUI). Unmetered, private, and the only truly *unlimited* option.
4. **Your own legitimate keys, orchestrated** — route many of *your* free keys through one
   hub ([LiteLLM/OpenRouter](./TOKEN-MAXXING.md#7-the-orchestration-layer-wire-it-together))
   with caching and fallback so you degrade gracefully instead of hitting a wall.

---

## The one thing that bites creators: licensing

If you monetize anything — a YouTube video, an app, a product — **the licence on a "free"
model matters more than its quality.** A huge share of popular open models are
**research / non-commercial only**, and several are silently bundled into the GUIs
everyone uses.

- ✅ **Safe to monetize:** MIT, BSD, Apache-2.0 — and even **GPL** (copyleft only governs
  redistributing the *software*, never your render/output).
- ⚠️ **Not without a paid licence:** **CC-BY-NC**, "research only," and bespoke
  non-commercial licences (CodeFormer, SUPIR, BRIA RMBG, SeamlessM4T/NLLB, Suno free,
  Coqui XTTS-v2, FLUX.1-dev, and more).

Each guide carries a **licensing-landmines** section for its domain. When in doubt, prefer
permissive weights and read the actual `LICENSE` file — quality you can't legally use is
worth zero.

---

## Glossary

- **Token** — ~¾ of a word; the unit models read/write and bill by.
- **Context window** — how many tokens a model can consider at once (e.g., 128k ≈ 96k words).
- **Open weights** — the trained model parameters are public; you can run/fine-tune them.
- **Free tier** — a recurring no-cost usage allowance from a vendor.
- **Prompt caching** — reusing a fixed prompt prefix at a deep discount (often ~90% off).
- **Quantization** — shrinking a model (e.g., to 4-bit) so it runs on smaller/free GPUs.
- **LoRA / QLoRA** — cheap fine-tuning that trains a small adapter, not the whole model.
- **Inference vs training** — running a model vs teaching it; inference is what you mostly pay for.
- **Scale-to-zero / idle-sleep** — a free service that pauses when unused (cold starts on wake).
- **MCP** — Model Context Protocol; the open standard "USB-C" that plugs tools into AI agents.
- **LUFS** — loudness units; streaming platforms normalize to a target (see [Post-Production](./POST-PRODUCTION.md)).

---

*Ready to go deep? Start with [Token-Maxxing](./TOKEN-MAXXING.md) for LLMs, or the
[Free Compute list](./README.md) for CPUs/GPUs. New tools and prices land in
**The Wire** on the home page, refreshed automatically.*
