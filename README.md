# Claude Stock

A Claude Code setup that works as a stock-research and trading partner. The agent does the
searching and the math. You make the decisions.

- **Company research:** financials, valuation vs peers, catalysts, risks, insiders,
  analysts, technicals, bull / base / bear scenarios and a buy grade with buy-below prices.
- **Merger arbitrage (Canada):** finds pending TSX / TSXV / CSE / Cboe Canada takeovers and
  computes spread, closing probability, edge, break loss and a limit-price ceiling.
- **Position tracking:** reads your broker screenshots, updates a trade journal and
  re-grades open positions.

Every number must come from a source fetched in the session. Gaps are marked
`NOT FOUND` or `UNVERIFIED` rather than filled in.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Python 3 (for `tools/fmt_md.py`)
- Recommended: the Claude in Chrome extension. TMX Money, SEC EDGAR and company IR pages
  read much better through the browser than through web search.

## Setup

1. **Make a private copy.** Your journal and research will hold your positions and
   capital. Don't commit them to a public repo. Create your own private repo from this
   one, or add `trade-journal.md`, `runs/` and `research/` to `.gitignore`.
2. **Fill in the investor profile** in `CLAUDE.md`: broker, account(s) in scope, base
   currency, FX fee, commission and position size.
3. **Fill in `trade-journal.md`:** capital, open positions and holdings.
4. **Set the playbook parameters** in `tsx-takeover-arb-agent-prompt.md` §0 before the
   first arb run (dates, size range, broker, FX fee).
5. Open the folder in Claude Code. `CLAUDE.md` and the skills load automatically.

## Usage

| You type                              | What happens                                           |
| ------------------------------------- | ------------------------------------------------------ |
| `/acquirer-check AMZN`                | Full research report → `research/AMZN-<date>.md`       |
| `/acquirer-check SHOP --quick`        | Snapshot, catalysts, risks, provisional grade          |
| `/acquirer-check <buyer> --acquirer`  | Credit and ability-to-close check on a takeover buyer  |
| `/position-refresh` + screenshots     | Updates positions, re-grades, explains moves           |
| `/deal-filing-extractor <PDF or URL>` | Deal terms sheet from a circular, agreement or 6-K     |
| "Run the arb playbook"                | Full Canadian takeover-arb scan → `runs/<date>-run.md` |

Plain requests work too: "research Descartes", "why did my position drop today",
"read this circular".

## How the grades work

**Stocks (`acquirer-check`):** is it a good buy at today's price?

| Grade | Meaning     | Rule of thumb                                               |
| ----- | ----------- | ----------------------------------------------------------- |
| A     | Strong buy  | E[R] ≥ hurdle + 12 pp, bear loss ≤ 25%, improving           |
| B     | Buy         | E[R] ≥ hurdle + 5 pp, bear loss ≤ 35%, stable or improving  |
| C     | Hold / wait | In between, or a B with earnings / a ruling within ~30 days |
| D     | Avoid       | E[R] < −5%, deteriorating, or unverifiable                  |

- **E[R]** is the 12-month probability-weighted scenario value plus dividends, compared
  with today's price.
- **Hurdle** is the 3-month T-bill yield.
- **Quality** (High / Medium / Low) is rated separately. A great company at a full price
  can be High quality and grade C.
- Every report prints **B-below** and **A-below** prices.

**Merger arb (playbook §9):** graded on edge (your closing probability minus the
market-implied one), downside-to-upside ratio and liquidity. See §6–§9 of the playbook.

## Files

| Path                               | Role                                          |
| ---------------------------------- | --------------------------------------------- |
| `CLAUDE.md`                        | Project rules, investor profile, data sources |
| `tsx-takeover-arb-agent-prompt.md` | Arb playbook: rules, math, grading, format    |
| `trade-journal.md`                 | Capital, positions, orders, closed, passed-on |
| `.claude/skills/`                  | The three skills above                        |
| `tools/fmt_md.py`                  | Aligns Markdown table pipes                   |
| `runs/`, `research/`               | Output files (one per run / report)           |

## It learns as you use it

When a run or a conversation teaches something new, the agent adds a dated lesson to
playbook §13 and edits the section it affects. The seed lessons in §13 come from the
original setup.

## Notes

- Built for a Canadian investor (TSX data sources, CAD accounts, Bank of Canada hurdle).
  Elsewhere, change the profile, the hurdle series and the data sources in `CLAUDE.md`.
- The `acquirer-check` report structure is adapted from claude-equity-research (MIT
  License, © 2024 Quant Sentiment AI).
- This is a research tool. Its output can be wrong. Check prices and filings yourself
  before you trade.
