# Space TEM — Nations & Control Points (Player-Facing Summary)

This page explains what appears on a Nation Card, how Control Points (CPs) work, and how government stats affect play.

---

## 1) Nation Card (Template)

**Control Points:** ◯ ◯ ◯ ◯ ◯ ◯  
*(Fill the circles left‑to‑right; the last slot is always the **Executive** CP.)*

### Governance

* 🏛️ **Government Type:** Autocracy / Theocracy / Monarchy / Oligarchy / Republic
* 🕊️ **Democracy Index:** 1–10 *(civil liberties & electoral process)*
* 🐌 **Bureaucracy Score:** 1–10 *(administrative efficiency; higher = more red tape)*
* 🤬 **Unrest:** 0–5 *(Peaceful, Subversion, Strife, Insurgency, Civil War)*

### Society & Economy

* 📊 **Public Opinion (PO):** 0–100% shared across all factions *(pie chart; sums to 100%)*
* 📈 **GDP (Bn):** nation’s economy in billions (drives CP count and income)
* 📖 **Education:** 1–10
* 🧪 **Science:** national science output (your CP share becomes **🔬 Research Income**)

### Forces & Assets

* 🪖 **Armies:** 0..N
* ⚓ **Navies:** 0..Armies
* ☢️ **Nukes:** 0..N

### Space Capability

* 🧑‍🚀 **Launch Facilities:** 0..N *(drives 🚀 Boost; requires Launch Capability)*

> **Icon Legend:** 💰 Money · ✨ Influence · ⚔️ Operations (Ops) · 🚀 Boost · 🧪 Science (nation) · 🔬 Research Income (faction)

---

## 2) Control Points (CPs)

Control Points represent key nodes of political and economic power in a nation. Every nation has between 1 and 6 control points, depending on its 📈 GDP.
The faction that owns a control point has loyal followers in positions of authority. Control points grant their faction a portion of the 💰 money, 🔬 research, and 🚀 boost income produced by the nation. Proportional to controlled CPs vs total CPs of a nation.

**How many CPs a nation has.** CP count comes from **GDP** (in billions).

|   GDP (Bn) | CPs |
| ---------: | --: |
|       0–81 |   1 |
|     81–625 |   2 |
|   625–2401 |   3 |
|  2401–6561 |   4 |
| 6561–14641 |   5 |
|     14641+ |   6 |

When GDP crosses a threshold, a CP is added/removed (minor hysteresis prevents flip‑flops).

>**Executive CP.** The last CP slot is always the **Executive**. It is **locked** until a faction meets the gate rule:  
> **Executive Gate:** A faction may seize the Executive CP **only** if it controls at least **⌊non‑executive majority⌋** of CPs **and** has **PO ≥ 60** in that nation.

**Ownership & defense.** Each CP tracks its owner (faction or none). A CP can be defended for one turn via **Protect Target**, granting the defender an advantage on opposed checks against hostile missions.

---

## 3) Government & Society

**Government Type** influences events, actions, and resting values for the civic stats below.  
**🕊️ Democracy** tends to speed **Unrest decay**.  
**🐌 Bureaucracy** slows civic change and wastes a portion of 💰/🔬 potential (flavor: “red tape”).  
**🤬 Unrest** rises via player actions and crises; sustained high Unrest triggers penalties and may flip government type.  

**Unrest scale (displayed as integer):**

* 0 **Peaceful** · 1 **Subversion** · 2 **Strife** · 3 **Insurgency** · 4 **Civil War** · 5 **Collapse**

When **Unrest ≥ 3 (Insurgency)**, **Coup Nation** becomes available to factions with strong PO.

---

## 4) Public Opinion (PO)

PO is a **shared 0–100% distribution** of national support **across all factions**. Your faction’s share is your **PO%**. The distribution **always sums to 100**; when one goes up, others go down.

**How it’s used.** PO affects mission odds; it is **not** a spendable resource.

* **Rule-of-thumb bonus:** `poBonus = floor(PO_percent / 10) − 3`  *(e.g., 30% → +0; 80% → +5).*
* **Executive gate:** your faction needs **PO ≥ 60%** **and** ⌊non‑exec majority⌋ of CPs to claim Exec.

**Changing PO (default transfer rule).** When a faction gains `Δ` PO via Public Campaign or events:

1. Add `Δ` to the target faction’s PO.
2. Subtract `Δ` from all **other factions proportionally to their current shares** (renormalize to keep total = 100).

   * *(Optional)* If you use an **Unaligned** bucket, subtract from Unaligned first, then proportionally from others.
3. Clamp each faction’s PO to `[0,100]` and round for UI (internally keep floats).

---

## 5) GDP, Science & Education  

* **📈 GDP (in billions):** shown on the Nation Card; determines CP count and the size of the economic pie each turn. **Only reinvestment grows GDP.**  
* **Economy & budget (one slider).** Each turn the nation produces a **gross flow** `G` of “investment points” from its **GDP** with diminishing returns. A single slider splits the entire pie:
  * **Exploit** `e` → **Money pot** `= e × G`. Your faction gets **💰 Money Income** `= Money pot × (CP\_controlled / total\_CPs)` (even split to players).
  * **Reinvest** `1−e` → **Reinvest pot** `= (1−e) × G`. This pays for policies and is the **only** source of **GDP growth.**  

* **🧪 Science (nation) → 🔬 Research Income (faction):** Science is produced nationally from Education and development; your CP share becomes **Research Income** and is applied directly to your projects this turn.  
* **📖 Education (1–10):** increases both the economic pie and Science; unrest/bureaucracy can drag them down.  
* **🚀 Boost:** `+0.1` per **Launch Facility** each turn.  
* **⚔ Ops:** mostly from **Orgs**; plus some councillor traits and hab modules.

---

## 6) Military & Aerospace

* **🪖 Armies / ⚓ Navies:** Built via `Fund Military` policy (-📈 GDP, +🐌 Bureaucracy)
* **☢️ Nuclear Weapons:** Built via `Build Nuclear Weapons` policy (-📈 GDP, +🤬 Unrest, +🧪 Science)
* **👨‍🚀 Launch Facilities:** directly determine 🚀 boost income. Built via `Fund Space Program` policy (-📈 GDP, +🐌 Bureaucracy, +📖 Education)

---

## 7) Example Policy Levers

* **Economic Investments:** +📈, +🐌
* **Fund Education Programs:** +📖, +🐌 
* **Deregulation:** -🐌, +🤬  
* **Fund Military:** −📈, +🐌; builds 🪖/⚓
* **Build Nuclear Weapons:** −📈, +🤬, +🧪; builds ☢ Nukes
* **Fund Space Program:** −📈, +🐌, +📖; Builds 👨‍🚀 Launch Facilities

*(Exact numbers live in the dev/balance docs; this page stays readable for players.)*

---
