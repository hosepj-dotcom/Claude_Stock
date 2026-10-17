---
name: deal-filing-extractor
description: Extract the deal terms that matter for merger arbitrage from a takeover filing — management information circular, arrangement agreement, take-over bid circular, material change report, 6-K/8-K or deal press release. Use when the user gives a filing PDF or URL, or asks to read a deal's circular or agreement.
---

# Deal filing extractor

Turn a long deal filing into a short, sourced terms sheet. Every value must be quoted
from the document, with its page or section. Never fill a gap from memory or another deal.

## Inputs

- A local PDF, or a URL (SEC EDGAR, SEDAR+, company site, newswire).
- The ticker. If not given, take it from the document.

## Reading the document

- **Local PDF:** use the Read tool with `pages` (max 20 per call). Read the table of
  contents first, then jump to the sections below.
- **Web page / EDGAR HTML:** Claude in Chrome `get_page_text`.
- **EDGAR exhibits:** the 6-K cover summarises; the full agreement is usually Exhibit 99.1.
- Circulars are long. Go straight to: Summary, The Arrangement, Required Approvals,
  Regulatory Matters, Conditions, Termination, Dissent Rights, Currency/Payment,
  Canadian/US tax (for the currency election), and the timeline/notice pages.

## What to extract

| Group         | Items                                                                                            |
| ------------- | ------------------------------------------------------------------------------------------------ |
| Consideration | Per-share cash and stock, currency, exchange ratio, proration, CVRs, collars                     |
| Payout        | Paying currency; **CAD election** and its FX rate; depositary; fractional shares                 |
| Dates         | Record date, meeting date, proxy deadline, interim/final order                                   |
| Closing       | Earliest effective date, expected close, outside date, extension terms                           |
| Votes         | 2/3 threshold; MI 61-101 minority vote and **whose votes are excluded**; lock-ups (%, hard/soft) |
| Approvals     | Each regulator by name (Competition Act, ICA, HSR, FCC, state, sector, foreign) with status      |
| Financing     | Sources, commitment letter expiry, financing condition, guarantees                               |
| Protection    | Target break fee, reverse break fee and triggers, fiduciary out, match right, go-shop            |
| Conditions    | Dissent cap, MAC, other closing conditions                                                       |
| Other lines   | Treatment of options, RSUs, warrants, debentures, preferreds, `.U` lines                         |
| Signals       | Fairness opinion range, background of the sale process, other bidders                            |

## Output

1. **File:** `runs/YYYY-MM-DD-<ticker>-filing.md`, following playbook §9-H:
   - `## Bottom line`: 3–6 bullets on what is **new or different** vs the journal and the
     newest run file (e.g. "payout is USD only, no CAD election → FX fee applies").
   - `## Terms` table: `Item | Value | Source`. The source cell is short (`Circ. p.42`,
     `AA §8.1`). Missing items: `NOT IN DOCUMENT`. Unclear: `UNVERIFIED` + one-line reason.
   - `## Key quotes`: up to 5 short direct quotes for the items that change the math
     (payout currency, minority-vote exclusions, outside date, reverse fee).
   - `## Impact on the trade`: which playbook inputs change (p_est §7.2, D §6.4,
     timing §7.3, FX fee §6.2) and by how much. Recompute the ceiling if any did.
2. **Journal:** update the ticker's notes in `trade-journal.md`. Resolve or keep
   `FX_FEE_UNRESOLVED`.
3. Run `python3 tools/fmt_md.py <each .md file you changed>`.
4. **Chat:** the bottom-line bullets, then the path to the file.

End the file with: *Information only, not investment advice. Verify prices and filings before trading.*
