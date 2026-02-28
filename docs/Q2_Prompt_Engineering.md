# Q2 - Prompt Engineering and Cross-API Comparison

## Goal

Generate a catchy pop song inspired by early-2000s aesthetics with:

- female lead vocal
- guitar-driven instrumentation
- upbeat radio energy
- clear verse-chorus structure

## 1) Master prompt (model-agnostic)

```text
Create a radio-friendly early-2000s pop song.

Style references:
- Era feel: early 2000s mainstream pop
- Lead: female vocal, expressive but clean tone
- Instruments: guitar-driven arrangement, tight drums, bright bass
- Energy: upbeat, danceable, hook-first
- Structure: Intro -> Verse 1 -> Pre-Chorus -> Chorus -> Verse 2 -> Chorus -> Bridge -> Final Chorus -> Outro

Creative direction:
- Melody should be memorable within first 20 seconds.
- Chorus must be bigger than verses and repeat a strong hook phrase.
- Keep lyrics PG, universal, and emotionally positive.
- Avoid artist-name imitation; produce an original composition.
```

## 2) API-specific prompt adaptations

### A) ElevenLabs Music API (vocals supported)

```text
Generate a 120-second pop song with female lead vocal.
Genre: early-2000s pop.
Instrumentation: guitar-led rhythm section, pop drums, bass, light synth pads.
Structure: intro 8 bars, verse, pre-chorus, chorus, verse, chorus, bridge, final chorus.
Mood: upbeat, radio-friendly, optimistic.
Lyric theme: summer-night confidence and young love.
```

### B) Google Lyria 2 (instrumental-only workflow)

```text
Generate a 30-second instrumental clip inspired by early-2000s pop.
Focus on guitar-driven rhythm, energetic drum groove, and bright major-key harmonic progression.
Make it chorus-ready and hook-heavy so a female vocal can be layered later.
```

Note: Lyria is instrumental-focused, so vocals should be produced in a second step.

### C) Mubert API (tag-oriented workflow)

```text
Prompt: upbeat early-2000s pop, guitar driven, catchy chorus energy, radio friendly, bright major key
Genre tags: pop, dance-pop
Mood tags: energetic, happy
BPM target: 118-124
```

## 3) Comparison summary

Because no paid API credentials are stored in this repo, this comparison is a practical pre-launch assessment based on official capabilities, published limits, and pricing.

| API | Output quality fit for this prompt | Cost signal | Usage/scaling notes |
| --- | --- | --- | --- |
| ElevenLabs Music | Best direct fit (female lead vocal + structure + editing controls in one system) | Medium-high per-minute economics compared to clip-based tools | Good API maturity; check plan-level minute quotas |
| Lyria 2 | Very strong instrumental quality, not direct fit for vocal requirement without second model | Transparent clip pricing (`$0.06`/30s) | Great for scalable instrumental generation and prompt iteration |
| Mubert | Strong for fast app embedding and mood/genre generation | Plan-based generation economics can be attractive at volume | Great for high-throughput consumer use, but less lyric/vocal control |

## 4) Recommended execution strategy for the case

1. Use ElevenLabs Music for full vocal song prototype.
2. Run Lyria for instrumental alternatives and A/B backing tracks.
3. Use Mubert for low-latency preview generation inside app UX.
4. Score outputs with a simple rubric:
   - Hook strength (1-5)
   - Vocal naturalness (1-5)
   - Structure clarity (1-5)
   - Mix readiness (1-5)
   - Cost efficiency (1-5)

## 5) Quick prompt variants for rapid iteration

### Variant 1 - More guitar presence
```text
Increase guitar prominence by +30%, reduce synth brightness, keep female vocal centered and energetic.
```

### Variant 2 - Stronger chorus contrast
```text
Make verses minimal and lift chorus with wider stereo instruments, stronger kick, and doubled hook vocal.
```

### Variant 3 - More radio polish
```text
Keep arrangement clean and concise, avoid long intros, deliver hook before 0:25, commercial radio pacing.
```

## Sources

- ElevenLabs music capabilities: https://elevenlabs.io/docs/overview/capabilities/music
- ElevenLabs Music API release: https://elevenlabs.io/blog/eleven-music-now-available-in-the-api
- ElevenLabs API pricing: https://elevenlabs.io/pricing/api
- Google Lyria generation docs: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/music/generate-music
- Google Vertex pricing: https://cloud.google.com/vertex-ai/generative-ai/pricing
- Mubert API: https://mubert.com/api
