# Implementation Plan: Real-Time Crisis De-escalation & Debrief Copilot

**Branch**: `001-crisis-deescalation-copilot` | **Date**: 2026-11-27 | **Spec**: [spec.md](./spec.md)

**Input**: [spec.md](./spec.md) and the user's proposed Python/FastAPI,
LangGraph, PostgreSQL, WhatsApp, speech-to-text, and PII-scrubbing stack.

## Summary

Deliver a safety-first crisis-support and caregiver-debrief service. FastAPI
receives messages from WhatsApp, SMS, and a web interface; LangGraph routes
each message through a separate safety gate before any coaching generation.
Detected imminent danger bypasses coaching and immediately returns verified
local crisis resources while dispatching an alert to the designated human
coordinator. Routine support uses only the minimum caregiver-approved crisis
plan context and returns three brief steps. Family messages require
recipient-specific, just-in-time caregiver confirmation.

Use PostgreSQL for caregiver-managed plans, confirmed incident details, and
durable delayed work. Audio is transcribed in a controlled worker and discarded
after processing. A two-hour debrief prompt and caregiver-confirmed incident
records support a downloadable clinician summary without retaining raw
transcripts by default. SMS and web channel adapters are included because the
feature specification requires them in addition to WhatsApp.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, Uvicorn, LangGraph, LangGraph PostgreSQL
checkpointer, SQLAlchemy 2.0 async, Alembic, Meta WhatsApp Cloud API, a
provider-neutral SMS adapter, Faster-Whisper, Microsoft Presidio, Jinja2,
pytest

**Storage**: PostgreSQL 16; encrypted sensitive fields; short-lived encrypted
audio staging, deleted after transcription

**Testing**: pytest unit, integration, and contract suites; HTTPX for API tests;
PostgreSQL-backed integration tests; channel-provider fakes for all outbound
message tests

**Target Platform**: Linux container service behind HTTPS; responsive web
interface and low-bandwidth messaging channels

**Project Type**: Python web service with browser and messaging clients

**Performance Goals**: Non-imminent crisis requests receive the first response
within 3 seconds under supported service conditions; all crisis-mode turns
remain at or below 50 words

**Constraints**: Safety assessment precedes coaching; detected imminent danger
must bypass generated coaching; verified local resources and coordinator
alerts are mandatory; external-family messages require explicit confirmation;
PII is masked before external LLM calls; no diagnosis or medication advice;
support WhatsApp, SMS, voice notes, web, regional languages, and low-literacy
flows

**Scale/Scope**: Feature 001 pilot; expected caregiver count and supported
locales are deployment inputs, not specified by the feature brief. API workers
remain stateless; PostgreSQL is the source of truth for plans, incidents, and
scheduled work.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate for this plan | Status |
|---|---|---|
| Non-Clinical Boundary | Coach only gives non-clinical, plan-based safety steps; no diagnosis, prescriptions, or dosage changes. | PASS |
| Mandatory Crisis Escalation | Check every message before coaching; any detected trigger bypasses generation, displays verified resources, and alerts the designated human coordinator. | PASS |
| Human Confirmation | Preview exact recipient and message; require a fresh caregiver confirmation before each external-family send. Coordinator crisis alerts remain automatic. | PASS |
| Transparent AI Identity | Disclose AI identity in each session and in crisis/debrief entry flows. | PASS |
| Privacy and Data Protection | Encrypt records in transit/at rest, mask PII before external LLM context, discard raw audio/transcripts by default, and minimize checkpoints/logs. | PASS |
| Accessible, Low-Friction Support | Provide WhatsApp, SMS, voice-note-capable and web flows; support regional languages, low bandwidth, and concise replies. | PASS |
| Technology-Neutral Specifications | Keep user behavior/outcomes in `spec.md`; place these stack decisions only in this plan and its design artifacts. | PASS |

No constitution exceptions are requested. The SMS and web adapters extend the
user-proposed WhatsApp-only ingress to meet the existing feature and
constitution requirements.

## Architecture and Safety Flow

1. Channel adapters validate provider signatures, deduplicate inbound event
   identifiers, normalize text/audio and locale, and acknowledge delivery.
2. Audio is downloaded to short-lived encrypted staging, transcribed with
   Faster-Whisper, and deleted after transcription. Raw media and transcript
   are not written to incident records, LangGraph checkpoints, or ordinary
   logs.
3. Every incoming message is evaluated before coaching by a safety gate that
   combines deterministic checks with a separate risk classifier. A positive
   signal for self-harm, suicidal ideation, violence, or acute medical
   emergency routes directly to deterministic escalation templates. The
   classifier's `critical` label is not the sole escalation condition.
4. The escalation path displays verified local helplines and initiates the
   designated coordinator alert without waiting for caregiver approval. It
   never automatically messages an external family contact. Helpline
   directory or coordinator delivery failures are reported accurately.
5. Non-imminent requests enter the coach only after the safety decision and
   PII minimization. The coach receives the minimum approved plan fields,
   returns three ordered steps within the 3-second response target, and is
   constrained to 50 words. A deterministic plan-based fallback is used if
   generation is slow or unavailable.
6. Any proposed external-family message is shown with its recipient and exact
   content. Approval is single-action, time-limited, and bound to that
   recipient/content; edits invalidate approval.
7. Marking an episode resolved creates durable scheduled work for the
   two-hour debrief. The debrief collects duration, suspected trigger, and
   what helped; caregivers review/correct/skip before saving. Any new message
   is safety-checked before the debrief flow continues.
8. Summaries are generated from saved caregiver-confirmed incident fields.
   Pattern statements are count-based, only after three incidents in 30 days,
   and do not claim causation.

## Data Protection and Reliability

- PostgreSQL is the source of truth for schedules, coordinator delivery status,
  caregiver confirmation records, debrief timers, and incident records.
  Delayed work uses a durable database-backed outbox/worker with idempotent
  dispatch; in-process timers are not relied upon for two-hour prompts.
- The proposed `condition_category` field is omitted because the feature does
  not need diagnoses. `raw_transcript_encrypted` is also omitted from the
  incident table by default; store only caregiver-confirmed fields. Keep
  encrypted raw input only in short-lived processing memory/staging.
- LangGraph checkpoints contain only the minimum sanitized state needed to
  resume a workflow. Never checkpoint raw message bodies, audio, phone numbers,
  or full crisis-plan context. Sensitive fields use application-level
  encryption in addition to database and transport encryption.
- Presidio plus narrowly scoped deterministic patterns redact identifiers
  before any external LLM call. If redaction fails or the provider is
  unavailable, do not send the context; use a safe deterministic response.
- All provider callbacks are authenticated and replay-safe. Delivery failures
  are surfaced to the caregiver or operator and never recorded as success.
- Logs and metrics use opaque identifiers, route/outcome codes, latency, and
  provider status only. They exclude user text, audio, helpline recipient
  details, and unredacted crisis-plan values.

## Project Structure

### Documentation (this feature)

```text
specs/001-crisis-deescalation-copilot/
├── plan.md              # This implementation plan
├── research.md          # Phase 0 decisions and sources
├── data-model.md        # Phase 1 entities and lifecycle
├── quickstart.md        # Phase 1 validation guide
├── contracts/
│   └── crisis-api.md
└── tasks.md             # Created later by /speckit-tasks
```

### Source Code (repository root)

```text
src/
├── core/
│   ├── config.py
│   ├── security.py
│   ├── privacy.py
│   └── database.py
├── agents/
│   ├── safety_guard.py
│   ├── crisis_graph.py
│   └── debrief.py
├── models/
│   ├── crisis.py
│   └── consent.py
├── channels/
│   ├── whatsapp.py
│   ├── sms.py
│   └── web.py
├── services/
│   ├── transcription.py
│   ├── crisis_resources.py
│   ├── incident_summary.py
│   └── outbox.py
└── api/
    ├── webhooks.py
    └── web.py

web/
└── templates/               # Accessible server-rendered caregiver interface

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: A single Python service with channel adapters and
separate safety, orchestration, and data-access modules keeps the initial
feature cohesive. The web interface is server-rendered with small progressive
enhancements rather than a separate frontend application; this minimizes
deployment and bandwidth costs while preserving an accessible web channel.
