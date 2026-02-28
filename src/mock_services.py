from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1


def _stable_id(*parts: str) -> str:
    digest = sha1("|".join(parts).encode("utf-8")).hexdigest()
    return digest[:12]


@dataclass(frozen=True)
class MusicGenerationResult:
    track_id: str
    prompt: str
    style: str
    duration_sec: int
    estimated_cost_usd: float
    quality_score: float
    audio_url: str


@dataclass(frozen=True)
class StemSeparationResult:
    vocals_url: str
    instrumental_url: str
    confidence: float


@dataclass(frozen=True)
class VoiceConversionResult:
    converted_vocals_url: str
    target_artist: str
    preserve_timing: bool
    confidence: float


@dataclass(frozen=True)
class MixResult:
    output_url: str
    loudness_lufs: float


class MockMusicGenerationService:
    """Deterministic mock that simulates text-to-music generation."""

    def generate(self, prompt: str, style: str, duration_sec: int) -> MusicGenerationResult:
        track_id = f"song_{_stable_id(prompt, style, str(duration_sec))}"
        estimated_cost_usd = round(0.015 * duration_sec, 4)
        quality_score = min(0.99, round(0.6 + (len(prompt) / 600), 3))
        return MusicGenerationResult(
            track_id=track_id,
            prompt=prompt,
            style=style,
            duration_sec=duration_sec,
            estimated_cost_usd=estimated_cost_usd,
            quality_score=quality_score,
            audio_url=f"https://mock.scate.ai/audio/{track_id}.wav",
        )


class MockStemSeparationService:
    """Simulates source separation into vocals and instrumental stems."""

    def separate(self, source_audio_url: str) -> StemSeparationResult:
        sid = _stable_id(source_audio_url)
        return StemSeparationResult(
            vocals_url=f"https://mock.scate.ai/stems/{sid}_vocals.wav",
            instrumental_url=f"https://mock.scate.ai/stems/{sid}_instrumental.wav",
            confidence=0.93,
        )


class MockVoiceConversionService:
    """Simulates voice-timbre conversion while preserving rhythm."""

    def convert(
        self,
        vocals_url: str,
        target_artist: str,
        preserve_timing: bool,
    ) -> VoiceConversionResult:
        vid = _stable_id(vocals_url, target_artist, str(preserve_timing))
        return VoiceConversionResult(
            converted_vocals_url=f"https://mock.scate.ai/voice/{vid}.wav",
            target_artist=target_artist,
            preserve_timing=preserve_timing,
            confidence=0.9 if preserve_timing else 0.84,
        )


class MockMixingService:
    """Simulates final vocal+instrumental mixing."""

    def mix(self, instrumental_url: str, converted_vocals_url: str) -> MixResult:
        mid = _stable_id(instrumental_url, converted_vocals_url)
        return MixResult(
            output_url=f"https://mock.scate.ai/final/{mid}.wav",
            loudness_lufs=-14.0,
        )
