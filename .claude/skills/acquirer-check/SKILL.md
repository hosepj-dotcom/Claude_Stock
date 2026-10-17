---
name: acquirer-check
description: Deep research on any company or stock — financials, valuation, trends, catalysts, regulatory and product news, insider activity, credit, analyst views — for an investment decision the user makes. Use when the user asks to research, analyze, check or size up a company, stock or ETF, asks about a deal's acquirer, or wants new ideas screened. Pass --acquirer for a credit-focused check on a takeover buyer.
argument-hint: <TICKER or company> [--acquirer] [--quick]
---

# Acquirer check / company research

Do the heavy lifting on a company so the user can make the call. The user knows investing;
give them the complete, sourced picture and how the evidence leans. No advisor disclaimers.

Report structure adapted from claude-equity-research (MIT License, © 2024 Quant Sentiment AI,
github.com/quant-sentiment-ai/claude-equity-research), with this project's sourcing rules added.

## Modes

| Mode         | Use for                                | Depth                        |
| ------------ | -------------------------------------- | ---------------------------- |
| default      | Any stock or idea the user is weighing | Full report, all sections    |
| `--acquirer` | The buyer in a takeover deal           | Credit and ability-to-close  |
| `--quick`    | A first look before going deeper       | Snapshot + catalysts + risks |

## Sourcing rules (non-negotiable)

1. **Every number has a source and a date** from this session. Never fill from memory.
2. **Missing data = `NOT FOUND`**, not an estimate. Options flow, insider dollar amounts and
   analyst targets are often unavailable for small caps — say so and move on.
3. **Primary first:** company filings (SEDAR+, EDGAR), releases and results beat news,
   which beats aggregators and blogs. Paywalled articles: headline + date only.
4. **Currency on every figure.** Convert with a dated FX rate when needed.
5. **Label inference** ("likely", "suggests") separately from reported facts.

## Research steps

Run independent searches in parallel. Use Claude in Chrome for pages WebSearch summarises
poorly (TMX Money, EDGAR, company IR). Close tabs when done.

**Canadian-listed stocks:** before writing, open TMX Money in Chrome: the quote page, the
News page (both the Press Releases and In The Media tabs) and the Insider Activity tab
(12-month range). See "Data sources that work" in `CLAUDE.md`.

| Area                 | Look for                                                        | Where                                  |
| -------------------- | --------------------------------------------------------------- | -------------------------------------- |
| Snapshot             | Price, 52-wk range, market cap, volume, dividend                | TMX Money, stockanalysis.com           |
| Financials           | Revenue, margins, EPS, FCF, debt, cash — last 4–8 quarters      | Latest results release, 10-Q/40-F/MD&A |
| Trend                | YoY and QoQ change; flag improving or declining                 | Same                                   |
| Valuation            | P/E, EV/EBITDA, P/S, P/B vs 2–4 named peers                     | stockanalysis.com, filings             |
| Catalysts            | Earnings dates, product launches, approvals, contracts, M&A     | Company releases, TMX news             |
| Regulatory and legal | Investigations, approvals, lawsuits, rule changes               | Releases, regulators, news             |
| Insiders and owners  | Insider buys/sells, buybacks, major holders, short interest     | SEDI/Form 4, TMX "Insider Activity"    |
| Analysts             | Ratings, targets, recent changes (name the firm)                | News, MarketBeat, TMX                  |
| Technicals           | Trend vs 50/200-day, support/resistance, volume                 | Chart data pages                       |
| Credit               | Debt maturities, leverage, interest cover, ratings, bond yields | Filings, rating releases, bond quotes  |

**`--acquirer` mode** puts Credit first and adds: deal funding sources, commitment letters,
liquidity vs the deal size, maturities before the deal's outside date, restructuring
history, bearish credit commentary, and other deals competing for the same cash. Finish
with the effect on the target's closing probability (arb playbook §7.2 rows).

## Output

Save to `research/<TICKER>-YYYY-MM-DD.md`, following playbook §9-H (bottom line first,
narrow aligned tables, short lines). Then run `python3 tools/fmt_md.py <file>`.

```
# <Company> (<TICKER>, <exchange>) — research, YYYY-MM-DD

## Bottom line            3–6 bullets: what it is, the case, the risk, how evidence leans
## Grade                  the grade table (see Grading) + one line on what moves it
## Snapshot               price, range, cap, volume, yield (one table)
## Financials             table: last 4–8 quarters, YoY/QoQ arrows; 2–3 bullets on trend
## Valuation vs peers     table: multiples vs named peers
## Catalysts              table: date | event | why it matters (next 0–6 and 6–24 months)
## Risks                  company, sector, macro, credit — bullets
## Insiders, owners, analysts
## Technicals             trend, levels, volume
## Scenarios              bull / base / bear: price, what has to happen, probability
## Evidence lean          Positive / Mixed / Negative, with the 3 facts that decide it,
                          and what would change the view
## Data gaps              what was NOT FOUND or UNVERIFIED
## Sources                bullet list of links with dates
```

- **Scenarios:** probabilities must sum to 100% and come with the reasoning.
- **Evidence lean:** summarise the data; the user decides. Note fit with their holdings
  (account concentration, overlap with positions and holdings in `trade-journal.md`,
  which line to buy and whether the FX fee from the investor profile applies) when
  relevant.
- **`--quick`:** Bottom line, Grade (marked provisional), Snapshot, Catalysts, Risks,
  Data gaps only.

## Grading (every run)

The grade answers one question: **is this a good buy at today's price?** Quality is
rated separately, so a great company at a full price can be High quality and grade C.

**Inputs**

- **E[R], 12 months** = (probability-weighted scenario price + 12-month dividends) ÷ price − 1.
- **Hurdle** = 3-month T-bill (playbook §0 `HURDLE_RATE`; Bank of Canada series
  TB.CDN.90D.MID). Refresh it if the last value is over a week old.
- **Bear loss** = bear-case price ÷ price − 1.

| Grade | Meaning     | Criteria (all must hold)                                                  |
| ----- | ----------- | ------------------------------------------------------------------------- |
| A     | Strong buy  | E[R] ≥ hurdle + 12 pp; bear loss ≤ 25%; fundamentals improving            |
| B     | Buy         | E[R] ≥ hurdle + 5 pp; bear loss ≤ 35%; fundamentals stable or improving   |
| C     | Hold / wait | E[R] between −5% and hurdle + 5 pp, or a B case with a binary event ahead |
| D     | Avoid       | E[R] < −5%, fundamentals deteriorating, or speculative / unverifiable     |

| Quality | Criteria                                                          |
| ------- | ----------------------------------------------------------------- |
| High    | Profitable, growing, positive FCF, net cash or modest debt        |
| Medium  | Profitable but slowing, or meaningful debt, or one key dependency |
| Low     | Losses, cash burn, heavy debt, or going-concern / dilution risk   |

**Buy-below prices.** Like the arb ceiling, always print the prices where the grade improves:

- **B below** = (weighted value + dividends) ÷ (1 + hurdle + 5 pp)
- **A below** = (weighted value + dividends) ÷ (1 + hurdle + 12 pp)

**Grade table** (top of the report; one row per stock when several are run):

`Grade | Stock | Price | Weighted value | E[R] 12m | Bear loss | Quality | B below | A below | Next catalyst`

Rules:

- Never grade A or B before the news, results and insider checks are done.
- A binary event inside ~30 days (earnings, ruling, vote) caps the grade at C unless the
  bear case is already priced in. Say so.
- Re-grade on every update run, and show the previous grade and why it changed.

## Chat reply

Grade line first (grade, quality, B-below price), then bottom-line bullets, the evidence
lean, the biggest data gap, and the file path.
If the user then trades, log it in `trade-journal.md`.
