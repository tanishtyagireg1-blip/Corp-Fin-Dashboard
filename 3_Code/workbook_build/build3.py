# ======================================================= FINANCIALS
wf=sheet('Financials','548235')
title(wf,'Task 2(c) inputs: Titan Company consolidated financials, FY19-FY26 (Rs crore)','Blue = typed from audited consolidated statements in the annual reports (see Sources). Each year uses the latest restated figure. FY19 converted from Rs lakh (AR 2019-20). FY ends 31 March.')
hdr(wf,4,1,['Line item']+F.FY+['Unit','Source / comment'],h=24)
FR={}; r=5
def fsec(txt):
    global r; sec(wf,r,txt,1,11); r+=1
fsec('Profit & loss')
for key,lab,vals,unit,src in F.IS:
    FR[key]=r; put(wf,f'A{r}',lab,F_B if not lab.startswith('  ') else F_BASE)
    for k,v in enumerate(vals): put(wf,f'{CL(2+k)}{r}',v,F_IN,nf='#,##0.00' if unit=='Rs' else NF_CR1)
    put(wf,f'J{r}',unit,F_SUB,al=AL_C); put(wf,f'K{r}',src,F_SUB); r+=1
fsec('Balance sheet (31 March)')
for key,lab,vals,unit,src in F.BS:
    FR[key]=r; put(wf,f'A{r}',lab,F_B if lab.isupper() or lab.startswith('TOTAL') else F_BASE)
    for k,v in enumerate(vals): put(wf,f'{CL(2+k)}{r}',v,F_IN,nf=NF_CR1)
    put(wf,f'J{r}',unit,F_SUB,al=AL_C); put(wf,f'K{r}',src,F_SUB); r+=1
fsec('Cash flow')
for key,lab,vals,unit,src in F.CF:
    FR[key]=r; put(wf,f'A{r}',lab,F_BASE)
    for k,v in enumerate(vals): put(wf,f'{CL(2+k)}{r}',v,F_IN,nf=NF_CR1)
    put(wf,f'J{r}',unit,F_SUB,al=AL_C); put(wf,f'K{r}',src,F_SUB); r+=1
fsec('Integrity checks (should be zero)')
FR['chk_bs']=r; put(wf,f'A{r}','Total assets - (equity + non-current + current liabilities)')
for k in range(8): c=CL(2+k); put(wf,f'{c}{r}',f'=ROUND({c}{FR["ta"]}-({c}{FR["eq"]}+{c}{FR["ncl"]}+{c}{FR["cl"]}),1)',nf='0.0;-0.0;"OK"',al=AL_C)
r+=1; FR['chk_fc']=r; put(wf,f'A{r}','Finance costs - sum of components')
for k in range(8): c=CL(2+k); put(wf,f'{c}{r}',f'=ROUND({c}{FR["fin"]}-SUM({c}{FR["fin_b"]}:{c}{FR["fin_o"]}),1)',nf='0.0;-0.0;"OK"',al=AL_C)
r+=1; FR['chk_pat']=r; put(wf,f'A{r}','PAT - (PBT - tax)')
for k in range(8): c=CL(2+k); put(wf,f'{c}{r}',f'=ROUND({c}{FR["pat"]}-({c}{FR["pbt"]}-{c}{FR["tax"]}),1)',nf='0.0;-0.0;"OK"',al=AL_C)
r+=1; FR['chk_pbt']=r; put(wf,f'A{r}','PBT - (PBT before exceptional - exceptional)')
for k in range(8): c=CL(2+k); put(wf,f'{c}{r}',f'=ROUND({c}{FR["pbt"]}-({c}{FR["pbt0"]}-{c}{FR["exc"]}),1)',nf='0.0;-0.0;"OK"',al=AL_C)
r+=1; FR['chk_gold']=r; put(wf,f'A{r}','Change in gold on loan: balance sheet - cash flow (FY26 diff = acquired Damas balances)')
for k in range(1,8): c=CL(2+k); p=CL(1+k); put(wf,f'{c}{r}',f'=ROUND(({c}{FR["gold"]}-{p}{FR["gold"]})-{c}{FR["dgold"]},0)',nf='0;-0;"OK"',al=AL_C)
widths(wf,{'A':58,'J':7,'K':70});
for k in range(8): wf.column_dimensions[CL(2+k)].width=11
wf.freeze_panes='B5'
def FX(k,c): return f'Financials!{c}{FR[k]}'
FYC=[CL(2+k) for k in range(8)]     # B..I = FY19..FY26

# ======================================================= RATIOS
wra=sheet('Ratios','548235')
title(wra,'Task 2(c): financial policy ratios - investment, capital structure, coverage, payout, liquidity','All formulas link to Financials. Definitions follow the brief; gold-on-loan and Ind AS 116 leases are shown separately so any treatment can be audited.')
hdr(wra,4,1,['Metric']+F.FY+['Definition / treatment'],h=24)
RR={}; r=5
def rsec(txt):
    global r; sec(wra,r,txt,1,10); r+=1
def rrow(key,lab,fn,nf,defn='',start=0,bold=False):
    global r
    RR[key]=r; put(wra,f'A{r}',lab,F_B if bold else F_BASE)
    for k in range(8):
        c=CL(2+k); p=CL(1+k)
        if k<start: put(wra,f'{c}{r}','n/a',F_SUB,al=AL_C); continue
        put(wra,f'{c}{r}',fn(c,p),nf=nf,al=Alignment(horizontal='right'),bold=bold)
    put(wra,f'J{r}',defn,F_SUB); r+=1
def X(k,c): return f'Ratios!{c}{RR[k]}'
rsec('A. Investment (capex) policy')
rrow('gfa','Gross fixed assets (gross PP&E + CWIP), Rs cr',lambda c,p:f'={FX("ppe_g",c)}+{FX("cwip",c)}',NF_CR,'Owned assets at cost; excludes right-of-use assets')
rrow('gfa_ta','Gross fixed assets / total assets  [brief proxy]',lambda c,p:f'={c}{RR["gfa"]}/{FX("ta",c)}',NF_PCT,'Brief: capex proxy = gross fixed assets / total assets. Falls when working capital grows faster than fixed assets',bold=True)
rrow('nfa_ta','Net fixed assets incl. right-of-use / total assets',lambda c,p:f'=({FX("ppe_n",c)}+{FX("cwip",c)}+{FX("rou",c)})/{FX("ta",c)}',NF_PCT,'Net PP&E + CWIP + ROU')
rrow('capex','Capex (cash), Rs cr',lambda c,p:f'={FX("capex",c)}',NF_CR,'Cash purchases of PP&E, intangibles, investment property')
rrow('capex_rev','Capex / revenue',lambda c,p:f'={c}{RR["capex"]}/{FX("rev",c)}',NF_PCT2,'Capital intensity (very low: Titan is a working-capital-heavy business)')
rrow('capex_dep','Capex / depreciation (x)',lambda c,p:f'={c}{RR["capex"]}/{FX("da",c)}',NF_X,'<1x means asset base is shrinking in real terms (ROU depreciation inflates D&A)')
rrow('capex_g','Capex growth y/y',lambda c,p:f'={c}{RR["capex"]}/{p}{RR["capex"]}-1',NF_PCTS,'',start=1)
rrow('dgfa','Increase in gross fixed assets, Rs cr',lambda c,p:f'={c}{RR["gfa"]}-{p}{RR["gfa"]}',NF_CR,'Accrual-based capex proxy (includes acquisitions & FX)',start=1)
rrow('invd','Inventory days (inventory / revenue x 365)',lambda c,p:f'={FX("inv",c)}/{FX("rev",c)}*365',"0",'Gold inventory is the real "capex" of a jeweller')
rsec('B. Capital structure')
rrow('d_b','Borrowings (non-current + current), Rs cr',lambda c,p:f'={FX("b_nc",c)}+{FX("b_c",c)}',NF_CR,'Bank loans, NCDs, commercial paper')
rrow('d_g','Gold on loan, Rs cr',lambda c,p:f'={FX("gold",c)}',NF_CR,'Gold borrowed from banks; hedges gold inventory price risk')
rrow('d_l','Lease liabilities, Rs cr',lambda c,p:f'={FX("l_nc",c)}+{FX("l_c",c)}',NF_CR,'Ind AS 116 (from FY20)')
rrow('d_2','Debt incl. gold on loan, Rs cr',lambda c,p:f'={c}{RR["d_b"]}+{c}{RR["d_g"]}',NF_CR,'')
rrow('d_3','Debt incl. gold on loan and leases, Rs cr',lambda c,p:f'={c}{RR["d_2"]}+{c}{RR["d_l"]}',NF_CR,'Broadest definition of financial debt',bold=True)
rrow('de1','D/E - borrowings only',lambda c,p:f'={c}{RR["d_b"]}/{FX("eq",c)}',NF_X,'Book debt / book equity')
rrow('de2','D/E - borrowings + gold on loan',lambda c,p:f'={c}{RR["d_2"]}/{FX("eq",c)}',NF_X,'')
rrow('de3','D/E - borrowings + gold on loan + leases',lambda c,p:f'={c}{RR["d_3"]}/{FX("eq",c)}',NF_X,'Primary D/E in the report',bold=True)
rrow('liq','Cash reserves: cash + bank balances + current investments, Rs cr',lambda c,p:f'={FX("cash",c)}+{FX("bank",c)}+{FX("cinv",c)}',NF_CR,'Liquid treasury')
rrow('nd1','Net debt (borrowings only), Rs cr  (negative = net cash)',lambda c,p:f'={c}{RR["d_b"]}-{c}{RR["liq"]}',NF_CR,'')
rrow('nd3','Net debt (all debt incl. gold & leases), Rs cr',lambda c,p:f'={c}{RR["d_3"]}-{c}{RR["liq"]}',NF_CR,'')
rrow('nde3','Net debt / equity (all debt)',lambda c,p:f'={c}{RR["nd3"]}/{FX("eq",c)}',NF_X,'')
rrow('dta','Debt (all) / total assets',lambda c,p:f'={c}{RR["d_3"]}/{FX("ta",c)}',NF_PCT,'')
rrow('gold_inv','Gold on loan / inventories (natural-hedge cover)',lambda c,p:f'={c}{RR["d_g"]}/{FX("inv",c)}',NF_PCT,'Share of inventory funded by metal loans; gold-price risk on that part is hedged')
rrow('st','Short-term share of borrowings',lambda c,p:f'=IFERROR({FX("b_c",c)}/{c}{RR["d_b"]},0)',NF_PCT,'Refinancing / rate-reset risk indicator (commercial paper)')
rsec('C. Interest coverage')
rrow('ebit','EBIT = profit before exceptional items & tax + finance costs, Rs cr',lambda c,p:f'={FX("pbt0",c)}+{FX("fin",c)}',NF_CR,'Includes other income (treasury income)')
rrow('opebit','Operating EBIT (ex other income), Rs cr',lambda c,p:f'={c}{RR["ebit"]}-{FX("oi",c)}',NF_CR,'Used for NOPAT / ROIC')
rrow('ebitda','EBITDA, Rs cr',lambda c,p:f'={c}{RR["ebit"]}+{FX("da",c)}',NF_CR,'')
rrow('cov1','Interest coverage = EBIT / finance costs  [brief proxy]',lambda c,p:f'={c}{RR["ebit"]}/{FX("fin",c)}',NF_X,'Brief: EBIT / interest expense (total finance costs incl. leases and gold on loan)',bold=True)
rrow('cov2','EBITDA / finance costs',lambda c,p:f'={c}{RR["ebitda"]}/{FX("fin",c)}',NF_X,'')
rrow('cov3','EBIT / (finance costs excl. gold-on-loan interest)',lambda c,p:f'={c}{RR["ebit"]}/({FX("fin",c)}-{FX("fin_g",c)})',NF_X,'Gold-loan interest is a pass-through of metal financing')
rrow('cov4','Operating EBIT / finance costs',lambda c,p:f'={c}{RR["opebit"]}/{FX("fin",c)}',NF_X,'Excludes treasury income')
rrow('fin_rev','Finance costs / revenue',lambda c,p:f'={FX("fin",c)}/{FX("rev",c)}',NF_PCT2,'')
rrow('fin_ebit','Finance costs / EBIT',lambda c,p:f'={FX("fin",c)}/{c}{RR["ebit"]}',NF_PCT,'Share of operating profit absorbed by financing')
rsec('D. Dividend policy, buy-backs and free cash flow')
rrow('eps','EPS (Rs)',lambda c,p:f'={FX("eps",c)}','0.00','')
rrow('dps','Dividend per share declared for the year (Rs)',lambda c,p:f'={FX("dps",c)}','0.00','')
rrow('payout','Dividend payout ratio = DPS / EPS',lambda c,p:f'={c}{RR["dps"]}/{c}{RR["eps"]}',NF_PCT,'Smoothed (Lintner): payout stays in a narrow 24-37% band while EPS swings -35% to +58%',bold=True)
rrow('dpsg','DPS growth y/y',lambda c,p:f'={c}{RR["dps"]}/{p}{RR["dps"]}-1',NF_PCTS,'',start=1)
rrow('epsg','EPS growth y/y',lambda c,p:f'={c}{RR["eps"]}/{p}{RR["eps"]}-1',NF_PCTS,'',start=1)
rrow('divpd','Dividends paid in the year (cash), Rs cr',lambda c,p:f'={FX("divpd",c)}',NF_CR,'Cash flow statement (FY19-20 include dividend distribution tax)')
rrow('cpay','Cash dividends / profit for the year',lambda c,p:f'={c}{RR["divpd"]}/{FX("pat",c)}',NF_PCT,'')
rrow('bb','Share buy-backs, Rs cr',lambda c,p:f'={FX("bb",c)}',NF_CR,'Titan has never bought back shares in the period (AR confirms)')
rrow('fcf','Free cash flow ex gold-loan movement = CFO - change in gold on loan - capex, Rs cr',lambda c,p:f'={FX("cfo",c)}-{FX("dgold",c)}-{FX("capex",c)}',NF_CR,'Gold-on-loan movements are classified as operating in Titan\'s cash flow; stripping them shows true cash generation')
rrow('fcfdiv','Dividend cover by FCF (x)',lambda c,p:f'=IFERROR({c}{RR["fcf"]}/{c}{RR["divpd"]},0)',NF_X,'Negative = dividends funded from borrowings / working-capital debt')
rsec('E. Liquidity')
rrow('liqta','Cash reserves / total assets',lambda c,p:f'={c}{RR["liq"]}/{FX("ta",c)}',NF_PCT,'')
rrow('liqd','Cash reserves in days of revenue',lambda c,p:f'={c}{RR["liq"]}/({FX("rev",c)}/365)',"0",'')
rrow('liqb','Cash reserves / borrowings (x)',lambda c,p:f'={c}{RR["liq"]}/{c}{RR["d_b"]}',NF_X,'>1x = borrowings fully covered by liquid assets')
rsec('F. Profitability and efficiency')
rrow('revg','Revenue growth y/y',lambda c,p:f'={FX("rev",c)}/{FX("rev",p)}-1',NF_PCTS,'',start=1)
rrow('opm','Operating EBIT margin',lambda c,p:f'={c}{RR["opebit"]}/{FX("rev",c)}',NF_PCT,'')
rrow('patm','PAT margin',lambda c,p:f'={FX("pat",c)}/{FX("rev",c)}',NF_PCT,'')
rrow('roe','ROE (PAT / average equity)',lambda c,p:f'={FX("pat",c)}/AVERAGE({FX("eq",p)},{FX("eq",c)})',NF_PCT,'',start=1)
rrow('at','Asset turnover (revenue / average total assets)',lambda c,p:f'={FX("rev",c)}/AVERAGE({FX("ta",p)},{FX("ta",c)})',NF_X,'',start=1)
rrow('em','Equity multiplier (average total assets / average equity)',lambda c,p:f'=AVERAGE({FX("ta",p)},{FX("ta",c)})/AVERAGE({FX("eq",p)},{FX("eq",c)})',NF_X,'DuPont: ROE = margin x turnover x multiplier',start=1)
RAT_END=r
widths(wra,{'A':64,'J':80});
for k in range(8): wra.column_dimensions[CL(2+k)].width=11
wra.freeze_panes='B5'
# charts on Ratios
def bar_from(ws,rows,cat_row,ttl,yt,colors,stacked=False,pct=False,w=18,h=8.5,anchor=None,c0=2,c1=9,title_col=1):
    ch=BarChart(); ch.type='col'; ch.grouping='stacked' if stacked else 'clustered'
    if stacked: ch.overlap=100
    else: ch.gapWidth=60
    for k,rw in enumerate(rows):
        s=Series(Reference(ws,min_col=c0,max_col=c1,min_row=rw),title_from_data=False,title=None)
        from openpyxl.chart.series import SeriesLabel
        from openpyxl.chart.data_source import StrRef
        s.tx=SeriesLabel(strRef=StrRef(f"'{ws.title}'!${CL(title_col)}${rw}"))
        s.graphicalProperties.solidFill=colors[k]; ch.series.append(s)
    ch.set_categories(Reference(ws,min_col=c0,max_col=c1,min_row=cat_row))
    style_chart(ch,ttl,None,yt,w=w,h=h)
    if pct: ch.y_axis.number_format='0%'
    if anchor: ws.add_chart(ch,anchor)
    return ch
def line_from(ws,rows,cat_row,ttl,yt,colors,pct=False,w=18,h=8.5,anchor=None,c0=2,c1=9,nf=None,title_col=1):
    ch=LineChart()
    for k,rw in enumerate(rows):
        s=Series(Reference(ws,min_col=c0,max_col=c1,min_row=rw),title=None)
        from openpyxl.chart.series import SeriesLabel
        from openpyxl.chart.data_source import StrRef
        s.tx=SeriesLabel(strRef=StrRef(f"'{ws.title}'!${CL(title_col)}${rw}"))
        s.graphicalProperties.line.solidFill=colors[k]; s.graphicalProperties.line.width=25400; s.marker=Marker(symbol='circle',size=6); s.marker.graphicalProperties=GraphicalProperties(solidFill=colors[k]); s.smooth=False
        ch.series.append(s)
    ch.set_categories(Reference(ws,min_col=c0,max_col=c1,min_row=cat_row))
    style_chart(ch,ttl,None,yt,w=w,h=h)
    if pct: ch.y_axis.number_format='0%'
    if nf: ch.y_axis.number_format=nf
    if anchor: ws.add_chart(ch,anchor)
    return ch
# helper rows for charts on Ratios (series labels in col A)
cr=RAT_END+2
sec(wra,cr,'Charts',1,10)
bar_from(wra,[RR['d_b'],RR['d_g'],RR['d_l']],4,'Debt composition (Rs crore)','Rs crore',[BLUE,ORANGE,GREY],stacked=True,anchor=f'A{cr+1}',w=17)
line_from(wra,[RR['de1'],RR['de2'],RR['de3']],4,'Debt-to-equity under three definitions (x)','x',[BLUE,ORANGE,GREY],anchor=f'F{cr+1}',w=17,nf='0.0"x"')
line_from(wra,[RR['cov1'],RR['cov4']],4,'Interest coverage (x): total vs operating EBIT','x',[BLUE,ORANGE],anchor=f'A{cr+19}',w=17,nf='0"x"')
line_from(wra,[RR['payout'],RR['gfa_ta']],4,'Payout ratio and gross fixed assets / total assets','%',[BLUE,ORANGE],pct=True,anchor=f'F{cr+19}',w=17)

# ======================================================= WACC & ROIC
ww2=sheet('WACC','548235')
title(ww2,'Task 2(c): cost of capital (WACC), ROIC and value creation by year','CAPM cost of equity; market-value weights at financial-year end; cost of debt = interest / average debt (selected debt definition on Inputs). FY20 beta uses 9 months of data (market data starts 1 Jul 2019).')
hdr(ww2,4,1,['Item']+F.FY+['Notes'],h=24)
WR={}; r=5
def wsec(txt):
    global r; sec(ww2,r,txt,1,10); r+=1
def wrow(key,lab,fn,nf,note='',start=1,bold=False,fnt_=None):
    global r
    WR[key]=r; put(ww2,f'A{r}',lab,F_B if bold else F_BASE)
    for k in range(8):
        c=CL(2+k); p=CL(1+k)
        if k<start: put(ww2,f'{c}{r}','n/a',F_SUB,al=AL_C); continue
        put(ww2,f'{c}{r}',fn(c,p,k),fnt_ or F_BASE if not bold else F_B,nf=nf,al=Alignment(horizontal='right'))
    put(ww2,f'J{r}',note,F_SUB); r+=1
def W_(k,c): return f'WACC!{c}{WR[k]}'
def IY(col,k): return f'Inputs!${col}${35+k}'     # FY table row
wsec('Market inputs')
wrow('px','Closing price at FY end (Rs)',lambda c,p,k:f'=INDEX(Data!$B${R0}:$B${R1},MATCH({IY("D",k)},Data!{DR},0))','#,##0.00','Last trading day on/before 31 March')
wrow('mcap','Market capitalisation (Rs cr) = price x shares',lambda c,p,k:f'={c}{WR["px"]}*{IN["sh"]}',NF_CR,'88.78 crore shares')
wrow('braw','Raw beta (daily regression within FY, excess returns)',lambda c,p,k:f'=SLOPE({rng("H",IY("E",k),IY("F",k))},{rng("I",IY("E",k),IY("F",k))})',NF_B,'FY20: Jul 2019-Mar 2020 only')
wrow('bse','Standard error of beta',lambda c,p,k:f'=STEYX({rng("H",IY("E",k),IY("F",k))},{rng("I",IY("E",k),IY("F",k))})/SQRT(DEVSQ({rng("I",IY("E",k),IY("F",k))}))',NF_B,'')
wrow('badj','Blume-adjusted beta',lambda c,p,k:f'={IN["blume"]}*{c}{WR["braw"]}+(1-{IN["blume"]})*1',NF_B,'')
wrow('bused','Beta used (per Inputs switch)',lambda c,p,k:f'=CHOOSE({IN["bch"]},{c}{WR["braw"]},{c}{WR["badj"]})',NF_B,'',bold=True)
wrow('rf','Risk-free: 10Y G-sec, March monthly average',lambda c,p,k:f'=INDEX(Inputs!$O${GS0}:$O${GS1},MATCH({IY("C",k)},Inputs!$N${GS0}:$N${GS1},1))',NF_PCT2,'Long-dated Rf matches the horizon of equity cash flows')
wrow('erp','Equity risk premium',lambda c,p,k:f'={IN["erp"]}',NF_PCT2,'Inputs')
wrow('ke','Cost of equity = Rf + beta x ERP',lambda c,p,k:f'={c}{WR["rf"]}+{c}{WR["bused"]}*{c}{WR["erp"]}',NF_PCT2,'',bold=True)
wsec('Debt and cost of debt (definition set on Inputs: gold-on-loan and leases switches)')
wrow('debt','Debt for WACC, year end (Rs cr)',lambda c,p,k:f'={X("d_b",c)}+{IN["fg"]}*{X("d_g",c)}+{IN["fl"]}*{X("d_l",c)}',NF_CR,'Borrowings + switches x (gold on loan, leases)',start=0)
wrow('debt_avg','Average debt (Rs cr)',lambda c,p,k:f'=AVERAGE({p}{WR["debt"]},{c}{WR["debt"]})',NF_CR,'')
wrow('int','Interest cost for the selected definition (Rs cr)',lambda c,p,k:f'={FX("fin_b",c)}+{FX("fin_o",c)}+{IN["fg"]}*{FX("fin_g",c)}+{IN["fl"]}*{FX("fin_l",c)}',NF_CR,'',start=0)
wrow('kd','Pre-tax cost of debt = interest / average debt',lambda c,p,k:f'={c}{WR["int"]}/{c}{WR["debt_avg"]}',NF_PCT2,'Effective (realised) cost of debt')
wrow('kdt','After-tax cost of debt = Kd x (1 - marginal tax)',lambda c,p,k:f'={c}{WR["kd"]}*(1-{IN["tax"]})',NF_PCT2,'')
wsec('Weights and WACC')
wrow('we','Equity weight E/(D+E), market value',lambda c,p,k:f'={c}{WR["mcap"]}/({c}{WR["mcap"]}+{c}{WR["debt"]})',NF_PCT,'')
wrow('wd','Debt weight D/(D+E)',lambda c,p,k:f'=1-{c}{WR["we"]}',NF_PCT,'Debt at book value as proxy for market value')
wrow('mde','Market D/E',lambda c,p,k:f'={c}{WR["debt"]}/{c}{WR["mcap"]}',NF_X,'')
wrow('wacc','WACC',lambda c,p,k:f'={c}{WR["we"]}*{c}{WR["ke"]}+{c}{WR["wd"]}*{c}{WR["kdt"]}',NF_PCT2,'',bold=True)
wsec('Return on invested capital and economic value added')
wrow('opebit','Operating EBIT (ex other income), Rs cr',lambda c,p,k:f'={X("opebit",c)}',NF_CR,'',start=0)
wrow('etr','Effective tax rate = tax / PBT',lambda c,p,k:f'={FX("tax",c)}/{FX("pbt",c)}',NF_PCT,'',start=0)
wrow('nopat','NOPAT = operating EBIT x (1 - effective tax)',lambda c,p,k:f'={c}{WR["opebit"]}*(1-{c}{WR["etr"]})',NF_CR,'',start=0)
wrow('ic','Invested capital, year end = equity + debt - cash reserves',lambda c,p,k:f'={FX("eq",c)}+{c}{WR["debt"]}-{X("liq",c)}',NF_CR,'Funding-side definition, consistent with the debt switches',start=0)
wrow('icavg','Average invested capital',lambda c,p,k:f'=AVERAGE({p}{WR["ic"]},{c}{WR["ic"]})',NF_CR,'')
wrow('roic','ROIC = NOPAT / average invested capital',lambda c,p,k:f'={c}{WR["nopat"]}/{c}{WR["icavg"]}',NF_PCT,'',bold=True)
wrow('spread','ROIC - WACC spread',lambda c,p,k:f'={c}{WR["roic"]}-{c}{WR["wacc"]}',"+0.0%;-0.0%;0.0%",'>0 = value creation',bold=True)
wrow('eva','EVA = spread x average invested capital (Rs cr)',lambda c,p,k:f'={c}{WR["spread"]}*{c}{WR["icavg"]}',NF_CR,'Economic profit after charging for all capital')
wrow('verdict','Verdict',lambda c,p,k:f'=IF({c}{WR["spread"]}>0,"Value created","Value destroyed")',None,'')
wrow('roe','ROE (PAT / average equity)',lambda c,p,k:f'={X("roe",c)}',NF_PCT,'')
wrow('roespr','ROE - cost of equity',lambda c,p,k:f'={c}{WR["roe"]}-{c}{WR["ke"]}',"+0.0%;-0.0%;0.0%",'')
wsec('Market valuation cross-check')
wrow('pe','P/E (price / EPS)',lambda c,p,k:f'={c}{WR["px"]}/{FX("eps",c)}','0.0"x"','')
wrow('pb','Price / book',lambda c,p,k:f'={c}{WR["mcap"]}/{FX("eq",c)}','0.0"x"','Premium to book reflects ROIC >> WACC')
wrow('ev','Enterprise value = market cap + debt - cash reserves (Rs cr)',lambda c,p,k:f'={c}{WR["mcap"]}+{c}{WR["debt"]}-{X("liq",c)}',NF_CR,'')
wrow('evebitda','EV / EBITDA',lambda c,p,k:f'={c}{WR["ev"]}/{X("ebitda",c)}','0.0"x"','')
# FY19 column: only book-based IC needed
for rk in ('debt','int','opebit','etr','nopat','ic'):
    pass
widths(ww2,{'A':60,'J':60});
for k in range(8): ww2.column_dimensions[CL(2+k)].width=11
ww2.freeze_panes='B5'
cw=r+1
sec(ww2,cw,'Charts',1,10)
line_from(ww2,[WR['roic'],WR['wacc']],4,'ROIC vs WACC','%',[BLUE,ORANGE],pct=True,anchor=f'A{cw+1}',w=17,c0=3)
bar_from(ww2,[WR['eva']],4,'Economic value added (Rs crore)','Rs crore',[BLUE],anchor=f'F{cw+1}',w=17,c0=3)
line_from(ww2,[WR['ke'],WR['kd'],WR['wacc']],4,'Cost of equity, cost of debt, WACC','%',[BLUE,GREY,ORANGE],pct=True,anchor=f'A{cw+19}',w=17,c0=3)
line_from(ww2,[WR['braw'],WR['badj']],4,'Annual beta: raw vs Blume-adjusted','beta',[BLUE,ORANGE],anchor=f'F{cw+19}',w=17,c0=3,nf='0.00')

# ======================================================= TSR & ALPHA
wt=sheet('TSR_Alpha','2A78D6')
title(wt,'Task 3 evidence: total shareholder return, Jensen\'s alpha and excess value created, by financial year','TSR = (end price + dividends paid in the period) / base price - 1. Dividends paid in a year = DPS declared for the previous year (record dates fall inside the year). Alpha: daily excess-return regression within each FY, annualised.')
hdr(wt,4,1,['Period','Base date','End date','Base price (Rs)','End price (Rs)','Dividend paid in period (Rs/share)','Price return','Dividend yield on base','Titan TSR','NIFTY 500 price return','Excess return (TSR - NIFTY)','Beta','Jensen alpha (ann.)','R-squared','Cost of equity (Ke)','Required return (Ke x period)','Excess return over Ke','Opening market cap (Rs cr)','Excess value created (Rs cr)','Verdict'],h=54)
for k in range(1,9):         # FY20..FY27YTD -> table rows 5..12
    r=4+k; ir=35+k; wc=CL(2+k) if k<8 else None   # WACC column (B=FY19) -> FY20 is col C
    put(wt,f'A{r}',FYL[k]+(' (partial: from 1 Jul 2019)' if k==1 else (' (to 4 Nov 2026)' if k==8 else '')),F_B)
    if k==1: put(wt,f'B{r}',f'=Data!$A${R0}',F_LINK,nf=NF_D,al=AL_C)
    else: put(wt,f'B{r}',f'=Inputs!D{ir-1}',F_LINK,nf=NF_D,al=AL_C)
    put(wt,f'C{r}',f'=Inputs!D{ir}',F_LINK,nf=NF_D,al=AL_C)
    put(wt,f'D{r}',f'=INDEX(Data!$B${R0}:$B${R1},MATCH(B{r},Data!{DR},0))',F_LINK,nf='#,##0.00'); put(wt,f'E{r}',f'=INDEX(Data!$B${R0}:$B${R1},MATCH(C{r},Data!{DR},0))',F_LINK,nf='#,##0.00')
    put(wt,f'F{r}',f'=Financials!{CL(1+k)}{FR["dps"]}',F_LINK,nf='0.00')    # DPS declared for previous FY paid this FY
    put(wt,f'G{r}',f'=E{r}/D{r}-1',nf=NF_PCTS); put(wt,f'H{r}',f'=F{r}/D{r}',nf=NF_PCT); put(wt,f'I{r}',f'=(E{r}+F{r})/D{r}-1',nf=NF_PCTS,bold=True)
    put(wt,f'J{r}',f'=INDEX(Data!$C${R0}:$C${R1},MATCH(C{r},Data!{DR},0))/INDEX(Data!$C${R0}:$C${R1},MATCH(B{r},Data!{DR},0))-1',nf=NF_PCTS)
    put(wt,f'K{r}',f'=I{r}-J{r}',nf='+0.0%;-0.0%;0.0%',bold=True)
    y=rng('H',IY('E',k),IY('F',k)); x=rng('I',IY('E',k),IY('F',k))
    put(wt,f'L{r}',f'=SLOPE({y},{x})',nf=NF_B); put(wt,f'M{r}',f'=INTERCEPT({y},{x})*{IN["td"]}',nf='+0.0%;-0.0%;0.0%',bold=True); put(wt,f'N{r}',f'=RSQ({y},{x})',nf='0.00')
    if k<8:
        put(wt,f'O{r}',f'=WACC!{CL(2+k)}{WR["ke"]}',F_LINK,nf=NF_PCT2)
        put(wt,f'P{r}',f'=O{r}' if k>1 else f'=O{r}*(C{r}-B{r})/365',nf=NF_PCT2)
    else:
        put(wt,f'O{r}',f'=WACC!I{WR["ke"]}',F_LINK,nf=NF_PCT2); put(wt,f'P{r}',f'=O{r}*(C{r}-B{r})/365',nf=NF_PCT2)
    put(wt,f'Q{r}',f'=I{r}-P{r}',nf='+0.0%;-0.0%;0.0%')
    mc_prev = f'WACC!{CL(1+k)}{WR["mcap"]}' if k>1 else f'INDEX(Data!$B${R0}:$B${R1},1)*{IN["sh"]}'
    put(wt,f'R{r}',f'={mc_prev}',F_LINK,nf=NF_CR); put(wt,f'S{r}',f'=Q{r}*R{r}',nf='#,##0;(#,##0);"-"',bold=True)
    put(wt,f'T{r}',f'=IF(Q{r}>0,"Value created","Value destroyed")',al=AL_C)
wt.conditional_formatting.add('T5:T12',FormulaRule(formula=['T5="Value created"'],fill=FILL_G)); wt.conditional_formatting.add('T5:T12',FormulaRule(formula=['T5="Value destroyed"'],fill=FILL_R))
sec(wt,14,'Cumulative performance',1,20)
hdr(wt,15,1,['Window','Start','End','Titan TSR (cumulative)','NIFTY 500 price return (cumulative)','Excess','Titan TSR (CAGR)','NIFTY 500 (CAGR)','Excess CAGR','Sum of excess value created (Rs cr)'],h=44)
put(wt,'A16','FY21-FY26 (Apr 2020 - Mar 2026): the brief period',F_B); put(wt,'B16','=B6',nf=NF_D,al=AL_C); put(wt,'C16','=C11',nf=NF_D,al=AL_C)
put(wt,'D16','=(1+I6)*(1+I7)*(1+I8)*(1+I9)*(1+I10)*(1+I11)-1',nf=NF_PCTS); put(wt,'E16','=(1+J6)*(1+J7)*(1+J8)*(1+J9)*(1+J10)*(1+J11)-1',nf=NF_PCTS)
put(wt,'A17','Full dataset (1 Jul 2019 - 4 Nov 2026)',F_B); put(wt,'B17','=B5',nf=NF_D,al=AL_C); put(wt,'C17','=C12',nf=NF_D,al=AL_C)
put(wt,'D17','=(1+I5)*(1+I6)*(1+I7)*(1+I8)*(1+I9)*(1+I10)*(1+I11)*(1+I12)-1',nf=NF_PCTS); put(wt,'E17','=(1+J5)*(1+J6)*(1+J7)*(1+J8)*(1+J9)*(1+J10)*(1+J11)*(1+J12)-1',nf=NF_PCTS)
for rr in (16,17):
    put(wt,f'F{rr}',f'=D{rr}-E{rr}',nf='+0.0%;-0.0%;0.0%',bold=True)
    put(wt,f'G{rr}',f'=(1+D{rr})^(365.25/(C{rr}-B{rr}))-1',nf=NF_PCT); put(wt,f'H{rr}',f'=(1+E{rr})^(365.25/(C{rr}-B{rr}))-1',nf=NF_PCT); put(wt,f'I{rr}',f'=G{rr}-H{rr}',nf='+0.0%;-0.0%;0.0%',bold=True)
put(wt,'J16','=SUM(S6:S11)',nf=NF_CR,bold=True); put(wt,'J17','=SUM(S6:S12)',nf=NF_CR,bold=True)
put(wt,'A19','Whole-period CAPM regression (daily, Jul 2019 - Nov 2026)',F_SEC)
yy=f'Data!$H$6:$H${R1}'; xx=f'Data!$I$6:$I${R1}'
for k,(l,f,nf) in enumerate([('Beta',f'=SLOPE({yy},{xx})',NF_B),('SE(beta)',f'=STEYX({yy},{xx})/SQRT(DEVSQ({xx}))',NF_B),('Jensen alpha (annualised)',f'=INTERCEPT({yy},{xx})*{IN["td"]}',NF_PCT),
        ('t-stat of alpha',f'=INTERCEPT({yy},{xx})/(STEYX({yy},{xx})*SQRT(1/COUNT({xx})+AVERAGE({xx})^2/DEVSQ({xx})))','0.00'),('R-squared',f'=RSQ({yy},{xx})','0.00'),('Observations',f'=COUNT({xx})','0')]):
    put(wt,f'A{20+k}',l); put(wt,f'B{20+k}',f,nf=nf,bold=True,al=AL_C)
put(wt,'D20','Reading: alpha > 0 with |t| > 2 would indicate genuine outperformance after adjusting for market risk; the FY rows show where it came from.',F_SUB)
cht=BarChart(); cht.type='col'; cht.gapWidth=60
cht.add_data(Reference(wt,min_col=9,min_row=4,max_row=12),titles_from_data=True); cht.add_data(Reference(wt,min_col=10,min_row=4,max_row=12),titles_from_data=True)
cht.set_categories(Reference(wt,min_col=1,min_row=5,max_row=12)); cht.series[0].graphicalProperties.solidFill=BLUE; cht.series[1].graphicalProperties.solidFill=GREY
style_chart(cht,'Titan TSR vs NIFTY 500 price return, by financial year',None,'Return',w=20,h=9); cht.y_axis.number_format='0%'; wt.add_chart(cht,'A28')
chv=BarChart(); chv.type='col'; chv.gapWidth=60
chv.add_data(Reference(wt,min_col=19,min_row=4,max_row=12),titles_from_data=True); chv.set_categories(Reference(wt,min_col=1,min_row=5,max_row=12)); chv.series[0].graphicalProperties.solidFill=ORANGE
chv.legend=None; style_chart(chv,'Excess value created over cost of equity (Rs crore)',None,'Rs crore',w=18,h=9); chv.legend=None; wt.add_chart(chv,'L28')
widths(wt,{'A':40,'B':12,'C':12,'D':12,'E':12,'F':14,'G':10,'H':11,'I':10,'J':12,'K':13,'L':8,'M':12,'N':9,'O':11,'P':12,'Q':12,'R':13,'S':14,'T':16})
wt.freeze_panes='B5'
