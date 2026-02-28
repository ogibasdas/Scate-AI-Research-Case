import pytest

from src.main import AIMusicPipeline, OriginalMusicRequest, PipelineValidationError


def test_original_generation_with_vocals() -> None:
    pipeline = AIMusicPipeline()
    response = pipeline.generate_original_song(
        OriginalMusicRequest(
            prompt="A catchy pop anthem",
            mood="upbeat",
            genre="pop",
            style="early 2000s",
            duration_sec=120,
            include_vocals=True,
        )
    )

    assert response.flow == "original_music_generation"
    assert response.output_url.startswith("https://mock.scate.ai/audio/song_")
    assert response.estimated_cost_usd > 0
    assert response.quality_score > 0.6
    assert any(step.name == "vocalization" and step.status == "ok" for step in response.steps)


def test_original_generation_instrumental_skips_vocalization() -> None:
    pipeline = AIMusicPipeline()
    response = pipeline.generate_original_song(
        OriginalMusicRequest(
            prompt="Energetic dance track",
            mood="energetic",
            genre="dance-pop",
            style="2000s",
            include_vocals=False,
        )
    )

    vocal_step = next(step for step in response.steps if step.name == "vocalization")
    assert vocal_step.status == "skipped"


@pytest.mark.parametrize("duration", [0, 10, 301, 500])
def test_original_generation_rejects_invalid_duration(duration: int) -> None:
    pipeline = AIMusicPipeline()
    request = OriginalMusicRequest(
        prompt="test",
        mood="upbeat",
        genre="pop",
        style="2000s",
        duration_sec=duration,
    )
    with pytest.raises(PipelineValidationError, match="duration_sec must be between 15 and 300"):
        pipeline.generate_original_song(request)


def test_generation_prompt_contains_optional_fields() -> None:
    request = OriginalMusicRequest(
        prompt="Summer hit",
        mood="upbeat",
        genre="pop",
        style="2000s",
        lyrics="This is the chorus line",
        inspiration="beach sunset colors",
    )
    generation_prompt = request.to_generation_prompt()

    assert "Lyrics seed:" in generation_prompt
    assert "Inspiration reference:" in generation_prompt
