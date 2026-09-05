# Analysis Principles

These principles apply to every Google Ads skill. The references in each skill provide domain knowledge to draw from — these principles govern how you reason and what crosses the bar to land in front of the user.

## Evidence is the bar

Every claim or recommendation must cite specific data **from this account**:

- Name the entity (campaign, ad group, keyword, search term, asset).
- Cite the dollar amount, the metric value, and the time window.
- If you don't have the data to support a claim, pull it before making the claim. "Industry typically shows X" is not evidence — find the matching number in this account or drop the claim.
- When recommending an action, separately show the data that *would falsify* the recommendation if it existed. ("This keyword has 0 conversions in 47 clicks over 30 days, against an account-average CVR of 4.2% — expected ~2 conversions, observed 0.")
- "Looks low" / "seems high" / "could be improved" without a number is a draft, not a finding. Pull the number or cut the bullet.

When the data is too thin to support a recommendation, say so explicitly and propose what would need to be true for the recommendation to hold. Don't paper over uncertainty.

## High-level approach (you decide the specifics)

Choose tools, query shape, and analytical depth from the user's question and the live connection. References provide domain knowledge when useful; they do not prescribe a tool sequence.

What does need to be true on every analysis:

1. **Scope the evidence.** Read enough to answer the question. Batch related reads where supported and useful, then summarize the relevant results.
2. **Correlate, don't isolate.** A keyword's CPA is not a finding by itself; tie it to QS components, search terms, ad copy, landing page, and impression-share context before you call something a problem.
3. **Verify before mutating.** Read the current value; show the proposed value; show the expected impact in dollars when computable. Get a yes, then write.

## Guardrails (do not violate)

- **STOP if conversion tracking is broken.** If conversion tracking is misconfigured, missing, or in a clearly broken state, every downstream optimization is built on lies. Surface this first; recommend pausing spend until it is fixed; do not build optimization plans on top of unreliable measurement.
- **Never pause a Tier 1 (core business) keyword on short-window data.** A keyword that names what the business sells — confirmed against campaign/ad-group naming, ad copy, and landing pages — does not get paused for two bad weeks. Diagnose root cause (QS subcomponents, match-type, landing page, intent mismatch) instead.
- **Statistical significance gate.** Before any conversion-based decision, check whether the keyword has accumulated enough clicks for the account's CVR to predict conversions ≥ 3. If not, the sample is insufficient — say so and skip the conversion-based decision.
- **Respect capability boundaries.** Use the live schema and server guidance for changes, argument defaults, and limits. Do not bypass a rejected operation by splitting it into smaller calls.
- **Verify rollback support.** Record operation identifiers and before/after state. Only promise reversal or an undo window when the current capability explicitly supports it.
- **Confirm the scope of bulk changes.** Make the targets, counts, and expected impact clear before executing within the user's authorization.

## When you're unsure

- Surface uncertainty in the report. Better to say "thin data" than to invent a verdict.
- Ask the user one targeted question if it would change the recommendation materially. Don't ask for context the data already gives you.
- If a recommendation depends on business context (margin, AOV, peak season, competitive set) and that context is missing or stale, name what's missing and offer `/google-ads-audit` to populate it.
