# 🎙️ The Free Audio Generation Guide (2026)

> Music · voice (TTS + cloning) · transcription — the **$0** stack for a solo
> creator who **monetizes**, with a hard focus on the thing every other list
> glosses over: **commercial licensing**.

**Verified June 2026.** Numbers and licenses change fast. Claims are marked
**✅ verified** (read from a primary source — pricing page, license file, or model
card) or **⚠️ verify** (page was JS/login-gated or the free-plan detail wasn't
exposed). Researched with a multi-model sweep (GPT-5.5, Gemini 3.1 Pro, Claude
Opus 4.8) and reconciled against official sources.

This is a companion to the main [Awesome Free Compute](./README.md) list and the
[Free Token-Maxxing Guide](./TOKEN-MAXXING.md) (LLMs/tokens). This file is the
**audio** half: anything you'd need to score, narrate, and caption a video for $0.

---

## Contents

- [TL;DR](#tldr)
- [The licensing landmines](#the-licensing-landmines)
- [1. Music generation](#1-music-generation)
- [2. Text-to-speech and voice cloning](#2-text-to-speech-and-voice-cloning)
- [3. Transcription and subtitles](#3-transcription-and-subtitles)
- [4. Free GPU to run it all](#4-free-gpu-to-run-it-all)
- [5. The $0 creator pipeline](#5-the-0-creator-pipeline)
- [Sources](#sources)

---

## TL;DR

The $0 audio stack for a creator who needs **commercial** rights:

| Need | Use | Why |
|---|---|---|
| 🎵 **Free + commercial full songs (with vocals)** | **ACE-Step** (Apache-2.0) on free GPU | The only open full-song model with vocals **and** a clean commercial license; runs on ~8 GB. |
| 🎹 **Free commercial instrumental, zero setup** | **Adobe Firefly Generate Soundtrack** (2 lifetime free) or **Stable Audio Open** (<$1M rev) | Hosted, royalty-free, WAV, YouTube-monetizable — but Firefly free = only 2 generations. |
| 🗣️ **Free TTS narration (incl. Hindi/Hinglish)** | **Azure Speech F0** (0.5M chars/mo) or **Google Cloud TTS** (1M chars/mo) | Perpetual free tier, full commercial rights, excellent `hi-IN`/`en-IN` voices. |
| 🧬 **Free + commercial voice cloning** | **GPT-SoVITS** / **F5-TTS** / **CosyVoice** (MIT/Apache) | Clone *your own* voice once, reuse forever, monetize legally. (Avoid XTTS-v2 + Fish Speech.) |
| 📝 **Free transcription + karaoke timestamps** | **WhisperX** (self-host) or **Groq Whisper** (hosted) | WhisperX = word-level alignment + diarization for lyric/subtitle timing. |
| 🇮🇳 **Best free Hindi/Hinglish STT** | **Azure continuous LID `[hi-IN,en-IN]`** or **Deepgram Nova-3 `multi`** | The two options that actually document Hindi *code-switching*. |
| ♾️ **Unlimited + offline (Mac)** | **whisper.cpp / MLX-Whisper / faster-whisper** + **Kokoro / Piper** TTS | MIT, on-device on Apple Silicon, no quota, private. |

**One-liner:** *Song → ACE-Step (or Firefly for an instrumental bed). Voice →
Azure F0 / Kokoro, clone your own voice with GPT-SoVITS. Captions & lyric timing →
WhisperX. Hinglish → Azure LID or Deepgram Nova-3. All $0, all commercial-clean.*

---

## The licensing landmines

For a monetized channel, **"free to use" almost never means "free to monetize."**
These are the traps that look free but are **not** commercially usable on their
free/open terms:

| ⚠️ Looks free, isn't commercial | Why | What it blocks |
|---|---|---|
| **Suno** free/Basic plan | ✅ Suno **owns** the song; personal/non-commercial only; **not retroactive** when you upgrade | Monetized YouTube |
| **Meta MusicGen / AudioGen / MAGNeT** | ✅ weights are **CC-BY-NC 4.0** | Any commercial output |
| **Coqui XTTS-v2** | ✅ **CPML** is a non-commercial model license | Monetized narration/cloning |
| **Fish Speech / OpenAudio** | ✅ research license — "commercial use requires a separate license" | Monetized narration/cloning |
| **ElevenLabs** free tier & **Scribe** free | ✅ commercial license only from Starter ($5/mo) | Monetized VO + transcripts |
| **Soundful** free/Standard, **Loudly** free | ✅ commercial rights are paid-plan only | Monetized music |
| **NVIDIA Parakeet / Canary** (STT) | License is fine (CC-BY-4.0) but **no Hindi** | Hindi/Hinglish work |

**Green-light — free *and* commercial:** ACE-Step (Apache-2.0), YuE (Apache-2.0),
Stable Audio Open / Open Small (under $1M revenue), Adobe Firefly Generate
Soundtrack, Azure Speech F0, Google Cloud TTS, Kokoro / Piper / F5-TTS /
GPT-SoVITS / CosyVoice (MIT/Apache), and the whole Whisper family (MIT) +
AI4Bharat IndicConformer (MIT).

---

## 1. Music generation

### 1.1 Open weights — self-host = truly free + commercial

The cleanest commercial path. Run them on a free Colab T4, Kaggle, HF ZeroGPU, or
a beefy local GPU (see [§4](#4-free-gpu-to-run-it-all)).

| Model | License | Vocals? | Max length | VRAM | Free GPU? |
|---|---|---|---|---:|---|
| **ACE-Step v1 (3.5B)** 🥇 | **Apache-2.0** ✅ | **Yes** | ~4 min coherent | **~8 GB** with `--cpu_offload` | ✅ Colab T4 / Kaggle / HF Space |
| **YuE** | **Apache-2.0** ✅ (attribution encouraged) | **Yes, full songs** | several min (30s segments) | 24 GB (≤2 sessions); 80 GB for full | ⚠️ marginal on T4; ZeroGPU/quantized UI |
| **Stable Audio Open 1.0** | Stability Community ✅ (<$1M rev, register) | No realistic vocals | **47 s** | 16–48 GB ideal | ⚠️ short runs on T4; ZeroGPU safer |
| **Stable Audio Open Small** | Stability Community ✅ (<$1M rev) | No vocals | **11 s** | low | ✅ T4 / ZeroGPU |
| **Meta MusicGen / MAGNeT** | ⚠️ **CC-BY-NC 4.0** | No vocals | 10–30 s | small models fit T4 | ✅ but **non-commercial** |

> **Pick:** **ACE-Step** is the standout — Apache-2.0, generates a full song with
> vocals from lyrics + a style prompt, duration control, lyric editing/remix, and
> a memory-optimized path down to ~8 GB. Ready-made free Space:
> `huggingface.co/spaces/ACE-Step/ACE-Step`. Use **your own lyrics**, keep the
> project files, and run a similarity check before publishing.

### 1.2 Hosted apps with free tiers

| App | Free allowance | Vocals? | Commercial on free? | Notes |
|---|---|---|---|---|
| **Adobe Firefly — Generate Soundtrack** 🥇 | **2 lifetime** free premium uses ✅ | No (instrumental) | **✅ Yes** — royalty-free, YouTube/TikTok OK | 5 s–5 min, WAV export, Content Credentials attached. Cleanest hosted $0 commercial path, but only 2 generations. |
| **Suno** | free/Basic exists | Yes | **❌ No** — Suno owns; non-commercial | Make the song *on a paid plan* if you want to monetize it. |
| **Soundful** | Standard/free | Mostly instrumental | **❌ No** | Standard tracks explicitly not for commercial use. |
| **Loudly** | free tier | Yes | **❌ No** (paid-only rights) | License grants monetization under paid plans. |
| **Stable Audio (hosted)** | free plan, monthly | Instrumental/SFX | ⚠️ unverified for free | Use **Stable Audio Open** self-host for clear rights. |
| **Mubert / SOUNDRAW / Beatoven** | varies | Instrumental/loops | ⚠️ unverified for free | SOUNDRAW's "All Plans" license is promising but its free-plan schedule wasn't exposed; verify in-app at download. |
| **Google MusicFX** | free experimental | n/a | ⚠️ unclear | No published commercial-output license; not recommended for monetized music. |

### 1.3 Chinese music apps — caveat

Mureka (Kunlun SkyMusic), Tiangong SkyMusic, Haimian Music (ByteDance), Tencent
Lingyin/TME, NetEase Tianyin, ACE Studio. Marketing often claims "full commercial
rights," but the free-plan ToS were **JS/PDF/login-gated and could not be verified
this pass**, and several need a **+86 phone number**. For a monetizing creator,
**prefer the open ACE-Step model** — its Apache-2.0 license is unambiguous, versus
trusting an in-app license you can only read at generation time.

**Verdict (music):** ① **ACE-Step** (open, Apache-2.0, vocals, free GPU) → ②
**YuE** if you need richer vocal songs and can find a 24 GB+ free GPU → ③ **Adobe
Firefly Generate Soundtrack** for a quick commercial-safe instrumental bed.
**Avoid for monetized YouTube:** Suno free, Soundful/Loudly free, MusicGen.

---

## 2. Text-to-speech and voice cloning

### 2.1 Hosted free tiers

| Engine | Free quota | Hindi/Hinglish | Commercial on free? | Notes |
|---|---|---|---|---|
| **Azure Speech F0** 🥇 | **0.5M chars/mo** neural ✅, perpetual | Excellent (`hi-IN` Swara/Madhur, `en-IN`) | **✅ Yes**, no watermark | Best $0 narration; you already use it. |
| **Google Cloud TTS** | **1M chars/mo** ✅ (Standard/WaveNet/Neural2) | Strong `hi-IN` | **✅ Yes**, no attribution | Highest perpetual free quota. |
| **Amazon Polly** | 1M neural chars/mo, **first 12 mo only** | Good | ✅ Yes (then expires) | Free-tier clock runs out after a year. |
| **ElevenLabs** | 10k chars/mo | Excellent | **❌ No** (+ attribution) | Commercial unlocks at Starter $5/mo. |
| **PlayHT / Murf / Speechify** | trial / very limited | Good | ❌ No | Free tiers prohibit commercial use. |
| **Deepgram Aura / Cartesia / Resemble** | sign-up credit | English-led | ✅ until credit ends | No perpetual commercial free tier. |

### 2.2 Open weights — free + commercial

Run on a free Colab T4, HF ZeroGPU, or locally on an Apple Silicon Mac (many run
on **CPU**).

| Model | License | Cloning? | Hindi/multiling | Runs on |
|---|---|---|---|---|
| **Kokoro-82M** 🥇 | **Apache-2.0** ✅ | No (uses voice embeddings) | Hindi added in v1.0 | **CPU** + any GPU; tiny |
| **Piper** | **MIT** ✅ | No (fine-tune) | **native Hindi voices** | **CPU**-optimized, edge |
| **F5-TTS** 🥇 | **MIT** ✅ | **Yes** (15s zero-shot) | cross-lingual | Mac / Colab T4 |
| **GPT-SoVITS** 🥇 | **MIT** ✅ | **Yes** (1-min few-shot, best) | cross-lingual (EN→Hindi) | Apple Silicon / T4 |
| **CosyVoice / CosyVoice2** (Alibaba) | **Apache-2.0** ✅ | **Yes** (3s zero-shot) | cross-lingual | CPU/GPU |
| **MeloTTS** | **MIT** ✅ | No | no Hindi (EN/ZH/ES/FR/KR/JP) | **CPU** fast |
| **Suno Bark** | **MIT** ✅ | audio-prompt only | multilingual | needs GPU |
| **Coqui XTTS-v2** | ⚠️ **CPML non-commercial** | Yes (6s) | native Hindi | — *don't monetize* |
| **Fish Speech** | ⚠️ research license | Yes (10s) | yes | — *don't monetize* |

### 2.3 Hindi/Hinglish + cloning legality

- **Best Hindi/Hinglish narration:** hosted **Azure F0** or **Google Cloud TTS** —
  they handle code-switched, transliterated text far better than most open models.
- **Best $0 local:** **Kokoro** (narration) and **GPT-SoVITS** (clone your own
  voice once, then unlimited Hindi/Hinglish output, MIT, monetizable).
- **Cloning legality:** open models won't stop you cloning anyone — but monetizing
  someone else's voice violates rights of publicity/likeness. **Only clone your
  own voice** (or one you have written permission for). YouTube also requires
  disclosure of realistic AI-generated content.

**Verdict (voice):** narration → **Azure F0 / Google TTS** (hosted) or **Kokoro**
(local); cloning → **GPT-SoVITS** (best, MIT) or **F5-TTS / CosyVoice** for
short-sample zero-shot. **Avoid XTTS-v2 and Fish Speech** for monetized work.

---

## 3. Transcription and subtitles

### 3.1 Open weights — self-host on free GPU/Mac

| Engine | License | Hindi/code-switch | Timestamps / diarization | Runs on |
|---|---|---|---|---|
| **Whisper large-v3 / turbo** | **MIT** ✅ | Hindi ✅; Hinglish ~OK | segment native | Colab/Kaggle; Mac |
| **faster-whisper** (CTranslate2) | **MIT** ✅ | = Whisper | **word ✅** | CPU int8 on Mac; T4 (~2.9 GB) |
| **WhisperX** 🥇 | **BSD-2** ✅ | = Whisper + Hindi wav2vec2 align | **word ✅ + diarization ✅** | Mac CPU int8; T4 |
| **whisper.cpp** | **MIT** ✅ | = Whisper | word ✅ | **Apple Silicon (Metal/CoreML)** |
| **MLX-Whisper** | **MIT** ✅ | = Whisper | word ✅ | **Apple Silicon (MLX)** |
| **AI4Bharat IndicConformer 600M** | **MIT** ✅ | **Hindi + 22 Indian langs** (Devanagari) | CTC timestamps | GPU/CPU |
| **NVIDIA Parakeet / Canary** | CC-BY-4.0 ✅ | ⚠️ **no Hindi** (EN/European) | word ✅ | GPU (NeMo/CUDA) |
| **distil-whisper** | MIT | ⚠️ **English-only** | word ✅ | any |

> **Key finding:** the models at the *top of the English ASR leaderboard* — NVIDIA
> Parakeet/Canary, IBM Granite, Cohere — **do not support Hindi**. For Hinglish,
> **Whisper large-v3** (via faster-whisper/WhisperX) is the best free open engine.

### 3.2 Hosted free tiers / credits

| Service | Free | Hindi/code-switch | Diarization | Commercial? |
|---|---|---|---|---|
| **Groq** Whisper-v3/turbo | free tier, 25 MB file cap, fast | Hindi ✅ (Whisper) | no | ✅ |
| **Deepgram** Nova-3 🥇 | **$200 credit**, no card | **`hi` + `multi` code-switch** ✅ | ✅ | ✅ |
| **AssemblyAI** | **$50 credit**, no card | Universal-2 Hindi (10–25% WER) | ✅ (+$0.02/hr) | ✅ |
| **Azure Speech F0** | **~5 audio-hr/mo** ⚠️ | **continuous LID `[hi-IN,en-IN]`** ✅ | ✅ (batch) | ✅ |
| **Google Cloud STT** | **$300/90d** + ~60 min/mo ⚠️ | `hi-IN` + Indian langs | ✅ | ✅ |
| **ElevenLabs Scribe** | 10k credits/mo | 90+ langs | ✅ (≤32 spk) | **❌ free = non-commercial** |

### 3.3 Hindi / Hinglish — the hard case

Casual Hindi-English code-switch is the toughest case (plain local Whisper
struggles). Ranked free options:

1. **Azure continuous LID `[hi-IN,en-IN]`** — verified-good, per-segment language
   switching, ~5 free hrs/mo. (Your existing baseline.)
2. **Deepgram Nova-3 `multi`** — the only *hosted free-credit* option that
   explicitly documents Hindi **plus** code-switching ($200 credit).
3. **Self-host Whisper large-v3** (faster-whisper/WhisperX) for unlimited free
   Hinglish; **AI4Bharat IndicConformer** or **IIT-Madras whisper-hindi** for
   *clean Devanagari* Hindi (these are weaker on English mixing).

### 3.4 Subtitles & karaoke timing

**WhisperX** is the best free tool: word-level forced alignment + speaker
diarization + subtitle export, on Colab or Mac. For Hindi songs, pair it with a
**Hindi wav2vec2** alignment model. Mac-local alternatives with word timings:
**faster-whisper** (`word_timestamps=True`), **MLX-Whisper**, **whisper.cpp**.

**Verdict (STT):** general → self-host **Whisper large-v3** (or **Groq** for zero
setup); Hindi/Hinglish → **Azure LID** / **Deepgram Nova-3**; karaoke timing →
**WhisperX**.

---

## 4. Free GPU to run it all

The open music/voice/STT models above are commercial-clean **only if you self-host**
— and you can do that for $0:

- **HF Spaces / ZeroGPU** — using existing ZeroGPU Spaces (ACE-Step, MusicGen,
  Whisper demos) is free; authenticated free accounts get **~5 min GPU/day** on a
  48 GB Blackwell slice (PRO = 40 min). Great for one-off generations.
- **Google Colab (free)** — ~16 GB **T4**. Comfortable for ACE-Step (offload),
  Stable Audio Open Small, MusicGen-small, and faster-whisper/WhisperX large-v3.
- **Kaggle Notebooks (free)** — weekly GPU quota (T4×2 / P100); best for batch
  transcription or longer renders. Verify the current quota in your account.
- **Mac-local (Apple Silicon)** — fully offline, unlimited minutes, private:
  **whisper.cpp / MLX-Whisper / faster-whisper** (STT) and **Kokoro / Piper**
  (TTS) all run well on an M-series CPU/GPU.

For more on these venues (and serverless GPU like Modal), see the main
[Awesome Free Compute](./README.md#2-free-gpu-notebooks--sessions) list.

---

## 5. The $0 creator pipeline

End-to-end for a music-video creator, every step commercial-clean and free:

1. **Song** — **ACE-Step** (Apache-2.0) on a free GPU for a full track with
   vocals from your own lyrics; *or* **Adobe Firefly Generate Soundtrack** for a
   quick instrumental bed.
2. **Narration / VO** — **Azure Speech F0** Hindi/Indian-English voices (0.5M
   chars/mo), or **Kokoro** locally for unlimited.
3. **Your signature voice** — clone *your own* voice once with **GPT-SoVITS**
   (MIT), then reuse it forever for hooks/VO.
4. **Lyric timing / karaoke captions** — **WhisperX** word-level timestamps on the
   vocal stem.
5. **Hinglish transcription / subtitles** — **Azure continuous LID
   `[hi-IN,en-IN]`** (your baseline) or **Deepgram Nova-3 `multi`** ($200 credit).

Total cost: **$0**. Total commercial exposure: **none**, as long as you stick to
the green-light tools in [the licensing landmines](#the-licensing-landmines).

---

## Sources

Primary sources fetched/verified June 2026 (representative):

- **Music — open weights:** `github.com/ace-step/ACE-Step` + `huggingface.co/ACE-Step/ACE-Step-v1-3.5B` (Apache-2.0); `github.com/multimodal-art-projection/YuE` (Apache-2.0); `huggingface.co/stabilityai/stable-audio-open-1.0` + `/stable-audio-open-small` + `stability.ai/license`; `huggingface.co/facebook/musicgen-small` (CC-BY-NC).
- **Music — hosted:** `adobe.com/products/firefly/features/ai-music-generator.html` (2 lifetime, commercial); `help.suno.com/en/articles/2746945` + `suno.com/terms` (free = non-commercial); `soundful.com/pricing` + `/license`; `loudly.com/license-agreement`.
- **TTS — hosted:** `azure.microsoft.com/pricing/details/speech` (F0 0.5M chars/mo); `cloud.google.com/text-to-speech/pricing` (1M chars/mo); `elevenlabs.io/pricing` (free non-commercial); `aws.amazon.com/polly/pricing`.
- **TTS — open weights:** `huggingface.co/hexgrad/Kokoro-82M` (Apache-2.0); `github.com/SWivid/F5-TTS` (MIT); `github.com/RVC-Boss/GPT-SoVITS` (MIT); `github.com/FunAudioLLM/CosyVoice` (Apache-2.0); `coqui/XTTS-v2` (CPML, non-commercial); `github.com/fishaudio/fish-speech` (research license); Piper / MeloTTS / Bark (MIT).
- **STT — open weights:** `github.com/openai/whisper` (MIT); `github.com/SYSTRAN/faster-whisper`; `github.com/m-bain/whisperX`; `github.com/ggml-org/whisper.cpp`; `huggingface.co/nvidia/parakeet-tdt-0.6b-v2` + `/canary-1b-flash` (CC-BY-4.0, no Hindi); `huggingface.co/ai4bharat/indic-conformer-600m-multilingual` (MIT); `huggingface.co/spaces/hf-audio/open_asr_leaderboard`.
- **STT — hosted:** `console.groq.com/docs/speech-to-text`; `deepgram.com/pricing` + `developers.deepgram.com` (Nova-3 `multi` Hindi); `assemblyai.com/pricing`; `learn.microsoft.com/azure/ai-services/speech-service/language-identification` (continuous LID); `cloud.google.com/speech-to-text/pricing`; `elevenlabs.io/pricing/api` (Scribe).
- **Free GPU:** `huggingface.co/docs/hub/spaces-zerogpu`; `research.google.com/colaboratory/faq.html`; `kaggle.com/docs/notebooks`.

*Quotas/licenses are point-in-time (June 2026) and change frequently — verify the
free-plan terms at signup/download before relying on them, especially for
**commercial** use. Corrections via PR welcome.*
