---
name: series-continuity
description: Keep On-Chain Operator lessons in one narrator voice, with each lesson recapping the previous one and setting up the next. Use when writing, extending, or ordering Module 4–14 lessons, module intros, lesson 8.3, or SERIES_FLOW.md.
---

# Series continuity

The program is one course, spoken by one narrator. A lesson that could be swapped with another module has failed this skill.

## Voice

Calm, second person, contractions, one idea per sentence. The same disclaimer, the same navy-and-cyan plate, the same caption box, the same music bed (`course/music/komiku-ambiant-truth.ogg`). Elite is not part of this series and stays teal.

Open every full lesson with the previous lesson's takeaway, then the new picture. Close every lesson by naming the next title and telling the viewer to bring the page. Module intros may be short. They still use the plate, the disclaimer, the music, and one ChatGPT still per beat.

## Terminology

Use the words the earlier module already taught. Do not rename them.

- Modules 0–3: wallet, seed phrase, gas, approval, stablecoin, AMM, liquidity, LTV, health factor, liquidation.
- Module 4: base yield, emissions, staking, LST, restaking, vault, points, RWA.
- Module 5: bridge, sequencer, oracle, TWAP, proxy, admin key, audit.
- Module 6: due diligence, unlock, FDV, governance, fee, revenue.
- Module 7: explorer, flow, entity, holder, liquidity.
- Module 8: register, playbook, journal, kill rule. Lesson 8.3 is the strategy-card map, not a list of trades.
- Modules 9–14: grid versus pool, hedge, balance sheet, income, watcher, multisig. Size stays blank unless the viewer already wrote it as an example.

## Files

`SERIES_FLOW.md` is the map. Each re-render job in `course/render/jobs/` waits on its stills and on `course/audio/<id>.wav`. Do not upload to Whop.
