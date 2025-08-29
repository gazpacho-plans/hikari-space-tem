# Space TEM — Economy & Control Points (GDP-based Systems Spec v1.1)

Purpose: define the exact math & logic to implement. Names use **snake\_case**; one weekly turn.

---

## 1) State (per nation)

```yaml
# Core economy
gdp_bn: float                  # GDP in billions (Prosperity = GDP)
gross_cap: float               # top-line flow scale at high GDP
pros_ref: float                # reference GDP for soft cap (use CP3 GDP ≈ 2401)
exploit_share: float           # e ∈ [0,1]; reinvest_share = 1 - e

# Civics
education: int   # 1..10
unrest:    int   # 0..5
bureaucracy: int # 1..10

# CPs
cp_total: int                 # 1..6 (derived each turn)
cp_controlled_by_faction: {faction_id: int}

# Science & space
base_science: float           # national science scale
has_launch_capability: bool
launch_facilities: int
```

Global constants (tune once):

```yaml
cp_thresholds_gdp: [81, 625, 2401, 6561, 14641]   # edges between CP counts (Bn)
econ_scale_weekly: float        # global multiplier for gross_flow per week
growth_lambda: float            # GDP gain per reinvest point (Bn per point)
```

---

## 2) Derived helpers

```text
clamp(x, lo, hi) = max(lo, min(hi, x))

edu_mult    = 1.0 + 0.02 * (education - 5)         # ±10%
unrest_mult = 1.0 - 0.08 * unrest                  # 0..-40%
bureau_mult = 1.0 - 0.03 * (bureaucracy - 5)       # ±15%
civics_mult = edu_mult * unrest_mult * bureau_mult

# CPs from GDP (TI-style, 1..6)
# Use thresholds for UI, keep formula for code if preferred
cp_total = clamp(round((gdp_bn ** 0.25) / 2), 1, 6)
```

---

## 3) Gross flow (weekly investment points)

**Soft cap via exponent < 1.0** (diminishing returns). Apply civics after scale.

```text
gross_flow = econ_scale_weekly * (gdp_bn ** 0.35) * civics_mult
```

> Intuition: when GDP doubles, gross\_flow grows slower than ×2.

*(Optional maintenance hook, off by default)*: subtract `force_penalty = 0.0 + navy_pen * navies + army_pen * armies` from `gross_flow` before clamping to ≥0.

---

## 4) Budget split (consumes 100% of the pie)

```text
reinvest_share = 1 - exploit_share
payout_pot     = exploit_share  * gross_flow   # becomes 💰 Money
reinvest_pot   = reinvest_share * gross_flow   # funds builds/reforms
```

### Money distribution

```text
cp_share(f)    = cp_controlled_by_faction[f] / cp_total
faction_money  = payout_pot * cp_share(f)
player_money   = faction_money / players_in_faction
```

---

## 5) GDP update (growth only from reinvestment)

```text
gdp_bn_next = gdp_bn + growth_lambda * reinvest_pot
```

* Exploitation **never** raises GDP.
* No auto-surplus → GDP. (If you later need very-long-campaign damping, add a tiny decay term separately.)

---

## 6) Science (nation) → Research Income (faction)

```text
pros_science_mult = 0.6 + 0.4 * clamp(gdp_bn / pros_ref, 0, 1)  # 60%→100% ramp
science_output    = base_science * edu_mult * pros_science_mult
research_income   = science_output * cp_share(f)   # applied directly to projects; no pool
```

**Boost:** `boost_income = 0.1 * launch_facilities` per turn (requires launch capability).  
**Ops:** mainly from Orgs; also councillor traits and some habs.

---

## 7) Public Opinion (PO)

* Store as `{faction_id: float}` that **sums to 100.0**.
* Mission bonus (rule of thumb): `floor(po_percent/10) − 3`.
* **Executive gate:** need ⌊non‑exec majority⌋ CPs **and** `po_percent ≥ 60`.

PO change (gain Δ for faction A): add Δ to A, subtract proportionally from others, renormalize to 100, clamp per‑faction to \[0,100].

---

## 8) Turn loop (reference pseudocode)

```python
def update_nation(n):
    # 1) Civics
    edu_mult    = 1.0 + 0.02 * (n.education - 5)
    unrest_mult = 1.0 - 0.08 * n.unrest
    bureau_mult = 1.0 - 0.03 * (n.bureaucracy - 5)
    civics_mult = edu_mult * unrest_mult * bureau_mult

    # 2) Gross flow (weekly)
    gross_flow  = n.econ_scale_weekly * (n.gdp_bn ** 0.35) * civics_mult
    gross_flow  = max(0.0, gross_flow)  # after optional force penalties

    # 3) Budget split
    payout_pot   = n.exploit_share * gross_flow
    reinvest_pot = (1 - n.exploit_share) * gross_flow

    # 4) GDP growth (only from reinvestment)
    n.gdp_bn += n.growth_lambda * reinvest_pot

    # 5) CP count from GDP
    n.cp_total = max(1, min(6, round((n.gdp_bn ** 0.25) / 2)))

    # 6) Science → Research Income
    pros_science_mult = 0.6 + 0.4 * max(0, min(1, n.gdp_bn / n.pros_ref))
    science_output    = n.base_science * edu_mult * pros_science_mult

    for f in factions_controlling_any_cp(n):
        share = n.cp_controlled_by_faction[f] / n.cp_total
        f.money += payout_pot * share
        apply_research_income(f, n, science_output * share)

    # 7) Boost (if capable)
    n.boost_income = 0.1 * n.launch_facilities if n.has_launch_capability else 0.0
```

---

## 9) Constraints & invariants

* `exploit_share ∈ [0,1]` and `reinvest_share = 1 − exploit_share`.
* `gross_flow ≥ 0` after any maintenance penalties.
* PO distribution always sums to 100.0 (float); round only for UI.
* Research Income is **not pooled**; it’s applied to current projects in the same turn.
* CP unlocks follow GDP mapping; apply a small hysteresis for downgrades if desired (e.g., lose last CP only if GDP falls below 92% of that CP’s lower bound).

---

## 10) Default picks (suggested starting values)

* `pros_ref = 2401`  (GDP for \~3 CP)
* `econ_scale_weekly = 0.50`
* `growth_lambda = 0.70`
* Starting `exploit_share` for AI nations = `0.30` (players can adjust each turn)

> Tuning: adjust `econ_scale_weekly` for overall payout size; adjust `growth_lambda` for GDP/CP pacing. Keep the exponents and thresholds stable for player readability.
