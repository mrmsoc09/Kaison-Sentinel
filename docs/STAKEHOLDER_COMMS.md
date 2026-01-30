# Stakeholder Communications (Payout-Safe)

## Purpose
- Provide calm, evidence-first communication to program stakeholders.
- Avoid aggressive payout demands; request fair assessment per program policy.
- Enforce HiL gate before any email is queued.

## Rules
- No email is queued unless `hil_confirmed=true`.
- No report is ready unless screen recording evidence is attached.
- Summaries must align with report evidence and scope.

## Workflow
1) Generate email draft (`/api/email/draft`) using run_id
2) Review/edit in GUI
3) Confirm HiL checkbox
4) Queue email (`/api/notify/email`) — stored locally in `outputs/emails/`

## Tone
- Respectful, factual, concise.
- Avoid emotional or payout inflation language.
- Emphasize evidence and reproduction steps.

## Payout Guidance
- Request alignment with program policy.
- Never threaten or demand.
- Provide objective severity rationale.
