# Awesome Free Compute 2026 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated, **source-cited** guide to free CPU, GPU, serverless, model-API, and LLM quotas in 2026 — and how to **stack** them for $0.

**Last verified: June 2026.** Free tiers change constantly — always confirm on the provider's official pricing page before relying on a number. Corrections via PR are very welcome.

This was compiled from a multi-model research sweep of official pricing/docs pages (not blog hearsay), with conflicts resolved against primary sources.

> [!TIP]
> **👉 Companion guides:**
> - **[The Free Token-Maxxing Guide](./TOKEN-MAXXING.md)** — maximum frontier-model
>   usage for $0: free LLM APIs, free coding tools, the BYO-key trick, LiteLLM/OpenRouter
>   orchestration, quota-stretching, and a full **🇨🇳 China section** ("100M tokens for
>   ~$1", cheap coding plans, free image/video generation).
> - **[The Free Audio Generation Guide](./AUDIO.md)** 🎙️ — free **music, voice (TTS +
>   cloning), and transcription** for creators, with a hard focus on **commercial
>   licensing** (which "free" tools you can actually monetize).

---

## Contents

- [TL;DR — the best $0 stack](#tldr--the-best-0-stack)
- [1. Always-free CPU / VMs](#1-always-free-cpu--vms)
- [2. Free GPU notebooks & sessions](#2-free-gpu-notebooks--sessions)
- [3. Serverless GPU (Modal-class)](#3-serverless-gpu-modal-class)
- [4. Hosted model APIs — image / video / utilities](#4-hosted-model-apis--image--video--utilities)
- [5. Free LLM APIs](#5-free-llm-apis)
- [6. Trial credits & student / startup programs](#6-trial-credits--student--startup-programs)
- [Corrections & caveats](#corrections--caveats)
- [Sources](#sources)
- [Contributing](#contributing)
- [License](#license)

---

## TL;DR — the best $0 stack

- **Always-on backend:** [Oracle Cloud Always Free](#1-always-free-cpu--vms) (4 OCPU / 24 GB ARM) + a tiny **GCP e2-micro** as backup.
- **Recurring free GPU:** **[Modal](#3-serverless-gpu-modal-class) — $30/month, resets monthly** (≈ 50 h T4 / 27 h A10 / 12 h A100 *every month*). The single best standing free-GPU allowance.
- **Long unattended GPU jobs:** **[Kaggle](#2-free-gpu-notebooks--sessions)** — 30 GPU-hrs/week, runs 12 h headless.
- **Upscale / interpolate / animate (no GPU setup):** **[Replicate](#4-hosted-model-apis--image--video--utilities)** — Real-ESRGAN, FILM, LTX-Video, Wan — *pennies per run*.
- **Free image gen, daily:** **Cloudflare Workers AI** FLUX (10k neurons/day).
- **Free LLM (text):** **Google AI Studio / Gemini Flash**; **GitHub Models** for no-card prototyping.

---

## 1. Always-free CPU / VMs

| Provider | Always-free? | What you get | Key gotchas |
|---|---|---|---|
| **Oracle Cloud Always Free** ⭐ | ✅ Forever | **4 OCPU / 24 GB RAM (Ampere A1)** + 2× AMD micro VMs, 200 GB block storage, 20 GB object storage | "Out of host capacity" errors; home-region lock-in; idle VMs reclaimed after 7 days of <20% use |
| **Google Cloud `e2-micro`** | ✅ Forever | 1 shared-vCPU / ~1 GB VM, 30 GB disk, 1 GB egress/mo — only in `us-west1`, `us-central1`, `us-east1` | Too small for AI; great for bots, monitors, webhooks |
| **AWS Free Tier** | ❌ | **2026 model: $100 credit + up to $100 earned, account closes after 6 months.** Lambda stays free (1M req + 400k GB-s/mo) | No more "12-month free EC2"; treat any EC2 free as introductory |
| **Azure Free Account** | ❌ | $200 / 30 days + 750 h B1s for 12 months | B-series throttles when CPU credits run out |
| **Alibaba Cloud** | ❌ | $90 ECS credit / 3 months; some non-VM "always free" products | Asia-centric; ECS is `limited_free`, not always-free |
| **Fly.io / Render / Railway / Koyeb** | ❌ (mostly) | Render free web svc sleeps after 15 min idle; Railway $1/mo credit; Fly no new free tier; Koyeb now Pro-first | Not viable as a real always-on free server |
| **Hetzner** | ❌ | No free tier — but cheapest reliable **paid** VPS fallback | Billed until deleted, even when powered off |

## 2. Free GPU notebooks & sessions

| Platform | GPU / TPU | Free quota | Persistence | Best for |
|---|---|---|---|---|
| **Kaggle** ⭐ | T4 ×2 / P100 / TPU v3-8 | **30 GPU-hrs/wk + 20 TPU-hrs/wk**, 12 h headless, 73 GB disk | Outputs persist (≤20 GB) | Long unattended renders / upscaling |
| **Google Colab** | T4 (16 GB) | ~10–15 h/wk (dynamic, throttled) | ❌ none (pipe to Drive) | Prototyping new repos fast |
| **Lightning AI Studio** | T4 (frac. A100) | **15 credits/mo (~15–22 h T4)** | ✅ full env persists | Multi-day project workspace |
| **Hugging Face ZeroGPU** | Shared A100 | Short bursts (<120 s/call) | ephemeral | Demo UIs — **not** renders |
| **Google TPU Research Cloud** | TPU v2–v5 | Free ~30 days (apply w/ research note) | n/a | Training a model from scratch |
| **SageMaker Studio Lab** | T4 | 4 h/session, 8 h/day, 15 GB persistent | ✅ | Colab alternative *if* approved |
| **Paperspace (DigitalOcean)** | M4000/A4000 | ⚠️ Free machines ~never available; needs $8/mo Pro | ✅ | Skip unless paying |

## 3. Serverless GPU (Modal-class)

> **Conflict resolved:** Modal's free tier **is $30/month recurring** (confirmed on `modal.com/pricing`). Blog posts claiming "no recurring free tier" are outdated/wrong.

| Platform | Free tier | Cheapest GPU $/hr | Scale-to-zero | Notes |
|---|---|---|---|---|
| **Modal** ⭐ | **$30/mo recurring** | T4 $0.59 · A10 $1.10 · A100-80 $2.50 · H100 $3.95 | ✅ | Best Python DX; CPU $0.047/core-hr |
| **Beam.cloud** | 15 h (one-time) | RTX 4090 $0.69 · H100 $3.50 | ✅ | Closest Modal clone; cold starts not billed |
| **Inferless** | **10 h / $30, no card** | frac-T4 $0.33 · T4 $0.66 | ✅ | Easiest instant trial *(joining Baseten)* |
| **Cerebrium** | signup credits | A10 $1.10 | ✅ (1–3 s) | Cold starts not billed |
| **Baseten** | signup credits | (per-min, JS-rendered) | ✅ | Production-grade serving (Truss) |
| **RunPod** | ❌ pay-go | **A5000 $0.27 · L4 $0.39 · A100 $1.39** | ✅ (serverless) | Cheapest *reliable paid* overflow |
| **Google Cloud Run** | ✅ CPU/req only (no free GPU) | L4 (instance-billed) | ✅ (~5 s) | Use the free **CPU** tier for render jobs |
| **Vast.ai** | ❌ pay-go | spot market (cheapest anywhere) | n/a | Fault-tolerant batch / training |

**What $30/mo on Modal buys (GPU-only):** ≈ 50 h T4 · 37 h L4 · 27 h A10 · 14 h A100-40 · 12 h A100-80 · 7.6 h H100 — **or** ≈ 638 CPU-core-hours.

## 4. Hosted model APIs — image / video / utilities

| Service | Free | Models & example costs | Best use |
|---|---|---|---|
| **Cloudflare Workers AI** ⭐ | **10,000 neurons/day** (recurring) | FLUX text-to-image | Free daily cover-art / image drafts |
| **Replicate** ⭐ | pay-per-run (no standing free) | **Real-ESRGAN** (upscale) · **FILM** ~$0.007/run · **LTX-Video** ~$0.014/run · **Wan I2V** $0.09–0.25/output-sec · FLUX/SDXL | Upscale → interpolate → animate utility shelf |
| **fal.ai** | small free credits | **Wan I2V $0.20 (480p) / $0.40 (720p)** per ~5 s clip · FLUX Schnell $0.003/MP | Fast hosted video gen |
| **Hugging Face Inference** | $0.10/mo (Free), $2/mo (PRO) | routed open models | Tiny monthly sandbox |
| **Together AI** | "start free" (credits) | FLUX Schnell $0.0027/MP · SDXL $0.0019/MP | Cheapest paid still images |

## 5. Free LLM APIs

| Provider | Free quota | Card? | Best for |
|---|---|---|---|
| **Google AI Studio (Gemini)** ⭐ | Broad free tier (Flash / Flash-Lite) | No | Best quality-free text ⚠️ *free-tier inputs used to improve products* |
| **GitHub Models** | 15 RPM / 150 RPD (low tier) | No | No-infra prototyping |
| **Cloudflare Workers AI** | 10,000 neurons/day | No | Open-model drafts; **not trained on your content** |
| **Groq** | fast free dev tier (check console) | No | Rapid iteration |
| **Cerebras** | free/trial (5–30 RPM, 1M tokens/day) | No | Ultra-fast brainstorming |
| **Cohere** | 1,000 calls/mo trial | No | Rewrites, translation |
| **OpenRouter** | `:free` model variants | No | Model variety in one API |
| **Mistral La Plateforme** | experiment tier | Usually no | EU provider option |

## 6. Trial credits & student / startup programs

| Program | Amount | Validity / eligibility |
|---|---|---|
| Google Cloud Free Trial | **$300** | 90 days |
| Oracle Cloud Free Trial | **$300** | 30 days (Always Free continues after) |
| Azure Free Account | **$200** | 30 days |
| AWS Free Tier (2026) | **$100 + up to $100** | closes after 6 months |
| Alibaba Cloud ECS | **$90** | 3 months |
| **GitHub Student Pack** | DigitalOcean $200/yr, Azure $100 (no card), Heroku credits, +more | verified students |
| **Google for Startups** | up to **$200k** ($350k for AI startups) | startup eligibility |
| **AWS Activate** | **$5k–$100k** | startup via Activate provider |
| **Google TPU Research Cloud** | free TPU v2–v5 | apply with a research note |

---

## Corrections & caveats

- **AWS Free Tier was overhauled in 2026** — it's now a credit model (closes after 6 months), *not* the old 12-month free EC2.
- **Replicate has no recurring free credit** — it's pay-pennies-per-run (still excellent for upscale/interpolate jobs).
- **Could not verify from official pages (client-rendered):** Baseten & Cerebrium exact free-credit amounts; Cloud Run's exact L4 GPU rate. Confirm in-browser.
- **Industry consolidation:** Inferless → joining Baseten; Koyeb → joining Mistral AI. Terms may shift.
- All numbers are **June 2026** snapshots. **Verify before relying.**

## Sources

Primary official pages referenced (accessed June 2026):

- Oracle — https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm · https://www.oracle.com/cloud/free/faq/
- Google Cloud — https://cloud.google.com/free/docs/free-cloud-features · https://cloud.google.com/run/pricing · https://cloud.google.com/startup
- AWS — https://aws.amazon.com/free/ · https://aws.amazon.com/free/terms/ · https://aws.amazon.com/lambda/pricing/ · https://aws.amazon.com/startups/faq
- Azure — https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account · https://azure.microsoft.com/en-us/free/students
- Alibaba Cloud — https://www.alibabacloud.com/en/free
- Modal — https://modal.com/pricing
- Beam — https://docs.beam.cloud/v2/resources/pricing-and-billing
- RunPod — https://www.runpod.io/pricing
- Replicate — https://replicate.com/pricing · model pages for Real-ESRGAN, FILM, LTX-Video, Wan
- fal.ai — https://fal.ai/pricing · https://fal.ai/models
- Inferless — https://www.inferless.com/pricing
- Cerebrium — https://www.cerebrium.ai/pricing
- Cloudflare Workers AI — https://developers.cloudflare.com/workers-ai/platform/pricing/
- Hugging Face — https://huggingface.co/docs/inference-providers/pricing
- Together AI — https://www.together.ai/pricing
- Google AI Studio (Gemini) — https://ai.google.dev/gemini-api/docs/pricing
- GitHub Models — https://docs.github.com/en/github-models
- Kaggle — https://www.kaggle.com/docs/efficient-gpu-usage
- Lightning AI — https://lightning.ai/pricing
- Hugging Face ZeroGPU — https://huggingface.co/docs

Community aggregators worth cross-checking:

- https://github.com/ripienaar/free-for-dev
- https://github.com/cloudcommunity/Cloud-Free-Tier-Comparison

## Contributing

Quotas drift fast. If you spot an outdated number:

1. Open an issue or PR with the **official source URL** and the date you checked it.
2. Keep entries source-cited — no blog hearsay.

## License

[CC0-1.0](LICENSE) — public domain. Copy, adapt, and share freely.
