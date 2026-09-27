#!/usr/bin/env python3
"""Gold-standard script for Lesson 5.8, Reading smart-contract code:
enough to verify claims (target 11-14 minutes, per the "a bit longer"
note for lessons from here on). Completes Module 5. Walks access control
patterns, dangerous powers to search for, upgradeability, external-call
ordering (reentrancy), unlimited parameters, and events, then the source
material's own worked example (a token claims "fixed supply", but its
code has an onlyOwner mint function — the claim is false unless
ownership is renounced or held by timelocked governance; check owner()
on the Read tab), as visual walk-throughs. Uses a wider icon vocabulary
(key, code, search, doc, bell, scale, exit) per the standing note to
diversify icons and keep every number/example visually represented.
Written in one pass at the full target length.

Writes video-scripts/gold/lesson-05-8.json (the generator skips lessons
with a gold script). Spoken text (vo) spells numbers for the voice; cap is
the written caption, same sentence count as vo."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = []


def sc(type_, vo, cap=None, **k):
    d = {"type": type_, **k, "vo": vo}
    if cap:
        d["cap"] = cap
    S.append(d)


def img(src, eyebrow, vo, cap=None, **k):
    sc("image", vo, cap, src=src, eyebrow=eyebrow, wide=True, **k)


D = "assets/diagrams/"

# ---------------------------------------------------------------- intro
sc("title", "Lesson five point eight. Reading smart-contract code: enough to verify claims. By the end, you'll be able to check what a protocol actually says about itself, directly against its own verified code, without needing to be a developer.",
   "Lesson 5.8. Reading smart-contract code: enough to verify claims. By the end, you'll be able to check what a protocol actually says about itself, directly against its own verified code, without needing to be a developer.",
   chapter="Intro", eyebrow="Lesson 5.8", num="5.8", title="Reading smart-contract code: enough to verify claims", sub="Verify the claim, not just the marketing.")
sc("pillars", "Here's the plan. Access control, the actual words to search for, and why they matter. Dangerous powers, the specific functions worth finding before you ever trust a claim. Upgradeability, and external-call ordering, the reentrancy pattern from Lesson five point five, spotted directly in code. And a full worked example, checking a real fixed-supply claim against its own real code.",
   chapter="Intro", title="What this lesson covers",
   items=[{"icon": "key", "title": "Access control", "text": "onlyOwner, onlyRole — who can call what"}, {"icon": "alert", "title": "Dangerous powers", "text": "mint, pause, upgradeTo, setFee, withdraw"},
          {"icon": "code", "title": "Upgradeability & ordering", "text": "Proxy patterns, and the reentrancy pattern"}, {"icon": "search", "title": "Worked example", "text": "\"Fixed supply\" — verified directly against the code"}])

# ---------------------------------------------------------------- access control
sc("title", "Access control.", chapter="Access control", eyebrow="Access control", num="1", title="Who can actually call what",
   sub="Search for these words directly. You don't need to be a developer.")
img(D + "read-verified-code.png", "Reading verified code, without being a developer",
    "Here's exactly what to search for, directly in a contract's own verified Solidity code, on any block explorer. The words onlyOwner, onlyRole, followed by a specific role name, or onlyGovernance. Every one of these guards a specific function, meaning only whoever holds that exact role can actually call it. Search the code for these words directly, and you've found exactly who controls what, without reading a single other line.",
    chapter="Access control")
sc("statement", "Worth being direct about why this single search is genuinely worth doing, even if you've never written a line of code in your life. These three words are simply text, searchable exactly like any other word on a page. Finding them tells you precisely which functions are restricted, and to whom, which is most of what actually matters about a contract's real power structure.",
   chapter="Access control", kicker="Why this search is genuinely worth it", lines=["These are just searchable words, like any other text.", "Finding them tells you most of what matters about its power structure."], sub="You're not reading code. You're searching for three specific words.")
sc("steps", "Here's exactly how to actually run this search yourself, on any block explorer's own code viewer. Open the contract's verified code tab directly. Use your browser's own find function, Control F, or Command F, to search the full page. Search specifically for onlyOwner, onlyRole, and onlyGovernance, one at a time, and note every single function each one guards.",
   chapter="Access control", title="Running this search yourself",
   steps=["Open the contract's verified code tab", "Use your browser's find (Ctrl+F / Cmd+F) on the full page", "Search onlyOwner, onlyRole, onlyGovernance — note what each guards"])
sc("quiz", "Quick check. What does onlyOwner on a mint function actually mean? [[pause 4]] The answer: the owner can mint new tokens whenever they genuinely like, with nothing else required.",
   chapter="Access control", n=1, of=3, q="What does onlyOwner on a mint function mean?",
   a="The owner can mint new tokens whenever they like.")

# ---------------------------------------------------------------- dangerous powers
sc("title", "Dangerous powers to search for.", chapter="Dangerous powers", eyebrow="Dangerous powers", num="1", title="The specific functions worth finding first",
   sub="mint · pause · upgradeTo · setOracle · setFee · withdraw/sweep/rescue")
sc("flow", "Here's exactly what each of these actually lets someone do, once you've found which role controls them. Mint creates new tokens, out of nothing. Pause can freeze the entire contract, instantly. UpgradeTo can swap the underlying logic, the pattern from Lesson five point four. SetOracle and setFee can change what price or cost the contract actually uses. And withdraw, sweep, or rescue functions can move user funds directly, sometimes for a genuinely legitimate reason, sometimes not.",
   chapter="Dangerous powers", title="What each function actually lets someone do",
   nodes=[{"label": "mint / pause", "sub": "Create tokens from nothing, or freeze everything", "icon": "alert"}, {"label": "upgradeTo", "sub": "Swaps the logic underneath (Lesson 5.4)", "icon": "code"},
          {"label": "setOracle / setFee", "sub": "Changes the price or cost the contract uses", "icon": "scale"}, {"label": "withdraw / sweep / rescue", "sub": "Can move user funds directly", "icon": "exit"}])
sc("statement", "Worth being fair about that last category specifically, since the names alone can sound alarming even when the function is genuinely legitimate. A rescue function recovering accidentally-sent tokens is a real, common, reasonable feature. The actual question is never simply whether the function exists; it's who controls it, and whether it's restricted specifically to funds that genuinely don't belong to any user.",
   chapter="Dangerous powers", kicker="Being fair about withdraw/sweep/rescue", lines=["Recovering accidentally-sent tokens is a real, reasonable feature.", "The question is who controls it, and whether it's restricted properly."], sub="Don't panic at the name alone. Read what it's actually scoped to do.")

sc("compare", "Here's what actually separates a well-scoped rescue function from a dangerously broad one, in the code itself. A well-scoped one explicitly checks the token isn't the contract's own primary asset, restricting it specifically to funds that genuinely aren't a user's real deposit. A broad one simply lets the owner withdraw any token, or even the contract's own native balance, directly, with no such restriction written in at all.",
   chapter="Dangerous powers",
   left={"label": "A well-scoped rescue function", "tone": "good", "items": ["Explicitly excludes the contract's own primary asset", "Restricted to genuinely stray funds only"]},
   right={"label": "A broad withdraw function", "tone": "bad", "items": ["Can withdraw any token, or the native balance, directly", "No restriction written in at all"]})

# ---------------------------------------------------------------- upgradeability and ordering
sc("title", "Upgradeability, and call ordering.", chapter="Upgradeability & ordering", eyebrow="Upgradeability & ordering", num="1", title="Two patterns worth spotting directly in code",
   sub="Proxy patterns, and the classic reentrancy shape.")
sc("flow", "Here's exactly what to search for to spot a proxy directly, and who to check once you've found one. The words delegatecall, or implementation, or upgradeTo, appearing anywhere in the code, are your signal it's an upgradeable proxy. Once you've spotted it, go find the actual admin, exactly the check covered back in Lesson five point four, since that's who genuinely controls what this contract does tomorrow.",
   chapter="Upgradeability & ordering", title="Spotting a proxy, directly in code",
   nodes=[{"label": "Search for: delegatecall, implementation, upgradeTo", "sub": "Your signal it's an upgradeable proxy", "icon": "search"}, {"label": "Then find the actual admin", "sub": "The exact check from Lesson 5.4", "icon": "key"}])
sc("statement", "Worth being precise about the classic reentrancy shape specifically, since it's genuinely recognisable even without deep expertise. Watch for a contract calling out to another, external contract, before it's actually finished updating its own internal state. That specific ordering, external call first, state update second, is exactly the pattern behind the reentrancy risk covered back in Lesson five point five.",
   chapter="Upgradeability & ordering", kicker="The classic reentrancy shape", lines=["An external call, made before the contract updates its own state.", "That specific ordering is the reentrancy pattern from Lesson 5.5."], sub="You're not debugging it. You're just recognising the shape.")
sc("quiz", "Quick check. What code pattern specifically suggests a reentrancy risk? [[pause 4]] The answer: an external call made before the contract actually finishes updating its own internal state.",
   chapter="Upgradeability & ordering", n=2, of=3, q="What code pattern suggests reentrancy risk?",
   a="An external call made before the contract updates its own state.")

# ---------------------------------------------------------------- unlimited parameters and events
sc("title", "Unlimited parameters, and events.", chapter="Unlimited parameters & events" , eyebrow="Unlimited parameters & events", num="1", title="What has no cap, and what actually gets logged",
   sub="A fee that can go to 100%. An oracle that can be swapped instantly.")
sc("compare", "Here's the actual difference a limit makes, made concrete. A fee parameter with a genuine hard cap, say a maximum of one percent, written directly into the code, can never exceed that, regardless of who controls it. A fee parameter with no such limit at all can technically be set to one hundred percent, entirely at whoever's own discretion holds that role.",
   chapter="Unlimited parameters & events",
   left={"label": "A capped parameter", "tone": "good", "items": ["Hard limit written directly into the code", "Can never exceed it, regardless of who holds the role"]},
   right={"label": "An unlimited parameter", "tone": "bad", "items": ["No cap at all, anywhere in the code", "Can technically be set to 100%, at their discretion"]})
sc("stats", "Here's that same capped-versus-uncapped difference, expressed as actual numbers, purely illustrative, to make the real stakes concrete rather than abstract. A genuinely capped fee parameter might allow a maximum of one percent, written directly into the code as a hard limit. An uncapped one has no such ceiling at all, meaning it could technically be set as high as one hundred percent, entirely at the role-holder's own discretion.",
   chapter="Unlimited parameters & events", title="A capped fee vs. an uncapped one (illustrative)",
   stats=[["1%", "A genuinely capped maximum"], ["100%", "An uncapped parameter's real ceiling"]])
sc("statement", "Worth naming events specifically too, since they're genuinely useful for exactly the kind of ongoing monitoring this whole module has been building toward. What a contract actually logs, as an event, is what you, or any monitoring tool, can actually watch after the fact. A contract logging every single admin action gives you real, ongoing visibility; one that logs almost nothing leaves you flying blind between checks.",
   chapter="Unlimited parameters & events", kicker="Why events matter here specifically", lines=["What's logged is what you can actually watch, after the fact.", "Logging every admin action gives real visibility. Logging little leaves you blind."], sub="Check what's logged, the same way you checked who controls what.")
sc("quiz", "Quick check. Why does it actually matter to check a parameter's own limits? [[pause 4]] The answer: an unlimited setter, like a fee or an oracle address, can be changed instantly, to genuinely harm users, with nothing stopping it.",
   chapter="Unlimited parameters & events", n=3, of=3, q="Why check parameter limits?",
   a="An unlimited setter (fee, oracle) can be changed to harm users instantly.")

# ---------------------------------------------------------------- worked example
sc("title", "Worked example.", chapter="Worked example", eyebrow="Worked example", num="1", title="\"Fixed supply\" — verified against the actual code",
   sub="The source material's own scenario.")
sc("steps", "Here's the actual line of code itself, exactly as the source material presents it, worth seeing in full rather than just described. Function mint, taking an address and an amount, marked external, guarded by onlyOwner, and its body simply calls the internal underscore-mint function directly. Four words matter most here: external, onlyOwner, and mint itself.",
   chapter="Worked example", title="function mint(address to, uint256 amount) external onlyOwner { _mint(to, amount); }",
   steps=["mint(address to, uint256 amount)", "external onlyOwner", "{ _mint(to, amount); }"], result="One guarded function. Genuinely unlimited minting power, for whoever holds owner")
sc("steps", "Here's the claim, and exactly what its own code actually shows. A token's own marketing states plainly: fixed supply. Its verified code, on the explorer, contains a mint function, guarded specifically by onlyOwner. That single guarded function means the owner can genuinely create unlimited new tokens, entirely contradicting the fixed-supply claim, unless something else specifically prevents it.",
   chapter="Worked example", title="The claim, against the code",
   steps=["Marketing claims: \"fixed supply\"", "Verified code contains: mint(...), guarded by onlyOwner", "That guard means the owner can create unlimited tokens"], result="A direct contradiction, unless ownership itself is neutralised")
sc("statement", "Worth being precise about the specific two conditions that would actually make this fixed-supply claim true, despite that mint function genuinely existing in the code. Either ownership has been fully renounced, meaning no address controls it at all anymore, or it's held specifically by a timelocked governance contract, giving real, public warning before any mint could ever actually happen.",
   chapter="Worked example", kicker="What would actually make the claim true", lines=["Ownership fully renounced, so no address controls it at all.", "Or held by timelocked governance, with real public warning first."], sub="The function existing isn't automatically disqualifying. Who holds it is.")
sc("steps", "Here's exactly how to actually check which of those two is true, directly on the block explorer itself. Go to the contract's own Read tab. Find the specific function called owner. Call it directly, and read the actual address it returns. If that address is the well-known zero address, ownership is genuinely renounced; if it's a timelocked governance contract, check that timelock's own real length.",
   chapter="Worked example", title="Checking owner() on the Read tab",
   steps=["Open the contract's Read tab", "Call owner() directly, and read the returned address", "Zero address: renounced. A contract: check its timelock"], result="Now you know whether \"fixed supply\" is actually true")

# ---------------------------------------------------------------- checklist and recap
sc("steps", "Here's your checklist. Do it for any contract whose claims you actually want to trust. Search the code for every owner or role-guarded function. List every single one that can mint, pause, upgrade, change fees or oracles, or move funds. And check exactly who holds those specific roles, on the Read tab, and behind what timelock, if any.",
   chapter="Checklist", title="Your checklist",
   steps=["Searched the code for owner/role-guarded functions", "Listed every function that can mint, pause, upgrade, change fees/oracles or move funds", "Checked who holds those roles (Read tab) and behind what timelock"])
sc("bullets", "Let's recap. Search verified code for onlyOwner, onlyRole, and onlyGovernance, to find who controls what. Find every mint, pause, upgradeTo, setFee, setOracle, and withdraw or rescue function specifically. Watch for an external call made before state updates, the reentrancy shape. Check whether parameters are genuinely capped. And always verify a claim directly against the owner, on the Read tab, not against the marketing alone.",
   chapter="Recap", title="Recap", check=False,
   items=["Search for onlyOwner, onlyRole, onlyGovernance to find who controls what", "Find every mint, pause, upgradeTo, setFee/setOracle, withdraw/rescue function",
          "Watch for an external call before state updates: the reentrancy shape", "Verify claims against owner() on the Read tab, not against the marketing"])
sc("statement", "Worth closing Module five on the actual point this entire module has been building toward, across all eight lessons. Every dependency, the chain, the bridge, the L2, the oracle, the contract, and now the code itself, is genuinely checkable, by you, directly, without needing anyone else's word for it.",
   chapter="Recap", kicker="The point this whole module builds to", lines=["Every dependency is genuinely checkable, by you, directly.", "Chain, bridge, L2, oracle, contract, and now the code itself."], sub="Not someone else's word for it. Your own read of the real thing.")
sc("cta", "Search for the guard words, list every dangerous function, and verify claims against owner() directly. That's the end of Module five. Next up, Module six.",
   "Search for the guard words, list every dangerous function, and verify claims against owner() directly. That's the end of Module 5. Next up, Module 6.",
   chapter="Recap", button="Next: Module 6", sub="Continuing the On-Chain Operator Program")

spec = {"id": "lesson-05-8", "title": "Lesson 5.8: Reading smart-contract code", "size": [1920, 1080], "group": "lessons", "maxMinutes": 25,
        "tag": "Lesson 5.8", "gold": True, "music": True, "musicLevel": 0.14, "seed": 86,
        "use": "Lesson 5.8 page in the Whop course. Hand-written gold-standard script: access control words, dangerous powers to search for, upgradeability and reentrancy patterns, unlimited parameters, events, and the source material's own fixed-supply-claim worked example, as walk-throughs. Completes Module 5.",
        "thumbnail": {"title": "Reading contract code", "subtitle": "Lesson 5.8"}, "scenes": S}
out = ROOT / "video-scripts" / "gold" / "lesson-05-8.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
words = sum(len(s["vo"].replace("[[pause 4]]", "").split()) for s in S)
print(f"{len(S)} scenes, {words} words, est {(words / 171 * 60 + len(S) * 1.3 + 4 * 3) / 60:.1f} min")
