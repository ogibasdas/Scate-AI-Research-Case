from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Optional

try:
    from src.mock_services import (
        MockMixingService,
        MockMusicGenerationService,
        MockStemSeparationService,
        MockVoiceConversionService,
    )
except ModuleNotFoundError:  # pragma: no cover - fallback for `py src/main.py`
    from mock_services import (  # type: ignore
        MockMixingService,
        MockMusicGenerationService,
        MockStemSeparationService,
        MockVoiceConversionService,
    )


class PipelineValidationError(ValueError):
    """Raised when a request payload is invalid."""


@dataclass(frozen=True)
class OriginalMusicRequest:
    prompt: str
    mood: str
    genre: str
    style: str
    duration_sec: int = 120
    lyrics: Optional[str] = None
    inspiration: Optional[str] = None
    include_vocals: bool = True

    def to_generation_prompt(self) -> str:
        blocks = [
            f"Create a {self.mood} {self.genre} song in {self.style} style.",
            f"Core direction: {self.prompt}",
        ]
        if self.lyrics:
            blocks.append(f"Lyrics seed: {self.lyrics}")
        if self.inspiration:
            blocks.append(f"Inspiration reference: {self.inspiration}")
        blocks.append(
            "Output should include AI lead vocals."
            if self.include_vocals
            else "Output should be instrumental only."
        )
        return " ".join(blocks)


@dataclass(frozen=True)
class VoiceCoverRequest:
    source_song_url: str
    voice_sample_url: str
    target_voice_label: str
    preserve_timing: bool = True
    preserve_melody: bool = True


@dataclass(frozen=True)
class PipelineStep:
    name: str
    status: str
    detail: str


@dataclass(frozen=True)
class PipelineResponse:
    flow: str
    output_url: str
    estimated_cost_usd: float
    quality_score: float
    steps: List[PipelineStep]

    def to_dict(self) -> dict:
        return {
            "flow": self.flow,
            "output_url": self.output_url,
            "estimated_cost_usd": self.estimated_cost_usd,
            "quality_score": self.quality_score,
            "steps": [asdict(step) for step in self.steps],
        }


class AIMusicPipeline:
    """Simple high-level pipeline implementation with deterministic mock services."""

    def __init__(
        self,
        music_service: Optional[MockMusicGenerationService] = None,
        separation_service: Optional[MockStemSeparationService] = None,
        voice_service: Optional[MockVoiceConversionService] = None,
        mixing_service: Optional[MockMixingService] = None,
    ) -> None:
        self.music_service = music_service or MockMusicGenerationService()
        self.separation_service = separation_service or MockStemSeparationService()
        self.voice_service = voice_service or MockVoiceConversionService()
        self.mixing_service = mixing_service or MockMixingService()

    def generate_original_song(self, request: OriginalMusicRequest) -> PipelineResponse:
        _validate_original_request(request)
        generation_prompt = request.to_generation_prompt()

        music = self.music_service.generate(
            prompt=generation_prompt,
            style=request.style,
            duration_sec=request.duration_sec,
        )
        steps = [
            PipelineStep("input_validation", "ok", "User prompt payload validated"),
            PipelineStep("music_generation", "ok", f"Track created: {music.track_id}"),
        ]

        if request.include_vocals:
            steps.append(
                PipelineStep(
                    "vocalization",
                    "ok",
                    "AI lead vocals generated in the same style",
                )
            )
        else:
            steps.append(
                PipelineStep(
                    "vocalization",
                    "skipped",
                    "Instrumental-only output requested",
                )
            )

        return PipelineResponse(
            flow="original_music_generation",
            output_url=music.audio_url,
            estimated_cost_usd=music.estimated_cost_usd,
            quality_score=music.quality_score,
            steps=steps,
        )

    def generate_voice_cover(self, request: VoiceCoverRequest) -> PipelineResponse:
        _validate_cover_request(request)

        stems = self.separation_service.separate(request.source_song_url)
        converted = self.voice_service.convert(
            vocals_url=stems.vocals_url,
            target_artist=request.target_voice_label,
            preserve_timing=request.preserve_timing,
        )
        mixed = self.mixing_service.mix(stems.instrumental_url, converted.converted_vocals_url)

        estimated_cost = round(0.08 + 0.12 + 0.05, 4)
        quality = round((stems.confidence + converted.confidence) / 2, 3)
        steps = [
            PipelineStep("input_validation", "ok", "Source song + voice sample validated"),
            PipelineStep("stem_separation", "ok", "Source split into vocals and instrumental"),
            PipelineStep(
                "voice_conversion",
                "ok",
                f"Voice converted to {request.target_voice_label}",
            ),
            PipelineStep(
                "mix_master",
                "ok",
                "Converted vocals mixed with instrumental backing",
            ),
            PipelineStep(
                "timing_and_melody_guard",
                "ok" if request.preserve_timing and request.preserve_melody else "warn",
                "Preservation constraints applied",
            ),
        ]

        return PipelineResponse(
            flow="ai_voice_cover_generation",
            output_url=mixed.output_url,
            estimated_cost_usd=estimated_cost,
            quality_score=quality,
            steps=steps,
        )

    @staticmethod
    def pipeline_mermaid() -> str:
        return (
            "flowchart TD\n"
            "    A[User Input] --> B{Flow Router}\n"
            "    B -->|Original Music| C[Prompt Builder + Guardrails]\n"
            "    C --> D[Music Generation API]\n"
            "    D --> E[Post-process and Loudness Normalize]\n"
            "    E --> F[Song Output]\n"
            "    B -->|AI Voice Cover| G[Song Upload + Voice Sample Upload]\n"
            "    G --> H[Stem Separation]\n"
            "    H --> I[Voice Conversion]\n"
            "    I --> J[Mix and Master]\n"
            "    J --> F[Song Output]\n"
        )


def _validate_original_request(request: OriginalMusicRequest) -> None:
    if not request.prompt.strip():
        raise PipelineValidationError("prompt cannot be empty")
    if request.duration_sec < 15 or request.duration_sec > 300:
        raise PipelineValidationError("duration_sec must be between 15 and 300")
    if not request.genre.strip() or not request.style.strip() or not request.mood.strip():
        raise PipelineValidationError("mood/genre/style are required")


def _validate_cover_request(request: VoiceCoverRequest) -> None:
    if not request.source_song_url.strip():
        raise PipelineValidationError("source_song_url cannot be empty")
    if not request.voice_sample_url.strip():
        raise PipelineValidationError("voice_sample_url cannot be empty")
    if not request.target_voice_label.strip():
        raise PipelineValidationError("target_voice_label cannot be empty")


def run_demo() -> dict:
    pipeline = AIMusicPipeline()
    original = pipeline.generate_original_song(
        OriginalMusicRequest(
            prompt="Catchy early-2000s pop anthem about a summer crush",
            mood="upbeat",
            genre="pop",
            style="early 2000s, radio friendly",
            include_vocals=True,
        )
    )
    cover = pipeline.generate_voice_cover(
        VoiceCoverRequest(
            source_song_url="https://example.com/song.wav",
            voice_sample_url="https://example.com/voice.wav",
            target_voice_label="female_pop_voice_v1",
        )
    )
    return {"original": original.to_dict(), "cover": cover.to_dict()}


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2))
