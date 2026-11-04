import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import CondPageBreak, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
D=json.load(open('data.json'))
NAVY=colors.HexColor('#1F3864'); BLUE=colors.HexColor('#2A78D6'); GREY=colors.HexColor('#5f6670'); LG=colors.HexColor('#F2F4F7'); MG=colors.HexColor('#D9DEE5')
body=ParagraphStyle('b',fontName='Helvetica',fontSize=9.7,leading=12.6,alignment=TA_JUSTIFY,spaceAfter=4.5)
h1=ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=12.6,leading=15.5,textColor=NAVY,spaceBefore=9,spaceAfter=4,keepWithNext=1)
h2=ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=10.4,leading=12.8,textColor=NAVY,spaceBefore=5,spaceAfter=2.5,keepWithNext=1)
cap=ParagraphStyle('c',fontName='Helvetica-Oblique',fontSize=8,leading=9.7,textColor=GREY,spaceAfter=6)
tt=ParagraphStyle('t',fontName='Helvetica',fontSize=8,leading=9.7)
tth=ParagraphStyle('th',fontName='Helvetica-Bold',fontSize=8,leading=9.7,textColor=colors.white)
ttl=ParagraphStyle('tl',fontName='Helvetica',fontSize=8,leading=9.7,alignment=TA_LEFT)
title=ParagraphStyle('ti',fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=NAVY,spaceAfter=3)
sub=ParagraphStyle('s',fontName='Helvetica',fontSize=9.2,leading=11.6,textColor=GREY,spaceAfter=7)
bul=ParagraphStyle('bu',parent=body,leftIndent=11,bulletIndent=0,spaceAfter=2.6)
def P(t,s=body): return Paragraph(t,s)
def B(t): return Paragraph(t,bul,bulletText='•')
def tbl(rows,cw,hdr=1,fs=None,zebra=True,align_first_left=True):
    data=[[Paragraph(str(c),tth if i<hdr else (ttl if j==0 or (isinstance(c,str) and len(c)>14) else tt)) for j,c in enumerate(r)] for i,r in enumerate(rows)]
    t=Table(data,colWidths=cw,repeatRows=hdr)
    st=[('BACKGROUND',(0,0),(-1,hdr-1),NAVY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),2.2),('BOTTOMPADDING',(0,0),(-1,-1),2.2),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('LINEBELOW',(0,hdr),(-1,-1),0.25,MG)]
    if zebra:
        for i in range(hdr,len(rows)):
            if (i-hdr)%2==1: st.append(('BACKGROUND',(0,i),(-1,i),LG))
    t.setStyle(TableStyle(st)); return t
def pc(x,d=1): return f'{x*100:.{d}f}%'
def rowv(k,key,fmt,cols=range(2,9)):
    for r in D[k]:
        if r[0] and str(r[0]).startswith(key): return [fmt(r[c]) for c in cols]
S=D['shocks']; REG={s[0]:s for s in D['shock_reg']}; ES={e[0]:e for e in D['es'][1:]}; ROB={r[0]:r for r in D['rob'][1:9]}
def footer(c,doc):
    c.saveState(); c.setFont('Helvetica',7); c.setFillColor(GREY)
    c.drawString(1.9*cm,1.0*cm,'Corporate Finance WAI | Titan Company Ltd | Tanish Tyagi, M56D-26, Section D | IIM Ranchi, Term II')
    c.drawRightString(A4[0]-1.9*cm,1.0*cm,f'Page {doc.page}'); c.restoreState()
doc=SimpleDocTemplate('Titan_WAI_Report.pdf',pagesize=A4,leftMargin=1.9*cm,rightMargin=1.9*cm,topMargin=1.7*cm,bottomMargin=1.8*cm,title='Titan Company Ltd: shocks, systematic risk and financial policy, 2020-26',author='Tanish Tyagi')
W=A4[0]-3.8*cm
st=[]
st.append(P('How Did Shocks Reshape Titan\'s Risk and Financial Policy? A CAPM and Financial-Policy Study, 2020–26',title))
st.append(P('Corporate Finance, Working with AI (individual project) | Tanish Tyagi, roll no. M56D-26, Section D, IIM Ranchi | Submission: 12 Nov 2026 | Annexure: analysis workbook, dashboard, code and data (zip)',sub))
# ---------------- 1
st.append(P('1. Problem Statement',h1))
st.append(P('Titan Company Ltd (NSE: TITAN) is India\'s largest branded jeweller. Its consolidated revenue grew from Rs 21,052 cr (FY20) to Rs 87,584 cr (FY26), and its balance sheet is dominated by gold inventory (Rs 42,743 cr, 178 days of sales in FY26), financed partly by gold-on-loan from banks. That makes Titan unusually exposed to demand shocks, the cost of capital and commodity prices, so it is a good test of two questions that the course raises: <b>(i)</b> does a firm\'s systematic risk (CAPM beta) stay constant through shocks, and <b>(ii)</b> how do investment, leverage, payout and hedging policy respond? The study then asks <b>(iii)</b> whether value was created or destroyed in 2020–26, and <b>(iv)</b> what the CFO should have done and should do over the next five years.'))
st.append(P('<b>Shock selection (Task 1).</b> Eight dated shocks between 2020 and 2026 were screened on three criteria: the event is exogenous and datable; it has a clear transmission channel to Titan; and there are at least six clean months of data on each side. All eight are tested, but three are <b>featured</b> because each works through a different channel: <b>S1</b> the COVID-19 lockdown (demand and liquidity: stores shut, jewellery is discretionary), <b>S5</b> the RBI rate-hike cycle (cost of capital: the repo rate went from 4.00% to 6.50%) and <b>S8</b> the US/Israel–Iran war and oil shock (commodity and geopolitical risk, the channel that matters most for a gold-inventory business and the most recent). The other five provide a robustness panel and expose overlapping windows (S1/S2, S4/S5, S5/S6 share months, flagged in the workbook).'))
chan={'S1':'Demand / liquidity','S2':'Monetary and fiscal relief','S3':'Demand (regional lockdowns)','S4':'Commodity / geopolitical','S5':'Cost of capital','S6':'Governance / market sentiment','S7':'Trade and tariffs','S8':'Commodity / geopolitical'}
rows=[['ID','Shock','Event date','Channel to Titan','Role']]
import datetime as dt
for s in D['shock_reg']:
    d=dt.datetime.strptime(s[3],'%Y-%m-%d').strftime('%d %b %Y')
    rows.append([s[0],s[1],d,chan[s[0]],'Featured' if s[5]==1 else 'Robustness'])
st.append(tbl(rows,[1.0*cm,6.5*cm,2.5*cm,5.0*cm,2.2*cm]))
st.append(P('Table 1. Shock register. The event day is the first trading session on or after the announcement.',cap))
st.append(P('1.1 Research questions and hypotheses',h2))
st.append(B('<b>H1 (risk).</b> Beta rises after shocks that raise uncertainty about demand or the cost of capital. CAPM beta is the covariance of the firm\'s returns with the market, so a firm with discretionary demand and large working-capital needs should become more market-sensitive in a downturn. <i>Test:</i> Task 2b regressions, with a formal test of the change and eight robustness variants.'))
st.append(B('<b>H2 (policy).</b> A liquidity shock leads to a precautionary response (investment cut, cash hoarded); a rate shock leads to a shift in debt maturity and in the use of leverage. Trade-off theory predicts leverage moves towards a target; the pecking order predicts debt before equity. <i>Test:</i> Task 2c ratios, with debt measured three ways because gold-on-loan and leases are a large part of Titan\'s funding.'))
st.append(B('<b>H3 (value).</b> Value is created only when the return earned exceeds the return required: total shareholder return above the CAPM cost of equity (market view) and ROIC above WACC (fundamental view). <i>Test:</i> Task 3, year by year, with theory used to explain the gaps.'))
st.append(B('<b>H4 (decision).</b> The right policy for the next five years is the one that keeps interest cover above a floor <i>under stress</i>, not only in the base case. <i>Test:</i> Task 4, a four-case model with a pre-set 5x cover floor and a 2.0x D/E ceiling.'))
st.append(P('Titan suits the question because the three featured shocks hit three different parts of its model: store footfall (S1), the cost of the debt that carries its inventory (S5), and the price of gold and oil-linked risk appetite (S8). The annexure holds the workbook (Excel, live formulas), an interactive dashboard, the code and the data, so every number below can be traced to a cell.'))
# ---------------- 2
st.append(P('2. Proposed Solution',h1))
st.append(P('The solution is a fully traceable analysis workbook (live Excel formulas, no pasted results) plus an independent Python check. <b>Data:</b> daily closes for Titan and the NIFTY 500 price index, 1 Jul 2019 to 4 Nov 2026 (1,823 sessions); consolidated financial statements FY19–FY26 from the annual reports; RBI repo history and the India 10-year G-sec yield. <b>Method:</b>'))
st.append(tbl([['Input','Source','Coverage and treatment'],
 ['Titan daily close','NSE India','1 Jul 2019 to 4 Nov 2026; 1,823 sessions; simple daily returns'],
 ['NIFTY 500 index','NSE Indices','Same dates; price-return index, so dividends are excluded (market return understated by about 1% a year)'],
 ['Repo rate','Reserve Bank of India','Policy-rate history as a daily step series; used as the risk-free rate (daily = annual rate / 252 trading days)'],
 ['10-year G-sec yield','FRED / OECD','Monthly; the March value is used as the risk-free rate in annual WACC and cost of equity'],
 ['Financial statements','Titan annual reports FY2019-20 to FY2025-26','Consolidated; balance sheet, P&amp;L, cash flow and notes (gold on loan, leases, dividends)']],[3.2*cm,4.2*cm,9.8*cm]))
st.append(P('Table 2. Data inputs. All raw files and the derived tables are in the annexure.',cap))
st.append(P('<b>Design choices.</b> Six-month windows (about 125 trading days each side) are long enough to detect a change in beta of roughly 0.3 to 0.4 at the 5% level and short enough to avoid mixing regimes; three- and twelve-month windows are tested as alternatives. Daily data are used for power, and weekly data as a check for non-synchronous trading. The repo rate is used as the risk-free rate because it is the overnight policy rate that investors can actually earn, with zero and the 10-year yield as alternatives. The NIFTY 500 is the broad market proxy; Titan is one of its constituents, which slightly biases beta towards 1, and this is noted as a limitation. In WACC, beta is Blume-adjusted (2/3 raw + 1/3 of 1), the equity risk premium is 6%, and debt weights use market capitalisation. The risk premium is an assumption, and a beta-by-premium sensitivity grid is in the workbook.'))
st.append(B('<b>Beta.</b> For each shock, the regression (R<sub>Titan</sub> − R<sub>f</sub>) = α + β (R<sub>NIFTY500</sub> − R<sub>f</sub>) + ε on daily returns for the six months before and six months after, with the event day in the post window. A change in beta is tested with t = (beta<sub>post</sub> − beta<sub>pre</sub>) / sqrt(SE<sub>pre</sub><sup>2</sup> + SE<sub>post</sub><sup>2</sup>), d.f. = n<sub>pre</sub> + n<sub>post</sub> − 4. Risk-free = repo rate (switchable).'))
st.append(B('<b>Event study.</b> A market model on 120 days ending 11 days before the event gives abnormal returns and cumulative abnormal returns (CAR) over [−1,+1].'))
st.append(B('<b>Financial policy (Task 2c).</b> Capex proxy = gross fixed assets / total assets; D/E and interest cover (EBIT / finance costs); dividend payout and buy-backs; cash reserves. Because Titan funds inventory with gold-on-loan and carries Ind AS 116 leases, debt is shown three ways (borrowings; plus gold on loan; plus leases).'))
st.append(B('<b>Value.</b> Annual WACC (Blume-adjusted annual beta, 10-year G-sec, 6% equity risk premium, market-value weights), ROIC and EVA; total shareholder return (TSR) against the CAPM-required return; Jensen\'s alpha.'))
st.append(B('<b>Decision tools.</b> A WACC-versus-leverage curve with an interest-cover constraint, an interest-rate stress test, and a four-case FY27–FY31 model. <b>Checks:</b> 17 integrity tests pass; Excel betas match NumPy/statsmodels to six decimals; eight alternative specifications test robustness.'))
# ---------------- 3
st.append(CondPageBreak(7*cm)); st.append(P('3. Implementation and Results',h1))
st.append(P('3.1 Price trend and returns around the shocks',h2))
st.append(P('Over the full period Titan returned +259% against +134% for the NIFTY 500 (price), with a whole-period beta of 0.93 (SE 0.03, R² 0.33) and Jensen\'s alpha of 8.9% a year (t = 1.04, so not significant on its own). The outperformance is lumpy: Titan beat the market by 42pp in FY22 and 33pp in FY26, but trailed it by 9pp in FY21 and 25pp in FY25. Around the featured shocks Titan fell slightly more than the market before S1 (−36.9% vs −32.8%) and recovered slightly less after it (+34.3% vs +40.5%); around S5 it returned −1.3% before and +15.8% after (market −3.6% and +5.1%); and around S8 it outperformed in both windows (+19.6% and +16.7% vs +2.0% and +0.7%). The event study shows significant negative abnormal returns at the rate-hike (S5: CAR[−1,+1] = −5.7%, p = 0.018) and the second COVID wave (S3: −5.4%, p = 0.036) but not at S1 or S8.'))
st.append(KeepTogether([Image('fig1.png',width=W,height=W*2.7/7.2),P('Figure 1. Titan vs NIFTY 500, indexed. Orange lines mark the featured shocks (S1, S5, S8); grey dashed lines mark the other five.',cap)]))
st.append(P('3.2 Did systematic risk change? (Task 2b)',h2))
rows=[['Shock','Beta pre','Beta post','Change','95% CI of change','p-value','Result','Robust specs*','CAR [-1,+1] (p)']]
for s in S:
    sid=s[0]; r=ROB[sid]; e=ES[sid]
    sig=s[11].replace(' level','')
    rows.append([sid+' '+('(featured)' if s[13]==1 else ''),f'{s[2]:.2f}',f'{s[3]:.2f}',f'{s[4]:+.2f}',f'{s[9]:+.2f} to {s[10]:+.2f}',f'{s[8]:.3f}',sig,f'{int(r[12])} of {int(r[11])}',f'{e[9]*100:+.1f}% ({e[11]:.2f})'])
st.append(tbl(rows,[2.5*cm,1.3*cm,1.4*cm,1.3*cm,2.8*cm,1.4*cm,2.1*cm,2.0*cm,2.4*cm]))
st.append(P('Table 3. CAPM beta six months before vs after each shock (daily excess returns, repo as risk-free). *Number of the valid specifications (3/12-month windows, ±5/±10-day buffers, three risk-free choices, weekly data) in which the change has the same sign and p &lt; 0.10.',cap))
T2=Table([[[Image('fig2.png',width=W*0.45,height=W*0.45*2.7/3.55),P('Figure 2. Bars show beta; whiskers are 95% confidence intervals; * p &lt; 0.10, ** p &lt; 0.01 for the change.',cap)],P('Beta is not constant. After <b>S8</b> it rose from 0.62 to 1.13 (change +0.51, p = 0.005) and the result holds in all eight valid specifications, making it the most robust finding. After <b>S1</b> it rose from 0.84 to 1.09 (p = 0.064; seven of eight specifications). After <b>S5</b> it rose only from 1.06 to 1.19 (p = 0.41) and the sign flips across specifications, so the rate hike changed Titan\'s <i>price</i> (negative CAR) more than its <i>risk</i>. S3 also shows a rise (+0.46, p = 0.07) but reverses on three-month windows, so it is treated as fragile. Rolling 126-day beta averaged 0.87 (range 0.39–1.45; above 1 on 29% of days), and annual betas were 0.90, 1.06, 1.12, 1.03, 0.77, 0.62, 0.75 for FY20–FY26. Financial leverage explains little of this: debt is only 4–9% of market-value capital, so re-levering Titan\'s FY26 beta changes the unlevered value from 0.83 to 0.78 only. The shifts are business and macro risk, not balance-sheet risk.')]],colWidths=[W*0.47,W*0.53])
T2.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)]))
st.append(T2)
st.append(KeepTogether([Image('fig5.png',width=W,height=W*2.4/7.2),P('Figure 3. Rolling 126-day beta against the NIFTY 500. Beta climbs through 2020-21, falls to 0.6-0.7 in 2023-25, and jumps after S8. Shock lines as in Figure 1.',cap)]))
import json as _j
DD=_j.load(open('/home/claude/dash/data.js'))
READ={'S1':'Marginal rise. Titan fell about as much as the market, then recovered a little less; the CAR is not significant because the lockdown was announced after the crash had started.','S2':'No change. The stimulus and repo cut calmed the whole market, so Titan and the index moved together as before.','S3':'Beta rises but reverses on three-month windows, so it is fragile. The negative CAR is significant: regional lockdowns closed stores in a key selling period.','S4':'No change. A global commodity shock, but gold-on-loan hedges the price risk on much of Titan\'s stock and the market fell with it.','S5':'Price effect, not risk effect. CAR is significantly negative, but beta rises only 0.13 and the sign flips across specifications.','S6':'No change. A governance shock to another group; no Titan-specific transmission channel, so beta did not move.','S7':'No change (beta falls). Tariffs and the H-1B fee mainly affect exporters; Titan sells overwhelmingly in India.','S8':'Largest and most robust rise: all eight valid specifications agree. Beta moves from below 1 to about 1, with no significant CAR: the reaction came through higher volatility (annualised 18% before, 28% after), not a one-off drop.'}
rows=[['Shock','Beta pre to post (p)','Titan vs NIFTY 500, before | after','CAR [-1,+1] (p)','Reading']]
for x in DD['shocks']:
    rows.append([x['id']+(' *' if x['feat'] else ''),f"{x['pre']:.2f} to {x['post']:.2f} ({x['p']:.2f})",f"{x['titanPre']*100:+.0f}% vs {x['niftyPre']*100:+.0f}% | {x['titanPost']*100:+.0f}% vs {x['niftyPost']*100:+.0f}%",f"{x['car']*100:+.1f}% ({x['carP']:.2f})",READ[x['id']]])
st.append(tbl(rows,[1.1*cm,2.6*cm,3.5*cm,2.0*cm,8.0*cm]))
st.append(P('Table 4. Shock-by-shock reading (* = featured). Returns are cumulative price returns over the six months before and after the event date.',cap))
st.append(P('The pattern is informative. Shocks that were <i>demand or commodity-risk</i> events specific to a discretionary, gold-heavy business (S1, S3, S8) moved beta up; shocks that were market-wide or about other firms or sectors (S2, S4, S6, S7) did not. The rate cycle (S5) is the exception: it hurt the price immediately but changed risk only modestly. That fits CAPM: beta measures how Titan\'s cash flows co-move with the market, and a discount-rate shock moves all stocks at once, whereas a demand shock changes the cash-flow covariance.'))
st.append(KeepTogether([Image('fig6.png',width=W,height=W*2.1/7.2),P('Figure 4. Cumulative abnormal return from 10 days before to 10 days after each featured shock (market model estimated on the 120 days before the window).',cap)]))
rows=[['Specification']+[n.replace('Exclude +-','Excl. +-').replace('Rf = ','Rf ') for n in DD['specNames']]]
for sid in ('S1','S5','S8'):
    x=[y for y in DD['shocks'] if y['id']==sid][0]
    rows.append([sid+' change in beta']+[(f'{v:+.2f}' if isinstance(v,(int,float)) else 'n/a') for v in x['specs']])
st.append(tbl(rows,[2.6*cm]+[1.63*cm]*9))
st.append(P('Table 5. Robustness of the change in beta (post minus pre) for the three featured shocks. n/a = the window needed more history or future data than exists (12-month windows for S1, S2 and S8).',cap))
st.append(P('S8 is positive and between +0.50 and +0.68 in every specification that can be run, so the conclusion does not depend on a window or risk-free choice. S1 is positive in all eight, between +0.19 and +0.36. S5 is unstable (between -0.10 and +0.37), which is why it is reported as a price effect and not as evidence of a change in risk. Treating these as three tests of three separate hypotheses, S8 clears even a Bonferroni-adjusted 5% level (p = 0.005 against 0.017); S1 does not, and is best read as suggestive.'))
st.append(CondPageBreak(7*cm)); st.append(P('3.3 How financial policy responded (Task 2c)',h2))
fy=['FY20','FY21','FY22','FY23','FY24','FY25','FY26']
def R(k,key,fmt): return rowv(k,key,fmt,range(2,9))
rows=[['Metric']+fy,
 ['Gross fixed assets / total assets (capex proxy)']+R('ratios','Gross fixed assets / total',lambda x:pc(x)),
 ['Capex / depreciation (x)']+R('ratios','Capex / depreciation',lambda x:f'{x:.2f}'),
 ['D/E, all debt incl. gold & leases (x)']+R('ratios','D/E - borrowings + gold on loan + leases',lambda x:f'{x:.2f}'),
 ['Interest cover, EBIT / finance costs (x)']+R('ratios','Interest coverage = EBIT',lambda x:f'{x:.1f}'),
 ['Dividend payout, DPS / EPS']+R('ratios','Dividend payout',lambda x:pc(x,0)),
 ['Buy-backs (Rs cr)']+['0']*7,
 ['Cash reserves / borrowings (x)']+R('ratios','Cash reserves / borrowings',lambda x:f'{x:.2f}'),
 ['Free cash flow ex gold-loan (Rs cr)']+R('ratios','Free cash flow',lambda x:f'{x:,.0f}'),
 ['WACC']+R('wacc','WACC',lambda x:pc(x)),
 ['ROIC']+R('wacc','ROIC =',lambda x:pc(x)),
 ['ROIC − WACC (pp)']+R('wacc','ROIC - WACC',lambda x:f'{x*100:+.1f}')]
st.append(KeepTogether([tbl(rows,[4.9*cm]+[1.75*cm]*7),P('Table 6. Policy and value metrics, FY20–FY26 (consolidated; FY20 beta and WACC use nine months of data).',cap)]))
st.append(Image('fig3.png',width=W,height=W*2.2/7.2))
st.append(P('Figure 5. Leverage rose and cover fell after 2023, while ROIC stayed above WACC in every year except FY21.',cap))
st.append(B('<b>S1 (FY20 to FY21): preserve liquidity.</b> Capex was cut 59% (Rs 355 cr to Rs 146 cr, 0.39x depreciation), borrowings were repaid (Rs 723 cr to Rs 172 cr), cash reserves rose from Rs 495 cr to Rs 3,365 cr, and gold-on-loan funding was increased (Rs 1,585 cr to Rs 4,210 cr). DPS was held at Rs 4 even though EPS fell 35% (payout 24% to 37%).'))
st.append(B('<b>S5 (FY22 to FY24): grow on short-term debt.</b> Borrowings jumped from Rs 518 cr to Rs 7,838 cr, D/E (all debt) from 0.78x to 1.65x and cover fell from 14.6x to 8.5x. Capex recovered (Rs 224 cr to Rs 691 cr), payout stayed in a 27–31% band, and borrowings were 99–100% short-term in FY22–FY23 (58% in FY24), with no sign of rate hedging in the reports.'))
st.append(B('<b>S8 (FY26): entered at peak leverage.</b> D/E 1.95x, cover 6.8x, free cash flow of −Rs 2,616 cr and cash covering only 0.37x of borrowings; gold-on-loan doubled to Rs 16,070 cr with the gold price. FY27 audited results are not yet available, so the policy response to S8 cannot be observed.'))
st.append(P('The capex proxy fell from 13% to 7%, which looks like under-investment but is mostly a denominator effect: gross fixed assets grew 2.7x while total assets grew 5.2x because inventory absorbed the growth. Capex stayed near 1% of revenue and revenue per rupee of fixed assets rose from 12x to 21x, so the real concern is capacity and the funding of working capital, not plant.'))
# ---------------- 4
st.append(P('4. Analysis and Conclusion',h1))
st.append(P('4.1 Value created or destroyed (Task 3)',h2))
t2=Table([[Image('fig4.png',width=W*0.48,height=W*0.48*2.3/3.55),P('<b>Market view.</b> Titan\'s cumulative TSR for FY21–FY26 was +330% (27.5% a year) against +193% (19.7%) for the NIFTY 500 price index. Against the CAPM-required return it created about Rs 1.16 lakh cr of excess value (indicative, years are not strictly additive) in four of six years, and destroyed Rs 31,600 cr in FY23 and Rs 1.02 lakh cr in FY25.<br/><br/><b>Fundamental view.</b> ROIC beat WACC in five of six years (cumulative EVA Rs 5,364 cr; FY21 was −Rs 205 cr). The gap between the two views is the point: with P/B of 12–36x and P/E of 55–142x, the market capitalises growth far beyond current EVA, so value is hypersensitive to the discount rate and the multiple. In FY25, ROIC (14.4%) exceeded WACC (10.6%) yet TSR was −19% as operating margin slipped from 9.2% to 8.3% and the P/E compressed from 96x to 81x.',body)]],colWidths=[W*0.5,W*0.5])
t2.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4)]))
st.append(t2)
st.append(P('Figure 6. Excess return over cost of equity, in Rs 000 cr (FY20 is a nine-month window; FY27 is year-to-date).',cap))
st.append(P('<b>Theory read through the numbers.</b> <b>(a) Systematic risk and CAPM.</b> A 0.5 rise in beta, as after S8, lifts the cost of equity by 3.0pp (6% premium). In a constant-growth valuation with g = 5% and Ke = 11.8%, that alone cuts equity value by about 31% (1 − 6.8/9.8), which is why shocks that move beta matter more to a high-multiple stock than shocks that move earnings. <b>(b) Trade-off theory.</b> Titan\'s market debt weight is 8%, so the WACC curve is flat: the minimum feasible WACC is 11.2% at 7.5% debt versus 11.1% actual. More debt buys almost no WACC benefit, while interest cover (6.8x) already leaves headroom of only Rs 4,582 cr before a 5x cover floor binds. WACC fell from 13.1% (FY23) to 11.1% (FY26) because beta and the risk-free rate fell, not because of leverage. <b>(c) Pecking order.</b> With free cash flow negative after working capital, Titan went to short-term debt first and never issued equity or bought back shares; at an earnings yield of 1.4% against an after-tax debt cost of 3.4%, a debt-funded buy-back would have cut EPS, so not buying back was right. <b>(d) Payout smoothing and signalling (Lintner).</b> DPS rose from Rs 4 to Rs 15 (30% a year) while EPS rose 39% a year, and payout stayed within 24–37%; holding DPS at Rs 4 in FY21 signalled confidence. But free cash flow after dividends was negative in three of six years, so part of the dividend was effectively debt-funded.'))
st.append(P('4.2 Recommendations for the CFO (Task 4)',h2))
st.append(P('<b>What the CFO should have done in 2020–26.</b>'))
st.append(B('<b>Cap leverage with explicit guardrails</b> (cover at least 6x, D/E on all debt at most 1.5x) and finance the post-2022 inventory build with longer-tenor debt rather than rolling commercial paper. Debt rose by Rs 10,655 cr in FY21–26 while free cash flow after dividends was −Rs 9,104 cr.'))
st.append(B('<b>Hedge the rate risk before 2022.</b> With 99% of borrowings short-term, a repeat of the 250 bp hiking cycle costs about Rs 385 cr a year (cover 6.8x to 5.2x, EPS −5.7%); fixing 75% of the debt cuts this to Rs 96 cr (cover 6.3x, EPS −1.4%).'))
st.append(B('<b>Use gold-on-loan as the commodity hedge</b> (raise it from 38% to about 45% of inventory): it is the cheapest funding (about 2.7% a year) and naturally hedges gold-price swings on stock.'))
st.append(B('<b>Keep the smoothed dividend but tie DPS growth to free cash flow;</b> no buy-backs at 20x+ book; protect core capex through shocks (it fell to 0.39x of depreciation in FY21 and 0.56x in FY22); rebuild a liquidity buffer of at least 20 days of revenue (cash fell from 3.1x to 0.37x of borrowings between FY22 and FY26).'))
st.append(P('<b>Five-year strategy (FY27–FY31).</b> The model runs the same business under two policies and two environments: the base case (growth fading from 16% to 10%, margin 8.6%) and a stress case (growth 4–8%, margin 7.0–8.3%, +250 bp rates).'))
SC=D['scen']
def sc(lab):
    for r in SC:
        if len(r)>9 and r[9]==lab: return r[10:14]
rows=[['Metric (FY27–FY31)','A. Status quo','B. Recommended','C. Status quo, stress','D. Recommended, stress']]
for lab,fm in (('Minimum interest cover (x)',lambda x:f'{x:.1f}'),('Peak D/E (x)',lambda x:f'{x:.2f}'),('FY31 total debt (Rs cr)',lambda x:f'{x:,.0f}'),('Cumulative EVA FY27-31 (Rs cr)',lambda x:f'{x:,.0f}'),('FY31 ROIC',lambda x:pc(x)),('Years in breach of guardrails',lambda x:f'{x:.0f}')):
    rows.append([lab]+[fm(v) for v in sc(lab)])
st.append(tbl(rows,[4.9*cm,2.9*cm,3.0*cm,3.1*cm,3.3*cm]))
st.append(P('Table 7. Scenario results. Recommended policy: capex 1.3% of revenue, inventory days 178 to 156, gold-on-loan 45% of inventory, payout 25%, 75% of borrowings fixed. Guardrails: cover at least 5x, D/E at most 2.0x.',cap))
st.append(P('The recommended policy leaves base-case profit almost unchanged but raises cumulative EVA by about Rs 2,000 cr and cuts FY31 debt by Rs 5,000–6,000 cr, mainly through faster inventory turns and cheaper gold-based funding. Under stress, hedging and lower inventory shrink the cover shortfall (3.7x to 4.3x) and move cumulative EVA from −Rs 1,022 cr to +Rs 975 cr, yet two years still breach the 5x floor. Hedging alone is therefore not enough: leverage has to be lower <i>before</i> the shock. The practical rule is a pre-committed trigger: if cover falls below 6x, pause DPS growth, slow the inventory build and term out commercial paper.'))
st.append(KeepTogether([Image('fig8.png',width=W,height=W*2.3/7.2),P('Figure 7. Scenario paths FY26-FY31. Dashed lines are the stress cases; grey lines show the 5x cover floor, the 2.0x D/E ceiling and zero EVA.',cap)]))
st.append(KeepTogether([Image('fig7.png',width=W,height=W*2.4/7.2),P('Figure 8. Left: WACC against leverage under Hamada re-levering and a rising credit spread; orange points breach the 5x cover floor. Right: interest cover on the FY26 balance sheet if rates rise by 0-400 bp, by share of debt fixed.',cap)]))
st.append(P('Figure 8 makes two points. First, the WACC curve is almost flat in the feasible zone (11.5% at zero debt, 11.2% at 7.5% debt, then the cover floor binds), so there is little to gain from adding debt and a lot to lose from the interest burden. Second, the hedge ratio matters more than any plausible leverage target: at +250 bp, cover is 5.2x unhedged and 6.3x with 75% fixed. Because the model reprices only borrowings and half the gold-on-loan, it understates the effect if gold-loan spreads move one for one with policy rates.'))
st.append(P('Implementation roadmap and early-warning triggers',h2))
st.append(tbl([['Year','Actions','Target at year-end (case B)'],
 ['FY27','Board adopts the guardrails (cover at least 6x, D/E on all debt at most 1.5x). Fix 75% of borrowings through swaps or fixed-rate term loans. Replace rolling commercial paper with 3 to 5 year paper.',f"D/E {DD['scen']['B']['de'][1]:.2f}x, cover {DD['scen']['B']['cover'][1]:.1f}x"],
 ['FY28','Move gold-on-loan towards 45% of inventory. Cut inventory days from 178 towards 165. Tie DPS growth to free cash flow after capex.',f"D/E {DD['scen']['B']['de'][2]:.2f}x, cover {DD['scen']['B']['cover'][2]:.1f}x"],
 ['FY29','Inventory days to about 160; capex held at 1.3% of revenue. Review hedge ratio against the rate outlook.',f"D/E {DD['scen']['B']['de'][3]:.2f}x, cover {DD['scen']['B']['cover'][3]:.1f}x"],
 ['FY30 to FY31','Payout 25%; use surplus free cash flow to rebuild a liquidity buffer of 20 days of revenue before any buy-back is considered.',f"D/E {DD['scen']['B']['de'][5]:.2f}x, cover {DD['scen']['B']['cover'][5]:.1f}x in FY31"]],[2.3*cm,10.2*cm,4.7*cm]))
st.append(P('Table 8. Five-year roadmap under the recommended policy (base macro).',cap))
st.append(tbl([['Indicator','Green','Amber: act','Red: escalate'],
 ['Interest cover (EBIT / finance cost)','6x or more','5x to 6x: pause DPS growth, slow inventory build','Below 5x: stop non-maintenance capex, draw liquidity buffer'],
 ['D/E, all debt','1.5x or less','1.5x to 2.0x: term out commercial paper','Above 2.0x: no new debt for growth'],
 ['Share of borrowings fixed or hedged','75% or more','50% to 75%: add swaps','Below 50%: board review'],
 ['Inventory days','165 or fewer','165 to 180: review purchasing','Above 180: inventory freeze'],
 ['Liquidity buffer (days of revenue)','20 or more','10 to 20: no buy-backs','Below 10: suspend dividend growth']],[4.6*cm,2.4*cm,5.2*cm,5.0*cm]))
st.append(P('Table 9. Early-warning dashboard for the CFO. Thresholds follow the guardrails used in the scenario model.',cap))
st.append(P('<b>Risks to the plan.</b> A sharp fall in the gold price would cut the value of gold on loan and inventory together; the plan leans on gold-on-loan, so the natural hedge only works if the loan is marked to the same price as the stock. Faster demand growth than modelled would push inventory and borrowing up. A change in the gold-metal-loan regulations or in the cost of funds could erode the funding advantage. Each of these is monitored through the Table 9 triggers.'))
st.append(P('4.3 Conclusion',h2))
st.append(P('Shocks changed what investors demanded of Titan more than what the firm did. Beta rose significantly after the lockdown and, most robustly, after the 2026 oil shock; policy followed the textbook playbook of liquidity first (S1) then debt-funded growth (S5), and Titan created large market value while keeping ROIC above WACC. The weakness is the funding mix: cover has fallen from 14.6x to 6.8x, 99% of borrowings are short-term, and dividends and growth are partly debt-financed. The decision for the next five years is therefore not whether to grow but how to fund growth so that a repeat of 2022 or a further oil shock cannot push cover through the floor. <i>Limitations:</i> the NIFTY file is a price index (benchmark understated by about 1% a year); the 6% equity risk premium is an assumption (sensitivity in the workbook); overlapping shock windows are not independent; FY20 is a nine-month window and FY27 has no audited accounts; the counterfactuals and scenarios are illustrative, not forecasts.'))
st.append(P('5. References',h1))
REF=['Blume, M. E. (1971). On the assessment of risk. <i>Journal of Finance</i>, 26(1), 1–10.','Brown, S. J., &amp; Warner, J. B. (1985). Using daily stock returns: the case of event studies. <i>Journal of Financial Economics</i>, 14(1), 3–31.','Hamada, R. S. (1972). The effect of the firm\'s capital structure on the systematic risk of common stocks. <i>Journal of Finance</i>, 27(2), 435–452.','Jensen, M. C. (1968). The performance of mutual funds in the period 1945–1964. <i>Journal of Finance</i>, 23(2), 389–416.','Kraus, A., &amp; Litzenberger, R. H. (1973). A state-preference model of optimal financial leverage. <i>Journal of Finance</i>, 28(4), 911–922.','Lintner, J. (1956). Distribution of incomes of corporations among dividends, retained earnings, and taxes. <i>American Economic Review</i>, 46(2), 97–113.','MacKinlay, A. C. (1997). Event studies in economics and finance. <i>Journal of Economic Literature</i>, 35(1), 13–39.','Modigliani, F., &amp; Miller, M. H. (1958). The cost of capital, corporation finance and the theory of investment. <i>American Economic Review</i>, 48(3), 261–297.','Myers, S. C., &amp; Majluf, N. S. (1984). Corporate financing and investment decisions when firms have information that investors do not have. <i>Journal of Financial Economics</i>, 13(2), 187–221.','Sharpe, W. F. (1964). Capital asset prices: a theory of market equilibrium under conditions of risk. <i>Journal of Finance</i>, 19(3), 425–442.','Data: NSE India (Titan daily prices); NSE Indices (NIFTY 500 historical data); Titan Company Ltd, Annual Reports FY2019–20 to FY2025–26; Reserve Bank of India (repo rate history); FRED/OECD series INDIRLTLT01STM (India 10-year yield). All accessed 5 Nov 2026.']
rs=ParagraphStyle('r',parent=body,fontSize=8.2,leading=10,leftIndent=9,firstLineIndent=-8,spaceAfter=1,alignment=TA_LEFT)
for r_ in REF: st.append(Paragraph(r_,rs))
doc.build(st,onFirstPage=footer,onLaterPages=footer)
print('built')
