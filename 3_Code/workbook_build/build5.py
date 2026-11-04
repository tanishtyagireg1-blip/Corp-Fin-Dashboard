# ======================================================= COUNTERFACTUAL
wc=sheet('Counterfactual','ED7D31')
title(wc,'Task 4: what should the CFO have done in 2020-26? Quantified counterfactuals','Illustrative, model-based estimates (assumptions in blue). They show direction and order of magnitude, not exact outcomes. Base year = FY26.')
def L(sh,rowmap,key,col='I'): return f'{sh}!${col}${rowmap[key]}'
sec(wc,4,'A. Capital-structure counterfactual: WACC and interest cover as leverage rises (market-value weights, Hamada relevering)',1,12)
put(wc,'A5','Long-run growth g (value index)'); put(wc,'B5',0.05,F_IN,nf='0.0%',fill=FILL_IN,al=AL_C)
put(wc,'A6','Minimum interest cover (guardrail, x)'); put(wc,'B6',5.0,F_IN,nf='0.0"x"',fill=FILL_IN,al=AL_C)
put(wc,'A7','Levered beta, FY26 (used)'); put(wc,'B7',f'={L("WACC",WR,"bused")}',F_LINK,nf='0.00',al=AL_C)
put(wc,'A8','Market D/E, FY26'); put(wc,'B8',f'={L("WACC",WR,"mde")}',F_LINK,nf='0.000',al=AL_C)
put(wc,'A9','Unlevered beta = bL / (1 + (1-t) D/E)'); put(wc,'B9',f'=B7/(1+(1-{IN["tax"]})*B8)',nf='0.00',al=AL_C)
put(wc,'A10','Actual pre-tax cost of debt FY26 / debt weight'); put(wc,'B10',f'={L("WACC",WR,"kd")}',F_LINK,nf=NF_PCT2,al=AL_C); put(wc,'C10',f'={L("WACC",WR,"wd")}',F_LINK,nf=NF_PCT,al=AL_C)
put(wc,'A11','Actual WACC FY26 / EBIT FY26 (Rs cr)'); put(wc,'B11',f'={L("WACC",WR,"wacc")}',F_LINK,nf=NF_PCT2,al=AL_C); put(wc,'C11',f'={L("Ratios",RR,"ebit")}',F_LINK,nf=NF_CR,al=AL_C)
put(wc,'E5','Credit-spread schedule (assumed): D/V from',F_B); put(wc,'E6','Spread over actual Kd',F_B)
SPR=[(0,0.0025),(0.10,0.005),(0.15,0.0075),(0.20,0.0125),(0.25,0.02),(0.30,0.0325)]
for j,(a,b) in enumerate(SPR):
    put(wc,f'{CL(6+j)}5',a,F_IN,nf='0%',fill=FILL_IN,al=AL_C); put(wc,f'{CL(6+j)}6',b,F_IN,nf='0.00%',fill=FILL_IN,al=AL_C)
hdr(wc,13,1,['Debt / (D+E) market','D/E','Relevered beta','Cost of equity','Spread (schedule)','Pre-tax Kd','WACC','Debt (Rs cr)','Interest cover (x)','Feasible (cover >= floor)','Value index vs actual (EV)','WACC if feasible'],h=44)
SP0="MATCH($C10,$F$5:$K$5,1)"
for k in range(13):
    r=14+k; w=k*0.025
    put(wc,f'A{r}',w,F_IN,nf='0.0%',al=AL_C)
    put(wc,f'B{r}',f'=A{r}/(1-A{r})',nf='0.000'); put(wc,f'C{r}',f'=$B$9*(1+(1-{IN["tax"]})*B{r})',nf='0.00')
    put(wc,f'D{r}',f'={L("WACC",WR,"rf")}+C{r}*{IN["erp"]}',nf=NF_PCT2)
    put(wc,f'E{r}',f'=INDEX($F$6:$K$6,MATCH(A{r},$F$5:$K$5,1))',nf=NF_PCT2)
    put(wc,f'F{r}',f'=$B$10+E{r}-INDEX($F$6:$K$6,{SP0})',nf=NF_PCT2)
    put(wc,f'G{r}',f'=(1-A{r})*D{r}+A{r}*F{r}*(1-{IN["tax"]})',nf=NF_PCT2,bold=True)
    put(wc,f'H{r}',f'=B{r}*{L("WACC",WR,"mcap")}',nf=NF_CR)
    put(wc,f'I{r}',f'=IF(H{r}=0,"n/a",$C$11/(H{r}*F{r}))',nf='0.0"x"',al=Alignment(horizontal='right'))
    put(wc,f'J{r}',f'=IF(H{r}=0,"Yes",IF(I{r}>=$B$6,"Yes","No"))',al=AL_C)
    put(wc,f'K{r}',f'=($B$11-$B$5)/(G{r}-$B$5)',nf='0.000')
    put(wc,f'L{r}',f'=IF(J{r}="Yes",G{r},"")',nf=NF_PCT2)
wc.conditional_formatting.add('J14:J26',FormulaRule(formula=['J14="No"'],fill=FILL_R))
sec(wc,28,'Result',1,12)
put(wc,'A29','Lowest WACC among feasible leverage levels'); put(wc,'B29','=MIN(L14:L26)',nf=NF_PCT2,bold=True,al=AL_C)
put(wc,'A30','...reached at debt / (D+E)'); put(wc,'B30','=INDEX(A14:A26,MATCH(B29,L14:L26,0))',nf='0.0%',bold=True,al=AL_C)
put(wc,'A31','Actual debt / (D+E), FY26'); put(wc,'B31','=C10',nf='0.0%',al=AL_C)
put(wc,'A32','Debt capacity at the cover floor = EBIT / (floor x actual Kd), Rs cr'); put(wc,'B32','=C11/(B6*B10)',nf=NF_CR,bold=True,al=AL_C)
put(wc,'A33','Actual debt (all, incl. gold and leases), Rs cr'); put(wc,'B33',f'={L("WACC",WR,"debt")}',F_LINK,nf=NF_CR,al=AL_C)
put(wc,'A34','Headroom before the cover floor binds, Rs cr'); put(wc,'B34','=B32-B33',nf=NF_CR,bold=True,al=AL_C)
put(wc,'A35','Headroom as % of FY26 EBITDA'); put(wc,'B35',f'=B34/{L("Ratios",RR,"ebitda")}',nf='0.0%',al=AL_C)
put(wc,'A36',f'="Reading: theory (trade-off) says WACC keeps falling with debt up to about "&TEXT(INDEX(A14:A26,MATCH(MIN(G14:G26),G14:G26,0)),"0%")&" of market value, but Titan\'s own cover guardrail ("&TEXT(B6,"0.0")&"x) binds at about Rs "&TEXT(B32,"#,##0")&" cr of debt, leaving only Rs "&TEXT(B34,"#,##0")&" cr of headroom against Rs "&TEXT(B33,"#,##0")&" cr already drawn. Market D/E looks low (equity is worth "&TEXT({L("WACC",WR,"pb")},"0")&"x book) but earnings-based capacity is nearly used."',F_SUB,al=wrapal())
wc.merge_cells('A36:L36'); wc.row_dimensions[36].height=44
chw=LineChart(); chw.add_data(Reference(wc,min_col=7,min_row=13,max_row=26),titles_from_data=True); chw.set_categories(Reference(wc,min_col=1,min_row=14,max_row=26))
chw.series[0].graphicalProperties.line.solidFill=BLUE; chw.series[0].graphicalProperties.line.width=28575; chw.series[0].marker=Marker(symbol='circle',size=6); chw.series[0].smooth=False
chw.legend=None; style_chart(chw,'WACC vs leverage (debt / (D+E), market value)','Debt / (D+E)','WACC',w=16,h=8); chw.y_axis.number_format='0.0%'; chw.x_axis.number_format='0%'; wc.add_chart(chw,'A38')
chc=LineChart(); chc.add_data(Reference(wc,min_col=9,min_row=13,max_row=26),titles_from_data=True); chc.set_categories(Reference(wc,min_col=1,min_row=14,max_row=26))
chc.series[0].graphicalProperties.line.solidFill=ORANGE; chc.series[0].graphicalProperties.line.width=28575; chc.series[0].marker=Marker(symbol='circle',size=6); chc.series[0].smooth=False
chc.legend=None; style_chart(chc,'Interest cover vs leverage (x)','Debt / (D+E)','x',w=16,h=8); chc.y_axis.number_format='0"x"'; chc.x_axis.number_format='0%'; wc.add_chart(chc,'G38')

r=56; sec(wc,r,'B. Interest-rate counterfactual (FY26 balance sheet): what a repeat of the 2022 hiking cycle would do',1,12)
put(wc,f'A{r+1}','Share of borrowings that reprices within a year'); put(wc,f'B{r+1}',1.0,F_IN,nf='0%',fill=FILL_IN,al=AL_C); put(wc,f'C{r+1}','99% of borrowings are short-term (Ratios)',F_SUB)
put(wc,f'A{r+2}','Share of gold-on-loan cost that reprices (pass-through)'); put(wc,f'B{r+2}',0.5,F_IN,nf='0%',fill=FILL_IN,al=AL_C); put(wc,f'C{r+2}','Assumption: gold lease rates move about half as much as policy rates',F_SUB)
put(wc,f'A{r+3}','Hedge ratio (fixed via swaps / fixed-rate NCDs)'); put(wc,f'B{r+3}',0.75,F_IN,nf='0%',fill=FILL_IN,al=AL_C)
hdr(wc,r+4,1,['Rate shock (bp)','Repricing debt (Rs cr)','Extra interest, unhedged (Rs cr)','Cover, unhedged (x)','EPS hit, unhedged','Extra interest, hedged (Rs cr)','Cover, hedged (x)','EPS hit, hedged'],h=44)
for j,bp in enumerate((100,200,250,300)):
    q=r+5+j
    put(wc,f'A{q}',bp,F_IN,fill=FILL_IN,al=AL_C)
    put(wc,f'B{q}',f'={L("Ratios",RR,"d_b")}*$B${r+1}+{L("Ratios",RR,"d_g")}*$B${r+2}*0.5',nf=NF_CR)
    put(wc,f'C{q}',f'=A{q}/10000*B{q}',nf=NF_CR); put(wc,f'D{q}',f'={L("Ratios",RR,"ebit")}/({L("Financials",FR,"fin")}+C{q})',nf='0.0"x"')
    put(wc,f'E{q}',f'=-C{q}*(1-{IN["tax"]})/{IN["sh"]}/{L("Financials",FR,"eps")}',nf='0.0%')
    put(wc,f'F{q}',f'=C{q}*(1-$B${r+3})',nf=NF_CR); put(wc,f'G{q}',f'={L("Ratios",RR,"ebit")}/({L("Financials",FR,"fin")}+F{q})',nf='0.0"x"')
    put(wc,f'H{q}',f'=-F{q}*(1-{IN["tax"]})/{IN["sh"]}/{L("Financials",FR,"eps")}',nf='0.0%')
put(wc,f'A{r+9}','The RBI raised the repo rate by 250 bp between May 2022 and Feb 2023 (Inputs). The 250 bp row is the direct analogue.',F_SUB)

r=68; sec(wc,r,'C. Payout and funding counterfactual: were dividends funded by operations or by debt?',1,12)
hdr(wc,r+1,1,['Item']+F.FY,h=24)
rows_=[('Free cash flow ex gold-loan (Rs cr)',lambda c:f'=Ratios!{c}{RR["fcf"]}',NF_CR),('Cash dividends paid (Rs cr)',lambda c:f'=Ratios!{c}{RR["divpd"]}',NF_CR),
       ('FCF after dividends (Rs cr)',lambda c:f'={c}{r+2}-{c}{r+3}',NF_CR),('Cumulative FCF after dividends from FY21 (Rs cr)',None,NF_CR),
       ('Change in borrowings (Rs cr)',None,NF_CR),('Earnings yield = EPS / price',None,NF_PCT2),('After-tax cost of debt',None,NF_PCT2)]
for i,(lab,fn,nf) in enumerate(rows_):
    q=r+2+i; put(wc,f'A{q}',lab)
    for k in range(8):
        c=CL(2+k); p=CL(1+k)
        if i==3:
            if k==0: put(wc,f'{c}{q}','n/a',F_SUB,al=AL_C)
            elif k==1: put(wc,f'{c}{q}','n/a',F_SUB,al=AL_C)
            else: put(wc,f'{c}{q}',f'={c}{r+4}' if k==2 else f'={p}{q}+{c}{r+4}',nf=nf)
        elif i==4:
            put(wc,f'{c}{q}','n/a' if k==0 else f'=Ratios!{c}{RR["d_b"]}-Ratios!{p}{RR["d_b"]}',F_BASE if k else F_SUB,nf=nf,al=Alignment(horizontal='right'))
        elif i==5:
            put(wc,f'{c}{q}','n/a' if k==0 else f'=Ratios!{c}{RR["eps"]}/WACC!{c}{WR["px"]}',F_BASE if k else F_SUB,nf=nf,al=Alignment(horizontal='right'))
        elif i==6:
            put(wc,f'{c}{q}','n/a' if k==0 else f'=WACC!{c}{WR["kdt"]}',F_LINK if k else F_SUB,nf=nf,al=Alignment(horizontal='right'))
        else: put(wc,f'{c}{q}',fn(c),nf=nf)
put(wc,f'A{r+9}',f'="Buy-back test (FY26): earnings yield "&TEXT(I{r+7},"0.00%")&" vs after-tax cost of debt "&TEXT(I{r+8},"0.00%")&IF(I{r+7}<I{r+8}," - a debt-funded buy-back would reduce EPS and destroy value at "&TEXT(WACC!I{WR["pb"]},"0")&"x book. Titan was right not to buy back."," - a buy-back would be EPS-accretive.")',F_B)
put(wc,f'A{r+10}',f'="Dividends vs cash generation: FCF after dividends was negative in "&COUNTIF(D{r+4}:I{r+4},"<0")&" of 6 years (FY21-FY26), cumulative Rs "&TEXT(I{r+5},"#,##0")&" cr, so borrowings rose by Rs "&TEXT(SUM(D{r+6}:I{r+6}),"#,##0")&" cr over the same years."',F_B)

r=82; sec(wc,r,'D. Investment counterfactual: was capex too thin?',1,12)
hdr(wc,r+1,1,['Item']+F.FY,h=24)
for i,(lab,fn,nf) in enumerate([('Revenue / gross fixed assets (x)',lambda c:f'=Financials!{c}{FR["rev"]}/Ratios!{c}{RR["gfa"]}','0.0"x"'),('Capex / revenue',lambda c:f'=Ratios!{c}{RR["capex_rev"]}',NF_PCT2),('Capex / depreciation (x)',lambda c:f'=Ratios!{c}{RR["capex_dep"]}',NF_X),('Net investment = capex - D&A (Rs cr)',lambda c:f'=Ratios!{c}{RR["capex"]}-Financials!{c}{FR["da"]}',NF_CR)]):
    q=r+2+i; put(wc,f'A{q}',lab)
    for k in range(8): put(wc,f'{CL(2+k)}{q}',fn(CL(2+k)),nf=nf)
put(wc,f'A{r+7}','Extra capex per year if raised to this % of revenue'); put(wc,f'B{r+7}',0.013,F_IN,nf='0.0%',fill=FILL_IN,al=AL_C)
put(wc,f'A{r+8}','Extra capex on FY26 revenue (Rs cr)'); put(wc,f'B{r+8}',f'=(B{r+7}-Ratios!I{RR["capex_rev"]})*Financials!I{FR["rev"]}',nf=NF_CR,al=AL_C)
put(wc,f'A{r+9}','Illustrative value of that capital = extra x (ROIC - WACC) / WACC (Rs cr)'); put(wc,f'B{r+9}',f'=B{r+8}*WACC!I{WR["spread"]}/WACC!I{WR["wacc"]}',nf=NF_CR,bold=True,al=AL_C)
put(wc,f'A{r+10}',f'="Capex/revenue stayed near "&TEXT(AVERAGE(C{r+3}:I{r+3}),"0.0%")&" and revenue per rupee of gross fixed assets rose from "&TEXT(C{r+2},"0.0")&"x to "&TEXT(I{r+2},"0.0")&"x: assets were sweated hard, partly because gold prices inflate revenue. The fall in gross fixed assets / total assets (13% to 7%) is mainly a denominator effect from inventory growth, not under-investment."',F_SUB,al=wrapal())
wc.merge_cells(f'A{r+10}:L{r+10}'); wc.row_dimensions[r+10].height=44

r=96; sec(wc,r,'E. CFO action table: what should have been done (2020-26) - evidence is live',1,12)
hdr(wc,r+1,1,['#','Decision area','Evidence (live)','What the CFO should have done','Theory'],h=24)
r_p4=72
ACT=[('R1','Leverage',f'="D/E (all debt) rose "&TEXT(Ratios!C{RR["de3"]},"0.00")&"x (FY20) to "&TEXT(Ratios!I{RR["de3"]},"0.00")&"x (FY26); cover fell "&TEXT(Ratios!C{RR["cov1"]},"0.0")&"x to "&TEXT(Ratios!I{RR["cov1"]},"0.0")&"x"',
      'Set an explicit guardrail (cover >= 6x, D/E <= 1.5x) and fund the post-2022 inventory build with equity-like cash flow and longer-tenor debt, not rolling commercial paper.','Trade-off theory; pecking order'),
 ('R2','Debt tenor and rates',f'="Short-term share of borrowings "&TEXT(Ratios!I{RR["st"]},"0%")&" in FY26; +250 bp costs Rs "&TEXT(C63,"#,##0")&" cr (cover "&TEXT(D63,"0.0")&"x)"',
      'Term out at least 40-50% of borrowings and swap about 75% to fixed before the 2022 cycle; the hedged column in section B shows the saving.','Interest-rate risk; MM with taxes'),
 ('R3','Gold-price hedge',f'="Gold on loan funds "&TEXT(Ratios!I{RR["gold_inv"]},"0%")&" of inventory in FY26 (peak "&TEXT(MAX(Ratios!C{RR["gold_inv"]}:I{RR["gold_inv"]}),"0%")&")"',
      'Raise gold-on-loan to about 45% of inventory: it is a natural hedge with the cheapest funding; avoid net-open gold positions as prices spike.','Hedging reduces cost of financial distress'),
 ('R4','Dividend / payout',f'="Payout "&TEXT(MIN(Ratios!C{RR["payout"]}:I{RR["payout"]}),"0%")&"-"&TEXT(MAX(Ratios!C{RR["payout"]}:I{RR["payout"]}),"0%")&"; FCF after dividends negative in "&COUNTIF(D{r_p4}:I{r_p4},"<0")&" of 6 years"',
      'Keep the smoothed policy (it signalled stability) but link DPS growth to FCF after working capital; do not raise DPS faster than EPS when FCF is negative.','Lintner smoothing; signalling'),
 ('R5','Buy-backs',f'="Earnings yield "&TEXT(I{r_p4+3},"0.0%")&" < after-tax Kd "&TEXT(I{r_p4+4},"0.0%")',
      'No buy-back at 20x+ book. If cash is surplus, special dividend or deleveraging beats repurchase.','Signalling; EPS accretion test'),
 ('R6','Investment',f'="Capex/dep "&TEXT(Ratios!D{RR["capex_dep"]},"0.00")&"x in FY21 and "&TEXT(Ratios!E{RR["capex_dep"]},"0.00")&"x in FY22, then "&TEXT(Ratios!I{RR["capex_dep"]},"0.00")&"x"',
      'Protect core capex through shocks (it fell 59% in FY21 and recovered); fund store and factory capacity before the cycle turns, since ROIC > WACC in 5 of 6 years.','NPV rule; real options'),
 ('R7','Liquidity',f'="Cash / borrowings "&TEXT(Ratios!I{RR["liqb"]},"0.00")&"x in FY26 vs "&TEXT(Ratios!E{RR["liqb"]},"0.0")&"x in FY22"',
      'Hold a liquidity buffer of at least 20 days of revenue or committed lines equal to 50% of short-term borrowings.','Precautionary motive for cash')]

hdr(wc,r+1,1,['Decision','Evidence (live)','','','','What the CFO should have done','','','','','Theory',''],h=24)
for c0,c1 in (('B','E'),('F','J'),('K','L')): wc.merge_cells(f'{c0}{r+1}:{c1}{r+1}')
for i,(a,b,c_,d,e) in enumerate(ACT):
    q=r+2+i
    put(wc,f'A{q}',f'{a}  {b}',F_B,al=wrapal()); put(wc,f'B{q}',c_,al=wrapal()); put(wc,f'F{q}',d,al=wrapal()); put(wc,f'K{q}',e,F_SUB,al=wrapal())
    wc.merge_cells(f'B{q}:E{q}'); wc.merge_cells(f'F{q}:J{q}'); wc.merge_cells(f'K{q}:L{q}'); wc.row_dimensions[q].height=52
widths(wc,{'A':46,'B':14,'C':14,'D':14,'E':14,'F':14,'G':14,'H':14,'I':14,'J':14,'K':14,'L':14})
