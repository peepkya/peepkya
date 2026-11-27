# Tasks: Real-Time Crisis De-escalation & Debrief Copilot

**Input**: Design documents from `specs/001-crisis-deescalation-copilot/`

**Prerequisites**: `plan.md` and `spec.md` are available. The detailed
`research.md`, `data-model.md`, `contracts/`, and `quickstart.md` design
artifacts are not yet present; implementation tasks below follow the current
plan/spec and must be reconciled with those artifacts when they are completed.

**Tests**: Tests are included because the supplied task list explicitly
requested safety unit tests and end-to-end integration tests. Safety tests
precede safety routing implementation.

**Organization**: Tasks are grouped by setup, shared foundation, then the
three independently testable user stories in priority order.

## Phase 1: Setup

**Purpose**: Initialize the Python service and its development environment.

- [ ] T001 Create the Python 3.12 application, `src/`, `tests/`, and `web/` structure in `pyproject.toml`, `src/__init__.py`, `tests/`, and `web/`.
- [X] T002 Add FastAPI, Uvicorn, LangGraph/PostgresSaver, SQLAlchemy, asyncpg, Alembic, HTTPX, Presidio, Faster-Whisper, encryption, and test dependencies in `pyproject.toml`.
- [X] T003 [P] Add typed environment configuration and safe example values in `src/core/config.py` and `.env.example`.
- [ ] T004 [P] Add shared test fixtures and fake channel clients in `tests/conftest.py` and `tests/fakes/channel_clients.py`.

## Phase 2: Foundational

**Purpose**: Build persistence, privacy, and channel foundations required by
all user stories.

- [ ] T005 Configure the async PostgreSQL connection, SQLAlchemy base, and Alembic migration environment in `src/core/database.py`, `alembic.ini`, and `alembic/env.py`.
- [X] T006 [P] Write encryption and PII-redaction tests, including fail-closed redaction behavior, in `tests/unit/test_privacy.py`.
- [X] T007 [P] Implement field encryption and pre-LLM PII masking in `src/core/security.py` and `src/core/privacy.py`; do not persist raw transcripts by default.
- [ ] T008 [P] Define normalized inbound/outbound channel events and delivery outcomes in `src/channels/base.py` and `src/models/channel_event.py`.
- [ ] T009 Create shared caregiver, care-recipient, contact, crisis-plan, helpline, and session models plus the initial migration in `src/models/crisis.py` and `alembic/versions/0001_crisis_foundation.py`; omit diagnosis categories and persistent raw transcripts not required by the spec.
- [ ] T010 Implement a PostgreSQL-backed transactional outbox with idempotent work claiming and delivery states in `src/services/outbox.py` and `src/models/outbox.py`.
- [ ] T011 Configure LangGraph's PostgreSQL checkpointer with sanitized resumable state in `src/agents/state.py`; exclude raw message bodies, audio, phone numbers, and full crisis-plan context.
- [ ] T012 Add structured error handling and privacy-safe operational logging in `src/core/errors.py` and `src/core/logging.py`; never log message bodies, transcripts, or unredacted plan fields.

## Phase 3: User Story 1 - Get immediate crisis support (Priority: P1) - MVP

**Goal**: Provide brief, caregiver-plan-based guidance and mandatory immediate
escalation for detected imminent danger.

**Independent Test**: Submit non-imminent and imminent-risk text/voice messages
through fake channel clients. Verify the non-imminent response uses three
ordered steps within 3 seconds and at most 50 words; verify an imminent-risk
message bypasses coaching, displays verified resources, and initiates a
coordinator alert.

### Tests for User Story 1

- [X] T013 [P] [US1] Write safety-routing unit tests for self-harm, suicidal ideation, violence, acute medical emergency, benign distress, ambiguous input, and classifier failure in `tests/unit/test_safety_guard.py`.
- [ ] T014 [P] [US1] Write contract tests for channel event normalization, duplicate webhook events, and external-message approval in `tests/contract/test_crisis_channels.py`.

### Implementation for User Story 1

- [X] T015 [US1] Implement the deterministic and independent risk-classification gate in `src/agents/safety_guard.py`; route any detected emergency trigger to escalation before generating coaching.
- [X] T016 [P] [US1] Implement location-scoped verified helpline lookup and the no-invented-number fallback in `src/services/crisis_resources.py`.
- [ ] T017 [P] [US1] Implement coordinator alert dispatch and accurate delivery-failure reporting in `src/services/coordinator_alerts.py`.
- [ ] T018 [US1] Implement WhatsApp webhook verification, event deduplication, and inbound message normalization in `src/api/webhooks/whatsapp.py` and `src/channels/whatsapp.py`.
- [ ] T019 [P] [US1] Implement the provider-neutral SMS webhook and channel adapter in `src/api/webhooks/sms.py` and `src/channels/sms.py`.
- [ ] T020 [P] [US1] Implement the responsive, low-bandwidth web crisis interface and message endpoint in `src/api/web.py`, `web/templates/crisis.html`, and `web/static/crisis.js`.
- [ ] T021 [US1] Implement recipient/content-bound, expiring caregiver approval before each external-family message in `src/models/consent.py` and `src/services/action_approval.py`; coordinator crisis alerts remain automatic.
- [ ] T022 [US1] Implement the crisis graph and concise plan-based coach in `src/agents/crisis_graph.py` and `src/agents/crisis_coach.py`; enforce the safety gate, three ordered steps, three-second target, and 50-word limit.
- [ ] T023 [P] [US1] Add regional-language crisis templates, AI disclosure, and numbered low-bandwidth fallback replies in `src/content/crisis_messages/`.
- [ ] T024 [US1] Write cross-channel crisis integration tests for WhatsApp, SMS, and web covering emergency bypass, coordinator alerts, family-message approval, and non-imminent response limits in `tests/integration/test_crisis_flow.py`.

**Checkpoint**: User Story 1 works independently with simulated channel
providers and no live emergency or family messages.

## Phase 4: User Story 2 - Debrief by voice after an episode (Priority: P2)

**Goal**: Prompt after caregiver-confirmed resolution, collect and review the
three debrief details, and save only caregiver-confirmed incident data.

**Independent Test**: Seed a resolved crisis session, advance a test clock by
two hours, submit a voice or text debrief, and verify review/correction/skip
behavior and incident persistence. Verify that new imminent-risk content
interrupts debrief and escalates.

### Tests for User Story 2

- [ ] T025 [P] [US2] Write transcription tests for multilingual short audio, 60-second debrief limits, cleanup, and failure-to-numbered-replies behavior in `tests/unit/test_transcription.py`.
- [ ] T026 [P] [US2] Write debrief workflow tests for two-hour timing, caregiver review, correction, skip, confirmation, and emergency interruption in `tests/integration/test_debrief_flow.py`.

### Implementation for User Story 2

- [ ] T027 [US2] Implement short-lived encrypted audio handling and speech transcription with cleanup and text/numbered-reply fallback in `src/services/transcription.py`.
- [ ] T028 [US2] Add incident-record persistence for duration, suspected trigger, what helped, event time, and caregiver confirmation in `src/models/incident.py` and `alembic/versions/0002_incident_records.py`.
- [ ] T029 [US2] Implement the three-question debrief collector with review, correction, skip, and confirm actions in `src/agents/debrief.py` and `src/api/debrief.py`.
- [ ] T030 [US2] Schedule the debrief prompt two hours after the caregiver marks an episode resolved using the durable outbox worker in `src/workers/debrief_scheduler.py`; do not rely on an in-process timer.
- [ ] T031 [US2] Add debrief integration tests using a fake clock and fake channels, including no prompt before resolution and no false success on delivery failure, in `tests/integration/test_debrief_schedule.py`.

**Checkpoint**: User Story 2 works independently with a seeded resolved
session and stores only caregiver-confirmed incident fields.

## Phase 5: User Story 3 - Prepare an incident summary for a clinician (Priority: P3)

**Goal**: Produce a chronological, plain-language, downloadable summary and
show patterns only at the specified threshold.

**Independent Test**: Seed confirmed incident records below and above the
three-incidents-in-30-days threshold. Preview and download summaries; verify
chronology, supporting counts, no causal claims, and explicit approval before
any external-family message.

### Tests for User Story 3

- [ ] T032 [P] [US3] Write summary tests for chronology, caregiver-reported language, and the three-incidents-in-30-days pattern threshold in `tests/unit/test_incident_summary.py`.
- [ ] T033 [P] [US3] Write export and external-share approval tests in `tests/integration/test_clinician_summary.py`.

### Implementation for User Story 3

- [ ] T034 [US3] Implement chronological summaries and count-based, non-causal pattern descriptions from confirmed incident fields in `src/services/incident_summary.py`.
- [ ] T035 [US3] Implement caregiver preview and PDF/plain-text download endpoints in `src/api/reports.py` and `src/services/report_export.py`.
- [ ] T036 [US3] Connect summary sharing to the existing recipient/content approval flow in `src/api/reports.py` and `src/services/action_approval.py`; do not send externally before confirmation.

**Checkpoint**: User Story 3 works with seeded incident records and does not
infer diagnoses, causes, or treatment recommendations.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate privacy, accessibility, and end-to-end acceptance across
the feature.

- [ ] T037 [P] Add tests proving raw audio/transcripts and unredacted PII are absent from checkpoints, external LLM requests, and logs in `tests/security/test_privacy_boundaries.py`.
- [ ] T038 [P] Add acceptance tests for the three-second first-response target and 50-word cap under supported service conditions in `tests/integration/test_crisis_response_limits.py`.
- [ ] T039 Update the runnable end-to-end scenarios and expected outcomes in `specs/001-crisis-deescalation-copilot/quickstart.md`.
- [ ] T040 Run the quickstart and all contract, integration, and security tests; record any failing scenario in `specs/001-crisis-deescalation-copilot/quickstart.md`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes the package and test harness.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user-story work.
- **User Story 1 (Phase 3)**: Depends on the database, privacy, channel, and checkpoint foundations.
- **User Story 2 (Phase 4)**: Depends on the shared session and outbox foundations; production scheduling consumes the resolved-session event from US1. It can be developed and tested independently with a seeded session.
- **User Story 3 (Phase 5)**: Depends on the confirmed incident-record contract from US2; it can be developed against seeded incident records.
- **Polish (Phase 6)**: Depends on the user stories selected for release.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2 and is the MVP.
- **US2 (P2)**: Starts after Phase 2; final event integration depends on US1's resolved-session state.
- **US3 (P3)**: Starts after Phase 2 using seeded incident records; production integration depends on US2's confirmed incident fields.

### Parallel Opportunities

- T003 and T004 can run in parallel after T001.
- T006, T008, and T012 can run in parallel after T005 begins, because they touch separate files.
- T013 and T014 can run in parallel; both precede their corresponding US1 implementation.
- T016, T017, T019, T020, and T023 can run in parallel after the foundational channel and model contracts are available.
- T025 and T026 can run in parallel; both precede US2 implementation.
- T032 and T033 can run in parallel; both precede US3 implementation.
- US2 and US3 can be developed against seeded data while US1 integration proceeds, subject to the dependencies above.

## Parallel Example: User Story 1

```text
After Phase 2:
Task: T013 safety-routing tests in tests/unit/test_safety_guard.py
Task: T014 channel contract tests in tests/contract/test_crisis_channels.py

After the channel and model contracts are ready:
Task: T016 verified helpline lookup in src/services/crisis_resources.py
Task: T017 coordinator alert delivery in src/services/coordinator_alerts.py
Task: T019 SMS adapter in src/channels/sms.py
Task: T020 web crisis interface in web/templates/crisis.html
```

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Setup and Foundational phases.
2. Implement and independently test crisis routing, verified resource display,
   coordinator alerts, and caregiver-confirmed family messages.
3. Validate three-step responses, the three-second target, and the 50-word
   cap with simulated channels before enabling live providers.

### Incremental Delivery

1. Deliver US1 for crisis response and escalation.
2. Add US2 for reviewed voice/text debriefs and durable two-hour prompts.
3. Add US3 for clinician-ready summaries and thresholded pattern insights.
4. Run cross-channel privacy and accessibility validation before production
   rollout.

## Notes

- Task IDs are sequential; `[P]` is used only for tasks that can work on
  separate files after their stated prerequisites.
- All crisis coordinator alerts are distinguished from external-family
  messages; only the latter require caregiver confirmation.
- No live crisis, family, or coordinator messages are sent by automated tests.
- Raw transcripts are not retained by default; implementers must follow the
  privacy and checkpoint constraints in `plan.md`.
