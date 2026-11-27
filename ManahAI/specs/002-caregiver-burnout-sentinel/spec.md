# Feature Specification: Proactive Burnout Sentinel & Family Task Delegator

**Feature Branch**: `002-caregiver-burnout-sentinel`

**Created**: 2026-11-27

**Status**: Draft

**Input**: User description: Proactive, check-in-based caregiver support and confirmed delegation of routine care tasks to trusted family members.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get support when strain persists (Priority: P1)

As a primary family caregiver, I want brief check-ins to notice my own
self-reported stress and sleep patterns and offer practical, optional support,
so I can find relief before strain builds further.

**Why this priority**: Caregivers may overlook their own needs while providing
care. Early, low-pressure support can help them consider practical relief
without labeling or diagnosing them.

**Independent Test**: Complete daily check-ins with sustained high stress or
poor sleep, then verify that the system offers a brief, optional supportive
check-in and, after sustained critical stress, asks for explicit approval
before contacting the respite coordinator.

**Acceptance Scenarios**:

1. **Given** a caregiver completes the daily check-in, **When** they report
   energy, stress, and sleep quality, **Then** they can complete it in about
   10 seconds, skip it, or leave it unanswered without the system inferring
   unreported values.
2. **Given** the caregiver reports high stress or poor sleep for three
   consecutive days, **When** the system reviews the reported pattern,
   **Then** it offers an empathetic check-in and an optional three-minute
   breathing audio or journaling prompt without diagnosing burnout or
   pressuring the caregiver.
3. **Given** the caregiver reports the highest stress rating for five
   consecutive days, **When** the system offers respite-coordinator support,
   **Then** it explains what information would be shared and requests
   just-in-time explicit caregiver confirmation before sending an alert.
   If the caregiver declines or does not respond, no respite alert is sent.
4. **Given** the caregiver repeatedly declines optional support, **When**
   the same reported trend continues, **Then** the system acknowledges the
   caregiver's choice in a validating, non-judgmental tone and does not repeat
   the same offer unless the caregiver asks for it or a new pattern emerges.
5. **Given** a message or check-in reveals self-harm, suicidal ideation,
   violence, or an acute medical emergency, **When** the system detects
   imminent danger, **Then** it immediately bypasses routine support, displays
   verified local crisis helplines, and alerts the designated human
   coordinator.

---

### User Story 2 - Delegate a routine task with control (Priority: P2)

As an overwhelmed primary caregiver, I want to organize routine care tasks
around trusted relatives' availability and preferences, so I can ask for
specific help without managing every coordination step myself.

**Why this priority**: Sharing practical tasks can reduce the primary
caregiver's administrative load, while clear requests and caregiver approval
preserve trust and control.

**Independent Test**: Add trusted relatives and a weekly task, review a
proposed task request, approve it, and verify that the relative can accept or
decline it and that the shared schedule reflects the response.

**Acceptance Scenarios**:

1. **Given** the caregiver registers trusted relatives, **When** they record
   each relative's availability and task preferences, **Then** those details
   can be used to suggest suitable recipients for tasks such as pharmacy
   pickups, appointment accompaniment, or meal preparation.
2. **Given** the caregiver has approved a weekly task list, **When** the
   system proposes delegating a specific task, **Then** it previews the
   recipient, task, due time, and message content and waits for a separate,
   explicit single-tap approval before sending each external message.
   Approval of the weekly list alone does not authorize dispatch.
3. **Given** a relative accepts or declines an approved task request,
   **When** their response is received, **Then** the shared care schedule is
   updated accordingly and the primary caregiver is notified.
4. **Given** a relative has not responded within four hours, **When** that
   period elapses, **Then** the system privately notifies the primary
   caregiver and may suggest another recipient, but does not automatically
   reassign the task or contact another relative.
5. **Given** the caregiver chooses to send a proposed reassignment, **When**
   the system presents the recipient and request, **Then** it sends nothing
   until the caregiver explicitly approves that message.
6. **Given** no trusted relative is available for a task, **When** delegation
   is proposed, **Then** the task remains unassigned and the caregiver is
   informed without contacting an unapproved person.

---

### Edge Cases

- If one or more daily check-ins are missing, the system does not infer a
  score or treat silence as evidence of caregiver distress.
- A single unusually high stress rating does not by itself trigger the
  sustained-strain respite offer.
- If the caregiver declines or ignores a respite-alert confirmation, no
  alert is sent; the system may continue routine check-ins without guilt or
  repeated pressure.
- If an external message cannot be delivered or a relative's response cannot
  be confirmed, the system reports that status accurately and does not claim
  the task was assigned.
- If a task lacks a due time, recipient, or approval, it remains a private
  draft and no family member is contacted.
- If the check-in or task flow is used over low-bandwidth channels, it offers
  concise text and numbered replies; voice notes are supported through
  audio-capable channels.
- Every session clearly identifies the assistant as an AI tool, not a human
  counselor.
- Caregiver and care-recipient health information is protected, and family
  task requests disclose only information needed to complete the approved
  task.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST offer a brief daily check-in for caregiver
  energy, stress, and sleep quality using a five-point scale. The check-in
  MUST be completable in about 10 seconds and may be skipped.
- **FR-002**: The system MUST evaluate caregiver-reported patterns over a
  rolling seven-day period against the caregiver's own recent pattern when
  enough check-ins are available. It MUST NOT treat one day's score or a
  missing check-in as sufficient evidence of sustained strain.
- **FR-003**: After three consecutive reported days of high stress or poor
  sleep, the system MUST offer an empathetic check-in and an optional
  three-minute breathing audio or journaling prompt. These offers MUST be
  non-clinical, optional, and non-judgmental. If the caregiver declines an
  offer, the system MUST NOT repeat that offer while the same reported pattern
  continues unless the caregiver requests it.
- **FR-004**: After five consecutive reported days at the highest stress
  rating, the system MUST offer the caregiver a respite-coordinator alert.
  Before sending the alert, it MUST explain the information to be shared and
  obtain explicit caregiver confirmation immediately before dispatch.
- **FR-005**: The system MUST NOT diagnose burnout or any other condition,
  prescribe medication, recommend dosage changes, or represent its support as
  a replacement for a licensed clinician.
- **FR-006**: The system MUST allow caregivers to register trusted family
  contacts with their stated availability and task preferences and to record
  routine care tasks with a due time and proposed recipient.
- **FR-007**: Before sending any task request, reassignment, or other message
  to an external family member, the system MUST preview the recipient and
  message content and obtain a separate, explicit single-tap caregiver
  confirmation for that message. Prior approval of a weekly list MUST NOT
  count as authorization to send.
- **FR-008**: The system MUST record a relative's acceptance or decline of an
  approved request, update the shared care schedule accordingly, and notify
  the primary caregiver.
- **FR-009**: If a relative has not responded within four hours, the system
  MUST privately notify the primary caregiver and MAY suggest another
  recipient. It MUST NOT automatically reassign the task or message another
  relative.
- **FR-010**: If a caregiver check-in or message indicates self-harm, suicidal
  ideation, violence, or an acute medical emergency, the system MUST
  immediately bypass routine support, display verified local crisis
  helplines, and alert the designated human coordinator.
- **FR-011**: Caregiver and care-recipient health records MUST be encrypted at
  rest and in transit. Personally identifiable information MUST be masked
  before context is sent to any external large language model service.
  External family task requests MUST disclose no more health information than
  needed to perform the caregiver-approved task.
- **FR-012**: Every session MUST clearly disclose that the assistant is an AI
  tool and not a human counselor.
- **FR-013**: Check-in and task-delegation flows MUST be usable over
  low-bandwidth, familiar channels, including WhatsApp, SMS, voice notes, and
  web, and MUST support regional languages and caregivers with low digital
  literacy. Voice notes MUST be available through audio-capable channels.

### Key Entities

- **Caregiver Check-in**: A caregiver's dated, self-reported energy, stress,
  and sleep-quality ratings, including whether the check-in was skipped.
- **Care Circle Contact**: A trusted relative, with caregiver-entered task
  preferences and availability.
- **Care Task**: A routine task with its description, due time, proposed
  recipient, approval status, and acceptance or decline.
- **Respite Alert**: A proposed message to the designated human respite
  coordinator, including the caregiver's confirmation and delivery status.
- **Care Schedule**: The shared, current view of tasks and their assignment
  status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A caregiver can complete the three-rating daily check-in in
  about 10 seconds, skip it, or leave it unanswered without a score being
  inferred.
- **SC-002**: Three consecutive reported days of high stress or poor sleep
  produce an optional supportive check-in; five consecutive highest-stress
  ratings produce a respite-alert offer, not an alert sent without explicit
  confirmation.
- **SC-003**: No respite alert or external family message is sent without
  explicit, just-in-time caregiver confirmation.
- **SC-004**: Every approved task request includes a due time and named
  recipient; a relative's acceptance or decline is reflected in the shared
  schedule and caregiver notification.
- **SC-005**: At four hours without a relative response, the caregiver is
  privately notified and no alternate relative is contacted without a new
  approval.
- **SC-006**: Caregivers can complete check-in and task-delegation flows using
  supported low-bandwidth channels and regional languages, with a text
  alternative when audio is unavailable.

## Assumptions

- The five-point check-in uses 1 for lowest and 5 for highest energy and
  stress; sleep quality uses 1 for poorest and 5 for best.
- For this feature, high stress means a rating of 4 or 5, poor sleep means a
  sleep-quality rating of 1 or 2, and critical stress means a rating of 5.
  The consecutive-day triggers use reported check-ins only.
- A weekly task list organizes possible tasks but never authorizes outgoing
  messages. The caregiver approves each recipient-specific message
  immediately before it is sent.
- Caregivers identify a designated human respite coordinator and choose
  trusted family contacts before using the related workflows.
- The breathing audio and journaling prompts are optional, non-clinical
  supports; declining them does not reduce access to other assistance.
- A missed check-in is unknown, not a negative or positive wellbeing signal.
