---
name: position-refresh
description: Refresh the user's open merger-arb positions and pending orders. Use when the user sends broker screenshots, reports a fill or new order, asks why a held stock moved, or asks to update/check their positions.
---

# Position refresh

Re-underwrite every open position and pending order in `trade-journal.md`, using the
playbook (`tsx-takeover-arb-agent-prompt.md`) for all math and rules. This is a partial
update, not a full §4 run.

## Inputs

- Screenshots the user names (iPhone screenshots are usually `~/Downloads/IMG_*.HEIC`),
  and anything they type.
- `trade-journal.md` and the newest file in `runs/`.

## Steps

### 1. Read the screenshots

```bash
# macOS: convert HEIC screenshots before reading
sips -s format jpeg -Z 1600 <in>.HEIC --out <scratchpad>/<name>.jpg
mdls -name kMDItemContentCreationDate <in>.HEIC      # capture time
```

From each one, record: ticker, shares, average price, book cost, account, % of account,
bid/ask/last/open/high/low, volume vs average, and for orders: limit, quantity, status,
submitted time, expiry. Note the account's cash/buying power if shown.

Scope is the account(s) in the investor profile (`CLAUDE.md`). A security page's
"Holdings" card may total all accounts, so take share counts from the order screen or the
in-scope account view.

Compare with the journal. Flag:
- **New items** not yet in the journal.
- **Fill vs plan:** price above the ceiling, or more shares than planned. State it plainly.
- **Funding:** pending orders larger than the available cash.

### 2. Pull live data (Claude in Chrome, one new tab)

For each position's target **and** acquirer:

| Data                | Where                                                       |
| ------------------- | ----------------------------------------------------------- |
| Quote               | `money.tmx.com/en/quote/<TICKER>` (US: `<TICKER>:US`)       |
| News, both tabs     | `money.tmx.com/en/quote/<TICKER>/news`, then "In The Media" |
| US interlisted line | `money.tmx.com/en/quote/<US_TICKER>:US`                     |
| USD/CAD             | `google.com/finance/quote/USD-CAD`                          |
| Filings             | SEC EDGAR 6-K/8-K for interlisted names; SEDAR+             |

Batch navigation and `get_page_text` calls with `browser_batch`. Close the tab at the end.

### 3. Explain any move

For a price move the user asks about, split it into a table:

| Driver                        | Effect (C$/sh) | Share of move |
| ----------------------------- | -------------- | ------------- |
| FX change                     |                |               |
| Acquirer stock change         |                |               |
| Spread change (the remainder) |                |               |

Check the US line in USD: if it moved too, it's the spread, not FX.
Say clearly whether there is news. Label inferences as inferences.

### 4. Recompute (playbook §6)

For each position, with and without the FX fee where it applies:
deal value, profit at the user's cost (per share and in C$ on their size), p_mkt at
today's bid, ceiling (§6.8), break loss at D_adj in C$, and break loss as % of the account.
Show the deal-value formula on its own line, then the result.

Keep p_est unless news justifies a change. Show each adjustment (§7.2).

**Re-grade every position** (arb: playbook §9-A grades; other stocks: the
`acquirer-check` grading). Put a grade table near the top of the update file with columns
`Grade | Prev | Stock | Price | Key number | Why it changed`. Never drop the grade on an update.

### 5. Pending orders

For each one: still below the ceiling? Funded? Does the expiry outlive a catalyst
(vote, regulatory decision)? Name the resting-order risk (§8).

### 6. Write it down

1. New file `runs/YYYY-MM-DD-<tickers>-update.md`, following playbook §9-H:
   `## Bottom line` first, then prices used, open items, why it moved, refreshed
   numbers, pending orders, sources.
2. Update `trade-journal.md`: the short table row, plus the `### <TICKER> notes` bullets.
   Non-arb holdings go under "Other holdings".
3. New lessons → playbook §13 (and the section they change).
4. Run `python3 tools/fmt_md.py <each .md file you changed>`.

### 7. Reply in chat

Bottom line first: why it moved, the position in C$ (close / break), anything the user
must act on (funding, expiry, ceiling breached). Short bullets, one small table at most.
No disclaimer line in chat; the run file keeps the playbook's footer line.
