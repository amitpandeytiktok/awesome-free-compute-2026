# 🎬 The Free Media Post-Production Guide (2026)

> *Generating* media is solved. This is the **finishing** half — upscale to 4K,
> smooth to 60fps, split stems, master to loudness spec, subtitle, and dub — all
> for **$0** and, because you **monetize**, all filtered hard on **commercial
> licensing**.

**Verified June 2026.** Claims are **✅ verified** (read from a primary source —
GitHub `LICENSE`, model card, or pricing page) or **⚠️ verify** (page was JS/login
-gated). Researched with a multi-model sweep (GPT-5.5, Gemini 3.1 Pro, Claude Opus
4.8) and reconciled against official sources. Companion to the
[Awesome Free Compute](./README.md) list, the [Token-Maxxing Guide](./TOKEN-MAXXING.md)
(image/video *generation*), and the [Audio Generation Guide](./AUDIO.md). This file
is the **post / finishing** layer that takes generated media to publish-ready.

---

## Contents

- [TL;DR](#tldr)
- [The licensing landmines](#the-licensing-landmines)
- [1. Video finishing](#1-video-finishing)
- [2. Audio finishing](#2-audio-finishing)
- [3. Translation, subtitles, dubbing](#3-translation-subtitles-dubbing)
- [4. The $0 finishing pipelines](#4-the-0-finishing-pipelines)
- [Sources](#sources)

---

## TL;DR

| Need | Use (commercial-safe) | Notes |
|---|---|---|
| 🔍 **4K upscale** | **Real-ESRGAN** (BSD-3) via **Upscayl** (Mac app) | Native Apple Silicon, no setup. |
| 🎞️ **Smooth 60fps** | **Google FILM** (Apache-2.0) | RIFE is faster but its *weights* license is disputed — see landmines. |
| 🙂 **Face restore** | **GFPGAN** / **RestoreFormer** (Apache-2.0) | **Not** CodeFormer (non-commercial). |
| 🎚️ **Stems / karaoke** | **Demucs** (MIT) via **UVR5** GUI (MPS on Mac) | SOTA open separation, clean license. |
| 🧹 **Vocal cleanup** | **DeepFilterNet** (MIT/Apache) / **Resemble Enhance** (MIT) | 48 kHz denoise, real-time on CPU. |
| 🎛️ **Mastering + loudness** | **Matchering** (GPL) + **ffmpeg `loudnorm`** → −14 LUFS | Output is 100% yours to monetize. |
| 🌐 **Translate (Indian langs)** | **IndicTrans2** (MIT) or **Azure Translator F0** (2M chars/mo) | The two best commercial-clean routes. |
| 📝 **Subtitles** | **Whisper** → translate → **Subtitle Edit** (MIT) | Burn with ffmpeg. |
| 🗣️ **Dub (voice-preserving)** | **OpenVoice** (MIT) + commercial TTS | SeamlessM4T/NLLB are non-commercial. |

**One-liner:** *Audio → Demucs → Matchering → ffmpeg `loudnorm` −14 LUFS. Video →
Upscayl (Real-ESRGAN 4×) → chaiNNer (FILM/RIFE → 60fps) → DaVinci Resolve. Reach →
Whisper → IndicTrans2/Azure → Subtitle Edit → OpenVoice dub. All $0, all clean.*

> **License = output, not just tool.** With **MIT / BSD / Apache / GPL** tools, the
> *media you output* (your masters, videos, subtitles) is **100% yours to monetize**.
> GPL copyleft only governs redistributing the *software*, never your render.

---

## The licensing landmines

The whole reason this guide leads with licensing: most "free" restoration and
translation models are **research/non-commercial**, and several are silently
bundled into the free GUIs everyone uses.

### ⚠️ Non-commercial — do NOT use on monetized output

| Tool | Restriction | Domain |
|---|---|---|
| **SUPIR** | academic / non-commercial license | Upscaling |
| **CodeFormer** | NTU **S-Lab License 1.0** (research only) — *bundled in most WebUIs; untick it* | Face restore |
| **Practical-RIFE** *weights* | code is MIT but the **weights' commercial status is disputed/version-dependent** | 60fps interpolation |
| **Open-Unmix `umxl`** (default model) | **CC BY-NC-SA 4.0** | Stem separation |
| **SeamlessM4T v2** · **NLLB-200** · **Aya Expanse** · **TowerInstruct** | **CC-BY-NC** | Translation / dubbing |
| **Coqui XTTS-v2** | CPML (non-commercial, incl. outputs) | Dubbing voice |
| **ElevenLabs** free tier | commercial license only from Starter ($5/mo) | Dubbing voice |
| ❔ **Mel-Band Roformer / many MDX-Net checkpoints** | code MIT but **weights often have *no stated license*** — treat as unverified | Stem separation |

### ✅ Green-light — free *and* commercial

Real-ESRGAN (BSD-3), SwinIR / BSRGAN (Apache), APISR (GPL-3), GFPGAN /
RestoreFormer / DDColor (Apache), **Google FILM / FLAVR / IFRNet** (Apache/MIT),
**Upscayl** (AGPL), **chaiNNer** (GPL), **DaVinci Resolve** Free · **Demucs** (MIT),
**DeepFilterNet** (MIT/Apache), Resemble Enhance / VoiceFixer (MIT), RNNoise (BSD),
**Matchering** (GPL), **ffmpeg** / **Audacity** · **IndicTrans2** (MIT), Opus-MT /
**MADLAD-400** (Apache), **Azure Translator F0** / **DeepL Free** / **Google
Translation** free tiers, **Whisper** (MIT), Subtitle Edit / Aegisub, **OpenVoice**
(MIT).

---

## 1. Video finishing

Goal: take a 1080p/30fps AI render to a **4K / 60fps** master, commercial-clean, on
an Apple Silicon Mac (or free Colab/Kaggle).

### 1.1 Upscaling / super-resolution

| Model | License | Commercial? | Notes |
|---|---|---|---|
| **Real-ESRGAN** 🥇 | BSD-3-Clause | ✅ | Fast, low VRAM (runs on 8 GB Macs); the default. Image + video variants. |
| **SwinIR / BSRGAN** | Apache-2.0 | ✅ | Heavier, more natural textures (less "plastic"); MPS on Mac. |
| **APISR** | GPL-3.0 | ✅ (output yours) | Best for anime / line-art renders; wants 32 GB+ unified memory. |
| **SUPIR** | ⚠️ custom **non-commercial** | ❌ | Stunning detail, but **legally radioactive** for monetized work + 24 GB VRAM. Skip. |

### 1.2 Frame interpolation → 60fps

| Model | License | Commercial? | Notes |
|---|---|---|---|
| **Google FILM** 🥇 | Apache-2.0 | ✅ | Unambiguously safe; great on large motion (can wobble backgrounds). The pick for monetized 60fps. |
| **Practical-RIFE** | code MIT; **weights disputed** | ⚠️ verify | Fastest + smoothest (NCNN on Apple Silicon). Some sources say v4.x weights are MIT, others "research only" — **verify your exact version**, or use FILM. |
| **FLAVR / IFRNet** | Apache-2.0 / MIT | ✅ | Solid, but lack the polished Mac/NCNN GUIs RIFE has. |

### 1.3 Face & video restoration

| Model | License | Commercial? | Notes |
|---|---|---|---|
| **GFPGAN** 🥇 | Apache-2.0 | ✅ | Fixes mangled AI faces; can over-smooth skin. Legally bulletproof. |
| **RestoreFormer** | Apache-2.0 | ✅ | Slightly more natural texture than GFPGAN. |
| **DDColor** | Apache-2.0 | ✅ | Colorize B&W/archival-style footage. |
| **CodeFormer** | ⚠️ **NTU S-Lab (non-commercial)** | ❌ | Best quality — but **bundled into nearly every WebUI/node graph. Actively untick it** on a monetized channel. |

### 1.4 Free Mac apps / GUIs (no code)

- **Upscayl** (AGPL) — native Apple-Silicon upscaler app; bundles Real-ESRGAN +
  Remacri; Vulkan/NCNN GPU. The easy button for 4K.
- **chaiNNer** (GPL) — node-based editor; drag `.pth` models (SwinIR, RIFE, GFPGAN)
  into a flowchart. The **most powerful Mac-native** option; runs RIFE via PyTorch/MPS.
- **DaVinci Resolve** (Free) — commercial use allowed; final color + encode to
  H.265/ProRes. Free timeline caps at 4K UHD — exactly your target.
- **Flowframes** (open) — great RIFE/FILM GUI but **Windows-only** (Parallels kills
  GPU accel on Mac); prefer chaiNNer on macOS.

> **Apple Silicon advantage:** unified memory means a 32 GB Mac effectively has
> 32 GB of "VRAM" — beating a 24 GB RTX 4090 for big 4K frames. Rough local time
> for a 3-min clip: **~1–2 h** to 4K (Real-ESRGAN) + **~15 min** to 60fps (RIFE),
> all background, $0. On an 8 GB M1, offload to **Kaggle** (30 GPU-h/wk) instead.

---

## 2. Audio finishing

Since you generate full mixes (Suno/ACE-Step), separation is optional — used for
instrumental/karaoke versions or to fix a single stem. Mastering + loudness is the
part you should always do.

### 2.1 Stem separation / karaoke

| Tool | License (code / weights) | Commercial? | Notes |
|---|---|---|---|
| **Demucs / HT-Demucs v4** 🥇 | MIT / **MIT** | ✅ | SOTA open separation (SDR 9.0). `--two-stems=vocals` → instrumental/karaoke. CPU-native on Mac (~1.5× track length). Active fork: `adefossez/demucs`. |
| **UVR5 (Ultimate Vocal Remover)** | MIT GUI / models vary | ✅ GUI; ⚠️ per-model | Mac **arm64 .dmg** with **MPS GPU**; the friendliest way to run Demucs/MDX on M-series. Also bundles Matchering. |
| **Mel-Band Roformer** | MIT code / **unstated weights** | ⚠️ | *Best* vocal isolation, but the popular checkpoints have **no license** — avoid for monetized output unless you confirm terms. |
| **Spleeter** | MIT | ✅ | Older, and ⚠️ **TensorFlow has M1 issues** — use on Colab if at all. |
| **Open-Unmix `umxl`** | MIT code / **CC BY-NC-SA** | ❌ | Default model is **non-commercial**. Don't. |

### 2.2 Denoise / cleanup (apply to an isolated vocal stem)

| Tool | License | Commercial? | Notes |
|---|---|---|---|
| **DeepFilterNet (2/3)** 🥇 | MIT *or* Apache-2.0 | ✅ | 48 kHz, real-time on CPU; ships a standalone `deep-filter` binary. |
| **Resemble Enhance** | MIT | ✅ | Denoise + restoration (44.1 kHz); free HF Space. |
| **VoiceFixer** | MIT | ✅ | Restores clipped/reverberant/noisy speech. |
| **RNNoise** | BSD-3 | ✅ | Lightweight real-time voice denoise (Audacity plugin). |
| **Adobe Podcast — Enhance Speech** | proprietary free web | ⚠️ verify | Excellent quality; commercial terms not verifiable from their SPA. |

### 2.3 Mastering & loudness

- **Matchering 2.0** (GPL-3.0) 🥇 — **reference mastering**: feed your TARGET track +
  a commercial REFERENCE song; it matches RMS, EQ, peak, and stereo width with a
  true-peak limiter. **Your master is unrestricted** (GPL governs only redistributing
  the software). `pip install matchering`, native on macOS; also in the UVR5 app.
- **ffmpeg `loudnorm`** — hit platform loudness (EBU R128) for free. **Two-pass**
  (recommended for files):

  ```sh
  # 1) measure
  ffmpeg -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
  # 2) apply the printed measured_* values
  ffmpeg -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:\
  measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true \
  -ar 48k out.wav
  ```

  ⚠️ **−14 LUFS** is the widely-cited YouTube target but is **not officially
  published** by YouTube (the AES *streaming* recommendation is −16 LUFS / −1.5 dBTP).
  Treat −14 LUFS / −1 dBTP as a sensible default, not gospel.
- **LANDR / eMastered / BandLab** free tiers — preview-only; **you must pay to
  download** a usable/commercial master. Matchering + ffmpeg beats them at $0.

### 2.4 Edit / convert

**Audacity** (GPLv3) for manual multitrack edits; **ffmpeg** for format/codec,
sample-rate, trim, normalize; **SoundTouch** / **Rubber Band** for pitch/tempo.
Output is yours.

---

## 3. Translation, subtitles, dubbing

To take Hindi/Hinglish content global — commercial-clean.

### 3.1 Translation — hosted free tiers

| Service | Free quota | Hindi/Indic | Commercial on free? |
|---|---|---|---|
| **Azure Translator F0** 🥇 | **2M chars/mo** | strong, many Indic langs | ✅ (you already use Azure) |
| **DeepL API Free** | **500k chars/mo** | now lists Hindi + Indic | ✅ (no NC clause found) |
| **Google Cloud Translation** | **500k chars/mo** + $300/90d | strong `hi` + Indic | ✅ |

### 3.2 Translation — open weights

| Model | License | Commercial? | Notes |
|---|---|---|---|
| **IndicTrans2** (AI4Bharat) 🥇 | **MIT** | ✅ | **Best commercial-clean open MT for Indian languages** (all 22). 200M distilled runs on Mac/Colab. |
| **Opus-MT / Helsinki-NLP** | MIT / Apache | ✅ | Light CPU baseline; modest hi→en quality. |
| **MADLAD-400** | Apache-2.0 | ✅ | Broad multilingual incl. Hindi; not Indic-specialized. |
| **NLLB-200 · Aya Expanse · TowerInstruct** | ⚠️ **CC-BY-NC** | ❌ | Strong, but **non-commercial** — avoid for monetized work. |

### 3.3 Subtitles

Pipeline: **Whisper / faster-whisper** (transcribe — MIT) → **IndicTrans2 / Azure**
(translate) → **Subtitle Edit** (MIT) or **Aegisub** for timing/styling/SRT →
**ffmpeg** to burn or mux. All commercial-clean. (For karaoke word-timing, see
[AUDIO.md §3.4](./AUDIO.md#34-subtitles--karaoke-timing) — WhisperX.)

### 3.4 Dubbing (the genuinely hard one)

**Fully voice-preserving, commercial-clean, $0 dubbing is still hard** — the best
speech-to-speech models (**SeamlessM4T v2, NLLB**) are **CC-BY-NC**. The clean path
is to assemble it:

1. **Transcribe** → Whisper / faster-whisper
2. **Translate** → IndicTrans2 or Azure F0
3. **Speak** → **OpenVoice** (MIT, commercial voice cloning/conversion) or a
   commercial-clean TTS (Azure F0; see [AUDIO.md §2](./AUDIO.md#2-text-to-speech-and-voice-cloning))
4. **Align / mux** → ffmpeg + manual timing in Subtitle Edit

Hosted free dubbing apps (**HeyGen ~3 videos/mo, Rask, Vozo, KapWing**) are easy but
their free-tier commercial rights/watermarks are **⚠️ unverified** — check before release.

---

## 4. The $0 finishing pipelines

Three end-to-end recipes, every step commercial-clean:

**A. Music master (audio):**
`Demucs` (optional stems/karaoke) → `DeepFilterNet` (optional vocal cleanup) →
**`Matchering`** (reference master) → **`ffmpeg loudnorm`** → −14 LUFS / −1 dBTP WAV.

**B. 4K / 60fps video master:**
**Upscayl** (Real-ESRGAN 4×) → **chaiNNer** (FILM, or RIFE if your weights verify →
60fps) → **DaVinci Resolve Free** (grade + encode H.265/ProRes). Offload to **Kaggle**
if on an 8 GB Mac.

**C. Global reach (subtitles + dub):**
**Whisper** → **IndicTrans2 / Azure F0** → **Subtitle Edit** (SRT) → *(optional)*
**OpenVoice** dub → **ffmpeg** mux.

Total cost: **$0**. Commercial exposure: **none**, as long as you stay on the
green-light tools in [the licensing landmines](#the-licensing-landmines).

---

## Sources

Primary sources fetched/verified June 2026 (representative):

- **Video — upscaling/interp/restore:** `github.com/xinntao/Real-ESRGAN` (BSD-3); `github.com/JingyunLiang/SwinIR`; `github.com/Fanghua-Yu/SUPIR` (non-commercial); `github.com/hzwer/Practical-RIFE`; `github.com/google-research/frame-interpolation` (FILM, Apache); `github.com/TencentARC/GFPGAN` (Apache); `github.com/sczhou/CodeFormer/blob/master/LICENSE` (NTU S-Lab, non-commercial).
- **Video — apps:** `github.com/upscayl/upscayl` (AGPL); `github.com/chaiNNer-org/chaiNNer` (GPL); `blackmagicdesign.com/products/davinciresolve`.
- **Audio — separation/cleanup:** `github.com/facebookresearch/demucs` + `adefossez/demucs` (MIT); `github.com/Anjok07/ultimatevocalremovergui` (MIT GUI); `github.com/sigsep/open-unmix-pytorch` (umxl = CC-BY-NC-SA); `github.com/Rikorose/DeepFilterNet` (MIT/Apache); `github.com/resemble-ai/resemble-enhance` (MIT).
- **Audio — mastering/loudness:** `github.com/sergree/matchering` (GPL-3.0); `k.ylo.ph/2016/04/04/loudnorm.html` (ffmpeg `loudnorm` two-pass); `audacityteam.org`.
- **Translation/dubbing:** `github.com/AI4Bharat/IndicTrans2` (MIT); `huggingface.co/google/madlad400-3b-mt` (Apache); `huggingface.co/Helsinki-NLP` (Opus-MT); `huggingface.co/facebook/seamless-m4t-v2-large` + `/nllb-200-distilled-600M` (CC-BY-NC); `github.com/myshell-ai/OpenVoice` (MIT); `azure.microsoft.com/pricing/details/translator` (F0 2M chars/mo); `developers.deepl.com/docs/resources/usage-limits` (500k/mo); `github.com/SubtitleEdit/subtitleedit` (MIT).

*Quotas/licenses are point-in-time (June 2026) and change — re-verify any
**non-commercial** flag and any "weights unstated" model before a commercial
release. Corrections via PR welcome.*
