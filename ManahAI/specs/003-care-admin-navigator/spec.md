# Feature Specification: Medical & Welfare Administrative Navigator

**Feature Branch**: `003-care-admin-navigator`

**Created**: 2026-11-27

**Status**: Draft

**Input**: User description: Help caregivers verify prescription details, follow-up reminders, and current welfare or insurance application requirements.

## Clarifications

### Session 2026-11-27

- Q: How should original prescription, discharge-summary, and welfare-document uploads be retained after they have served their application or verification purpose? → A: Delete source files when the relevant task is complete by default, while keeping caregiver-confirmed schedules or checklist status; allow caregivers to explicitly retain a file and delete it at any time.
- Q: After how long without a successful check against its official source should a welfare or insurance program be labeled potentially outdated? → A: 90 days.
- Q: When a caregiver reports a possible side effect that is not an apparent emergency, should the system only record it or also suggest a follow-up action? → A: Record the observation and suggest contacting the prescriber or pharmacist for advice; never recommend changing the medication.
- Q: Should a care-circle family member be able to view a caregiver's extracted medication schedule or visit document without the caregiver explicitly sharing it? → A: Keep schedules and documents private to the caregiver by default; require explicit confirmation for each external share.
- Q: What sources should the navigator use for general medication purpose and side-effect information? → A: Use official medicine leaflets or regulator information first, then reputable health-authority sources; show the source and state when reliable information cannot be found.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify visit instructions and follow-ups (Priority: P1)

As a caregiver leaving a clinician visit, I want to turn a prescription or
discharge summary into a reviewable schedule so I can follow the clinician's
written instructions without relying on memory.

**Why this priority**: Medication schedules and follow-up dates are
consequential. The caregiver must be able to verify the information before
reminders are created.

**Independent Test**: Provide a legible prescription image, verify the
extracted fields and their sources, correct or confirm them, and confirm that
no reminder is created before verification.

**Acceptance Scenarios**:

1. **Given** a caregiver uploads a prescription or discharge summary, **When**
   the system extracts its contents, **Then** it presents medicine names,
   prescribed doses, timings, frequencies, and follow-up dates in a structured
   table for caregiver verification. It states a medicine's purpose only when
   the clinician's document says it; otherwise it marks the purpose as not
   provided.
2. **Given** an extracted medicine name or dose has confidence below 85%,
   **When** the caregiver reviews the table, **Then** the field is visibly
   flagged in red and with a text label, the caregiver is told to verify it
   with a pharmacist or prescriber, and no reminder using that field is
   scheduled.
3. **Given** all schedule details are legible and the caregiver confirms their
   accuracy, **When** the caregiver saves the schedule, **Then** reminders are
   based only on the confirmed instructions and a side-effect check-in is
   offered seven days later. The source image is deleted after verification
   unless the caregiver explicitly chooses to retain it for ongoing reference.
4. **Given** the caregiver asks about a medicine's terms or side effects,
   **When** the system responds, **Then** it provides sourced, plain-language
   general information in the caregiver's preferred supported language using
   official medicine leaflets or regulator information first and reputable
   health-authority sources when those are unavailable. It shows the source,
   distinguishes general information from the clinician's instructions, and
   does not diagnose, infer why the medicine was prescribed, or recommend
   starting, stopping, or changing medication. If no reliable information is
   found, it says so rather than generating an unsupported explanation.
5. **Given** the caregiver reports a possible non-emergency side effect,
   **When** the system records the observation, **Then** it suggests contacting
   the prescriber or pharmacist for personalized advice without claiming the
   medicine caused the symptom or recommending a medication change.
6. **Given** a side-effect check-in or other message indicates an acute
   medical emergency, **When** the system detects imminent danger, **Then**
   it bypasses routine assistance, displays verified local crisis helplines,
   and alerts the designated human coordinator.
7. **Given** a family member requests access to a medication schedule or visit
   document, **When** the caregiver has not explicitly approved sharing that
   item, **Then** it remains private to the caregiver.

---

### User Story 2 - Find potentially relevant support programs (Priority: P2)

As a caregiver looking for government, NGO, or insurance support, I want
current, understandable eligibility information so I can decide which
programs are worth pursuing.

**Why this priority**: Clear requirements and trustworthy sources can reduce
the time caregivers spend navigating unfamiliar programs, while the
responsible authority remains the source of final eligibility decisions.

**Independent Test**: Provide a region and only the eligibility details
requested for a program search. Verify that potentially relevant programs
include their requirements, source, verification date, and an appropriate
qualification that final eligibility is determined by the program authority.

**Acceptance Scenarios**:

1. **Given** the caregiver supplies a region and requested non-identifying
   eligibility categories, **When** they request a search, **Then** the
   system lists potentially matching government or NGO programs and insurance
   support options with required documents and plain-language application
   steps, without promising eligibility.
2. **Given** a program result is displayed, **When** the caregiver reviews
   it, **Then** the result includes its last verified date and a link to the
   official government, insurer, or program-provider source.
3. **Given** a program has not been successfully checked against its official
   source within the past 90 days or its source is unavailable, **When** it
   appears in results, **Then** it is clearly marked as unverified or
   potentially outdated and the system does not present its requirements as
   current fact.
4. **Given** no suitable program is found, **When** the search completes,
   **Then** the system reports that no match was found and does not invent a
   program or eligibility rule.

---

### User Story 3 - Track application documents and deadlines (Priority: P3)

As a caregiver preparing an application, I want a simple document checklist
and deadline reminders so I can track progress without keeping unnecessary
sensitive information in the system.

**Why this priority**: A clear checklist supports follow-through after the
caregiver identifies a program, without requiring the system to make
eligibility decisions or submit applications.

**Independent Test**: Select a program, review its document checklist,
provide a document or mark an item complete, and verify that progress and
deadlines are visible and that sensitive identifiers can be deleted.

**Acceptance Scenarios**:

1. **Given** the caregiver selects a program, **When** they begin preparing
   an application, **Then** the system shows required documents, completion
   status, and known deadlines, and sends reminders for those deadlines.
2. **Given** the caregiver uploads a document to verify a checklist item,
   **When** the system records the item's status, **Then** it retains only
   the checklist status and deletes the source document by default. The
   caregiver may explicitly retain it for the active application and can
   delete it at any time; sensitive identity numbers are not copied into the
   checklist.
3. **Given** the caregiver asks the system to submit a form or share an
   application document, visit document, or medication schedule externally,
   **When** the recipient and contents are presented, **Then** nothing is
   submitted or shared until the caregiver gives explicit confirmation
   immediately before that action.

---

### Edge Cases

- If handwriting is illegible or any medicine name or dose has confidence
  below 85%, the system flags the field in red and with text, does not schedule
  a reminder based on it, and directs the caregiver to verify with a
  pharmacist or prescriber.
- If fields conflict or a prescription is incomplete, the system does not
  choose or infer a dose, timing, frequency, or purpose; it asks the caregiver
  to verify the instruction with the prescriber or pharmacist.
- If the caregiver reports a possible side effect, the system records it as
  caregiver-reported, suggests contacting the prescriber or pharmacist for
  personalized advice, and does not conclude that a medicine caused it or
  advise a medication change.
- If no official or reputable health-authority source is available for a
  medication question, the system says it cannot verify reliable information
  and does not invent an explanation.
- If a scheme source is outdated, missing, or unreachable, the system
  identifies the information as unverified and links to the official source
  when available instead of presenting it as current.
- If an uploaded file includes sensitive identity details, the system
  minimizes their use, does not copy them into the application checklist, and
  deletes the source file after its task unless the caregiver chooses to
  retain it for ongoing reference.
- Medication schedules and visit documents remain private to the caregiver
  unless the caregiver explicitly confirms sharing them with an external
  person.
- If an image upload, translation, or reminder cannot be completed, the
  system clearly reports the failure and does not claim the document was
  processed or a reminder was scheduled.
- If the caregiver uses a low-bandwidth channel or voice note, the feature
  offers concise text alternatives and does not require long-form typing.
- Every session clearly identifies the assistant as an AI tool, not a human
  counselor.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept images of printed or legible handwritten
  prescriptions and discharge summaries and extract medicine names, written
  doses, timings, frequencies, and follow-up dates for caregiver review. It
  MUST delete each source image after the caregiver verifies its extraction
  unless the caregiver explicitly chooses to retain it for ongoing reference.
- **FR-002**: The system MUST present extracted medication schedules for
  explicit caregiver verification before saving them or creating reminders.
  Any medicine name or dose with confidence below 85% MUST be visibly flagged
  in red and with text, MUST NOT be used to schedule a reminder, and MUST
  prompt verification with a pharmacist or prescriber.
- **FR-003**: The system MUST explain medical terms and general side-effect
  information in plain language and the caregiver's preferred supported
  language. It MUST use official medicine leaflets or regulator information
  first, then reputable health-authority sources when those are unavailable,
  and show the source. If no reliable source is available, it MUST say so
  rather than generate an unsupported explanation. It MUST NOT diagnose,
  infer a medicine's prescribed purpose when it is not stated by the
  clinician, or recommend starting, stopping, or changing medication.
- **FR-004**: After caregiver confirmation, the system MUST create reminders
  only from the verified schedule and offer a caregiver check-in seven days
  after confirmation. It MUST NOT alter the clinician's instructions.
- **FR-005**: The system MUST record side-effect check-in responses as
  caregiver-reported observations and suggest contacting the prescriber or
  pharmacist for personalized advice. It MUST NOT claim that a medicine
  caused a symptom or recommend a treatment change.
- **FR-006**: The system MUST identify potentially relevant government, NGO,
  and insurance support options using only eligibility information necessary
  for the search, such as region, income bracket, or a caregiver-provided
  diagnosis category. It MUST state that the responsible program determines
  final eligibility.
- **FR-007**: Each program result MUST show its required documents,
  plain-language application steps, last verified date, and an official
  government, insurer, or program-provider source link. Information MUST be
  labeled potentially outdated when it has not been successfully checked
  against its official source within 90 days; unverified information MUST
  also be clearly labeled.
- **FR-008**: The system MUST track application checklist status and known
  deadlines. Sensitive identity numbers MUST NOT be copied into checklist
  entries. It MUST delete each uploaded source document by default after it
  has served to verify a checklist item. The caregiver MAY explicitly retain
  a document for an active application and MUST be able to delete it at any
  time.
- **FR-009**: The system MUST obtain explicit caregiver confirmation
  immediately before submitting a form or sharing any application document,
  visit document, or medication schedule externally. Prior consent or
  completion of a checklist MUST NOT count as confirmation. Medication
  schedules and visit documents MUST remain private to the caregiver unless
  that share is explicitly confirmed.
- **FR-010**: If the system detects self-harm, suicidal ideation, violence, or
  an acute medical emergency in any interaction, it MUST immediately bypass
  routine assistance, display verified local crisis helplines, and alert the
  designated human coordinator.
- **FR-011**: Caregiver and care-recipient health records MUST be encrypted at
  rest and in transit. Personally identifiable information MUST be masked
  before context is sent to any external large language model service.
- **FR-012**: Every session MUST clearly disclose that the assistant is an AI
  tool and not a human counselor.
- **FR-013**: Prescription, scheme-search, and checklist flows MUST be usable
  over low-bandwidth, familiar channels, including WhatsApp, SMS, voice notes,
  and web, and MUST support regional languages and caregivers with low
  digital literacy. When image or audio transfer is unavailable, the system
  MUST offer a concise text alternative where the task allows it.
- **FR-014**: The system MUST report processing, source-verification, and
  reminder-scheduling failures clearly and MUST NOT represent an incomplete
  action as successful.

### Key Entities

- **Visit Document**: A caregiver-provided prescription or discharge summary
  containing clinician-written instructions and follow-up details.
- **Verified Medication Schedule**: A caregiver-confirmed transcription of
  medication instructions, with reminder details and confirmation status.
- **Side-Effect Check-in**: A dated caregiver report of observed symptoms or
  concerns, without a system conclusion about cause.
- **Support Program**: A government, NGO, or insurance option with
  eligibility categories, document requirements, deadlines, source, and last
  verified date.
- **Application Checklist**: A caregiver's completion status for required
  documents and steps, with known deadlines and user-controlled uploads.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: No medication reminder is created before the caregiver verifies
  the corresponding medication name, dose, timing, and frequency.
- **SC-002**: Every extracted medicine name or dose below 85% confidence is
  visibly flagged, excluded from reminder scheduling, and accompanied by a
  pharmacist-or-prescriber verification instruction.
- **SC-003**: Seven days after a caregiver confirms a schedule, the system
  offers the side-effect check-in; all responses are recorded as caregiver
  observations without a causal conclusion, with a prescriber-or-pharmacist
  follow-up suggestion for any reported possible side effect. General
  medication information displays an approved source or says when reliable
  information is unavailable.
- **SC-004**: Every displayed program result includes a source and last
  verified date; unverified results and results not checked against their
  official source within 90 days are visibly labeled.
- **SC-005**: No form is submitted and no application document is shared
  externally without explicit caregiver confirmation immediately before the
  action; medication schedules and visit documents remain private unless
  their sharing is explicitly confirmed.
- **SC-006**: Caregivers can view and update checklist completion and deadlines
  without sensitive identity numbers being copied into checklist entries,
  and can delete retained documents at any time.
- **SC-007**: Caregivers can use the supported feature flows in supported
  regional languages and familiar low-bandwidth channels, with text
  alternatives where image or audio transfer is unavailable.

## Assumptions

- The caregiver's confirmation applies to the specific extracted schedule
  shown for review; a correction requires review and confirmation of the
  corrected details before reminders are created.
- The seven-day check-in is timed from caregiver confirmation, not from an
  inferred medication start date.
- Medicine purpose is not inferred from a medicine name. General medicine
  information is informational, uses official or reputable health-authority
  sources, and is not a personalized assessment.
- Eligibility search uses broad, non-identifying categories where possible;
  final eligibility and current requirements are determined by the
  responsible program authority.
- This feature organizes and tracks applications but does not submit
  government, NGO, or insurance applications automatically.
- Uploaded source documents are deleted by default after verification; the
  caregiver may explicitly retain them for an active application or ongoing
  reference and may delete retained files at any time.
