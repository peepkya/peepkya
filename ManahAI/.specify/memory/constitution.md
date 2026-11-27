<!--
Sync Impact Report
Version change: unratified scaffold → 1.0.0 (initial constitution)
Modified principles: none; seven principles established from the project brief
Added sections: Safety & Accessibility; Product and Specification Constraints
Removed sections: none
Follow-up TODO: confirm the original ratification date
-->

# Caregiver Support Agentic System Constitution

## Core Principles

### I. Non-Clinical Boundary
The system MUST NOT diagnose conditions, prescribe medication, recommend dosage
changes, or represent itself as a replacement for a licensed clinician. It MUST
support caregivers with practical, non-clinical assistance and encourage
appropriate professional care. This boundary protects the care recipient and
caregiver from unsafe substitution of AI for clinical judgment.

### II. Mandatory Crisis Escalation
When the system detects self-harm, suicidal ideation, violence, or an acute
medical emergency, it MUST immediately bypass standard AI response generation,
display verified local crisis helplines, and alert the designated human
coordinators. Crisis handling MUST take precedence over routine assistance so
urgent situations reach human support without delay.

### III. Human Confirmation for High-Stakes Actions
The system MUST obtain explicit caregiver confirmation immediately before
submitting a government form, sending a message to an external family member,
or triggering a respite alert. It MUST NOT treat prior consent, inferred intent,
or an automated recommendation as confirmation. This preserves caregiver
control over consequential actions.

### IV. Transparent AI Identity
Every session MUST clearly identify the assistant as an AI tool and MUST NOT
imply that it is a human counselor. This disclosure supports informed use and
appropriate expectations.

### V. Privacy and Data Protection
Caregiver and care-recipient health records MUST be encrypted at rest and in
transit. Personally identifiable information MUST be masked before any context
is sent to an external large language model API. Features MUST minimize the
personal and health data they collect, retain, and disclose to what is needed
for the caregiver-requested outcome.

### VI. Accessible, Low-Friction Support
Every core caregiver feature MUST be designed to work over low-bandwidth,
familiar channels, including WhatsApp, SMS, and voice notes, as well as web
interfaces. The experience MUST support regional languages and people with low
digital literacy. This ensures support is usable beyond high-bandwidth,
English-first, or technically experienced audiences.

### VII. Technology-Neutral Feature Specifications
Feature specifications (`spec.md`) MUST describe user behavior, needs, and
outcomes only. Framework, database, and other implementation decisions MUST be
documented in `plan.md`, not in `spec.md`. This separation keeps feature
requirements focused on user value and independently reviewable from design
choices.

## Safety and Accessibility

The system exists to reduce the emotional, administrative, and crisis-management
burden on family caregivers supporting loved ones with any mental health
condition. Product decisions MUST prioritize empathetic, reliable support and
the safety, privacy, and agency of caregivers and care recipients.

## Product and Specification Constraints

All feature work MUST preserve the seven Core Principles. Specifications MUST
include observable acceptance outcomes for applicable safety, privacy,
confirmation, transparency, and accessibility requirements. Plans MUST describe
how those outcomes will be delivered without weakening the user-facing
requirements.

## Governance

This constitution governs feature specifications, plans, implementation, and
reviews. Every feature review MUST check applicable principles, including the
crisis escalation and human-confirmation requirements. A proposal that cannot
meet a principle MUST be revised or explicitly brought to the project
maintainers for a constitution amendment before implementation; no feature may
silently waive a safety requirement.

Amendments require maintainer approval, an updated version and amendment date,
and a summary of the affected principles. Constitution versions use semantic
versioning: MAJOR for backward-incompatible changes to existing principles,
MINOR for new principles or materially expanded obligations, and PATCH for
clarifications that do not change obligations. Compliance MUST be reviewed
during feature planning and code review.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-11-27
