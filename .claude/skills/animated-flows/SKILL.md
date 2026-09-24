---
name: animated-flows
description: Design animated flow diagrams for course videos - how money, transactions, orders or risk move between parties - as flow scenes whose nodes and arrows animate in sync with the narration. Use when a lesson explains a mechanism, process, cycle or failure path (transactions, swaps, lending and liquidation, bridges, staking, MEV, grid bot cycles), or when asked for "flows", "process animations" or "show how it works".
---

# Animated Flows

A `flow` scene turns "here's how it works" into something the viewer watches happen.
Nodes appear as they're named, arrows draw into them, and a glowing token travels along
the arrow into whichever node the voice is on. Spec: `.claude/skills/lesson-script-writing/references/scene-reference.md`.

## Design rules

1. **One question per flow.** "What happens when I borrow?", not "everything about lending".
2. **3 to 6 nodes.** More than 6: split into two flows (e.g. "happy path" then "what goes wrong").
3. **Nodes are actors or places** (your wallet, the pool, the oracle, the exchange). **Edges are what moves** (collateral, signed transaction, price, USDC). Label edges with 1 to 3 words.
4. **Order the narration in node order.** The token only makes sense if the voice follows the path.
5. **Failure paths in orange:** `tone: "bad"` on the node or edge, `dashed: true` for "only if...".
6. **Happy path first, then the failure.** Two flows back to back, or one flow whose last node is the bad outcome.
7. **Layout:** `row` for a pipeline, `cycle` for anything that repeats (bot loops, compounding, staking rewards), custom `x`/`y` for hub-and-spoke (an aggregator routing to several pools).
8. **Follow each flow with a line that says what it means for the viewer:** "So the only protection you have is the buffer you choose."

## Flow library (starting points)

Copy, then adjust the labels and narration to the lesson.

**Transaction lifecycle (1.2)**
Wallet (signs) → RPC node (broadcasts) → Mempool (waits, visible) → Validator (orders, includes) → Block (final). Edges: signed tx, gossip, picked by fee, confirmed.

**Swap via an aggregator (2.1)** custom layout: Wallet at left, Aggregator centre, three pools on the right (x 0.85, y 0.1 / 0.5 / 0.9), edges split the order with labels "60%", "30%", "10%".

**Sandwich attack (2.5)** Your swap (mempool) → Searcher (sees it) → Front-run buy → Your swap fills worse → Back-run sell (`tone: bad`). Follow with a `compare`: public mempool vs private RPC.

**Borrow and liquidation (3.2, 3.3)** Wallet → Lending pool → Oracle → Liquidator (`bad`, dashed edge "HF below 1").

**Looping (3.4)** `cycle`: Deposit ETH → Borrow USDC → Swap to ETH → Deposit again. Then a second flow for the unwind.

**Bridge (5.1)** Chain A contract (locks) → Relayer / validators (attest) → Chain B contract (mints). Then the failure flow: compromised signers mint unbacked tokens (`bad`).

**Liquid staking (4.3)** You → Staking protocol → Validators; return edge "stETH" back to You with `bend`.

**Grid bot cycle (grid-bot-design, 9.1)** `cycle`: Price falls → Buy order fills → Price rises → Sell order fills → Profit per grid. Then the failure flow: price leaves the range → bot stops, holding the asset (`bad`).

**Delta-neutral carry (10.3)** Spot ETH (long) ↔ Perp short (hedge); Funding payments flow in; failure: funding flips negative (`bad`).

**Incident response (11.5)** Detect → Contain (revoke approvals, move funds) → Assess → Recover → Review.

## Checklist before you render

- Every node label is 1 to 3 words; `sub` is at most 5 words.
- The `vo` mentions every node label (or a word from it) in order; otherwise use `at` with sentence indexes.
- Edge labels don't repeat node labels.
- Test-render the scene: `SCENES=5 node build_video.js lesson-NN-M` and look at the last frame to check the whole flow is readable.

## Beyond the built-in scene

If a mechanism needs more than a node graph (a price curve moving, an order book filling),
build it as an image or chart in `export/build_images.js`, then use an `image` scene with
`callouts` and `zoom`. For truly bespoke motion, add a new scene type to `sceneBody`,
`planTimes` and `setTime` in `export/build_video.js`, following the `flow` implementation.
