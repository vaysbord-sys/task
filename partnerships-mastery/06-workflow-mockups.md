# 06 — Workflow Mockups

Visual, build-ready mockups of the operational machine. Diagrams are ASCII so they render anywhere. **Caveats:** benchmark numbers are directional (vendor-sourced). **Salesforce object/field names below are vendor-claimed — verify against official Salesforce documentation before building anything.**

---

## 1. The partner lifecycle (end-to-end workflow)

```
 ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
 │ IDENTIFY │─►│ RECRUIT  │─►│  VET /   │─►│ CONTRACT │─►│ ONBOARD  │─►│ ENABLE / │─►│ ACTIVATE │
 │ /ATTRACT │  │          │  │ QUALIFY  │  │          │  │          │  │  TRAIN   │  │(1st deal)│
 └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └────┬─────┘
   IPP +         outreach,     fit-score,    agreement,    portal,       role-based    first
   ecosystem     pitch,        reference     RoE, tier,    admin,        training,     REGISTERED
   mapping       value prop    checks        CLM sign      kickoff       certs,        deal / opp
                                                           +30/60/90     sales kit         │
                                                                                            ▼
                                                               ┌──────────┐  ┌──────────┐  ┌──────────┐
                                                               │  RENEW   │◄─│  GROW /  │◄─│  MANAGE  │
                                                               │ (or EXIT)│  │   QBR    │  │          │
                                                               └──────────┘  └──────────┘  └──────────┘
                                                                 re-tier /    joint plan,   cadence calls,
                                                                 offboard      tier upgrade  pipeline reviews
       EXIT CRITERIA per stage ─ each gate must be passed before the next:
       Identify→ qualified target list      Contract→ signed agreement       Enable→ certs complete
       Recruit→ partner agrees to proceed   Onboard→ portal active, training  Activate→ FIRST registered deal
       Vet→ pass/fail vs IPP                 started                           Manage→ repeatable pipeline
```

| Stage | Key metric | Typical timeline |
|---|---|---|
| Onboard | portal active, training started | **30–60 days** |
| Activate (first deal) | first registered deal/opp | **60–120 days to first deal** (1–2 quarters typical for B2B software) |
| Grow / QBR | revenue growth / tier promotion | quarterly |

> **The one insight to burn in:** the biggest leak is the **enrollment → activation gap**. Low activation *despite* good onboarding almost always means you recruited the wrong partners. **Fix qualification first.**

---

## 2. Program design — tiers, incentives, rules of engagement

**Tier ladder (3 tiers to start; status is not permanent — demote for inactivity):**
```
            REGISTERED ──────────► GOLD ──────────► PLATINUM
 entry:     1 closed deal,         ~$250K ARR,       ~$1M ARR, dedicated
            sales-certified        3 certified reps  practice, exec sponsor
 margin:    base                   base +2–4 pts     base +5–8 pts
 MDF:       standard pool          up to ~$10K       dedicated (~$50K), priority
 support:   portal + self-serve    named PM          dedicated PM + early access
```

**The four incentive levers:**
```
 MARGIN/DISCOUNT ── baseline reseller economics, uplifted by tier
 MDF ──────────── vendor money for PARTNER marketing, pre-approved + proof of spend
 REBATES ───────── back-end reward on volume/growth targets
 SPIFFs ────────── short-term, rep-level cash on specific products/motions
```

**Rules of engagement — the conflict-prevention core:**
```
 ┌─────────────────────────────────────────────────────────────────────┐
 │ 1. Define partner-sourced vs. vendor-sourced leads UP FRONT          │
 │ 2. Reserve named segments/accounts for the direct team                │
 │ 3. First-to-register wins net-new; territory/vertical carve-outs      │
 │ 4. Disputes go to the channel manager (human), never auto-reject      │
 │ 5. ★ Pay direct reps to SUPPORT (not compete with) partner deals ★    │
 │    — the single most-cited fix for channel conflict                   │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Salesforce / CRM attribution model

> Vendor-claimed field/object names — **verify in Salesforce docs.**

**Sourced vs. Influenced — the counterfactual test:**
```
   "Would this deal still close — but slower or smaller — WITHOUT the partner?"
            │                                              │
           YES ──────────────────────────────────────────►  = INFLUENCED
            │
            NO (deal wouldn't exist) ──────────────────────► = SOURCED
```

**Data model:**
```
  Account (Partner)              Deal_Registration__c  (custom object,            Opportunity
  ─ Account Type = "Partner"      dated, created BEFORE the deal is contested)    ─ Partner_Attribution__c
  ─ Tier = Registered/Gold/Plat   ─ Partner (lookup → Partner Account)               picklist: Sourced /
        │                         ─ Prospect / Account                               Influenced / None
        │                         ─ Registered date  ─ Expiration date            ─ Deal_Registration__c (lookup)
  Contact (Partner users via      ─ Status (Submitted/Approved/Rejected)          ─ Sourcing_Partner (lookup)
  Experience/Partner Cloud)       ─ Approval Process → Flow converts to Opp       ─ Influencing_Partner(s)
        │                                   │                                      ─ KEEP sourced & influenced
        └──────────── lookup ───────────────┴──────────────────────────────────────►  in SEPARATE fields
```

**Rules that keep you credible:**
- Put attribution on the **Opportunity**, with **sourced and influenced in separate fields** (never one blended picklist value).
- Anchor "sourced" on a **dated deal-registration record** created before the deal is contested — gives you auditable history a picklist can't.
- Validate *influence* with **account-overlap data** (Crossbeam/Reveal), not partner self-report.

**The two reports you show a CRO:**
```
 ┌─ Partner-SOURCED pipeline & closed-won ─┐   ┌─ Partner-INFLUENCED pipeline & win-rate lift ─┐
 │  (binary, registration-backed)          │   │  (deals touched; show win-rate vs. no-partner) │
 └─────────────────────────────────────────┘   └───────────────────────────────────────────────┘
```
**Pitfalls:** reporting influenced as sourced (inflates credit, destroys trust); a lone picklist with no dated registration (unauditable); self-reported influence with no overlap data (bad data).

---

## 4. The metrics dashboard (what you report)

```
 ┌───────────────────────────── PARTNER PROGRAM SCORECARD ─────────────────────────────┐
 │ OUTCOME METRICS (lead with these)              directional benchmark                 │
 │  • Partner-SOURCED pipeline / ARR  ............  20–30% of new pipeline (early);      │
 │                                                  40–50%+ (mature channel-led)         │
 │  • Partner-INFLUENCED revenue (separate) ......  report win-rate lift vs. no-partner  │
 │  • Partner activation rate (1st deal ≤90d) ....  30–50% typical; >60% high performers │
 │  • Time to first deal .........................  60–120 days                          │
 │  • Partner deal conversion (reg→won) ..........  15–25%                               │
 │  • Revenue per active partner .................  no standard — "recruit more vs grow" │
 │  • Program ROI = (sourced+influenced margin) ÷ (headcount + MDF + tooling)            │
 │ HEALTH / LEADING METRICS                                                             │
 │  • % partners active  • enablement content usage 40–60%  • % active partners trained │
 │    (goal 65%+)  • partner NPS (goal 40+)  • # account maps live                      │
 └──────────────────────────────────────────────────────────────────────────────────────┘
```
**Warnings:** partner *count* alone is a weak signal — pair it with activation + sourced pipeline + revenue-per-active-partner. Define "active" explicitly (one referral vs. sustained production). All benchmarks are vendor-origin and conflict — **baseline against your own data before setting targets.**

---

## 5. Referral & co-sell mechanics (the two motions, operationally)

**Referral motion (partner introduces, then steps back):**
```
 Partner submits referral ─► Company QUALIFIES FAST ─► status visible to partner ─►
 customer signs ─► billing confirms payment ─► commission becomes ELIGIBLE ─►
 finance approves ─► PAYOUT (e.g., via Stripe / PartnerStack)
```
*Company's job = fast qualification + status visibility back to the partner.*

**Co-sell motion (partner stays active in a live deal):**
```
 Account mapping (Crossbeam) ─► find overlapping accounts ─► register JOINT opp ─►
 shared/joint account plan + defined sales roles ─► co-work the deal rep-to-rep ─►
 close ─► credit per attribution rules
```
*Stress-test with a single-partner pilot before scaling.* For **hyperscaler co-sell** (AWS ACE, Microsoft, marketplace private offers) research AWS/Microsoft partner docs separately — it's a distinct workstream with its own opportunity-submission and marketplace mechanics.

---

## 6. The tool stack

```
 CRM / attribution ───── Salesforce (deal-reg object + sourced/influenced fields)   [START HERE]
 PRM (portal, deal-reg, ─ PartnerStack (if payouts/referral are day-one)             [PICK ONE]
   MDF, tiering)          Impartner / Allbound / Magentrix / Zift (if enablement-heavy)
 Ecosystem mapping ───── Crossbeam (merged w/ Reveal) — account overlap, influence    [HIGH LEVERAGE]
 Commission / payout ─── PartnerStack / impact.com / Kiflo (calculate vs. move money) [WHEN VOLUME JUSTIFIES]
 Contracts (CLM) ─────── DocuSign CLM / Ironclad / PandaDoc                            [STANDALONE]
```
**Minimum viable stack to start:** Salesforce + one PRM + Crossbeam + a CLM. Add rebate/commission tooling only when volume justifies it.

---

## 7. The build-from-zero sequence (30/60/90 + first year)

```
 DAYS 1–30   ORIENT & DESIGN
   • Learn the business; define IPP, program thesis, FIRST motion (referral/reseller/co-sell)
   • Draft program architecture: tiers, economics, Rules of Engagement + deal-reg policy, partner agreement
   • Stand up CRM attribution (sourced/influenced fields, deal-reg object); select PRM

 DAYS 31–60  JOINT PLANNING & PLUMBING
   • Account mapping; target customer lists; FIRST co-marketing activity; deal-reg practice run
   • Recruit first-wave partners; begin onboarding (30–60 day ramp)

 DAYS 61–90  EXECUTION
   • Target outputs: first REGISTERED deal, first co-selling conversation, first joint customer pitch
   • Build a dated 30/60/90 joint plan WITH each partner, presented at kickoff

 MONTHS 4–12 PROVE → SCALE → OPERATIONALIZE
   • Q2: drive first-deal activation (>50% within 90 days of signing); instrument all KPIs; first QBRs
   • Q3: expand first-wave partners; formalize MDF/rebate/SPIFF; launch tiering; tighten RoE from real conflicts
   • Q4: renewal/re-tiering cycle; hit partner-sourced pipeline target (20–30% of new pipeline early);
         build year-2 recruitment plan around revenue-per-active-partner (recruit more vs. grow existing)
```
> One company's public bar (illustrative, not a standard): **2–4 signed SI partners with active co-sell by day 90**, **3–6 producing partners by day 180.**
