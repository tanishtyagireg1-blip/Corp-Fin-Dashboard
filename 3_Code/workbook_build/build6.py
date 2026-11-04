import json, os
# ======================================================= ROBUSTNESS
wro=sheet('Robustness','7F7F7F')
title(wro,'Robustness: does the beta-change conclusion survive different choices?','Window length, event buffer, risk-free proxy and data frequency are varied. Each cell re-runs the pre/post regressions with live formulas. n/a = window not available in the data.')
FULL='Data!$A$1:$V$%d'%R1
def rc(col,a,b): return f'INDEX({FULL},{a},{col}):INDEX({FULL},{b},{col})'
VAR=[('Base (6m, Rf per Inputs)',6,0,8,9),('3-month windows',3,0,8,9),('12-month windows',12,0,8,9),('Exclude +-5 days around event',6,5,8,9),('Exclude +-10 days around event',6,10,8,9),('Rf = 0 (raw returns)',6,0,4,5),('Rf = repo rate',6,0,19,20),('Rf = 10Y G-sec',6,0,21,22)]
NV=len(VAR); T0=30
hdr(wro,T0-1,1,['ID','Variant','Months','Buffer (days)','Y col','X col','Event row','Pre start','Pre end','Post start','Post end','Valid?','Beta pre','SE pre','Beta post','SE post','Change','t-stat','p-value','Sig.'],h=36)
for i in range(NS):
    ir=23+i
    for v,(lab,m,k,yc,xc) in enumerate(VAR):
        r=T0+i*NV+v
        put(wro,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(wro,f'B{r}',lab); put(wro,f'C{r}',m,F_IN,al=AL_C); put(wro,f'D{r}',k,F_IN,al=AL_C); put(wro,f'E{r}',yc,F_IN,al=AL_C); put(wro,f'F{r}',xc,F_IN,al=AL_C)
        put(wro,f'G{r}',f'=MATCH(Inputs!E{ir},Data!{DR},0)+4',al=AL_C)
        put(wro,f'H{r}',f'=IFERROR(MATCH(EDATE(Inputs!E{ir},-C{r})-1,Data!{DR},1)+5,0)',al=AL_C); put(wro,f'I{r}',f'=G{r}-1-D{r}',al=AL_C); put(wro,f'J{r}',f'=G{r}+D{r}',al=AL_C)
        put(wro,f'K{r}',f'=MATCH(MIN(EDATE(Inputs!E{ir},C{r})-1,MAX(Data!{DR})),Data!{DR},1)+4',al=AL_C)
        put(wro,f'L{r}',f'=AND(H{r}>=6,I{r}-H{r}+1>=40,K{r}-J{r}+1>=40,EDATE(Inputs!E{ir},C{r})-1<=MAX(Data!{DR}))',al=AL_C)
        yp,xp=rc(f'E{r}',f'H{r}',f'I{r}'),rc(f'F{r}',f'H{r}',f'I{r}'); yq,xq=rc(f'E{r}',f'J{r}',f'K{r}'),rc(f'F{r}',f'J{r}',f'K{r}')
        put(wro,f'M{r}',f'=IF(L{r},SLOPE({yp},{xp}),"n/a")',nf=NF_B); put(wro,f'N{r}',f'=IF(L{r},STEYX({yp},{xp})/SQRT(DEVSQ({xp})),"n/a")',nf=NF_B)
        put(wro,f'O{r}',f'=IF(L{r},SLOPE({yq},{xq}),"n/a")',nf=NF_B); put(wro,f'P{r}',f'=IF(L{r},STEYX({yq},{xq})/SQRT(DEVSQ({xq})),"n/a")',nf=NF_B)
        put(wro,f'Q{r}',f'=IF(L{r},O{r}-M{r},"n/a")',nf='+0.00;-0.00;0.00',bold=True); put(wro,f'R{r}',f'=IF(L{r},Q{r}/SQRT(N{r}^2+P{r}^2),"n/a")',nf='0.00')
        put(wro,f'S{r}',f'=IF(L{r},TDIST(ABS(R{r}),(I{r}-H{r}+1)+(K{r}-J{r}+1)-4,2),"n/a")',nf=NF_P)
        put(wro,f'T{r}',f'=IF(L{r},IF(S{r}<0.01,"***",IF(S{r}<0.05,"**",IF(S{r}<0.1,"*",""))),"")',al=AL_C)
TE=T0+NS*NV-1
# weekly block
WT=TE+3
sec(wro,WT-1,'Weekly-return betas (6-month calendar windows, Friday closes)',1,20)
hdr(wro,WT,1,['ID','Variant','','','','','','Pre start','Pre end','Post start','Post end','Valid?','Beta pre','SE pre','Beta post','SE post','Change','t-stat','p-value','Sig.'],h=30)
WFULL='Weekly!$A$1:$I$%d'%WR1; WD='Weekly!$A$%d:$A$%d'%(WR0,WR1)
def rw(col,a,b): return f'INDEX({WFULL},{a},{col}):INDEX({WFULL},{b},{col})'
for i in range(NS):
    r=WT+1+i; ir=23+i
    put(wro,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(wro,f'B{r}','Weekly, 6 months')
    put(wro,f'H{r}',f'=IFERROR(MATCH(EDATE(Inputs!E{ir},-{IN["win"]})-1,{WD},1)+5,0)',al=AL_C); put(wro,f'I{r}',f'=MATCH(Inputs!E{ir}-1,{WD},1)+4',al=AL_C)
    put(wro,f'J{r}',f'=I{r}+1',al=AL_C); put(wro,f'K{r}',f'=MATCH(MIN(EDATE(Inputs!E{ir},{IN["win"]})-1,MAX({WD})),{WD},1)+4',al=AL_C)
    put(wro,f'L{r}',f'=AND(H{r}>=6,I{r}-H{r}+1>=15,K{r}-J{r}+1>=15)',al=AL_C)
    yp,xp=rw(8,f'H{r}',f'I{r}'),rw(9,f'H{r}',f'I{r}'); yq,xq=rw(8,f'J{r}',f'K{r}'),rw(9,f'J{r}',f'K{r}')
    put(wro,f'M{r}',f'=IF(L{r},SLOPE({yp},{xp}),"n/a")',nf=NF_B); put(wro,f'N{r}',f'=IF(L{r},STEYX({yp},{xp})/SQRT(DEVSQ({xp})),"n/a")',nf=NF_B)
    put(wro,f'O{r}',f'=IF(L{r},SLOPE({yq},{xq}),"n/a")',nf=NF_B); put(wro,f'P{r}',f'=IF(L{r},STEYX({yq},{xq})/SQRT(DEVSQ({xq})),"n/a")',nf=NF_B)
    put(wro,f'Q{r}',f'=IF(L{r},O{r}-M{r},"n/a")',nf='+0.00;-0.00;0.00',bold=True); put(wro,f'R{r}',f'=IF(L{r},Q{r}/SQRT(N{r}^2+P{r}^2),"n/a")',nf='0.00')
    put(wro,f'S{r}',f'=IF(L{r},TDIST(ABS(R{r}),(I{r}-H{r}+1)+(K{r}-J{r}+1)-4,2),"n/a")',nf=NF_P)
    put(wro,f'T{r}',f'=IF(L{r},IF(S{r}<0.01,"***",IF(S{r}<0.05,"**",IF(S{r}<0.1,"*",""))),"")',al=AL_C)
# summary matrix at top
sec(wro,4,'Change in beta (post - pre) under each specification; green = significant at 10%',1,20)
hdr(wro,5,1,['ID','Shock']+[v[0] for v in VAR]+['Weekly (6m)','Specs valid','Same sign as base & p<0.10','Share of valid specs'],h=58)
for i in range(NS):
    r=6+i; put(wro,f'A{r}',f'=Inputs!A{23+i}',F_LINK,al=AL_C); put(wro,f'B{r}',f'=Inputs!B{23+i}',F_LINK)
    for v in range(NV): put(wro,f'{CL(3+v)}{r}',f'=Q{T0+i*NV+v}',nf='+0.00;-0.00;0.00',al=Alignment(horizontal='right'))
    put(wro,f'{CL(3+NV)}{r}',f'=Q{WT+1+i}',nf='+0.00;-0.00;0.00',al=Alignment(horizontal='right'))
    pc=[f'S{T0+i*NV+v}' for v in range(NV)]+[f'S{WT+1+i}']; qc=[f'Q{T0+i*NV+v}' for v in range(NV)]+[f'Q{WT+1+i}']
    put(wro,f'{CL(4+NV)}{r}','='+'+'.join(f'ISNUMBER({q})' for q in qc),al=AL_C)
    put(wro,f'{CL(5+NV)}{r}','='+'+'.join(f'IF(ISNUMBER({q}),IF(AND(SIGN({q})=SIGN($Q${T0+i*NV}),{p}<0.1),1,0),0)' for q,p in zip(qc,pc)),al=AL_C)
    put(wro,f'{CL(6+NV)}{r}',f'={CL(5+NV)}{r}/{CL(4+NV)}{r}',nf='0%',al=AL_C,bold=True)
    for v in range(NV+1):
        pr=T0+i*NV+v if v<NV else WT+1+i
        wro.conditional_formatting.add(f'{CL(3+v)}{r}',FormulaRule(formula=[f'AND(ISNUMBER(S{pr}),S{pr}<0.1)'],fill=FILL_G))
# ERP x beta grid and debt-definition table
G0=WT+12
sec(wro,G0,'FY26 WACC sensitivity to equity risk premium and beta',1,20)
put(wro,f'A{G0+1}','ERP (down) / beta (across)',F_B)
BETAS=[0.6,0.7,0.8,0.9,1.0,1.1,1.2]; ERPS=[0.045,0.05,0.055,0.06,0.065,0.07,0.075]
for j,b in enumerate(BETAS): put(wro,f'{CL(2+j)}{G0+1}',b,F_IN,nf='0.0',al=AL_C,fill=FILL_IN)
for k,e in enumerate(ERPS):
    q=G0+2+k; put(wro,f'A{q}',e,F_IN,nf='0.0%',al=AL_C,fill=FILL_IN)
    for j in range(len(BETAS)):
        c=CL(2+j); put(wro,f'{c}{q}',f'=WACC!$I${WR["we"]}*(WACC!$I${WR["rf"]}+{c}${G0+1}*$A{q})+WACC!$I${WR["wd"]}*WACC!$I${WR["kdt"]}',nf=NF_PCT2)
D0=G0+11
sec(wro,D0,'FY26 WACC under three debt definitions (independent of the Inputs switches)',1,20)
hdr(wro,D0+1,1,['Definition','Debt FY25','Debt FY26','Interest FY26','Pre-tax Kd','After-tax Kd','Equity weight','WACC'],h=30)
DEFS=[('D1: borrowings only','d_b',f'Financials!I{FR["fin_b"]}+Financials!I{FR["fin_o"]}'),('D2: + gold on loan','d_2',f'Financials!I{FR["fin_b"]}+Financials!I{FR["fin_o"]}+Financials!I{FR["fin_g"]}'),('D3: + leases','d_3',f'Financials!I{FR["fin"]}')]
for j,(lab,key,intf) in enumerate(DEFS):
    q=D0+2+j; put(wro,f'A{q}',lab)
    put(wro,f'B{q}',f'=Ratios!H{RR[key]}',F_LINK,nf=NF_CR); put(wro,f'C{q}',f'=Ratios!I{RR[key]}',F_LINK,nf=NF_CR); put(wro,f'D{q}',f'={intf}',F_LINK,nf=NF_CR)
    put(wro,f'E{q}',f'=D{q}/AVERAGE(B{q}:C{q})',nf=NF_PCT2); put(wro,f'F{q}',f'=E{q}*(1-{IN["tax"]})',nf=NF_PCT2)
    put(wro,f'G{q}',f'=WACC!$I${WR["mcap"]}/(WACC!$I${WR["mcap"]}+C{q})',nf=NF_PCT); put(wro,f'H{q}',f'=G{q}*WACC!$I${WR["ke"]}+(1-G{q})*F{q}',nf=NF_PCT2,bold=True)
put(wro,f'A{D0+6}','Take-away: WACC moves by well under 1 percentage point across all debt definitions because debt is under 10% of market-value capital; the beta and ERP assumptions matter far more than the debt definition.',F_SUB)
widths(wro,{'A':8,'B':34,'C':13,'D':13,'E':13,'F':13,'G':13,'H':13,'I':13,'J':13,'K':14,'L':14,'M':11,'N':11,'O':11,'P':11,'Q':11,'R':9,'S':10,'T':8})
wro.freeze_panes='C6'

# ======================================================= CHECKS
wk=sheet('Checks','00B050')
title(wk,'Model integrity and verification log','Every test returns PASS/FAIL. The Python rows are an independent re-computation (NumPy / statsmodels) pasted as values; the Excel rows are the live workbook.')
hdr(wk,4,1,['#','Check','Result / value','Tolerance','Status'],h=24)
CHK=[]
def chk(lab,val,tol,cond,nf=None):
    CHK.append((lab,val,tol,cond,nf))
chk('Trading days loaded',f'=COUNT(Data!B{R0}:B{R1})','=1823','=C{r}=1823','0')
chk('Largest daily Titan move (abs)',f'=MAX(MAX(Data!D6:D{R1}),-MIN(Data!D6:D{R1}))','< 25%','=C{r}<0.25','0.0%')
chk('Largest daily NIFTY 500 move (abs)',f'=MAX(MAX(Data!E6:E{R1}),-MIN(Data!E6:E{R1}))','< 15%','=C{r}<0.15','0.0%')
chk('Dates strictly increasing (count of violations)',f'=SUMPRODUCT(--(Data!A{R0+1}:A{R1}<=Data!A{R0}:A{R1-1}))','= 0','=C{r}=0','0')
chk('Balance sheet identity, all years (sum of abs differences)',f'=SUMPRODUCT(ABS(Financials!B{FR["chk_bs"]}:I{FR["chk_bs"]}))','< Rs 2 cr','=C{r}<2','0.0')
chk('Finance cost = sum of components',f'=SUMPRODUCT(ABS(Financials!B{FR["chk_fc"]}:I{FR["chk_fc"]}))','< Rs 2 cr','=C{r}<2','0.0')
chk('PAT = PBT - tax',f'=SUMPRODUCT(ABS(Financials!B{FR["chk_pat"]}:I{FR["chk_pat"]}))','< Rs 2 cr','=C{r}<2','0.0')
chk('PBT = PBT before exceptional - exceptional',f'=SUMPRODUCT(ABS(Financials!B{FR["chk_pbt"]}:I{FR["chk_pbt"]}))','< Rs 2 cr','=C{r}<2','0.0')
chk('Gold-on-loan: balance sheet change vs cash-flow (FY21-FY25, abs)',f'=SUMPRODUCT(ABS(Financials!C{FR["chk_gold"]}:G{FR["chk_gold"]}))','< Rs 5 cr','=C{r}<5','0')
chk('Dividends paid vs prior-year DPS x shares, FY22-FY26 (max abs % gap)','=MAX('+','.join(f'ABS(Financials!{CL(2+k)}{FR["divpd"]}/(Financials!{CL(1+k)}{FR["dps"]}*{IN["sh"]})-1)' for k in range(3,8))+')','< 6%','=C{r}<0.06','0.0%')
chk('EPS vs PAT / shares (max abs % gap, FY19-FY26)','=MAX('+','.join(f'ABS(Financials!{CL(2+k)}{FR["pat"]}/{IN["sh"]}/Financials!{CL(2+k)}{FR["eps"]}-1)' for k in range(8))+')','< 8%','=C{r}<0.08','0.0%')
chk('All 8 shock dates mapped to trading days','=COUNT(Inputs!E23:E30)','= 8','=C{r}=8','0')
chk('Smallest regression window (days)','=MIN(Shocks!H6:H21)','>= 100','=C{r}>=100','0')
chk('Whole-period price chain (FY returns compound to full-period return) - difference','=ABS('+'*'.join(f'(1+TSR_Alpha!G{k})' for k in range(5,13))+f'-1-(Data!B{R1}/Data!B{R0}-1))','< 0.01','=C{r}<0.01','0.0000')
chk('Rolling beta at last date = SLOPE over last window (difference)',f'=ABS(Data!J{R1}-SLOPE(INDEX(Data!H1:H{R1},{R1}-{IN["roll"]}+1):INDEX(Data!H1:H{R1},{R1}),INDEX(Data!I1:I{R1},{R1}-{IN["roll"]}+1):INDEX(Data!I1:I{R1},{R1})))','< 1e-9','=C{r}<0.000000001','0.0E+00')
chk('Robustness base variant equals Shocks sheet (max abs difference in beta change)','=MAX('+','.join(f'ABS(Robustness!Q{T0+i*NV}-Shocks!E{26+i})' for i in range(NS))+')','< 1e-9','=C{r}<0.000000001','0.0E+00')
chk('Event study: estimation windows end before the event window (min gap, days)','=SUMPRODUCT(MIN(EventStudy!C6:C13-EventStudy!E6:E13))','>= 11','=C{r}>=11','0')
r=5
for lab,val,tol,cond,nf in CHK:
    put(wk,f'A{r}',r-4,al=AL_C); put(wk,f'B{r}',lab); put(wk,f'C{r}',val,nf=nf,al=Alignment(horizontal='right')); put(wk,f'D{r}',tol,F_SUB,al=AL_C)
    put(wk,f'E{r}',f'=IF({cond[1:].format(r=r)},"PASS","FAIL")',al=AL_C,bold=True); r+=1
LAST=r-1
# Python cross-check
r+=1; sec(wk,r,'Independent re-computation of the featured regressions (Python: NumPy polyfit and statsmodels OLS on the same windows)',1,9); r+=1
hdr(wk,r,1,['ID','Excel beta pre','Python beta pre','Excel beta post','Python beta post','Max abs diff','Excel change in beta','Dummy-variable regression: interaction coefficient','Excel t (Welch)','Dummy-regression t (pooled variance)','Dummy-regression p','Status'],h=58); r+=1
PY=json.load(open('/home/claude/wai/pyvals.json')) if os.path.exists('/home/claude/wai/pyvals.json') else None
PY0=r
for i in range(NS):
    q=r+i; put(wk,f'A{q}',f'=Inputs!A{23+i}',F_LINK,al=AL_C)
    put(wk,f'B{q}',f'=Shocks!C{26+i}',F_LINK,nf='0.0000'); put(wk,f'D{q}',f'=Shocks!D{26+i}',F_LINK,nf='0.0000')
    if PY:
        put(wk,f'C{q}',PY[i]['pre'],F_IN,nf='0.0000'); put(wk,f'E{q}',PY[i]['post'],F_IN,nf='0.0000')
        put(wk,f'H{q}',PY[i]['dummy_d'],F_IN,nf='0.0000'); put(wk,f'J{q}',PY[i]['dummy_t'],F_IN,nf='0.00'); put(wk,f'K{q}',PY[i]['dummy_p'],F_IN,nf=NF_P)
    put(wk,f'F{q}',f'=MAX(ABS(B{q}-C{q}),ABS(D{q}-E{q}))',nf='0.0E+00'); put(wk,f'G{q}',f'=Shocks!E{26+i}',F_LINK,nf='+0.0000;-0.0000'); put(wk,f'I{q}',f'=Shocks!G{26+i}',F_LINK,nf='0.00')
    put(wk,f'L{q}',f'=IF(AND(F{q}<0.000001,ABS(G{q}-H{q})<0.000001),"PASS","FAIL")',al=AL_C,bold=True)
PY1=r+NS-1; r=PY1+2
put(wk,f'A{r}','The interaction coefficient from a pooled dummy-variable regression (y = a + b x + d D + g D x) equals the difference in the two separate betas exactly; only the standard error differs (pooled vs separate variance). Both t-statistics are reported; conclusions agree.',F_SUB)
r+=2
put(wk,f'B{r}','OVERALL MODEL STATUS',F_TITLE)
put(wk,f'C{r}',f'=IF(AND(COUNTIF(E5:E{LAST},"FAIL")=0,COUNTIF(L{PY0}:L{PY1},"FAIL")=0),"ALL CHECKS PASS","CHECK FAILURES")',F_TITLE,al=AL_C)
OVR=f'Checks!C{r}'
wk.conditional_formatting.add(f'E5:E{LAST}',FormulaRule(formula=['E5="PASS"'],fill=FILL_G)); wk.conditional_formatting.add(f'E5:E{LAST}',FormulaRule(formula=['E5="FAIL"'],fill=FILL_R))
wk.conditional_formatting.add(f'L{PY0}:L{PY1}',FormulaRule(formula=[f'L{PY0}="PASS"'],fill=FILL_G)); wk.conditional_formatting.add(f'L{PY0}:L{PY1}',FormulaRule(formula=[f'L{PY0}="FAIL"'],fill=FILL_R))
widths(wk,{'A':6,'B':72,'C':18,'D':16,'E':16,'F':12,'G':16,'H':20,'I':13,'J':18,'K':13,'L':10})

# ======================================================= SOURCES
wso=sheet('Sources','7F7F7F')
title(wso,'Sources, data provenance and references','Accessed 5 November 2026. All market data and statements were downloaded or extracted by the author; Claude was used for analysis support (see the AI Contribution Statement in the report).')
SRC=[('DATA','NSE India - Titan Company Ltd (TITAN) daily closing prices, 1 Jul 2019 - 4 Nov 2026','https://www.nseindia.com/'),
('DATA','NSE Indices - NIFTY 500 historical index values (price return), 1 Jul 2019 - 4 Nov 2026','https://www.niftyindices.com/reports/historical-data'),
('DATA','Titan Company Ltd - Annual Reports FY2019-20 to FY2025-26 (consolidated financial statements, notes, Board report, dividend policy)','https://www.titancompany.in/investors'),
('DATA','Reserve Bank of India - repo rate history and monetary policy statements (effective dates on Inputs)','https://www.rbi.org.in/'),
('DATA','FRED / OECD - Long-term government bond yields: 10-year, India (INDIRLTLT01STM), monthly','https://fred.stlouisfed.org/series/INDIRLTLT01STM'),
('THEORY','Sharpe, W. F. (1964). Capital asset prices: a theory of market equilibrium under conditions of risk. Journal of Finance, 19(3), 425-442.',''),
('THEORY','Jensen, M. C. (1968). The performance of mutual funds in the period 1945-1964. Journal of Finance, 23(2), 389-416.',''),
('THEORY','Blume, M. E. (1971). On the assessment of risk. Journal of Finance, 26(1), 1-10.',''),
('THEORY','Modigliani, F. and Miller, M. H. (1958). The cost of capital, corporation finance and the theory of investment. American Economic Review, 48(3), 261-297.',''),
('THEORY','Modigliani, F. and Miller, M. H. (1963). Corporate income taxes and the cost of capital: a correction. American Economic Review, 53(3), 433-443.',''),
('THEORY','Hamada, R. S. (1972). The effect of the firm\'s capital structure on the systematic risk of common stocks. Journal of Finance, 27(2), 435-452.',''),
('THEORY','Kraus, A. and Litzenberger, R. H. (1973). A state-preference model of optimal financial leverage. Journal of Finance, 28(4), 911-922.',''),
('THEORY','Myers, S. C. and Majluf, N. S. (1984). Corporate financing and investment decisions when firms have information that investors do not have. Journal of Financial Economics, 13(2), 187-221.',''),
('THEORY','Lintner, J. (1956). Distribution of incomes of corporations among dividends, retained earnings, and taxes. American Economic Review, 46(2), 97-113.',''),
('THEORY','Bhattacharya, S. (1979). Imperfect information, dividend policy, and the "bird in the hand" fallacy. Bell Journal of Economics, 10(1), 259-270.',''),
('THEORY','Brown, S. J. and Warner, J. B. (1985). Using daily stock returns: the case of event studies. Journal of Financial Economics, 14(1), 3-31.',''),
('THEORY','MacKinlay, A. C. (1997). Event studies in economics and finance. Journal of Economic Literature, 35(1), 13-39.',''),
('THEORY','Fama, E. F. and French, K. R. (2002). Testing trade-off and pecking order predictions about dividends and debt. Review of Financial Studies, 15(1), 1-33.',''),
('THEORY','Damodaran, A. Equity risk premiums (ERP): determinants, estimation and implications (annual update). NYU Stern.','https://pages.stern.nyu.edu/~adamodar/'),
('TOOLS','Python 3 (pandas, NumPy, statsmodels) for independent verification; openpyxl for workbook generation; LibreOffice for recalculation.','')]
hdr(wso,4,1,['Type','Reference','Link'],h=22)
for i,(a,b,c) in enumerate(SRC):
    q=5+i; put(wso,f'A{q}',a,F_B,al=AL_C); put(wso,f'B{q}',b,al=wrapal()); wso.row_dimensions[q].height=32 if len(b)>110 else 20
    if c: put(wso,f'C{q}',c,Font(name=FONT,color='0563C1',underline='single')); wso[f'C{q}'].hyperlink=c
q=5+len(SRC)+1
put(wso,f'A{q}','Limitations',F_SEC)
LIM=['NIFTY 500 file is a price-return index: Titan TSR includes dividends but the market comparison excludes them (understates the benchmark by roughly 1% a year).','Repo rate is the short risk-free proxy for beta regressions; 10Y G-sec and zero are switchable and tested in Robustness.','Equity risk premium (6.0%) is an assumption; the sensitivity grid is on Robustness.','FY20 is a 9-month window (data starts 1 Jul 2019); FY27 is year-to-date and has no audited accounts yet.','Overlapping shock windows (S1/S2, S4/S5, S5/S6) mean the pre/post betas are not independent across those pairs; flagged on Shocks column M.','Counterfactuals and scenarios are illustrative model outputs, not forecasts.','Titan Q1/Q2 FY27 results are not included.']
for j,t_ in enumerate(LIM): put(wso,f'B{q+1+j}',f'{j+1}. {t_}',al=wrapal()); wso.row_dimensions[q+1+j].height=30
widths(wso,{'A':10,'B':120,'C':50})
