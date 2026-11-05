import json,glob,os,re
B='/workspace/course-images/batch-web'; O=B+'/v3'
REF='/workspace/course-images/style-ref-gbb-v1/'
ANCH_ELITE=[REF+'01M6MSHVNG1R56TMTX6163QTJT.png',REF+'01M6MSHVNHDS25DF52A243CTZG.png']
STYLE=("STYLE (GBB v3, Elite TEAL): Premium course still, 1536x1024. SAFE AREA: keep the headline, every label and all key content inside the centre 1536x864 band; leave the top ~80px and bottom ~80px free of text and key content (background only). "
"Near-black navy background (#05080F to #0B1424) with depth: faint grid, soft bokeh and glowing TEAL (#14E0C8 / #0FB5A5) neon accent light. Frosted glass cards with glowing teal borders, subtle reflections. "
"Bold condensed all-caps headline in crisp white with ONE keyword in teal; a few short crisp labels only (no paragraphs). Circled teal line icons, numbered step badges, dashed level lines, glossy 3D detail. Rich, layered, premium; never flat or minimal. "
"Education only: any price or level shown carries the word EXAMPLE; no profit, return, win-rate or income claims; no exchange names or logos; no people or faces. Optional glossy G-badge robot mascot with visor-bar eyes only; no other face-like shapes.")
NEG=("NEGATIVE: no flat or minimal look, no off-white paper cards, no blue-dominant palette (teal replaces blue), no paragraphs, no misspelt or garbled text, no real exchange/app UI or logos, no people, no extra faces or face-like dot pairs, no money piles, rockets, trophies or upward profit arrows, no unlabelled prices, nothing important in the top or bottom 80px.")
ANCHOR_LINE="Match the attached reference images' style exactly (premium near-black navy, neon glow, glass cards, crisp condensed headlines, detailed charts) but recolour every blue accent to TEAL. Landscape 1536x1024 with all text and key content inside the centre 1536x864 safe area. New subject below."
# concept map: (lesson, shot-text prefix) -> (headline, hero visual, labels)
C={
('el-06','two small cards side by side: the left shows a mint pause'):("CIRCUIT BREAKER: [PAUSE] OR [STOP]","two glowing glass cards side by side: left a large teal circled pause icon, right a closed metal shutter icon with a dim red edge; a teal candlestick chart fades behind them",["PAUSE","STOP"]),
('el-06','a horizontal mint band with one small bell'):("THE [ALERT] LINE","detailed teal candlestick chart; one labelled dashed horizontal ALERT level line; price candles touch the line and a circled teal bell icon glows exactly at the touch point",["ALERT LEVEL (EXAMPLE)","PRICE TOUCHES"]),
('el-06','a mint bell dot with a thin line leading'):("ALERT = [ONE RULE]","a circled teal bell icon linked by a glowing connector line to one glass rule card with a single short sentence",["ALERT","IF HIT: PAUSE THE BOT"]),
('el-06','a single large manual toggle switch'):("THE MANUAL [OFF] SWITCH","one large glossy 3D toggle switch on a glass panel, set to OFF, teal rim light; small G-badge robot standing idle beside it",["MANUAL","OFF"]),
('el-06','three tiny icons in a row'):("[3]-STEP BREAKER","numbered step flow of three glass cards joined by teal arrows: circled pause icon, circled bell icon, circled rule-card icon",["1 PAUSE","2 ALERT","3 RULE"]),
('el-06','one worksheet card with three short grey bars'):("FIX THE [RULE]","a glass worksheet card with three rule lines; the middle line struck through in red-orange and a corrected teal line glowing beneath it",["OLD RULE","CORRECTED"]),
('*','a closed worksheet folder'):("LESSON [WORKSHEET]","a closed glossy glass folder with a teal glowing tab and a small numbered checklist peeking out, soft depth behind",["WORKSHEET","SAVE IT"]),
('el-07','a single path line that curves downward'):("HOW [LIQUIDATION] HAPPENS","detailed candlestick chart falling toward a red dashed LIQUIDATION level line (labelled EXAMPLE); a red circled warning icon where price meets it",["LIQUIDATION LEVEL (EXAMPLE)","POSITION CLOSED"]),
('el-07','two separate rounded boxes, one holding three mint'):("[ISOLATED] VS CROSS","comparison: two separate glass vaults with a clear gap; left vault holds three teal 3D USDT coins, right vault three cyan 3D coins; a teal wall icon between them",["ISOLATED","SEPARATE RISK"]),
('el-07','two plain unlabelled outlined regions'):("REGION [RULES] APPLY","two abstract glowing outlined regions (no real maps, no flags), each with a closed gate icon on it",["REGION A","REGION B","CHECK LOCAL RULES"]),
('el-07','one highlighted grey bar with a mint outline'):("PICK ONE [LIMIT]","four glass bars in a row, three dimmed, one lit with a glowing teal border and check icon",["YOUR LIMIT"]),
('el-07','a gate outline, one framed square and two short fence'):("[GUARDRAILS] FIRST","numbered step flow: circled gate icon, framed checklist card, two fence-post icons, teal arrows between",["1 GATE","2 CHECK","3 FENCE"]),
('el-08','a small calendar square with one mint-circled day beside a flat'):("SIZE ON A [SCHEDULE]","glass calendar with one day ringed in teal beside a flat level teal line chart (no rise)",["REVIEW DAY","SIZE STAYS LEVEL"]),
('el-08','four short grey bars in a column'):("THE [SIZING] CHECKLIST","glass checklist card with four rows, each with a circled teal tick icon",["CAP","DATE","SIZE","PAUSE"]),
('el-08','one grey bar shown twice'):("SAME SIZE [EVERY TIME]","two identical glowing position bars side by side joined by a bold teal equals sign, small 3D USDT coin stack under each",["ORDER 1","ORDER 2"]),
('el-08','a small calendar square with one mint-circled day, next to one'):("ONE [DATE], ONE NOTE","glass calendar with one teal-ringed day next to a short note card",["NEXT REVIEW (EXAMPLE)"]),
('el-08','a calendar square, four short grey bars'):("THE [SCHEDULE] SYSTEM","numbered step flow: calendar icon, four-row size card, brake-pedal icon, teal arrows",["1 DATE","2 SIZE","3 BRAKE"]),
('el-09','one filled grey bar, one dashed empty bar'):("[MULTI-VENUE] SPLIT","a filled glass capital bar, a dashed empty bar, then two fence posts; generic unbranded venue cards with no names or logos",["VENUE A","VENUE B (EMPTY)","LIMITS"]),
('el-10','a question card with three fields'):("ASK THE [RIGHT] QUESTION","glass question form with three fields; two fields hidden under frosted blocks, one glowing teal",["CONTEXT","GOAL","LIMIT"]),
('el-10','three small cards connected left to right'):("[3] STEPS TO ASK","numbered step flow of three glass cards joined by glowing teal lines (no clock or timer)",["1 CONTEXT","2 QUESTION","3 CHECK"]),
('el-10','one question card with three tiny mint tick boxes'):("CHECK [BEFORE] YOU SEND","glass question card with three teal tick boxes beneath",["CLEAR","SPECIFIC","SAFE"]),
('el-10','an outline shape with two small orange drips'):("AVOID [LEAKS]","a glass container outline leaking two orange drips with a clean teal path routed through it",["LEAK","CLEAN PATH"]),
('el-11','a single worksheet with four grey bars'):("YOUR [PAPER] PLAN","glass worksheet with four step rows and a teal gap marker between rows 3 and 4; a small futures tile crossed out in orange",["STEP 4 MISSING","NO FUTURES"]),
('el-11','three small stacked grey tiles'):("[SPOT] ONLY ON PAPER","three stacked futures/leverage tiles each slashed in orange beside one clean teal-bordered paper plan sheet",["FUTURES: NO","PAPER PLAN"]),
('el-11','a paper sheet sliding into a plain tray'):("FILE THE [PLAN]","a glowing paper plan sheet sliding into a glass tray; no chart, no result",["FILED"]),
('el-11','a sheet with three short grey bars, each preceded'):("WHAT [NOT] TO DO","glass sheet with three rows each led by a red-orange circled X icon",["NO LEVERAGE","NO FUTURES","NO RUSH"]),
}
E5={
'18':("[CORRELATED] = ONE RISK","glowing teal glass frame grouping two 3D coins (BTC and ETH) of different sizes",["ONE GROUP"]),
'19':("GROUP VS [INDEPENDENT]","glass frame grouping 3D BTC and ETH coins on the left; one separate 3D coin standing alone on the right",["CORRELATED","INDEPENDENT"]),
'20':("CHECK [BEFORE] GROUPING","two 3D coins side by side with a small detailed comparison chart card to their right",["MOVE TOGETHER?"]),
'21':("THE GROUP [NOTE]","teal glass frame grouping BTC and ETH coins with a short note card to the right",["GROUPED","NOTE"]),
'22':("THE [EXAMPLE] NUMBER","short label card beside a dashed teal formula box holding a single value",["CAP = 10% (EXAMPLE)"]),
'29':("CEILING, [CAP], GROUP","numbered step flow: ceiling bar, cap line over a position bar, glass frame grouping two coins",["1 CEILING","2 CAP","3 GROUP"]),
'30':("BUILD THE [PORTFOLIO] MAP","row: wide budget bar, one lone coin, glass frame grouping two coins",["BUDGET","SINGLE","GROUP"]),
'31':("[RESTATE] THE GROUP","fresh crisp glass frame grouping BTC and ETH coins under a headline bar",["SAME GROUP"]),
'40':("SECOND PASS, [CLEAN] PAGE","faded scrap card on the left, clean glowing card on the right with a grouping frame and note",["DRAFT","CLEAN"]),
'41':("START [CLEAN]","faded tilted scrap card set aside; crisp upright card with a grouped-coin frame",["SCRAP","CLEAN COPY"]),
'45':("GROUP + SINGLE, [NO TARGET]","grouped two coins on the left, one lone coin with a note on the right; no target or bullseye",["GROUP","SINGLE"]),
'47':("REMOVE THE [TARGET]","two rule lines, the upper struck through in orange, beside a grouped-coin frame",["NO PRICE TARGET","KEEP GROUP"]),
'48':("[REBUILT] PLAN","row of budget bar, lone coin and grouped coins, with an empty dashed EXAMPLE slot beneath",["SLOT (EXAMPLE)"]),
}
VAR=[('base layout','VARIANT, base: hero centred.'),
('shifted slightly left','DIFFERENT FROM the centred sibling: subject at 80% scale, left of centre, with a glow trail to the right.'),
('highlighted mint','DIFFERENT FROM the centred sibling: all except the key element dimmed to 25%. Only the key element is lit in teal.'),
('outline only','DIFFERENT FROM the centred sibling: the key element is a glowing teal wireframe, not a solid render.'),
('60% scale','DIFFERENT FROM the centred sibling: hero at 60% scale with deep fog and bokeh.'),
('two-step layout','DIFFERENT FROM the centred sibling: a faint empty glass card on the left and the hero card on the right.'),
('mirrored','DIFFERENT FROM the centred sibling: the hero layout is mirrored left-right.')]
def hl(h): return re.sub(r'\[(.+?)\]',r'"\1" (teal)',h)
def shot(head,hero,labels,var):
    return (f"STYLE ANCHOR: course/images/_anchors/elite-teal-anchor.png, the passed el-08 shot 28. Deep navy, electric teal wireframe glass, faint grid and bokeh. No flat off-white card, no soft mint wash, and no grey-blue fog. "
            f"{var} SHOT: Headline below the top 80px, inside the safe area: {hl(head)}. Hero visual: {hero}. "
            f"Labels (short, crisp): {', '.join(labels)}. Keep it a hero visual with a few labels, not a full infographic page. All text and key content inside the centre 1536x864 safe area. Do not redraw the sibling.")
def varof(s):
    for k,v in VAR:
        if k in s: return v
    return 'hero centred'
def write(name,data,items_txt):
    json.dump(data,open(f'{O}/{name}.json','w'),indent=1)
    open(f'{O}/{name}.txt','w').write(ANCHOR_LINE+"\nAnchors: "+", ".join(ANCH_ELITE)+"\n\n"+"\n\n".join(items_txt)+"\n")
n=0;miss=[]
for f in sorted(glob.glob(B+'/*.json')):
    d=json.load(open(f)); name=os.path.basename(f)[:-5]; txt=[]
    for it in d['items']:
        s=it['prompt'].split('SHOT:',1)[1].strip(); les=it.get('lesson','el-05')[:5]
        if name.startswith('el-05'):
            c=E5[it['shot']]
        else:
            c=next((v for (l,p),v in C.items() if (l==les or l=='*') and s.startswith(p)),None)
            if not c: miss.append((name,it['shot'],s[:60]));continue
        it['prompt_v2']=it['prompt']
        it['prompt']=STYLE+"\n"+NEG+"\n"+shot(*c,varof(s))
        it['style_anchor']=ANCH_ELITE; it['style']='GBB-v3-elite-teal'; n+=1
        txt.append(f"=== {it.get('lesson','el-05-portfolio-risk')} SHOT {it['shot']} ===\n{ANCHOR_LINE}\n{it['prompt']}")
    d['style_anchor']=ANCH_ELITE; write(name,d,txt)
print(n,miss)
