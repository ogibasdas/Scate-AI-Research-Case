import pytest

from src.main import AIMusicPipeline, PipelineValidationError, VoiceCoverRequest


def test_voice_cover_happy_path() -> None:
    pipeline = AIMusicPipeline()
    response = pipeline.generate_voice_cover(
        VoiceCoverRequest(
            source_song_url="https://example.com/source.wav",
            voice_sample_url="https://example.com/voice.wav",
            target_voice_label="female_pop_voice_v1",
            preserve_timing=True,
            preserve_melody=True,
        )
    )

    assert response.flow == "ai_voice_cover_generation"
    assert response.output_url.startswith("https://mock.scate.ai/final/")
    assert response.estimated_cost_usd > 0
    assert response.quality_score >= 0.85
    assert [s.name for s in response.steps] == [
        "input_validation",
        "stem_separation",
        "voice_conversion",
        "mix_master",
        "timing_and_melody_guard",
    ]
    assert response.steps[-1].status == "ok"


def test_voice_cover_warns_when_preservation_is_not_required() -> None:
    pipeline = AIMusicPipeline()
    response = pipeline.generate_voice_cover(
        VoiceCoverRequest(
            source_song_url="https://example.com/source.wav",
            voice_sample_url="https://example.com/voice.wav",
            target_voice_label="female_pop_voice_v1",
            preserve_timing=False,
            preserve_melody=False,
        )
    )

    assert response.steps[-1].status == "warn"


@pytest.mark.parametrize(
    "payload,field_name",
    [
        (
            VoiceCoverRequest(
                source_song_url="",
                voice_sample_url="https://example.com/voice.wav",
                target_voice_label="v1",
            ),
            "source_song_url",
        ),
        (
            VoiceCoverRequest(
                source_song_url="https://example.com/source.wav",
                voice_sample_url="",
                target_voice_label="v1",
            ),
            "voice_sample_url",
        ),
        (
            VoiceCoverRequest(
                source_song_url="https://example.com/source.wav",
                voice_sample_url="https://example.com/voice.wav",
                target_voice_label="",
            ),
            "target_voice_label",
        ),
    ],
)
def test_voice_cover_requires_mandatory_fields(payload: VoiceCoverRequest, field_name: str) -> None:
    pipeline = AIMusicPipeline()
    with pytest.raises(PipelineValidationError, match=field_name):
        pipeline.generate_voice_cover(payload)
