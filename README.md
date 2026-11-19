# Portfolio Review Queue – JuSIIIIAE Team 1

Dashboard that tells an impact-investment fund committee **which projects to review first, and why**.

## Run it
Open `index.html` in any browser (double-click). It is one self-contained file and works offline, so it is safe for a live demo.

If the dataset changes, put the new `.xlsx` in `data/` and re-embed it:

```bash
python3 tools/build_data.py
```

## What it does
- **Review queue**: all 250 projects grouped into *Review now* (top 10), *Review later* (ranks 11–50), *Not ready* (rest) and *Completed* (65, at the bottom). Filters for group, status, sector, region, policy goal, key risk, red flag, min. score and max. budget. Click a row for the full explanation. You can export the filtered list to CSV.
- **Insights**: the "high score ≠ top priority" examples, overall vs adjusted score, red-flag counts, and review group by status.
- **Method & rules**: the team rules in plain language, plus live controls for what-if scenarios (penalty, thresholds, which flags and risks count, group sizes).

## Scoring (team defaults, agreed in Meeting 1)
`adjusted = overall score − 0.5 × number of red flags`

| Red flag | Trigger |
|---|---|
| Early stage | Status *Concept* or *In planning* |
| Serious risk | Key risk is *Funding uncertainty*, *Regulatory approval delays* or *Maintenance costs* |
| Big budget + early | Early stage **and** budget > €20M (so −1.0 in total, together with the early-stage flag) |
| Weak spot | Any of the 10 dimension scores ≤ 1 |

Strict rule: a project with a 0 in any dimension can never be *Review now*.
Tiebreak: adjusted score → overall score → fewer flags → higher lowest dimension → project ID.

## Results with the team rules (verified 19 Nov 2026)
- Review now: SYN-038, 078, 152, 102, 149, 163, 154, 012, 214, 036
- High score, not top priority: **SYN-177** (overall 4.50, 3rd highest active project) → rank 40 due to *Early stage* + *Big budget + early*. **SYN-120** (4.40) → rank 46.
- Boundary ties: SYN-036 (rank 10) and SYN-208 (rank 11) both score 4.10; the tiebreak decides. Same at rank 50/51 (SYN-010 vs SYN-231, 3.35).
- None of the 10 active zero-score projects ranks above #116, so the strict rule never changes the default top 10. It is a safety net.
- Adjusted scores can go below 0 (e.g. SYN-148: −0.2). This only affects the ranking.

## Suggested test scenarios (for the testing record)
| # | Scenario | Steps | Expected |
|---|---|---|---|
| 1 | High average, but flagged | Search `SYN-177`, open it | Review later, rank 40, 4.50 − 2 × 0.5 = 3.50, two flags explained, info requests listed |
| 2 | Rules sensitivity | Method & rules → penalty 0 | Warning banner appears; SYN-177, SYN-120 move into Review now; reset restores the default top 10 |
| 3 | Strict rule (edge case) | Set "Review now: top" to 130 | SYN-064 (adjusted rank #116) is still kept out of Review now and its explanation names the strict rule (0 in Technological) |
| 4 | Missing information / Not ready | Group = Not ready, open any project with no flags | Explanation says the score is just lower and suggests evidence for its weakest dimensions |
| 5 | Filters | Status = Concept, Group = Review now | Only SYN-012 |
| 6 | Completed | Group = Completed | 65 projects, listed last, no review action |
