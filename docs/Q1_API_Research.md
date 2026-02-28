# Q1 - Model and API Research (as of February 28, 2026)

## 1) Music generation options

| Option | Output quality | Latency / speed | Cost | Usage constraints | Scalability |
| --- | --- | --- | --- | --- | --- |
| Google Vertex AI `Lyria 2` | High-quality instrumental clips; strong prompt adherence for genre/mood/instrument mix | Docs state typical generation in ~10-20s per clip | `$0.06` per 30s output clip | Instrumental only, US-English prompt input, clip-based output (around 30s) | Built on Vertex AI infra; production-friendly if quotas and regional deployment are planned |
| ElevenLabs `Eleven Music API` | High-fidelity tracks, supports vocals + lyrics + section editing workflows | Batch-style generation; processing proportional to track length | Business API list price starts around `$0.28/min` for music generation | 3s-5min duration constraints; paid tier required for API use; commercial terms vary by plan/use-case | Strong API/SDK ecosystem; suitable for consumer product integration at scale |
| Mubert Music API | Practical for app embedding: text/image/BPM to royalty-safe tracks; strong UGC orientation | Supports instant-feel streaming (3s buffer, WebRTC sub-second stream mode) | Published tiers: `$49`/100 generations, `$199`/5,000, `$499`/30,000 | Plan-gated features (e.g., sublicensing/export), generation quotas by tier | Good for large UGC/streaming contexts because pricing and usage units are explicit |

## 2) Voice cloning / cover generation options

| Option | Output quality | Latency / speed | Cost | Usage constraints | Scalability |
| --- | --- | --- | --- | --- | --- |
| ElevenLabs `Voice Changer` | Very strong emotional carryover and naturalness for speech-to-speech transformation | Fast processing; optimized for near-real-time usage | Business API list price starts around `$0.12/min` | API billing in credits; long files should be chunked under 5 minutes per request | Mature API platform, voice library, and operational tooling |
| Resemble AI `Speech-to-Speech / Voice Changer` | Strong for real-time transformation and custom voice workflows | Marketing/docs indicate ultra-low latency mode (~100ms claim for real-time changer) | Flex pricing shows `$0.0005/sec` (~`$0.03/min`) for AI voice changer | Business plan needed for some low-latency channels (e.g., WebSocket on certain features) | Enterprise controls include concurrency upgrades, SSO, and on-prem options |
| OpenVoice V2 (self-hosted model) | Good zero-shot cloning with multilingual support; quality depends on your inference setup | Depends on your infra and optimization (GPU, quantization, batch sizing) | No per-minute vendor fee (MIT open-source); infra/GPU ops cost is yours | You own compliance, safety, and abuse prevention controls | Highly scalable with your own infra but requires ML/MLOps ownership |

## 3) Recommended stack for this case

1. Original music generation:
   - Primary: `Eleven Music API` (if vocals are required directly from one model).
   - Alternative: `Lyria 2` for instrumental base + downstream vocal stack.
2. AI voice/cover generation:
   - `Stem separation` -> `Voice conversion` (ElevenLabs or Resemble) -> `Mix/master`.
3. Reliability fallback:
   - Keep an open-source path (`OpenVoice V2`) for cost control and vendor redundancy.

## 4) Why this stack matches product goals

- Product-first UX: fast enough for iterative creation with controllable prompt behavior.
- Cost/performance tuning: can route premium or long-form requests by user tier.
- Compliance readiness: commercial terms and content constraints are explicit in paid APIs.

## Sources

- Google Lyria docs and limits: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/music/generate-music
- Google Vertex Generative AI pricing (Lyria): https://cloud.google.com/vertex-ai/generative-ai/pricing
- Mubert API product + pricing: https://mubert.com/api
- Mubert developer use case details: https://mubert.com/use-cases/developers
- ElevenLabs music capability docs: https://elevenlabs.io/docs/overview/capabilities/music
- ElevenLabs Music API release note: https://elevenlabs.io/blog/eleven-music-now-available-in-the-api
- ElevenLabs API pricing page: https://elevenlabs.io/pricing/api
- ElevenLabs Voice Changer docs: https://elevenlabs.io/docs/capabilities/voice-changer
- Resemble pricing: https://www.resemble.ai/pricing/
- Resemble speech-to-speech docs: https://docs.app.resemble.ai/docs/speech_to_speech/
- Resemble voice changer page: https://www.resemble.ai/voice-changer/
- OpenVoice repository: https://github.com/myshell-ai/OpenVoice
