# Trade journal

Every order and position, plus deals looked at and passed on.
The agent refreshes every open item at the start of each run (prompt §4 Phase E step 0).
Outcomes feed the calibration log (prompt §10).

## Capital

As reported by the user on `<YYYY-MM-DD>`. Update whenever cash moves.

| Bucket                        | Amount (C$) | Note                                   |
| ----------------------------- | ----------- | -------------------------------------- |
| `<account>` — cash            | —           | —                                      |
| `<account>` — holdings        | —           | —                                      |
| Outside cash, ready to deploy | —           | —                                      |
| Investable capital            | —           | Basis for sizing (playbook §11 rule 3) |

- **Before moving cash in:** check the account's contribution room or limits.

## Open orders / positions

| Opened | Ticker | Side | Price (C$) | Shares | Status | p_est | Ceiling | Break loss |
| ------ | ------ | ---- | ---------- | ------ | ------ | ----- | ------- | ---------- |

Add a `### <TICKER> notes` section per position: thesis, timeline, approvals, entry,
size, ceiling, cancel / review triggers, and a link to the latest `runs/` file.

## Other holdings (not arbitrage)

Long-term holdings the user reports. Not refreshed each run; listed so position sizing
(§11 rule 3) sees the whole account.

| Bought | Ticker | Shares | Avg price (C$) | Cost (C$) | Account |
| ------ | ------ | ------ | -------------- | --------- | ------- |

## Closed

| Opened | Closed | Ticker | Entry | Exit / payout | P&L (C$) | Outcome (closed / late / broke / bumped) | What we got right / wrong |
| ------ | ------ | ------ | ----- | ------------- | -------- | ---------------------------------------- | ------------------------- |

## Passed on (and why)

| Date | Ticker | Why we passed | What happened later |
| ---- | ------ | ------------- | ------------------- |
