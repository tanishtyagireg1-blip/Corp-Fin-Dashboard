# ======================================================= SCENARIOS (FY27-FY31)
wsn=sheet('Scenarios','ED7D31')
title(wsn,'Task 4: five-year financial strategy (FY27-FY31) - four cases on one engine','Status quo vs Recommended policy, each under a base and a stress macro. Interest is charged on opening balances (no circularity); borrowings are the funding plug. Blue = editable assumptions.')
sec(wsn,4,'Calibration from FY26 actuals (live)',1,8)
CAL=[('Operating EBIT margin',f'=Ratios!I{RR["opebit"]}/Financials!I{FR["rev"]}',NF_PCT2),('Other income % revenue',f'=Financials!I{FR["oi"]}/Financials!I{FR["rev"]}',NF_PCT2),
 ('D&A % revenue',f'=Financials!I{FR["da"]}/Financials!I{FR["rev"]}',NF_PCT2),('Capex % revenue',f'=Ratios!I{RR["capex_rev"]}',NF_PCT2),('Inventory days',f'=Ratios!I{RR["invd"]}','0.0'),
 ('Gold on loan / inventory',f'=Ratios!I{RR["gold_inv"]}',NF_PCT),('Payout (DPS/EPS)',f'=Ratios!I{RR["payout"]}',NF_PCT),
 ('Cost of borrowings (interest / avg borrowings)',f'=(Financials!I{FR["fin_b"]}+Financials!I{FR["fin_o"]})/AVERAGE(Ratios!H{RR["d_b"]},Ratios!I{RR["d_b"]})',NF_PCT2),
 ('Cost of gold on loan',f'=Financials!I{FR["fin_g"]}/AVERAGE(Ratios!H{RR["d_g"]},Ratios!I{RR["d_g"]})',NF_PCT2),('Cost of leases',f'=Financials!I{FR["fin_l"]}/AVERAGE(Ratios!H{RR["d_l"]},Ratios!I{RR["d_l"]})',NF_PCT2),
 ('Cash reserves in days of revenue',f'=Ratios!I{RR["liqd"]}','0.0'),('WACC FY26',f'=WACC!I{WR["wacc"]}',NF_PCT2),('Lease liability growth (assumed)',0.05,NF_PCT),('Gold-loan cost pass-through of policy-rate shock',0.5,'0%')]
CA={}
for i,(lab,f,nf) in enumerate(CAL):
    q=5+i; CA[lab]=f'$B${q}'; put(wsn,f'A{q}',lab)
    put(wsn,f'B{q}',f,F_LINK if isinstance(f,str) else F_IN,nf=nf,fill=None if isinstance(f,str) else FILL_IN,al=AL_C)
put(wsn,'D5','Guardrails',F_B); put(wsn,'D6','Minimum interest cover (x)'); put(wsn,'F6',5.0,F_IN,nf='0.0"x"',fill=FILL_IN,al=AL_C)
put(wsn,'D7','Maximum D/E, all debt (x)'); put(wsn,'F7',2.0,F_IN,nf='0.0"x"',fill=FILL_IN,al=AL_C)
YC=['C','D','E','F','G']; YL=['FY27E','FY28E','FY29E','FY30E','FY31E']
B_=lambda k:CA[k]
GB=[0.16,0.13,0.12,0.11,0.10]; GS=[0.04,0.04,0.06,0.08,0.08]; MS=[0.070,0.073,0.076,0.080,0.083]
CASES=[
 ('A','Status quo policy, base macro',dict(g=GB,m=[f'={B_("Operating EBIT margin")}']*5,capex=[f'={B_("Capex % revenue")}']*5,inv=[f'={B_("Inventory days")}']*5,gs=[f'={B_("Gold on loan / inventory")}']*5,pay=[f'={B_("Payout (DPS/EPS)")}']*5,hedge=[0]*5,shock=[0]*5,cash=[f'={B_("Cash reserves in days of revenue")}']*5,wacc=[f'={B_("WACC FY26")}']*5)),
 ('B','Recommended policy, base macro',dict(g=GB,m=[f'={B_("Operating EBIT margin")}']*5,capex=[0.013]*5,inv=[172,168,164,160,156],gs=[0.45]*5,pay=[0.25]*5,hedge=[0.75]*5,shock=[0]*5,cash=[20]*5,wacc=[f'={B_("WACC FY26")}']*5)),
 ('C','Status quo policy, STRESS macro',dict(g=GS,m=MS,capex=[f'={B_("Capex % revenue")}']*5,inv=[f'={B_("Inventory days")}+15']*5,gs=[f'={B_("Gold on loan / inventory")}']*5,pay=[f'={B_("Payout (DPS/EPS)")}']*5,hedge=[0]*5,shock=[250]*5,cash=[f'={B_("Cash reserves in days of revenue")}']*5,wacc=[f'={B_("WACC FY26")}+0.005']*5)),
 ('D','Recommended policy, STRESS macro',dict(g=GS,m=MS,capex=[0.013]*5,inv=[188,182,176,170,164],gs=[0.45]*5,pay=[0.25]*5,hedge=[0.75]*5,shock=[250]*5,cash=[20]*5,wacc=[f'={B_("WACC FY26")}+0.005']*5))]
SR={}          # case -> dict of row numbers
start=24
for cid,cname,P in CASES:
    r=start; R={}
    sec(wsn,r,f'Case {cid}: {cname}',1,8); r+=1
    hdr(wsn,r,1,['Item','FY26A']+YL+['Note'],h=22); r+=1
    def row(key,lab,vals,nf,note='',fnt=None,fill=None,b0=None):
        global r
        R[key]=r; put(wsn,f'A{r}',lab,F_B if key in('fcff','cover','de','roic','eva') else F_BASE)
        if b0 is not None: put(wsn,f'B{r}',b0,F_LINK if isinstance(b0,str) else F_BASE,nf=nf,al=Alignment(horizontal='right'))
        for j,c in enumerate(YC):
            v=vals(j,c,CL(ord(c)-65)) if callable(vals) else vals[j]
            isin=not (isinstance(v,str) and v.startswith('=') and ('$' not in v or '!' not in v) and callable(vals))
            put(wsn,f'{c}{r}',v,fnt or (F_IN if not callable(vals) else F_BASE),nf=nf,fill=fill,al=Alignment(horizontal='right'))
        put(wsn,f'H{r}',note,F_SUB); r+=1
    put(wsn,f'A{r}','Assumptions',F_SEC); r+=1
    row('g','Revenue growth',P['g'],NF_PCT,'FY26 +45% reflects gold price; base case mean-reverts',fill=FILL_IN)
    row('m','Operating EBIT margin',P['m'],NF_PCT2,'Stress ~ FY21 trough (6.2%) partly recovering',fill=FILL_IN)
    row('capex','Capex % revenue',P['capex'],NF_PCT2,'Recommended: 1.3% (protect core capacity)',fill=FILL_IN)
    row('inv','Inventory days',P['inv'],'0','Recommended: faster turns (coverage of gold-linked stock)',fill=FILL_IN)
    row('gs','Gold on loan / inventory',P['gs'],NF_PCT,'Natural hedge: raise to 45% in recommended',fill=FILL_IN)
    row('pay','Payout (dividend / PAT)',P['pay'],NF_PCT,'',fill=FILL_IN)
    row('hedge','Hedge ratio on borrowings',P['hedge'],'0%','Share fixed via swaps / fixed-rate paper (recommended 75%)',fill=FILL_IN)
    row('shock','Policy-rate shock (bp, from FY27)',P['shock'],'0','Stress = repeat of 2022 (+250 bp)',fill=FILL_IN)
    row('cashd','Target cash reserves (days of revenue)',P['cash'],'0.0','',fill=FILL_IN)
    row('wacc','WACC for EVA',P['wacc'],NF_PCT2,'Stress adds 50 bp',fill=FILL_IN)
    put(wsn,f'A{r}','Operating model',F_SEC); r+=1
    P_=lambda j,c: CL(ord(c)-65)   # previous column letter
    row('rev','Revenue (Rs cr)',lambda j,c,p:f'={p}{r}*(1+{c}{R["g"]})',NF_CR,b0=f'=Financials!I{FR["rev"]}')
    row('opebit','Operating EBIT',lambda j,c,p:f'={c}{R["rev"]}*{c}{R["m"]}',NF_CR,b0=f'=Ratios!I{RR["opebit"]}')
    row('oi','Other income',lambda j,c,p:f'={c}{R["rev"]}*{B_("Other income % revenue")}',NF_CR,b0=f'=Financials!I{FR["oi"]}')
    row('da','D&A',lambda j,c,p:f'={c}{R["rev"]}*{B_("D&A % revenue")}',NF_CR,b0=f'=Financials!I{FR["da"]}')
    row('kb','Cost of borrowings (after hedge)',lambda j,c,p:f'={B_("Cost of borrowings (interest / avg borrowings)")}+(1-{c}{R["hedge"]})*{c}{R["shock"]}/10000',NF_PCT2,b0=f'={B_("Cost of borrowings (interest / avg borrowings)")}')
    row('kg','Cost of gold on loan',lambda j,c,p:f'={B_("Cost of gold on loan")}+{c}{R["shock"]}/10000*{B_("Gold-loan cost pass-through of policy-rate shock")}',NF_PCT2,b0=f'={B_("Cost of gold on loan")}')
    row('int','Interest (opening balances)',lambda j,c,p:f'={p}{{B}}*{c}{R["kb"]}+{p}{{G}}*{c}{R["kg"]}+{p}{{L}}*{B_("Cost of leases")}',NF_CR,b0=f'=Financials!I{FR["fin"]}')
    row('pbt','Profit before tax',lambda j,c,p:f'={c}{R["opebit"]}+{c}{R["oi"]}-{c}{R["int"]}',NF_CR,b0=f'=Financials!I{FR["pbt"]}')
    row('pat','Profit after tax',lambda j,c,p:f'={c}{R["pbt"]}*(1-{IN["tax"]})',NF_CR,b0=f'=Financials!I{FR["pat"]}')
    row('nopat','NOPAT',lambda j,c,p:f'={c}{R["opebit"]}*(1-{IN["tax"]})',NF_CR,b0=f'=WACC!I{WR["nopat"]}')
    row('capexv','Capex',lambda j,c,p:f'={c}{R["rev"]}*{c}{R["capex"]}',NF_CR,b0=f'=Ratios!I{RR["capex"]}')
    row('inv_','Inventory',lambda j,c,p:f'={c}{R["rev"]}*{c}{R["inv"]}/365',NF_CR,b0=f'=Financials!I{FR["inv"]}')
    row('gold','Gold on loan',lambda j,c,p:f'={c}{R["inv_"]}*{c}{R["gs"]}',NF_CR,b0=f'=Financials!I{FR["gold"]}')
    row('dnwc','Increase in inventory net of gold on loan',lambda j,c,p:f'=({c}{R["inv_"]}-{c}{R["gold"]})-({p}{R["inv_"]}-{p}{R["gold"]})',NF_CR)
    row('fcff','Free cash flow to firm = NOPAT + D&A - capex - increase in net inventory',lambda j,c,p:f'={c}{R["nopat"]}+{c}{R["da"]}-{c}{R["capexv"]}-{c}{R["dnwc"]}',NF_CR)
    row('div','Dividends paid (payout x prior-year PAT)',lambda j,c,p:f'={c}{R["pay"]}*{p}{R["pat"]}',NF_CR,b0=f'=Ratios!I{RR["divpd"]}')
    row('ncf','Cash flow before borrowing = PAT + D&A - capex - net inventory - dividends',lambda j,c,p:f'={c}{R["pat"]}+{c}{R["da"]}-{c}{R["capexv"]}-{c}{R["dnwc"]}-{c}{R["div"]}',NF_CR)
    row('cashtg','Cash reserve target',lambda j,c,p:f'={c}{R["rev"]}*{c}{R["cashd"]}/365',NF_CR)
    row('bor','Borrowings (plug, floor 0)',lambda j,c,p:f'=MAX(0,{p}{r}-{c}{R["ncf"]}+({c}{R["cashtg"]}-{p}{r+1}))',NF_CR,b0=f'=Ratios!I{RR["d_b"]}')
    row('cash','Cash reserves',lambda j,c,p:f'={c}{R["cashtg"]}+MAX(0,-({p}{R["bor"]}-{c}{R["ncf"]}+({c}{R["cashtg"]}-{p}{r})))',NF_CR,b0=f'=Ratios!I{RR["liq"]}')
    row('lease','Lease liabilities',lambda j,c,p:f'={p}{r}*(1+{B_("Lease liability growth (assumed)")})',NF_CR,b0=f'=Ratios!I{RR["d_l"]}')
    row('eq','Equity',lambda j,c,p:f'={p}{r}+{c}{R["pat"]}-{c}{R["div"]}',NF_CR,b0=f'=Financials!I{FR["eq"]}')
    row('debt','Total debt incl. gold & leases',lambda j,c,p:f'={c}{R["bor"]}+{c}{R["gold"]}+{c}{R["lease"]}',NF_CR,b0=f'=Ratios!I{RR["d_3"]}')
    put(wsn,f'A{r}','Credit and value metrics',F_SEC); r+=1
    row('de','D/E (all debt)',lambda j,c,p:f'={c}{R["debt"]}/{c}{R["eq"]}',NF_X,b0=f'=Ratios!I{RR["de3"]}')
    row('cover','Interest cover = (operating EBIT + other income) / interest',lambda j,c,p:f'=({c}{R["opebit"]}+{c}{R["oi"]})/{c}{R["int"]}',NF_X,b0=f'=Ratios!I{RR["cov1"]}')
    row('ic','Invested capital = equity + debt - cash',lambda j,c,p:f'={c}{R["eq"]}+{c}{R["debt"]}-{c}{R["cash"]}',NF_CR,b0=f'=WACC!I{WR["ic"]}')
    row('roic','ROIC (NOPAT / average invested capital)',lambda j,c,p:f'={c}{R["nopat"]}/AVERAGE({p}{R["ic"]},{c}{R["ic"]})',NF_PCT,b0=f'=WACC!I{WR["roic"]}')
    row('eva','EVA = (ROIC - WACC) x average invested capital',lambda j,c,p:f'=({c}{R["roic"]}-{c}{R["wacc"]})*AVERAGE({p}{R["ic"]},{c}{R["ic"]})',NF_CR,b0=f'=WACC!I{WR["eva"]}')
    row('breach','Guardrail breach?',lambda j,c,p:f'=IF(OR({c}{R["cover"]}<$F$6,{c}{R["de"]}>$F$7),"BREACH","ok")','@')
    # resolve placeholders {B} {G} {L} in interest row with actual rows (bor, gold, lease)
    for c in YC:
        cell=wsn[f'{c}{R["int"]}']; cell.value=cell.value.replace('{B}',str(R['bor'])).replace('{G}',str(R['gold'])).replace('{L}',str(R['lease']))
    wsn.conditional_formatting.add(f'C{R["breach"]}:G{R["breach"]}',FormulaRule(formula=[f'C{R["breach"]}="BREACH"'],fill=FILL_R,font=Font(name=FONT,bold=True,color='C00000')))
    SR[cid]=R; start=r+2
# ---- summary table (rows 20-23 area is too small -> placed on top-right) : build at columns J..
sec(wsn,4,'Calibration from FY26 actuals (live)',1,8)
put(wsn,'J4','Scenario comparison (FY27-FY31)',F_SEC)
hdr(wsn,5,10,['Metric','A Status quo','B Recommended','C Status quo, stress','D Recommended, stress'],h=44)
SUMM=[('FY31 revenue (Rs cr)',lambda R:f'=G{R["rev"]}',NF_CR),('FY31 PAT (Rs cr)',lambda R:f'=G{R["pat"]}',NF_CR),('Cumulative FCFF FY27-31 (Rs cr)',lambda R:f'=SUM(C{R["fcff"]}:G{R["fcff"]})',NF_CR),
      ('Cumulative dividends (Rs cr)',lambda R:f'=SUM(C{R["div"]}:G{R["div"]})',NF_CR),('FY31 total debt (Rs cr)',lambda R:f'=G{R["debt"]}',NF_CR),('Peak D/E (x)',lambda R:f'=MAX(C{R["de"]}:G{R["de"]})',NF_X),
      ('Minimum interest cover (x)',lambda R:f'=MIN(C{R["cover"]}:G{R["cover"]})',NF_X),('FY31 ROIC',lambda R:f'=G{R["roic"]}',NF_PCT),('Cumulative EVA FY27-31 (Rs cr)',lambda R:f'=SUM(C{R["eva"]}:G{R["eva"]})',NF_CR),
      ('Years in breach of guardrails',lambda R:f'=COUNTIF(C{R["breach"]}:G{R["breach"]},"BREACH")','0')]
SMR={}
for i,(lab,fn,nf) in enumerate(SUMM):
    q=6+i; SMR[lab]=q; put(wsn,f'J{q}',lab)
    for j,cid in enumerate('ABCD'): put(wsn,f'{CL(11+j)}{q}',f'{fn(SR[cid])[0]}{fn(SR[cid])[1:]}'.replace('=','=',1),nf=nf,al=Alignment(horizontal='right'))
# fix: summary formulas reference same-sheet rows; they are already correct row numbers
widths(wsn,{'A':58,'B':12,'C':11,'D':11,'E':11,'F':11,'G':11,'H':42,'I':3,'J':32,'K':14,'L':15,'M':17,'N':17})
wsn.freeze_panes='B4'
# charts
def scen_chart(key,ttl,nf,anchor,ytitle):
    ch=LineChart()
    for cid,cname,_ in CASES:
        R=SR[cid]
        s=Series(Reference(wsn,min_col=2,max_col=7,min_row=R[key]),title=cname); s.smooth=False
        col={'A':GREY,'B':BLUE,'C':ORANGE,'D':NAVY}[cid]; s.graphicalProperties.line.solidFill=col; s.graphicalProperties.line.width=25400
        if cid in 'CD': s.graphicalProperties.line.dashStyle='dash'
        s.marker=Marker(symbol='circle',size=5); s.marker.graphicalProperties=GraphicalProperties(solidFill=col)
        ch.series.append(s)
    ch.set_categories(Reference(wsn,min_col=2,max_col=7,min_row=SR['A']['g']-2))
    style_chart(ch,ttl,None,ytitle,w=15,h=7.5); ch.y_axis.number_format=nf; wsn.add_chart(ch,anchor)
scen_chart('cover','Interest cover by case (x)','0"x"','J18','x')
scen_chart('de','D/E (all debt) by case (x)','0.0"x"','J34','x')
scen_chart('roic','ROIC by case','0%','J50','ROIC')
