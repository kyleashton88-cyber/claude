# BP-04..11 remake prompts vs PR #17 smoothed narration (6df2536)

Checked 14 Nov 2026 (WITA) by Creative Studio. Prompts only: no images generated, nothing re-scored.

**Manifest:** `course/blueprint-rebuild/BP04-11_IMAGE_MANIFEST.json` @6df2536 lists 161 images. The (lesson, beat, path) set is identical to the 161 rows in BP04-11_PASS_LIST.json. Every name is `course/images/<lesson>/NNN.png` matching its beat number, and every file is 1536x1024 (PNG header read from the 6df2536 blobs). Every blob equals its scored_blob. No beats lack an image field and no files are missing. The smoothed scripts change only `vo`: no image, concept, caption, title or next-lesson field changed.

**Method:** I diffed the vo of all 161 beats between fbb3f9c and 6df2536 and set aside the boilerplate edits ("The shapes are the lesson", "Mark the page Example...", the pointing lines, "The answer names a shape"). That left 68 beats with real wording changes, and I read each one against its prompt's headline, scene and labels. Most changes only add a plain definition the image already agrees with. I updated a prompt only where the image would contradict the new narration or use a different word for a term the narration now defines, plus the 8 disclaimer cards.

**Changed: 19 prompts** (before copies on the box at bp04-11-qa/pr17b/before/):

| Prompt | Why |
|---|---|
| bp-04-market-regimes__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-04-market-regimes__012.txt | Narration now defines both "news bar" and "thin book: few resting orders, so price can jump"; old prompt showed only a news spike. |
| bp-05-spacing-and-range__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-05-spacing-and-range__008.txt | Narration now defines "round trip" and says flat or negative; old label "Fees bigger than gap = loss" overstated it and used a different term. |
| bp-05-spacing-and-range__011.txt | Narration now defines "wick" and "close"; old prompt called them "spikes" ("quick jump that snaps back"), which no longer matches. |
| bp-06-entry-and-exit__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-06-entry-and-exit__010.txt | Narration now says the finish path "says the idea is done"; old prompt framed it as "I was wrong" / "idea is wrong here". |
| bp-07-spot-paper-trading__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-07-spot-paper-trading__006.txt | Narration now defines spot as "the asset itself" and leverage as "borrowed size" (a different product, "not this walk"); old headline said "BUY THE COIN" (coin wording is off-brief). |
| bp-07-spot-paper-trading__007.txt | Narration now names and defines "API key" and "seed phrase"; old tags said "App keys" / "Secret words". |
| bp-07-spot-paper-trading__013.txt | Beat now ends "The lesson stops in front of that control." (the old line about the bot confirming for you is gone); old label "Never press confirm" was a rule the narration no longer states. |
| bp-08-managing-and-monitoring__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-08-managing-and-monitoring__004.txt | Narration now defines inventory (what piled up on one side) and the finish sentence; old row 3 said "stop rule still fit". |
| bp-08-managing-and-monitoring__014.txt | Beat now ends "The homework is that card on the path you drew." (live-position warning removed); old label "Test it on a sketch". |
| bp-08-managing-and-monitoring__016.txt | Kept consistent with the reworded beat 4 questions (finish sentence, side). |
| bp-09-common-mistakes__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-10-scaling-up__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-11-advanced-liquidation__002.txt | Disclaimer card must show exactly "Education only. Not financial advice." (old prompt had tags "Learn the idea" / "Not financial advice" and a crossed buy button). |
| bp-11-advanced-liquidation__010.txt | Narration now defines funding as "a payment that moves between the two sides of a contract", separate from the price move; old headline called it a "fee". |

**bp-04 001..010 needing a re-run:** bp-04-market-regimes__002.txt. Only beat 002 (disclaimer wording) changed. Beats 001 and 003..010 got new definition sentences that the existing prompts already match, so their images stay valid.

**Checked and left unchanged** (57 of the 68; the new narration adds definitions the image already agrees with): bp-04 001, 003, 004, 005, 006, 007, 008, 015, 016, 017, 018; bp-05 001, 003, 004, 006, 016, 017; bp-06 001, 003, 016, 017, 018; bp-07 001, 003, 016, 017, 018; bp-08 001, 003, 008, 010, 011, 017, 018; bp-09 001, 003, 013, 016, 017, 018, 019; bp-10 001, 003, 004, 005, 013, 016, 017, 018, 019; bp-11 001, 003, 005, 013, 016, 017, 018.

