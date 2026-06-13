# 🚀 The Free Ship-It Stack (2026)

> Free *model* tokens are only half a product. This guide is the **other half** — the
> database, vector store, embeddings, hosting, storage, auth, and cron you need to
> actually **ship an AI app for $0** — with a hard focus on **which "free" tiers you can
> legally use commercially** (several popular ones quietly can't).

Companion to the main [Awesome Free Compute](./README.md) list, the
[Free Token-Maxxing Guide](./TOKEN-MAXXING.md) (LLMs/tokens), the
[Free Audio Generation Guide](./AUDIO.md), and the
[Media Post-Production Guide](./POST-PRODUCTION.md). Compiled from a multi-model research
sweep (Claude Opus 4.8, GPT-5.5, Gemini 3.1 Pro) and reconciled against official pricing
pages. **All quotas are June 2026 snapshots — verify before relying.**

## Contents

- [TL;DR — the commercial-safe $0 stack](#tldr--the-commercial-safe-0-stack)
- [⚠️ 2026 reality check (read this first)](#-2026-reality-check-read-this-first)
- [1. Databases](#1-databases)
- [2. Vector search and RAG](#2-vector-search-and-rag)
- [3. Embeddings](#3-embeddings)
- [4. Hosting and serverless](#4-hosting-and-serverless)
- [5. Object storage](#5-object-storage)
- [6. Auth, email, cron](#6-auth-email-cron)
- [7. Reference architectures](#7-reference-architectures)
- [The free-tier cliffs](#the-free-tier-cliffs)
- [Sources](#sources)

---

## TL;DR — the commercial-safe $0 stack

| Layer | Pick (commercial-safe) | Free headroom |
|---|---|---|
| 🖥️ **Frontend + edge API** | **Cloudflare Pages + Workers** | static unlimited · 100k req/day · **$0 egress** |
| 🗄️ **Database** | **Neon** or **Supabase** Postgres | 0.5 GB · **pgvector built-in** |
| 🔎 **Vector / RAG** | **pgvector** on that same DB | no extra service to outgrow |
| 🧬 **Embeddings** | **Voyage** (200M free tokens) or **local Ollama** | commercial-clean, no data-sharing |
| 🪣 **Object storage** | **Cloudflare R2** | 10 GB · **free egress** |
| 🔐 **Auth** | **Supabase Auth** (50k MAU) or **Auth0** (25k MAU) | generous ceilings |
| ✉️ **Email** | **Resend** | 3k/mo (100/day) |
| ⏰ **Cron / queue** | **Upstash QStash** or **CF Cron** | 1k msg/day · free retries |

**One-liner:** *the cleanest $0 commercial stack is **all-Cloudflare** (Pages + Workers +
D1 + R2) or **all-Supabase** (Postgres + pgvector + Auth + Storage) — both minimize the
number of free tiers you can outgrow, and neither has a commercial-use trap.*

> 🍰 **Two simplest "one-vendor" stacks:**
> **(a) Supabase-only** — Postgres + pgvector + Auth + Storage + Edge Functions.
> **(b) Cloudflare-only** — Pages + Workers + D1 + R2 + Workers AI.
> Both are commercial-OK and need just one dashboard.

---

## ⚠️ 2026 reality check (read this first)

The free-tier landscape shifted hard in 2024–2026. The internet is full of stale guides;
these are the traps that actually matter:

- 🚫 **Vercel Hobby is personal / non-commercial ONLY.** The moment your project is
  commercial you must move to **Pro ($20/mo)** — this is a ToS rule, not a usage limit.
  For a commercial $0 app, deploy on **Cloudflare Pages** instead.
- 🚫 **GitHub Pages forbids commercial use** — "no business, e-commerce, or commercial
  SaaS." Fine for docs/landing pages, not your product.
- 💸 **No longer free (perpetual):** **PlanetScale** (Hobby removed), **Fly.io** (free
  allowances gone Oct 2024), **Railway** ($5 trial only), **Xata** (credit then PAYG).
  Don't plan a $0 stack around these.
- 📅 **Deno Deploy Classic** (1M req/mo) **sunsets July 20, 2026** — no new signups;
  migrate to the new Deno Deploy.
- 📉 **Netlify** moved to a **credit model** (~300 credits ≈ **15 GB** bandwidth/mo) —
  far tighter than the old 100 GB.
- 🕵️ **Gemini free-tier embeddings (and chat) train on your inputs.** Google's free tier
  uses your content to improve products; the paid tier doesn't. For anything proprietary,
  use **Voyage** (200M free tokens) or **local** embeddings.
- 😴 **"Free" often means "sleeps":** Neon scale-to-zero (5-min cold start), Render
  spin-down (15 min), Supabase pause (1 week idle), Qdrant/Weaviate idle-suspend (1–4
  weeks), HF Spaces sleep (~48 h). Fine for side-projects; budget an "always-on" upgrade
  for latency-sensitive production.

---

## 1. Databases

| Service | Free quota (June 2026) | Commercial? | Idle behavior |
|---|---|---|---|
| **Neon** (serverless PG) | 0.5 GB/project · **100 CU-hrs/mo** · 100 projects · 10 branches · **pgvector included** | ✅ | scale-to-zero after 5 min (cold starts; can't disable on Free) |
| **Supabase** (PG) | 500 MB DB · 5 GB egress · 1 GB files · **50k MAU** · unlimited API | ✅ | **paused after 1 week idle** · max 2 free projects |
| **Turso** (libSQL/SQLite) | 100 DBs · 5 GB · **500M row-reads/mo** · 10M writes · native vector | ✅ | always-on (no sleep) |
| **Cloudflare D1** (SQLite) | **5M row-reads/day** · 100k writes/day · 5 GB · **no egress fees** | ✅ | scale-to-zero, resets daily 00:00 UTC |
| **MongoDB Atlas** (M0) | **512 MB** · shared vCPU · **never expires** · 1 cluster/project | ✅ (small) | always-on but tiny |
| **Upstash Redis** | 256 MB · **500k commands/mo** · 10 GB bandwidth | ✅ | serverless scale-to-zero |
| ~~PlanetScale · Fly.io · Railway · Xata~~ | **no perpetual free tier** (paid / trial only) | 💲 | — |

**Pick:** **Neon** if you want Postgres + pgvector with the fewest moving parts;
**Supabase** if you also want bundled Auth + Storage; **Cloudflare D1** if you're going
all-Cloudflare and want zero egress fees.

---

## 2. Vector search and RAG

| Service | Free quota | Commercial? | Notes |
|---|---|---|---|
| **pgvector** (on Neon/Supabase) | within the host DB's free tier | ✅ | **zero extra services** — the simplest RAG; one fewer tier to outgrow |
| **Qdrant Cloud** | 1 GB RAM · 4 GB disk · 1 node (~1M × 768-dim) | ✅ | suspended after 1 wk idle, deleted after 4 wks |
| **Upstash Vector** | **200M** (vectors × dims) · ≤1536 dims · **10k queries/day** | ✅ | serverless scale-to-zero |
| **Pinecone** (Starter) | 1M read-units · 2M write-units · 5M embed-tokens /mo | ✅ | serverless; Inference + Assistant included |
| **Weaviate Cloud** | 1 always-free cluster/user · Query Agent 1k req/mo | ✅ | suspended after 7 days idle, deleted after 30 |
| **Chroma · LanceDB · Milvus** | **open-source, self-host = free & unlimited** | ✅ | LanceDB = "SQLite of vectors" (embedded); Milvus = Apache-2.0 |

**Pick:** **pgvector** on your existing Postgres for 90% of apps. Reach for **Qdrant** or
**Upstash Vector** only when you need a dedicated ANN service; **LanceDB** (embedded) when
you want zero infra.

---

## 3. Embeddings

| Service | Free quota | Commercial? | Gotcha |
|---|---|---|---|
| **Local** (bge / e5 / nomic via **Ollama**) | **unlimited, self-host** | ✅ | best for privacy/commercial — nothing leaves your box |
| **Voyage** | **200M free tokens** (one-time per account) | ✅ | generous; great default hosted option |
| **Nomic** (`nomic-embed-text-v1.5`) | Apache-2.0 → **local free**; Atlas API has credits | ✅ | resizable dims (64–768) |
| **Jina** (`jina-embeddings-v4`) | ~10M free tokens, no card | ✅ | multimodal; verify quota at signup |
| **Gemini embeddings** | free tier (RPM/RPD capped) | ⚠️ | **free tier trains on your data** — paid tier doesn't |
| **Cohere embed** | trial: **1,000 calls/mo, eval-only** | ❌ | production key is paid |

**Pick:** **local (Ollama)** for unlimited + private, or **Voyage** for a hosted,
commercial-clean key. **Avoid Gemini's free tier for proprietary data** (it's used for
training).

---

## 4. Hosting and serverless

| Service | Free quota | Commercial? | Cold-start / sleep |
|---|---|---|---|
| **Cloudflare Pages + Workers** | **static unlimited** · Functions **100k req/day** · 10 ms CPU · **no egress** | ✅ | edge, no sleep |
| **Netlify** | $0 — **300 credits/mo** ≈ **15 GB** bandwidth | ✅ | static = none |
| **HF Spaces** | CPU Basic: **2 vCPU · 16 GB RAM · 50 GB disk** | ✅ | free Spaces sleep ~48 h idle |
| **Render** | 750 instance-hrs/mo · web + PG + KV | ⚠️ "not for production" | **spins down after 15 min** (~1 min cold start) |
| **Deno Deploy** | new free tier (Classic 1M req/mo **sunsets Jul 20 2026**) | ✅ | edge isolates |
| ~~Vercel Hobby~~ | 1M invocations · 1M edge req · 100 GB-hrs | ❌ **personal only** | → **Pro $20/mo for commercial** |
| ~~GitHub Pages~~ | 1 GB site · 100 GB/mo | ❌ **no commercial SaaS** | static |
| ~~Fly.io · Railway~~ | paid / trial only | 💲 | — |

**Pick:** **Cloudflare Pages + Workers** is the $0 **commercial** hero — unlimited static,
100k req/day, zero egress. Use **Vercel Hobby** only for personal/non-commercial projects
(the DX is great, but commercial = $20/mo).

---

## 5. Object storage

| Service | Free quota | Commercial? | Notes |
|---|---|---|---|
| **Cloudflare R2** | **10 GB-mo** · 1M Class-A · 10M Class-B ops · **EGRESS FREE** | ✅ | S3-compatible; the headline is **$0 egress** for any storage class |
| **Backblaze B2** | **10 GB** · free egress up to 3× daily storage · **unlimited free egress via partner CDNs** (Cloudflare/Fastly/bunny) | ✅ | beyond free: $6/TB-mo |
| **Supabase Storage** | 1 GB files · 5 GB egress (shared w/ project) | ✅ | bundled with Supabase Free |

**Pick:** **Cloudflare R2** — free egress means no surprise bandwidth bills, and it pairs
natively with Pages/Workers.

---

## 6. Auth, email, cron

| Service | Free quota | Commercial? | Gotcha |
|---|---|---|---|
| **Supabase Auth** | **50,000 MAU** · unlimited total users | ✅ | free if already on Supabase |
| **Auth0** | **25,000 MAU** · 5 orgs · 1 custom domain | ✅ | most generous standalone MAU ceiling |
| **Clerk** | 50,000 MRU · ≤3 seats | ✅ | free shows Clerk branding · no MFA · fixed 7-day sessions |
| **Firebase Auth** (Spark) | 50k MAU · Firestore 1 GiB + 50k reads/day | ✅ | **Cloud Storage now needs billing** (Blaze) for new buckets |
| **Resend** (email) | **3,000/mo · 100/day** · 1 domain | ✅ | the **100/day** cap is the real constraint |
| **Upstash QStash** (cron/queue) | **1,000 messages/day** · 10 cron schedules | ✅ | retries are free |
| **Cloudflare Cron · GitHub Actions** | within Workers free · 2,000 min/mo (private) | ✅ | cheap schedulers for batch jobs |

**Pick:** **Supabase Auth** if you're on Supabase, else **Auth0** (25k MAU, no branding).
**Resend** for email (mind 100/day). **QStash** or **CF Cron** for scheduled jobs.

---

## 7. Reference architectures

**🅰️ Commercial-safe $0 (recommended):**

```
Cloudflare Pages + Workers   ← frontend + edge API ($0 egress, commercial OK)
        │
        ├── Neon / Supabase Postgres + pgvector   ← data + RAG (one service)
        ├── Voyage (200M free) or local Ollama     ← embeddings (no data-sharing)
        ├── Cloudflare R2                          ← file/asset storage (free egress)
        ├── Supabase Auth (50k) / Auth0 (25k)      ← login
        ├── Resend (3k/mo)                         ← transactional email
        └── Upstash QStash / CF Cron               ← jobs & queues
```

**🅱️ Simplest one-vendor:**
- **Supabase-only:** Postgres + pgvector + Auth + Storage + Edge Functions.
- **Cloudflare-only:** Pages + Workers + D1 + R2 + Workers AI.

**🅲 Best DX, non-commercial / hobby:** Next.js on **Vercel Hobby** + **Neon** +
Gemini-free embeddings + **R2** + **Resend**. Smoothest to build — but **the instant it's
commercial, Vercel forces Pro ($20/mo)** and GitHub Pages becomes disallowed.

---

## The free-tier cliffs

When (and why) each free tier forces a paid upgrade:

- **Vercel Hobby → Pro $20/mo** — the instant the project is *commercial* (ToS, not usage).
- **GitHub Pages → move off** — any business / e-commerce / commercial SaaS is prohibited.
- **Supabase → Pro $25/mo** — >500 MB, >50k MAU, backups/PITR, or to stop the 1-week pause.
- **Neon → PAYG** — >0.5 GB, >100 CU-hrs/mo, or to **disable scale-to-zero** (kill cold starts).
- **Render → ~$7/mo** — any production app (free spins down after 15 min; "not for production").
- **Resend → $20/mo** — >3,000/mo or the **100/day** cap; or >1 domain.
- **Clerk → $25/mo** — to remove branding, add MFA, or change session length.
- **Vector DBs** — outgrow Qdrant (1 GB, suspends 1 wk), Upstash Vector (200M, 10k q/day),
  Weaviate (suspends 7 d), or Pinecone (1M read / 2M write units) → paid.
- **Latency-sensitive production** — pay to make Neon / Render / Qdrant / Weaviate / HF
  Spaces "always-on" (kill the idle sleep).
- **Already paid-only (no $0 path):** PlanetScale, Fly.io, Railway, Xata.

---

## Sources

Primary pricing/docs pages fetched & verified June 2026 (representative):

- **Databases:** [Supabase pricing](https://supabase.com/pricing) · [Neon pricing](https://neon.com/pricing) · [Turso pricing](https://turso.tech/pricing) · [Cloudflare D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/) · [MongoDB Atlas M0](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/) · [Upstash Redis](https://upstash.com/pricing/redis) · [PlanetScale](https://planetscale.com/pricing) · [Xata](https://xata.io/pricing)
- **Vector:** [Qdrant Cloud](https://qdrant.tech/documentation/cloud/create-cluster/) · [Pinecone limits](https://docs.pinecone.io/reference/api/database-limits) · [Weaviate Cloud](https://docs.weaviate.io/cloud/manage-clusters/create) · [Upstash Vector](https://upstash.com/pricing/vector) · [Chroma Cloud](https://docs.trychroma.com/cloud/pricing) · [LanceDB](https://www.lancedb.com)
- **Embeddings:** [Voyage pricing](https://docs.voyageai.com/docs/pricing) · [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Cohere rate limits](https://docs.cohere.com/docs/rate-limits) · [Nomic](https://docs.nomic.ai/atlas/embeddings-and-retrieval/generate-embeddings) · [Jina](https://jina.ai/embeddings/)
- **Hosting:** [Vercel Hobby](https://vercel.com/docs/plans/hobby) · [Netlify pricing](https://www.netlify.com/pricing/) · [Cloudflare Workers](https://developers.cloudflare.com/workers/platform/pricing/) / [Pages](https://developers.cloudflare.com/pages/functions/pricing/) · [Render free](https://render.com/docs/free) · [Fly.io pricing](https://fly.io/docs/about/pricing/) · [Railway](https://railway.com/pricing) · [Deno Deploy](https://docs.deno.com/deploy/) · [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) · [HF Spaces](https://huggingface.co/docs/hub/spaces-gpus)
- **Storage:** [Cloudflare R2](https://developers.cloudflare.com/r2/pricing/) · [Backblaze B2](https://www.backblaze.com/cloud-storage/pricing)
- **Auth / email / cron:** [Supabase](https://supabase.com/pricing) · [Clerk](https://clerk.com/pricing) · [Auth0](https://auth0.com/pricing) · [Firebase](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans) · [Resend](https://resend.com/pricing) · [Upstash QStash](https://upstash.com/pricing/qstash)

> Some vendor pages are JS-gated; a few figures (MongoDB M0 512 MB, Zilliz/Weaviate exact
> vector caps, Jina/Mistral quotas, new Deno Deploy tier) are widely-documented but should
> be reconfirmed in-browser. Quotas change often — treat every number as a June 2026
> snapshot.

---

*Part of [Awesome Free Compute 2026](./README.md). PRs welcome — correct a stale quota,
add a tier, flag a commercial-use trap.*
