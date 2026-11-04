# ======================================================= SUMMARY
ws=ws_sum
title(ws,'Titan Company Ltd - financial policy and systematic risk through the shocks of 2020-26','Corporate Finance WAI | Tanish Tyagi, M56D-26 | Data to 4 Nov 2026 | All figures are live formulas linked to the analysis sheets')
put(ws,'A3',f'="Model status: "&{OVR}',F_B)
def kpi(r,c,lab,f,nf):
    c2=CL(ord(c)-64+1)
    put(ws,f'{c}{r}',lab,F_SUB,al=wrapal('left','bottom')); ws.merge_cells(f'{c}{r}:{c2}{r}'); ws.row_dimensions[r].height=30
    put(ws,f'{c}{r+1}',f,fnt(bold=True,size=16,color=NAVY),nf=nf,al=Alignment(horizontal='left')); ws.merge_cells(f'{c}{r+1}:{c2}{r+1}')
sec(ws,5,'Headline numbers',1,12)
kpi(6,'A','Titan price return, Jul 2019 - Nov 2026',f'=Data!B{R1}/Data!B{R0}-1','0%'); kpi(6,'C','NIFTY 500 price return, same period',f'=Data!C{R1}/Data!C{R0}-1','0%')
kpi(6,'E','Titan beta, whole period','=TSR_Alpha!B20','0.00'); kpi(6,'G','Jensen alpha (annualised)','=TSR_Alpha!B22','0.0%'); kpi(6,'I','Excess value over cost of equity, FY21-26 (Rs cr)','=Verdict!H14','#,##0'); kpi(6,'K','Years with ROIC > WACC (FY21-26)','=Verdict!K16','@')
kpi(9,'A','D/E (all debt), FY26',f'=Ratios!I{RR["de3"]}','0.00"x"'); kpi(9,'C','Interest cover, FY26',f'=Ratios!I{RR["cov1"]}','0.0"x"'); kpi(9,'E','Gross fixed assets / total assets, FY26',f'=Ratios!I{RR["gfa_ta"]}','0.0%')
kpi(9,'G','Payout ratio, FY26',f'=Ratios!I{RR["payout"]}','0%'); kpi(9,'I','WACC, FY26',f'=WACC!I{WR["wacc"]}','0.0%'); kpi(9,'K','ROIC, FY26',f'=WACC!I{WR["roic"]}','0.0%')
sec(ws,12,'Key findings (text updates with the model)',1,12)
FIND=[
 '="1. Systematic risk is not constant. Beta rose after the COVID lockdown ("&TEXT(Shocks!C26,"0.00")&" to "&TEXT(Shocks!D26,"0.00")&", p = "&TEXT(Shocks!I26,"0.000")&") and after the Iran-war oil shock ("&TEXT(Shocks!C33,"0.00")&" to "&TEXT(Shocks!D33,"0.00")&", p = "&TEXT(Shocks!I33,"0.000")&"), but not significantly after the 2022 rate hikes ("&TEXT(Shocks!C30,"0.00")&" to "&TEXT(Shocks!D30,"0.00")&", p = "&TEXT(Shocks!I30,"0.00")&")."',
 '="2. The S8 result is the most robust: the beta rise is the same sign and significant at 10% in "&Robustness!M13&" of "&Robustness!L13&" specifications ("&TEXT(Robustness!N13,"0%")&")."',
 f'="3. Leverage rose sharply: D/E (all debt) went from "&TEXT(Ratios!E{RR["de3"]},"0.00")&"x in FY22 to "&TEXT(Ratios!I{RR["de3"]},"0.00")&"x in FY26 and interest cover fell from "&TEXT(Ratios!E{RR["cov1"]},"0.0")&"x to "&TEXT(Ratios!I{RR["cov1"]},"0.0")&"x, while gross fixed assets / total assets fell from "&TEXT(Ratios!E{RR["gfa_ta"]},"0%")&" to "&TEXT(Ratios!I{RR["gfa_ta"]},"0%")&" because inventory, not plant, absorbed the growth."',
 f'="4. Value: ROIC exceeded WACC in "&Verdict!K16&" years and the stock beat its CAPM-required return in "&Verdict!H15&" years; cumulative excess value over cost of equity FY21-26 was about Rs "&TEXT(Verdict!H14,"#,##0")&" cr, with large give-backs in FY23 and FY25."',
 f'="5. Dividends were smoothed (payout "&TEXT(MIN(Ratios!C{RR["payout"]}:I{RR["payout"]}),"0%")&"-"&TEXT(MAX(Ratios!C{RR["payout"]}:I{RR["payout"]}),"0%")&"), but FCF after dividends was negative in 3 of 6 years, so part of the payout was debt-funded; Titan has never bought back shares and at "&TEXT(WACC!I{WR["pb"]},"0")&"x book that was right."',
 f'="6. Looking ahead: under a repeat of 2022 (+250 bp, weak demand) the status-quo policy has minimum interest cover of "&TEXT(Scenarios!M12,"0.0")&"x ("&Scenarios!M15&" years in breach of the 5x guardrail) versus "&TEXT(Scenarios!N12,"0.0")&"x ("&Scenarios!N15&" years) under the recommended policy."']
for j,t_ in enumerate(FIND):
    put(ws,f'A{13+j}',t_,al=wrapal()); ws.merge_cells(f'A{13+j}:L{13+j}'); ws.row_dimensions[13+j].height=36
sec(ws,20,'Featured shocks at a glance',1,12)
hdr(ws,21,1,['ID','Shock','Beta pre','Beta post','Change','p-value','Verdict','CAR [-1,+1]','CAR p-value'],h=30)
for j,i in enumerate((0,4,7)):
    q=22+j; put(ws,f'A{q}',f'=Shocks!A{26+i}',F_LINK,al=AL_C); put(ws,f'B{q}',f'=Shocks!B{26+i}',F_LINK)
    put(ws,f'C{q}',f'=Shocks!C{26+i}',F_LINK,nf='0.00'); put(ws,f'D{q}',f'=Shocks!D{26+i}',F_LINK,nf='0.00'); put(ws,f'E{q}',f'=Shocks!E{26+i}',F_LINK,nf='+0.00;-0.00'); put(ws,f'F{q}',f'=Shocks!I{26+i}',F_LINK,nf='0.000')
    put(ws,f'G{q}',f'=Shocks!L{26+i}',F_LINK,al=AL_C); put(ws,f'H{q}',f'=EventStudy!J{6+i}',F_LINK,nf='+0.0%;-0.0%'); put(ws,f'I{q}',f'=EventStudy!L{6+i}',F_LINK,nf='0.000')
# charts
c1=LineChart()
for col,nm,colr in ((11,'Titan (indexed)',BLUE),(12,'NIFTY 500 (indexed)',GREY)):
    s=Series(Reference(wd,min_col=col,min_row=R0,max_row=R1),title=nm); s.smooth=False; s.marker.symbol='none'; s.graphicalProperties.line.solidFill=colr; s.graphicalProperties.line.width=19050; c1.series.append(s)
c1.set_categories(Reference(wd,min_col=1,min_row=R0,max_row=R1)); style_chart(c1,'Titan vs NIFTY 500 (1 Jul 2019 = 100)',None,'Index',w=17,h=8); c1.x_axis.number_format='mmm-yy'; c1.x_axis.tickLblSkip=250; c1.x_axis.tickMarkSkip=250
ws.add_chart(c1,'A27')
c2=BarChart(); c2.type='col'; c2.gapWidth=50; c2.add_data(Reference(wsx,min_col=5,min_row=25,max_row=33),titles_from_data=True); c2.set_categories(Reference(wsx,min_col=1,min_row=26,max_row=33))
c2.series[0].graphicalProperties.solidFill=BLUE; c2.series[0].invertIfNegative=False; c2.legend=None; style_chart(c2,'Change in beta after each shock (post - pre)',None,'Change in beta',w=15,h=8); c2.legend=None; c2.y_axis.number_format='0.0'
ws.add_chart(c2,'H27')
c3=LineChart()
for rw_,nm,colr in ((WR['roic'],'ROIC',BLUE),(WR['wacc'],'WACC',ORANGE)):
    s=Series(Reference(ww2,min_col=3,max_col=9,min_row=rw_),title=nm); s.smooth=False; s.graphicalProperties.line.solidFill=colr; s.graphicalProperties.line.width=25400; s.marker=Marker(symbol='circle',size=6); s.marker.graphicalProperties=GraphicalProperties(solidFill=colr); c3.series.append(s)
c3.set_categories(Reference(ww2,min_col=3,max_col=9,min_row=4)); style_chart(c3,'ROIC vs WACC',None,None,w=17,h=8); c3.y_axis.number_format='0%'; ws.add_chart(c3,'A45')
c4=BarChart(); c4.type='col'; c4.gapWidth=50
for rw_,nm,colr in ((9,'Titan TSR',BLUE),(10,'NIFTY 500',GREY)):
    c4.add_data(Reference(wt,min_col=rw_,min_row=4,max_row=12),titles_from_data=True); c4.series[-1].graphicalProperties.solidFill=colr; c4.series[-1].invertIfNegative=False
c4.set_categories(Reference(wt,min_col=1,min_row=5,max_row=12)); style_chart(c4,'Return by financial year',None,None,w=15,h=8); c4.y_axis.number_format='0%'; ws.add_chart(c4,'H45')
c5=LineChart()
for rw_,nm,colr,ax_ in ((RR['de3'],'D/E (all debt)',BLUE,0),):
    s=Series(Reference(wra,min_col=2,max_col=9,min_row=rw_),title=nm); s.smooth=False; s.graphicalProperties.line.solidFill=colr; s.graphicalProperties.line.width=25400; s.marker=Marker(symbol='circle',size=6); s.marker.graphicalProperties=GraphicalProperties(solidFill=colr); c5.series.append(s)
c5.set_categories(Reference(wra,min_col=2,max_col=9,min_row=4)); c5.legend=None; style_chart(c5,'Debt / equity, all debt (x)',None,None,w=17,h=8); c5.legend=None; c5.y_axis.number_format='0.0"x"'; ws.add_chart(c5,'A63')
c6=LineChart()
s=Series(Reference(wra,min_col=2,max_col=9,min_row=RR['cov1']),title='Interest cover'); s.smooth=False; s.graphicalProperties.line.solidFill=ORANGE; s.graphicalProperties.line.width=25400; s.marker=Marker(symbol='circle',size=6); s.marker.graphicalProperties=GraphicalProperties(solidFill=ORANGE); c6.series.append(s)
c6.set_categories(Reference(wra,min_col=2,max_col=9,min_row=4)); c6.legend=None; style_chart(c6,'Interest cover, EBIT / finance costs (x)',None,None,w=15,h=8); c6.legend=None; c6.y_axis.number_format='0"x"'; ws.add_chart(c6,'H63')
widths(ws,{c:13 for c in 'ABCDEFGHIJKL'}); ws.column_dimensions['B'].width=30
# ======================================================= README
wr_=ws_readme
title(wr_,'Titan Company Ltd - Corporate Finance WAI: analysis workbook','IIM Ranchi, Term II | Tanish Tyagi, roll no. M56D-26, Section D | Prepared 5 Nov 2026 | Companion to the 3-5 page report')
put(wr_,'A4','Question: how did eight shocks between 2020 and 2026 change Titan\'s systematic risk (CAPM beta), and how did its financial policy (investment, capital structure, payout, hedging) respond? Was value created or destroyed, and what should the CFO have done?',al=wrapal())
wr_.merge_cells('A4:F4'); wr_.row_dimensions[4].height=44
sec(wr_,6,'Contents (click to jump)',1,6)
hdr(wr_,7,1,['Sheet','What it does','Brief task'],h=22)
TOC=[('Summary','Headline numbers, key findings, six charts','All'),('Inputs','All assumptions and switches (blue/yellow), shock register, FY calendar, repo and G-sec tables','Task 1'),('Data','Daily prices and return engine (1,823 sessions)','Task 2a'),('Weekly','Weekly returns for robustness','Task 2a'),
('Shocks','CAPM regressions 6 months pre/post each shock, SE, t, p, R2, CI; test of beta change','Task 2b'),('PriceTrend','Indexed price chart with shock markers; calendar-year returns','Task 2a'),('Rolling','126-day rolling beta with shock markers','Task 2b'),('Beta_Charts','Beta before/after with 95% CI; change-in-beta chart','Task 2b'),
('EventStudy','Market-model abnormal returns and CARs around each shock','Task 2a/2b'),('Returns','Firm vs market returns before and after each shock','Task 2a'),('Financials','Consolidated statements FY19-FY26 (typed from annual reports) with integrity checks','Task 2c'),
('Ratios','Capex proxy, D/E (3 definitions), coverage (4 variants), payout, buy-backs, cash, FCF, DuPont','Task 2c'),('WACC','Annual beta, cost of equity, cost of debt, weights, WACC, ROIC, EVA, valuation','Task 2c / 3'),('TSR_Alpha','TSR vs NIFTY, Jensen alpha, excess return over Ke, value created in Rs cr','Task 3'),
('Policy','Before/during/after policy scorecard for the featured shocks, with live diagnosis','Task 2c / 3'),('Verdict','Value created or destroyed by year: market view and ROIC-WACC view','Task 3'),('Counterfactual','Leverage and WACC curve, rate shock, payout funding, capex test, CFO action table','Task 4'),
('Scenarios','FY27-FY31 four-case model (status quo vs recommended; base vs stress)','Task 4'),('Robustness','Window, buffer, Rf proxy, weekly data, ERP and debt-definition sensitivities','Task 2b'),('Checks','Integrity tests and independent Python verification','Quality'),('Sources','References, data provenance, limitations','Task 5')]
for j,(a,b,c_) in enumerate(TOC):
    q=8+j; put(wr_,f'A{q}',a,Font(name=FONT,color='0563C1',underline='single')); wr_[f'A{q}'].hyperlink=f"#'{a}'!A1"; put(wr_,f'B{q}',b,al=wrapal()); put(wr_,f'C{q}',c_,al=AL_C)
q=8+len(TOC)+1
sec(wr_,q,'Colour code',1,6)
put(wr_,f'A{q+1}','Blue text',F_IN); put(wr_,f'B{q+1}','Typed input or source data (prices, financial statements, rates)')
put(wr_,f'A{q+2}','Black text',F_BASE); put(wr_,f'B{q+2}','Formula')
put(wr_,f'A{q+3}','Green text',F_LINK); put(wr_,f'B{q+3}','Link to another sheet')
put(wr_,f'A{q+4}','Yellow fill',F_B,fill=FILL_IN); put(wr_,f'B{q+4}','Key assumption you can change (Inputs, Scenarios, Counterfactual)')
sec(wr_,q+6,'Switches on Inputs (everything recalculates)',1,6)
for j,t_ in enumerate(['B5 risk-free proxy for betas: 1 = repo, 2 = 10Y G-sec, 3 = zero','B6 window length in months (default 6)','B9 equity risk premium; B10 raw vs Blume-adjusted beta','B11 and B12 include gold-on-loan and lease liabilities in WACC debt','Shock dates (D23:D30) and featured flags (F23:F30) can be edited']):
    put(wr_,f'B{q+7+j}',t_)
sec(wr_,q+13,'Method notes',1,6)
for j,t_ in enumerate(['Beta: daily simple returns, excess over the risk-free rate; slope of Titan excess on NIFTY 500 excess; windows are exact row ranges; the event-day return sits in the post window.','Test of beta change: difference of the two betas divided by sqrt(SE_pre^2 + SE_post^2), t-distribution with n_pre + n_post - 4 d.f.; cross-checked by a pooled dummy-variable regression in Python (Checks).','Event study: market model estimated on 120 days ending 11 days before the event; CARs over [-1,+1], [0,+5], [-10,+10].','Capex proxy per the brief: gross fixed assets (gross PP&E + CWIP) / total assets; interest coverage = EBIT / finance costs.','Debt is shown three ways (borrowings; + gold on loan; + leases) because Titan funds inventory with gold-on-loan and Ind AS 116 leases.','Excess value created = (TSR - cost of equity) x opening market capitalisation.']):
    put(wr_,f'B{q+14+j}',f'{j+1}. {t_}',al=wrapal()); wr_.merge_cells(f'B{q+14+j}:F{q+14+j}'); wr_.row_dimensions[q+14+j].height=32
widths(wr_,{'A':22,'B':84,'C':14,'D':12,'E':12,'F':12})
# ---------- global polish
for w_ in wb.worksheets:
    w_.sheet_view.zoomScale=90
wb.active=1
