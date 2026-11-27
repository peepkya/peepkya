# Feature Specification: Real-Time Crisis De-escalation & Debrief Copilot

**Feature Branch**: `001-crisis-deescalation-copilot`

**Created**: 2026-11-27

**Status**: Draft

**Input**: User description: Real-time, plan-based crisis support for family caregivers, followed by voice-first incident debriefs and clinician-ready summaries.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get immediate crisis support (Priority: P1)

As a family caregiver facing an acute episode, I want concise guidance based on
the care recipient's caregiver-managed crisis plan so I can focus on immediate
safety instead of searching through long instructions.

**Why this priority**: Immediate safety support is the core value of this
feature, and the caregiver may be under significant stress.

**Independent Test**: Send a text or voice note describing a non-imminent
episode and verify that the response is timely, brief, and consistent with the
caregiver-managed plan. Then send an imminent-danger message and verify that
emergency escalation takes precedence over routine guidance.

**Acceptance Scenarios**:

1. **Given** a caregiver-managed crisis plan is available and the caregiver
   sends a non-imminent “Help / Crisis” message, **When** the system receives
   the message, **Then** it returns three ordered, plan-based safety or
   grounding steps within 3 seconds, with no more than 50 words in the
   crisis-mode response.
2. **Given** an incoming message or voice note indicates self-harm, suicidal
   ideation, violence, or an acute medical emergency, **When** the system
   checks the message for danger before generating coaching, **Then** it
   bypasses standard response generation on detection, immediately displays
   verified local crisis helplines, and alerts the designated human
   coordinator.
3. **Given** an imminent-danger response offers to contact an external family
   member, **When** the caregiver has not confirmed the action, **Then** no
   message is sent; the system sends it only after explicit caregiver
   confirmation. The caregiver can choose to initiate a call to a displayed
   helpline.
4. **Given** the caregiver has not created a crisis plan, **When** they request
   help, **Then** the system does not invent personalized strategies and uses
   concise basic safety checks while preserving any required emergency
   escalation.
5. **Given** a caregiver creates or updates a crisis plan, **When** the plan is
   saved, **Then** subsequent guidance uses the caregiver-confirmed triggers
   and strategies in that plan.
6. **Given** a caregiver starts a crisis session through a supported channel
   and regional language, **When** the assistant responds, **Then** the crisis
   flow is usable through that channel and the session clearly identifies the
   assistant as an AI tool, not a human counselor.
7. **Given** the system provides crisis guidance, **When** the caregiver
   receives it, **Then** it does not diagnose, prescribe medication, or
   recommend dosage changes.

---

### User Story 2 - Debrief by voice after an episode (Priority: P2)

As a fatigued caregiver after an episode has passed, I want to record a short
voice debrief so I can save what happened without having to type a detailed
account.

**Why this priority**: A low-effort debrief helps caregivers preserve useful
information while respecting their limited time and energy after an episode.

**Independent Test**: Mark an episode as resolved, wait for the debrief prompt,
and provide the three requested details by voice. Verify that the caregiver
can review and save the resulting incident record.

**Acceptance Scenarios**:

1. **Given** the caregiver marks an episode resolved, **When** two hours have
   elapsed and the caregiver has not already started a debrief, **Then** the
   system offers a debrief with three simple prompts: duration, suspected
   trigger, and what helped.
2. **Given** an episode is marked resolved, **When** the caregiver initiates
   a debrief before the two-hour prompt, **Then** the caregiver can provide
   the same three details by text or by a voice summary of up to 60 seconds.
3. **Given** the caregiver reviews the captured debrief, **When** they correct,
   skip, or confirm an answer, **Then** only the caregiver-confirmed incident
   details are saved.
4. **Given** the caregiver's debrief contains signs of a new imminent danger,
   **When** the system detects them, **Then** emergency escalation takes
   precedence over debrief questions.

---

### User Story 3 - Prepare an incident summary for a clinician (Priority: P3)

As a caregiver preparing for a psychiatric follow-up, I want a chronological,
plain-language summary of recorded incidents so I can share relevant
caregiver-reported observations without reconstructing events from memory.

**Why this priority**: A reviewable summary makes accumulated incident records
useful for follow-up while keeping interpretation with the caregiver and
clinician.

**Independent Test**: Save incident records with and without repeated
caregiver-reported triggers, then preview and download a summary. Verify that
it is chronological, uses plain language, and only describes a potential
pattern when the minimum incident threshold is met.

**Acceptance Scenarios**:

1. **Given** one or more incidents have been saved, **When** the caregiver
   requests a summary, **Then** the system provides a chronological,
   jargon-free summary of the saved details for caregiver review and download.
2. **Given** at least three incidents were logged within the preceding 30
   days, **When** a caregiver-reported observation recurs, **Then** the
   summary may highlight it as a possible pattern and show the supporting
   incident count and period without claiming causation or offering clinical
   advice.
3. **Given** fewer than three incidents were logged within the preceding 30
   days, **When** the caregiver requests a summary, **Then** the system does
   not present a pattern insight.
4. **Given** the caregiver chooses to send a summary or related message to an
   external family member, **When** the caregiver has not confirmed sending,
   **Then** no message is sent.
5. **Given** incident health information is retained or sent as context to an
   external large language model service, **When** it is stored or sent,
   **Then** the health information is encrypted at rest and in transit, and
   personally identifiable information is masked before it is sent.

---

### Edge Cases

- If a voice note is incoherent or its transcription is unclear, the system
  asks one brief physical-safety question or offers numbered quick replies
  rather than asking complex questions. This does not delay escalation when
  imminent danger is detected.
- If audio transcription is unavailable or connectivity is poor, the system
  offers low-bandwidth text or numbered replies, such as panic, agitation, or
  emergency. It does not claim that an unheard voice note was understood.
- If a coordinator alert cannot be delivered, the system makes the failure
  clear to the caregiver and still displays available verified local crisis
  helplines. It does not report an alert as successful when delivery failed.
- If no verified local helpline is available for the caregiver's configured
  location, the system does not invent a number; it clearly directs the
  caregiver to local emergency services and alerts the designated coordinator.
- If the caregiver has not marked an episode resolved, the system does not
  send a routine post-episode debrief prompt.
- If an incident record mentions missed sleep or medication, the summary
  reports it only as a caregiver-reported observation and does not recommend
  medication changes or imply a clinical cause.
- Every session clearly identifies the assistant as an AI tool, including
  crisis and debrief interactions.
- Crisis and debrief flows remain available over low-bandwidth familiar
  channels, including WhatsApp, SMS, voice notes, and web, and support
  regional languages and low digital literacy.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Caregivers MUST be able to create and update a care
  recipient-specific crisis plan containing caregiver-reported triggers,
  preferred calming strategies, emergency contacts, and a preferred hospital.
- **FR-002**: The system MUST accept crisis requests as text or voice notes,
  transcribe voice notes, and identify whether they request crisis support.
  When a transcript or intent is unclear, it MUST use the concise safety-check
  or quick-reply flow. Crisis and debrief interactions MUST support the
  supported regional languages and familiar low-bandwidth channels, including
  WhatsApp, SMS, voice notes, and web; voice notes MUST be available through
  channels that support audio.
- **FR-003**: For a non-imminent crisis request with a crisis plan, the system
  MUST return three ordered safety or grounding steps based on that plan within
  3 seconds of receiving the request. Crisis-mode response text MUST NOT
  exceed 50 words per turn.
- **FR-004**: Before generating coaching in response to any incoming message
  or voice-note transcript, the system MUST assess it for imminent danger. On
  detection of self-harm, suicidal ideation, violence, or an acute medical
  emergency, it MUST bypass standard response generation, immediately display
  verified local crisis helplines, and alert the designated human coordinator.
- **FR-005**: The system MUST NOT invent local crisis telephone numbers. If
  verified local helplines are unavailable for the configured location, it
  MUST say so clearly, direct the caregiver to local emergency services, and
  alert the designated human coordinator.
- **FR-006**: The system MUST require explicit caregiver confirmation before
  sending messages to external family members. It MUST NOT interpret a crisis
  trigger, prior consent, or a proposed action as confirmation. The caregiver
  MUST be able to initiate a call to a displayed helpline.
- **FR-007**: The system MUST offer a debrief two hours after the caregiver
  marks an episode resolved, unless the caregiver has already initiated a
  debrief. The caregiver MUST also be able to initiate a debrief at any time
  after marking the episode resolved.
- **FR-008**: A debrief MUST request duration, suspected trigger, and what
  helped. It MUST accept a voice summary of up to 60 seconds and allow the
  caregiver to review, correct, skip, or confirm captured details before they
  are saved.
- **FR-009**: The system MUST create a chronological, jargon-free summary from
  saved incident details for caregiver review and download. A possible pattern
  MUST only be presented when at least three incidents were logged within the
  preceding 30 days; the summary MUST show supporting counts and MUST NOT
  assert causation, diagnose, prescribe, or recommend dosage changes.
- **FR-010**: Caregiver and care-recipient health records MUST be encrypted at
  rest and in transit. Personally identifiable information MUST be masked
  before context is sent to any external large language model service.
- **FR-011**: Every session MUST clearly disclose that the assistant is an AI
  tool and not a human counselor.
- **FR-012**: The system MUST NOT diagnose conditions, prescribe medication,
  recommend dosage changes, or represent its guidance as a substitute for a
  licensed clinician.
- **FR-013**: The system MUST make required crisis and debrief interactions
  usable over low-bandwidth, familiar channels and in supported regional
  languages, including for caregivers with low digital literacy. When audio
  processing is unavailable, it MUST offer a text-based alternative.

### Key Entities

- **Crisis Plan**: Caregiver-managed information for one care recipient,
  including known triggers, preferred calming strategies, emergency contacts,
  and preferred hospital.
- **Incident Record**: A caregiver-reviewed account of an episode, including
  its duration, suspected trigger, what helped, and time of occurrence.
- **Crisis Escalation**: A detected imminent-danger event with its displayed
  local crisis resources and human-coordinator alert outcome.
- **Clinician Summary**: A chronological, downloadable presentation of saved
  incident details and eligible caregiver-reported patterns.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Under supported service conditions, a non-imminent crisis
  request receives three ordered, plan-based steps within 3 seconds, and no
  crisis-mode response turn exceeds 50 words.
- **SC-002**: In every validation scenario with detected imminent danger,
  standard response generation is bypassed, verified local crisis resources
  are displayed, and a coordinator alert is initiated without waiting for a
  generated answer.
- **SC-003**: No message to an external family member is sent without explicit
  caregiver confirmation.
- **SC-004**: After a caregiver marks an episode resolved, a debrief is offered
  at two hours unless already initiated; every debrief requests the same three
  details and accepts voice input up to 60 seconds.
- **SC-005**: Pattern insights appear only when at least three incidents fall
  within the preceding 30 days, and each insight shows its supporting count
  and time period.
- **SC-006**: Caregivers can complete the crisis and debrief flows through
  each supported familiar channel and supported regional language, including
  with low-bandwidth text alternatives when audio processing is unavailable.

## Assumptions

- A caregiver or authorized coordinator configures the care recipient's plan,
  the caregiver's location, and the designated human coordinator before
  personalized crisis support is used.
- Local crisis resources are maintained as verified for the configured
  location. If a verified number is unavailable, the system follows the
  explicit fallback in FR-005 and does not fabricate a number.
- A caregiver marks when an episode has passed and is ready for debrief; the
  system does not infer that an episode has ended from silence.
- Pattern insights describe repeated caregiver-entered observations only.
  They are not clinical findings or recommendations.
- The caregiver reviews and confirms transcribed incident details before they
  are saved.
