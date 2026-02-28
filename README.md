# Scate AI - AI Researcher Case Submission

## Scope

This repository contains my solution for the **Scate AI - AI Researcher Case Study** in the **AI Music Generation** domain.  
The solution covers both required use cases:

1. Original music generation from text-based inputs
2. AI voice / cover generation from source song + voice sample

## Deliverables

| Question | Deliverable | File |
| --- | --- | --- |
| Q1 | Model/API research and evaluation (quality, latency, cost, constraints, scalability) | `docs/Q1_API_Research.md` |
| Q2 | Prompt design for early-2000s pop + cross-API comparison | `docs/Q2_Prompt_Engineering.md` |
| Q3 | High-level generation pipeline design for both flows | `docs/Q3_Pipeline_Design.md` |

## Implementation

The codebase includes a deterministic mock implementation to demonstrate product flow and API orchestration logic without paid keys.

- Pipeline entry point: `src/main.py`
- Mock provider layer: `src/mock_services.py`
- Unit tests: `tests/test_music_gen.py`, `tests/test_voice_cover.py`

## Project Structure

```text
src/
  main.py
  mock_services.py
tests/
  test_music_gen.py
  test_voice_cover.py
docs/
  Q1_API_Research.md
  Q2_Prompt_Engineering.md
  Q3_Pipeline_Design.md
requirements.txt
README.md
```

## Run Locally (Windows PowerShell)

```powershell
py -m pip install -r requirements.txt
py -m pytest -q
py src/main.py
```

## Test Status

- Current result: **12 passed**
- Test coverage focus:
  - Request validation
  - Original music flow behavior
  - Voice cover flow behavior
  - Step-level pipeline response consistency

## Important Notes

- This implementation is **mock-based** by design for deterministic outputs and reproducible tests.
- Q2 comparison is based on official API docs/pricing and architecture fit.
- **No live cross-API benchmark was executed** in this repo due credential/time constraints.
- Research references are dated and captured in each document.
