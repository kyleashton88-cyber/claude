# On-Chain Operator Program — Operations Kit

Everything around the lessons needed to sell, deliver and run the program.
Items marked **YOU DECIDE** need your call. Legal wording is a starting draft:
**have a lawyer review terms and disclaimers before launch.**

Contents: 1. Whop course layout · 2. Capstones & rubrics · 3. Certification ·
4. Application form & scoring · 5. Sales call script · 6. Member email sequence ·
7. Live tier design · 8. Community rules · 9. Terms, disclaimers & refunds ·
10. Support & FAQ · 11. Launch plan

---

## 1. Whop course layout

| Whop section | Contents | Video |
|---|---|---|
| Start here | Welcome, how the program works, Day-1 Setup Kit (PDF) | `video/welcome.mp4` |
| Module 0–14 | One chapter per module; one lesson per page, with images; module practical at the end | `video/module-NN-intro.mp4` at the top of each module |
| Tools | Strategy calculator (`defi_calc.py`) instructions, worksheet templates (`08-worksheets.md`) | n/a |
| Capstones | Briefs, rubrics, submission form | n/a |
| Live (Live tier only) | Session calendar, recordings, review booking | n/a |

**Drip (recommended):** release a stage at a time as the previous stage's quiz is
passed, not by date. Beginners shouldn't reach leverage before safety.

---

## 2. Capstones & rubrics

### Analyst capstone (after Module 7)
**Brief:** a due-diligence file on one real protocol: the 6-step loop
(Module 6), tokenomics and governance, and an on-chain section (Module 7), ending
in a verdict with size, conditions and exit.

| Criterion | Weight | Pass standard |
|---|---|---|
| Mechanism and cash flow correctly explained | 20% | Fees vs emissions separated with sources |
| Dependency map complete | 20% | Oracles, bridges, admin/timelock, stablecoins, other protocols |
| Evidence quality | 20% | Primary sources + at least two independent data views |
| On-chain analysis without over-interpretation | 15% | Caveats stated for every metric |
| Verdict: size, conditions, exit | 25% | Actionable, with kill rules and an unwind path |

Pass: ≥ 70%. Resubmission allowed.

### Operator capstone (Module 14.4)
**Brief:** the ten-section personal bank (see 14.4). No keys, seeds or account access anywhere.

| Criterion | Weight | Pass standard |
|---|---|---|
| Balance sheet & policies internally consistent | 20% | LTV, HF and runway match the credit and ladder policies |
| Custody & security | 15% | Multisig or equivalent, limits, a tested recovery, succession |
| Income engine honesty | 20% | Loss assumptions stated; payout ≤ 80% of expected income |
| Stress test & fixes | 20% | Five scenarios, each failure fixed |
| Operations | 15% | Alerts mapped to actions; automation scoped; signing procedure |
| Clarity | 10% | A stranger could run it from the document |

Pass: ≥ 70%. Distinction: ≥ 90% plus one quarter of books kept to standard.

---

## 3. Certification
- **On-Chain Analyst:** analyst capstone passed
- **On-Chain Operator:** operator capstone passed
- **On-Chain Operator, with distinction:** as above
Certificates state that they reflect course completion only, not a licence or a professional qualification.

---

## 4. Application form & scoring

**Form (Typeform or Whop form):**
1. Name, email, country
2. Experience: never owned crypto / some / active trader / advanced
3. Capital you plan to operate: < $10k / $10–50k / $50–250k / $250k+
4. Goal: learn safely from zero / earn income / borrow against assets / run a structured portfolio / other
5. Do you already use Grid Bot Builder? (yes/no)
6. Why now? (short text)
7. Acknowledgement (required): *"I understand this is education, not financial advice, and that no returns are promised."*

**Scoring** (plugs into `gbb-new-lead` as `interest = defi`):
| Answer | Points |
|---|---|
| Capital $250k+ / $50–250k / $10–50k / < $10k | 4 / 3 / 1 / 0 |
| Clear goal (not "get rich quick") | 2 |
| GBB customer | 1 |
| Thoughtful "why now" | 1 |

≥ 6 → invite to call · 3–5 → call optional + nurture · < 3 → nurture + Elite Intel Community trial.
**Disqualify** anyone seeking guaranteed returns or asking the program to manage funds.

---

## 5. Sales call script (30 min)

1. **Open (2 min):** "This call is to see if the program fits you. If it doesn't, I'll tell you."
2. **Where are you now? (8 min):** experience, current setup, what's gone wrong before, goal.
3. **Where do you want to be? (5 min):** in a year, what does "working" look like? (Steer from return targets to capabilities: a safe setup, research ability, income policy, credit line.)
4. **The gap (5 min):** reflect back what's missing: process, safety, policy.
5. **The program (5 min):** stages, what they'll build, Course vs Live, capstones. Show the path image.
6. **Fit and objections (4 min):** see below.
7. **Close (1 min):** "Would you like the enrolment link?" If yes, send a per-buyer checkout link (with UTM metadata).

**Objection answers (never make return promises):**
- *"Will I make my money back?"* "I can't promise returns and nobody honestly can. What you'll leave with is a process to research, size and exit positions, and an income policy that doesn't depend on luck."
- *"It's expensive."* "It is. If the cost would strain you, don't do it now; start with the free Day-1 Setup Kit and Elite Intel."
- *"I've lost money in crypto before."* "Most losses come from setup mistakes, leverage and yields nobody explained. Those are the first things we fix."

**Never:** promise returns, pressure with fake deadlines, or ask for keys or account access.

---

## 6. Member email sequence (after purchase)

| Day | Subject | Body (plain text, < 120 words) |
|---|---|---|
| 0 | Welcome, operator | Access link · watch the welcome video · start Module 0 · print the Day-1 Setup Kit · "we'll never ask for your seed phrase" |
| 2 | Your Day-1 Setup Kit | "Tick Part A today. Secure your email before anything else." |
| 7 | Did your restore test pass? | Nudge for Lesson 0.5; link to support |
| 14 | Stage 1 unlocked | What Modules 1–2 build; Live tier: first session date |
| 30 | Your first month | Progress check; invite to book a check-in (Live) |
| 60 | Halfway to analyst | Analyst capstone brief |
| 90 | From analyst to operator | Stage 4–5 preview; operator capstone brief |

---

## 7. Live tier design (**YOU DECIDE: price, cadence**)

| Component | Proposed | Notes |
|---|---|---|
| Group sessions | 2 × 60 min per month | One teaching deep-dive, one Q&A |
| Capstone reviews | Written review + 20-min call, each capstone | Uses the rubrics above |
| Portfolio/policy review | 1 per quarter, 30 min | Reviews policies, never gives personalised investment advice |
| Protocol research clinic | Monthly, recorded | Walks through a due-diligence file live |
| Recordings | All sessions | Stored in the Live section |

Boundaries: education and process review only; no personalised financial
advice, no trade calls, no fund management.

---

## 8. Community rules
1. Education, not signals. No "buy X now" posts.
2. Never ask for or share seed phrases, keys or account access. Anyone who asks is removed.
3. No DMs offering "help", "recovery" or investments. Report them.
4. No referral links or shilling.
5. Show your working: numbers from the calculators, sources linked.
6. Be kind to beginners. Everyone started at Module 0.

---

## 9. Terms, disclaimers & refunds (draft; lawyer review required)

**Disclaimer (listing, checkout, every module):**
*The On-Chain Operator Program is educational content only. It is not
financial, investment, tax or legal advice, and nothing in it is a
recommendation to buy, sell or hold any asset. Digital assets are volatile and
you can lose some or all of your capital. No results or income are promised or
guaranteed. Examples are illustrative. "Operate as your own bank" describes a
personal method, not a licence or financial service. We will never ask for your
seed phrase, private keys or account access.*

**Refund policy (YOU DECIDE):** options:
- (a) 14 days, if under 30% of lessons completed
- (b) 7 days, no questions asked
- (c) no refunds after access (state clearly at checkout)

**Other terms to include:** access duration (lifetime / 12 months), no sharing
of accounts, content copyright, conduct rules (section 8), Live-tier boundaries (section 7).

---

## 10. Support & FAQ
- Support channel: email (response within 2 business days) + community.
- **Top questions:** "I sent crypto on the wrong network" (check whether the address
  exists on that network; contact the receiving service; prevention in 0.6) ·
  "I lost my seed phrase" (if the wallet is still accessible, move funds to a new
  wallet with a new seed now) · "A support person DM'd me" (it's a scam; block) ·
  "Is X protocol safe?" (run the 6-step loop; staff don't give recommendations).

---

## 11. Launch plan
1. Reconnect Whop in Zapier; create the hidden product; upload logo, banner and gallery images; paste the listing.
2. Upload the course: 15 modules, lesson pages with images, intro videos, Day-1 Setup Kit.
3. Create plans via Zapier (course $15,000 one-time; live tier once priced), approved first.
4. Publish the application form; connect scoring to `gbb-new-lead`.
5. Test end to end: application → call → per-buyer checkout → onboarding email → access.
6. Soft launch to the warm list (GBB customers, Elite Intel) and cold ads at the same time (per decision), with the VSLs.
7. Weekly: `gbb-ad-performance` and `gbb-pipeline-check` including DeFi.
