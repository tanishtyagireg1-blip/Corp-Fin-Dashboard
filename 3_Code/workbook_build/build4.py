# ======================================================= POLICY RESPONSE SCORECARD
def LK(sh,row,lab_cell,first='B',last='I'):
    return f'IFERROR(INDEX({sh}!${first}${row}:${last}${row},MATCH({lab_cell},{sh}!${first}$4:${last}$4,0)),"n/a")'
wpo=sheet('Policy','7030A0')
title(wpo,'Task 2(c) and Task 3: how did financial policy respond to the featured shocks?','Each block pulls the same metrics for the year before, the year of, and the year after a featured shock (change the blue FY labels to re-point it). "Rose / Fell" compares the last available year with the pre-shock year.')
MET=[('Leverage & liquidity',None,None,None,None),
 ('Debt / equity, all debt incl. gold & leases','Ratios','de3','x',NF_X),('Net debt / equity','Ratios','nde3','x',NF_X),('Borrowings (Rs cr)','Ratios','d_b','cr',NF_CR),('Gold on loan (Rs cr)','Ratios','d_g','cr',NF_CR),
 ('Cash reserves (Rs cr)','Ratios','liq','cr',NF_CR),('Interest coverage, EBIT / finance costs','Ratios','cov1','x',NF_X),
 ('Investment',None,None,None,None),
 ('Gross fixed assets / total assets','Ratios','gfa_ta','pct',NF_PCT),('Capex (Rs cr)','Ratios','capex','cr',NF_CR),('Capex / depreciation','Ratios','capex_dep','x',NF_X),('Inventory days','Ratios','invd','abs','0'),
 ('Payout',None,None,None,None),
 ('Dividend per share (Rs)','Ratios','dps','abs','0.00'),('Payout ratio, DPS / EPS','Ratios','payout','pct',NF_PCT),('Free cash flow ex gold-loan movement (Rs cr)','Ratios','fcf','abs',NF_CR),
 ('Risk and return',None,None,None,None),
 ('Annual beta (raw)','WACC','braw','abs','0.00'),('Cost of equity','WACC','ke','pct',NF_PCT2),('WACC','WACC','wacc','pct',NF_PCT2),('ROIC','WACC','roic','pct',NF_PCT),('ROIC - WACC spread','WACC','spread','pct','+0.0%;-0.0%;0.0%'),('Titan TSR in the year','TSR','tsr','pct',NF_PCTS)]
BLK=[('S1','COVID-19 national lockdown (25 Mar 2020)','FY20','FY21','FY22'),('S5','RBI rate-hike cycle (from 4 May 2022)','FY22','FY23','FY24'),('S8','US/Israel-Iran war & oil shock (2 Mar 2026)','FY25','FY26','FY27')]
PR={}      # (block,metric key) -> row
r=4
for bi,(sid,nm,a,b,c) in enumerate(BLK):
    sec(wpo,r,f'{sid}: {nm}',1,7); r+=1
    hdr(wpo,r,1,['Metric','Pre-shock FY','Shock FY','Post-shock FY','Change (last available vs pre)','Direction','Sheet / definition'],h=30)
    r+=1; hr=r-1
    put(wpo,f'A{r}','Financial year (edit)',F_SUB)
    for j,v in enumerate((a,b,c)): put(wpo,f'{CL(2+j)}{r}',v,F_IN,fill=FILL_IN,al=AL_C)
    lr=r; r+=1
    for lab,sh,key,typ,nf in MET:
        if sh is None:
            put(wpo,f'A{r}',lab,F_SEC); r+=1; continue
        PR[(sid,key,sh)]=r
        put(wpo,f'A{r}',lab)
        if sh=='TSR':
            r+=1; continue
        for j in range(3):
            c_=CL(2+j)
            if sh=='Ratios': rowsrc=RR[key]
            elif sh=='WACC': rowsrc=WR[key]
            put(wpo,f'{c_}{r}',f'={LK(sh,rowsrc,f"{c_}${lr}")}',nf=nf,al=Alignment(horizontal='right'))
        if typ=='cr': put(wpo,f'E{r}',f'=IF(ISNUMBER(D{r}),D{r}/B{r}-1,IF(ISNUMBER(C{r}),C{r}/B{r}-1,"n/a"))',nf='+0%;-0%;0%',al=Alignment(horizontal='right'))
        else:
            enf={'x':'+0.00"x";-0.00"x"','pct':'+0.0%;-0.0%;0.0%','abs':'+0.00;-0.00;0.00'}[typ]
            put(wpo,f'E{r}',f'=IF(ISNUMBER(D{r}),D{r}-B{r},IF(ISNUMBER(C{r}),C{r}-B{r},"n/a"))',nf=enf,al=Alignment(horizontal='right'))
        put(wpo,f'F{r}',f'=IF(ISNUMBER(E{r}),IF(E{r}>0,"Rose",IF(E{r}<0,"Fell","Flat")),"n/a")',al=AL_C)
        put(wpo,f'G{r}',f'{sh}!{key}' if False else f'{sh} sheet',F_SUB)
        r+=1
    # TSR row handled separately (not on Ratios/WACC)
    r+=1
# patch TSR rows: map FY label to TSR_Alpha rows (A5:A12 start with FY label)
for bi,(sid,nm,a,b,c) in enumerate(BLK):
    rr_=PR[(sid,'tsr','TSR')]; lr=rr_-0
    # find label row of the block: search upward for 'Financial year (edit)'
    k=rr_
    while wpo[f'A{k}'].value!='Financial year (edit)': k-=1
    for j in range(3):
        c_=CL(2+j)
        put(wpo,f'{c_}{rr_}',f'=IFERROR(INDEX(TSR_Alpha!$I$5:$I$12,MATCH({c_}${k}&"*",TSR_Alpha!$A$5:$A$12,0)),"n/a")',nf=NF_PCTS,al=Alignment(horizontal='right'))
    put(wpo,f'G{rr_}','TSR_Alpha sheet',F_SUB)
    put(wpo,f'F{rr_}',f'=IF(ISNUMBER(E{rr_}),IF(E{rr_}>0,"Rose",IF(E{rr_}<0,"Fell","Flat")),"n/a")',al=AL_C)
    put(wpo,f'E{rr_}',f'=IF(ISNUMBER(D{rr_}),D{rr_}-B{rr_},IF(ISNUMBER(C{rr_}),C{rr_}-B{rr_},"n/a"))',nf='+0.0%;-0.0%;0.0%',al=Alignment(horizontal='right'))
# live diagnosis strings
def PC(sid,key,sh,col): return f'{col}{PR[(sid,key,sh)]}'
sec(wpo,r,'Diagnosis (text is formula-driven; numbers update with the workbook)',1,7); r+=1
DIAG={}
d1=(f'="S1 COVID: Titan cut capex from Rs "&TEXT({PC("S1","capex","Ratios","B")},"#,##0")&" cr to Rs "&TEXT({PC("S1","capex","Ratios","C")},"#,##0")&" cr ("&TEXT({PC("S1","capex_dep","Ratios","C")},"0.00")&"x depreciation), repaid borrowings from Rs "&TEXT({PC("S1","d_b","Ratios","B")},"#,##0")&" cr to Rs "&TEXT({PC("S1","d_b","Ratios","C")},"#,##0")&" cr, built cash to Rs "&TEXT({PC("S1","liq","Ratios","C")},"#,##0")&" cr and held DPS at Rs "&TEXT({PC("S1","dps","Ratios","C")},"0.0")&" (payout "&TEXT({PC("S1","payout","Ratios","C")},"0%")&"). Beta moved "&TEXT({PC("S1","braw","WACC","B")},"0.00")&" to "&TEXT({PC("S1","braw","WACC","C")},"0.00")&"."')
d5=(f'="S5 rate hikes: borrowings rose from Rs "&TEXT({PC("S5","d_b","Ratios","B")},"#,##0")&" cr to Rs "&TEXT({PC("S5","d_b","Ratios","D")},"#,##0")&" cr two years on; D/E (all debt) went "&TEXT({PC("S5","de3","Ratios","B")},"0.00")&"x to "&TEXT({PC("S5","de3","Ratios","D")},"0.00")&"x and interest coverage fell from "&TEXT({PC("S5","cov1","Ratios","B")},"0.0")&"x to "&TEXT({PC("S5","cov1","Ratios","D")},"0.0")&"x. Payout stayed near "&TEXT({PC("S5","payout","Ratios","D")},"0%")&" (smoothed) while capex/depreciation was "&TEXT({PC("S5","capex_dep","Ratios","C")},"0.00")&"x then "&TEXT({PC("S5","capex_dep","Ratios","D")},"0.00")&"x."')
d8=(f'="S8 Iran war: Titan entered the shock at its most levered point - D/E (all debt) "&TEXT({PC("S8","de3","Ratios","C")},"0.00")&"x, coverage "&TEXT({PC("S8","cov1","Ratios","C")},"0.0")&"x, free cash flow ex gold-loan Rs "&TEXT({PC("S8","fcf","Ratios","C")},"#,##0")&" cr, cash only "&TEXT({PC("S8","liq","Ratios","C")}/{PC("S8","d_b","Ratios","C")},"0.00")&"x borrowings. Annual beta "&TEXT({PC("S8","braw","WACC","B")},"0.00")&" to "&TEXT({PC("S8","braw","WACC","C")},"0.00")&". FY27 audited accounts are not yet available, so the policy response is not observable."')
for t_ in (d1,d5,d8):
    put(wpo,f'A{r}',t_,al=wrapal()); wpo.merge_cells(f'A{r}:G{r}'); wpo.row_dimensions[r].height=48; r+=1
widths(wpo,{'A':46,'B':14,'C':14,'D':14,'E':18,'F':11,'G':22})
wpo.freeze_panes='A4'
wpo.conditional_formatting.add(f'F5:F{r}',FormulaRule(formula=['F5="Fell"'],font=Font(name=FONT,color='C00000')))

# ======================================================= VERDICT
wv=sheet('Verdict','7030A0')
title(wv,'Task 3: value created or destroyed - market view and fundamental view, year by year','Market view: TSR vs the CAPM required return (cost of equity). Fundamental view: ROIC vs WACC (economic profit). Both are live links.')
hdr(wv,4,1,['Financial year','Main shocks in the year (edit)','Titan TSR','NIFTY 500 price return','Excess vs market','Cost of equity','Excess over cost of equity','Excess value (Rs cr)','Jensen alpha','ROIC - WACC','EVA (Rs cr)','Market verdict','Fundamental verdict','Combined reading'],h=48)
SHK_TXT=['S1 COVID lockdown (Mar 2020)','S2 stimulus & repo cut; first-wave recovery','S3 second wave (May 2021); S4 Ukraine war (Feb 2022)','S5 rate hikes (May 2022); S6 Adani-Hindenburg (Jan 2023)','Post-hike normalisation; election year','Gold-price spike; cost pressure on margins','S7 US tariffs (Aug 2025); S8 Iran war (Mar 2026)','S8 aftermath, oil shock, gold at record']
for k in range(8):
    r=5+k; t_=5+k; wc=CL(3+k) if k<7 else None
    put(wv,f'A{r}',f'=TSR_Alpha!A{t_}',F_LINK); put(wv,f'B{r}',SHK_TXT[k],F_IN,al=wrapal())
    put(wv,f'C{r}',f'=TSR_Alpha!I{t_}',F_LINK,nf=NF_PCTS); put(wv,f'D{r}',f'=TSR_Alpha!J{t_}',F_LINK,nf=NF_PCTS); put(wv,f'E{r}',f'=C{r}-D{r}',nf='+0.0%;-0.0%;0.0%')
    put(wv,f'F{r}',f'=TSR_Alpha!P{t_}',F_LINK,nf=NF_PCT2); put(wv,f'G{r}',f'=TSR_Alpha!Q{t_}',F_LINK,nf='+0.0%;-0.0%;0.0%',bold=True); put(wv,f'H{r}',f'=TSR_Alpha!S{t_}',F_LINK,nf='#,##0;(#,##0);"-"')
    put(wv,f'I{r}',f'=TSR_Alpha!M{t_}',F_LINK,nf='+0.0%;-0.0%;0.0%')
    if k<7:
        put(wv,f'J{r}',f'=WACC!{CL(3+k)}{WR["spread"]}',F_LINK,nf='+0.0%;-0.0%;0.0%'); put(wv,f'K{r}',f'=WACC!{CL(3+k)}{WR["eva"]}',F_LINK,nf='#,##0;(#,##0);"-"')
        put(wv,f'M{r}',f'=IF(J{r}>0,"ROIC > WACC","ROIC < WACC")',al=AL_C)
    else:
        put(wv,f'J{r}','n/a',F_SUB,al=AL_C); put(wv,f'K{r}','n/a',F_SUB,al=AL_C); put(wv,f'M{r}','FY27 accounts pending',F_SUB,al=AL_C)
    put(wv,f'L{r}',f'=IF(G{r}>0,"Value created","Value destroyed")',al=AL_C)
    put(wv,f'N{r}',f'=IF(J{r}="n/a","Market only",IF(AND(G{r}>0,J{r}>0),"Both positive",IF(AND(G{r}<=0,J{r}>0),"Fundamentals good, market de-rated",IF(AND(G{r}>0,J{r}<=0),"Market looked through weak year","Both negative"))))',al=AL_C)
    wv.row_dimensions[r].height=30
put(wv,'A14','FY21-FY26 total (the brief period)',F_B); put(wv,'H14','=SUM(H6:H11)',nf='#,##0;(#,##0);"-"',bold=True); put(wv,'K14','=SUM(K6:K11)',nf='#,##0;(#,##0);"-"',bold=True)
put(wv,'A15','Years with value created (market view, FY21-FY26)',F_BASE); put(wv,'H15','=COUNTIF(L6:L11,"Value created")&" of 6"',al=Alignment(horizontal='right'),bold=True)
put(wv,'A16','Years with ROIC > WACC (FY21-FY26)',F_BASE); put(wv,'K16','=COUNTIF(J6:J11,">0")&" of 6"',al=Alignment(horizontal='right'),bold=True)
put(wv,'A17','Excess value is (TSR - Ke) x opening market cap each year; years are not strictly additive, so the total is indicative. FY20 is a 9-month partial year; FY27 is year-to-date.',F_SUB)
wv.conditional_formatting.add('L5:L12',FormulaRule(formula=['L5="Value created"'],fill=FILL_G)); wv.conditional_formatting.add('L5:L12',FormulaRule(formula=['L5="Value destroyed"'],fill=FILL_R))
wv.conditional_formatting.add('M5:M12',FormulaRule(formula=['M5="ROIC > WACC"'],fill=FILL_G)); wv.conditional_formatting.add('M5:M12',FormulaRule(formula=['M5="ROIC < WACC"'],fill=FILL_R))
chv2=BarChart(); chv2.type='col'; chv2.gapWidth=50
chv2.add_data(Reference(wv,min_col=7,min_row=4,max_row=12),titles_from_data=True); chv2.set_categories(Reference(wv,min_col=1,min_row=5,max_row=12))
chv2.series[0].graphicalProperties.solidFill=BLUE; chv2.series[0].invertIfNegative=False
style_chart(chv2,'Market view: return above the CAPM required return',None,'Excess over cost of equity',w=17,h=8.5); chv2.legend=None; chv2.y_axis.number_format='0%'; wv.add_chart(chv2,'A20')
chv3=BarChart(); chv3.type='col'; chv3.gapWidth=50
chv3.add_data(Reference(wv,min_col=10,min_row=4,max_row=11),titles_from_data=True); chv3.set_categories(Reference(wv,min_col=1,min_row=5,max_row=11))
chv3.series[0].graphicalProperties.solidFill=ORANGE; chv3.series[0].invertIfNegative=False
style_chart(chv3,'Fundamental view: ROIC minus WACC',None,'Spread',w=17,h=8.5); chv3.legend=None; chv3.y_axis.number_format='0%'; wv.add_chart(chv3,'H20')
widths(wv,{'A':30,'B':34,'C':10,'D':11,'E':10,'F':10,'G':12,'H':12,'I':10,'J':10,'K':11,'L':15,'M':16,'N':32})
wv.freeze_panes='C5'
