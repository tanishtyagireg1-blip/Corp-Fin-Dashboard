import sys, datetime as dt
sys.path.insert(0,'/home/claude/wai')
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.chart import ScatterChart, BarChart, LineChart, Reference, Series
from openpyxl.chart.error_bar import ErrorBars
from openpyxl.chart.data_source import NumDataSource, NumRef
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.marker import Marker
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.comments import Comment
import fin as F

exec(open('/home/claude/wai/load.py').read())   # t (Titan), n (NIFTY)
px = t[['Date','Close Price']].merge(n[['Date','Close']],on='Date').sort_values('Date').reset_index(drop=True)
px.columns=['Date','T','N']
NR = len(px); R0=5; R1=R0+NR-1          # data rows 5..1827
LASTDATE = px.Date.max()

# ---------- palette & styles ----------
NAVY='1F3864'; BLUE='2A78D6'; ORANGE='EB6834'; GREY='8A8F98'; LGREY='F2F4F7'; MGREY='D9DEE5'; YEL='FFF2CC'; GRN='E2F0D9'; RED='FBE5E1'
FONT='Arial'
def fnt(**k):
    k.setdefault('name',FONT); k.setdefault('size',10); return Font(**k)
F_BASE=fnt(); F_B=fnt(bold=True); F_IN=fnt(color='0000FF'); F_LINK=fnt(color='006100'); F_H=fnt(bold=True,color='FFFFFF')
F_TITLE=fnt(bold=True,size=16,color=NAVY); F_SUB=fnt(italic=True,color='595959'); F_SEC=fnt(bold=True,size=11,color=NAVY)
FILL_H=PatternFill('solid',fgColor=NAVY); FILL_SEC=PatternFill('solid',fgColor=MGREY); FILL_L=PatternFill('solid',fgColor=LGREY)
FILL_IN=PatternFill('solid',fgColor=YEL); FILL_G=PatternFill('solid',fgColor=GRN); FILL_R=PatternFill('solid',fgColor=RED)
THIN=Side(style='thin',color='BFBFBF'); BOX=Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
BOT=Border(bottom=Side(style='thin',color='7F7F7F'))
NF_CR='#,##0;(#,##0);"-"'; NF_CR1='#,##0.0;(#,##0.0);"-"'; NF_PCT='0.0%;(0.0%);"-"'; NF_PCT2='0.00%'; NF_X='0.00"x"'; NF_B='0.00'; NF_D='dd-mmm-yy'; NF_P='0.000'
NF_PCTS='0.0%;-0.0%;0.0%'

wb=Workbook()
def sheet(name,tab=None,first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title=name; ws.sheet_view.showGridLines=False
    if tab: ws.sheet_properties.tabColor=tab
    return ws
def put(ws,ref,v,font=None,nf=None,fill=None,al=None,border=None,bold=False):
    c=ws[ref]; c.value=v
    c.font = font or (F_B if bold else F_BASE)
    if nf: c.number_format=nf
    if fill: c.fill=fill
    if al: c.alignment=al
    if border: c.border=border
    return c
def title(ws,text,sub=None):
    put(ws,'A1',text,F_TITLE);
    if sub: put(ws,'A2',sub,F_SUB)
    ws.row_dimensions[1].height=24
def hdr(ws,row,col0,labels,widths=None,wrap=True,h=30):
    for i,l in enumerate(labels):
        c=ws.cell(row=row,column=col0+i,value=l); c.font=F_H; c.fill=FILL_H
        c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=wrap); c.border=BOX
    ws.row_dimensions[row].height=h
def sec(ws,row,text,c0=1,c1=12):
    for c in range(c0,c1+1): ws.cell(row=row,column=c).fill=FILL_SEC
    put(ws,f'{CL(c0)}{row}',text,F_SEC,fill=FILL_SEC)
def widths(ws,d):
    for k,v in d.items(): ws.column_dimensions[k].width=v
def wrapal(h='left',v='top'): return Alignment(horizontal=h,vertical=v,wrap_text=True)
AL_C=Alignment(horizontal='center',vertical='center')
DR=f'$A${R0}:$A${R1}'          # Data dates
def dcol(c): return f'Data!${c}$1:${c}${R1}'
def rng(c,a,b): return f'INDEX({dcol(c)},{a}):INDEX({dcol(c)},{b})'

# ======================================================= README placeholder (filled last) & Summary placeholder
ws_readme=sheet('README','1F3864',first=True)
ws_sum=sheet('Summary','2A78D6')
# ======================================================= INPUTS
wi=sheet('Inputs','FFC000')
title(wi,'Inputs, assumptions & event definitions','Blue text = hard-coded input (editable). Yellow fill = key assumption/switch. Black = formula. Green = link to another sheet.')
hdr(wi,4,1,['Parameter','Value','Notes / rationale'],h=20)
params=[
 ('Risk-free source for excess returns (1 = RBI repo, 2 = 10Y G-sec, 3 = none/raw)',1,'0','Repo is the overnight policy rate and is used as the short-rate proxy for daily CAPM (91-day T-bill history not available offline). Change to 2 or 3 to test robustness - every beta in the workbook recalculates.'),
 ('Pre / post event window (months)',6,'0','Brief: 6 months before and after each shock. Robustness sheet re-runs 3 and 12 months.'),
 ('Trading days per year',252,'0','Annualisation factor for alpha and volatility.'),
 ('Rolling-beta window (trading days)',126,'0','~6 months. Keep between 60 and 126 (chart range starts after the first 126 days).'),
 ('Equity risk premium (India)',0.06,'0.0%','ASSUMPTION. Practitioner range for India ~5-7.5%; sensitivity shown on Robustness sheet.'),
 ('Beta used for cost of equity (1 = raw FY regression, 2 = Blume-adjusted)',2,'0','Blume (1971): adjusted beta = w x raw + (1-w) x 1. Reduces sampling noise in single-year betas.'),
 ('Treat gold-on-loan as debt in WACC / ROIC (1 = yes, 0 = no)',1,'0','Metal loans carry interest and are a financial liability; they also hedge gold inventory (see Ratios).'),
 ('Treat lease liabilities as debt in WACC / ROIC (1 = yes, 0 = no)',1,'0','Ind AS 116 leases are interest-bearing; EBIT is stated before lease interest.'),
 ('Marginal tax rate',0.2517,'0.00%','Statutory rate under s.115BAA (22% + surcharge + cess) used for after-tax cost of debt. Effective rate used for NOPAT.'),
 ('Shares outstanding (crore)',88.78,'0.00','Equity share capital Rs 88.78 cr at Rs 1 face value (AR 2019-20, Rs 8,878 lakh); unchanged through FY26.'),
 ('Event study: estimation window length (days)',120,'0','Market-model parameters estimated on [-(gap+length), -gap] trading days before the event.'),
 ('Event study: gap before event (days)',11,'0','Keeps estimation window clear of the event window [-10,+10].'),
 ('Significance level (two-sided)',0.05,'0.00','Used for confidence intervals and verdict flags.'),
 ('Blume weight on raw beta',0.67,'0.00','Standard Blume weights (0.67 raw + 0.33 market).'),
]
for i,(lab,val,nf,note) in enumerate(params):
    r=5+i
    put(wi,f'A{r}',lab,al=wrapal()); put(wi,f'B{r}',val,F_IN,nf=nf if nf!='0' else '0',fill=FILL_IN,al=AL_C,border=BOX)
    put(wi,f'C{r}',note,F_SUB,al=wrapal())
    wi.row_dimensions[r].height=30
dv=DataValidation(type='list',formula1='"1,2,3"',allow_blank=False); wi.add_data_validation(dv); dv.add('B5')
dv2=DataValidation(type='list',formula1='"1,2"',allow_blank=False); wi.add_data_validation(dv2); dv2.add('B10')
dv3=DataValidation(type='list',formula1='"0,1"',allow_blank=False); wi.add_data_validation(dv3); dv3.add('B11'); dv3.add('B12')
IN=dict(rf='Inputs!$B$5',win='Inputs!$B$6',td='Inputs!$B$7',roll='Inputs!$B$8',erp='Inputs!$B$9',bch='Inputs!$B$10',fg='Inputs!$B$11',fl='Inputs!$B$12',
        tax='Inputs!$B$13',sh='Inputs!$B$14',estn='Inputs!$B$15',gap='Inputs!$B$16',alpha='Inputs!$B$17',blume='Inputs!$B$18')
# ---- shocks table
sec(wi,21,'Shock register (2020-2026) - all eight shocks in the brief are tested; three are featured for deep-dive',1,8)
hdr(wi,22,1,['ID','Shock','Category','Event date (as announced)','Event trading day (first session on/after)','Featured? (1/0)','Transmission channel to Titan','Source / dating note'],h=42)
NS=len(F.SHOCKS)
for i,(sid,nm,cat,d,feat,chan,src) in enumerate(F.SHOCKS):
    r=23+i
    put(wi,f'A{r}',sid,F_B,al=AL_C); put(wi,f'B{r}',nm,al=wrapal()); put(wi,f'C{r}',cat,al=wrapal())
    put(wi,f'D{r}',dt.datetime.strptime(d,'%Y-%m-%d'),F_IN,nf=NF_D,fill=FILL_IN,al=AL_C)
    put(wi,f'E{r}',f'=IFERROR(INDEX(Data!{DR},MATCH(D{r},Data!{DR},0)),INDEX(Data!{DR},MATCH(D{r},Data!{DR},1)+1))',F_LINK,nf=NF_D,al=AL_C)
    put(wi,f'F{r}',feat,F_IN,fill=FILL_IN,al=AL_C)
    put(wi,f'G{r}',chan,al=wrapal()); put(wi,f'H{r}',src,F_SUB,al=wrapal())
    wi.row_dimensions[r].height=32
# ---- FY calendar
sec(wi,33,'Financial-year calendar (Titan FY ends 31 March) and trading-day row mapping',1,8)
hdr(wi,34,1,['FY','FY start','FY end','Last trading day in FY','First Data row (returns)','Last Data row','Trading days','Note'],h=30)
FYL=F.FY+['FY27 YTD']
for k,lab in enumerate(FYL):
    r=35+k; y=2018+k if k<9 else 2026
    yr=2018+k   # FY19 starts Apr 2018
    put(wi,f'A{r}',lab,F_B,al=AL_C)
    put(wi,f'B{r}',dt.datetime(yr,4,1),F_IN,nf=NF_D,al=AL_C); put(wi,f'C{r}',dt.datetime(yr+1,3,31),F_IN,nf=NF_D,al=AL_C)
    if k==0:
        for c in 'DEFG': put(wi,f'{c}{r}','n/a',F_SUB,al=AL_C)
        put(wi,f'H{r}','Price data begins 1 Jul 2019 - FY19 used for balance-sheet opening values only',F_SUB)
    else:
        put(wi,f'D{r}',f'=INDEX(Data!{DR},MATCH(C{r},Data!{DR},1))',F_LINK,nf=NF_D,al=AL_C)
        put(wi,f'E{r}',f'=IFERROR(MATCH(B{r}-1,Data!{DR},1)+5,6)',F_LINK,al=AL_C)
        put(wi,f'F{r}',f'=MATCH(C{r},Data!{DR},1)+4',F_LINK,al=AL_C)
        put(wi,f'G{r}',f'=F{r}-E{r}+1',al=AL_C)
        if k==1: put(wi,f'H{r}','Partial year: market data from 1 Jul 2019 (9 months)',F_SUB)
        if k==8: put(wi,f'H{r}','Partial year: to latest data date (4 Nov 2026)',F_SUB)
# ---- Repo
put(wi,'J3','RBI repo-rate history (effective dates)',F_SEC)
hdr(wi,4,10,['Effective date','Repo rate','Source / note'],h=20)
for i,(d,v,s) in enumerate(F.REPO):
    r=5+i
    put(wi,f'J{r}',dt.datetime.strptime(d,'%Y-%m-%d'),F_IN,nf=NF_D,al=AL_C); put(wi,f'K{r}',v/100,F_IN,nf=NF_PCT2,al=AL_C); put(wi,f'L{r}',s,F_SUB)
RP0,RP1=5,5+len(F.REPO)-1
# ---- G-sec
put(wi,'N3','India 10Y G-sec yield, monthly avg',F_SEC)
hdr(wi,4,14,['Month','10Y yield'],h=20)
for i,(m,v) in enumerate(F.GSEC):
    r=5+i
    put(wi,f'N{r}',dt.datetime.strptime(m+'-01','%Y-%m-%d'),F_IN,nf='mmm-yy',al=AL_C); put(wi,f'O{r}',v/100,F_IN,nf=NF_PCT2,al=AL_C)
GS0,GS1=5,5+len(F.GSEC)-1
put(wi,f'N{GS1+2}','Source: FRED series INDIRLTLT01STM (OECD Main Economic Indicators), monthly average of daily 10-year benchmark yield.',F_SUB)
widths(wi,{'A':46,'B':26,'C':34,'D':16,'E':18,'F':12,'G':38,'H':44,'I':3,'J':14,'K':11,'L':44,'M':3,'N':12,'O':11})
wi.freeze_panes='A5'

# ======================================================= DATA
wd=sheet('Data','7F7F7F')
title(wd,'Daily price data and return engine (Titan Company vs NIFTY 500)','Prices are typed from NSE / NSE Indices downloads (blue); every other column is a live formula. 1 Jul 2019 - 4 Nov 2026.')
labs=['Date','Titan close (Rs)','NIFTY 500 close (price index)','Titan return','NIFTY 500 return','Risk-free (annual, selected)','Risk-free (daily)','Titan excess return','Market excess return',
      'Rolling beta (window per Inputs)','Titan indexed (100 = 1 Jul 2019)','NIFTY 500 indexed','Titan relative to NIFTY (index)','Financial year','Titan drawdown from peak','NIFTY 500 drawdown',
      'Repo (annual)','10Y G-sec (annual)','Titan excess (repo)','Mkt excess (repo)','Titan excess (G-sec)','Mkt excess (G-sec)']
hdr(wd,4,1,labs,h=54)
for i in range(NR):
    r=R0+i
    put(wd,f'A{r}',px.Date[i].to_pydatetime(),F_IN,nf=NF_D)
    put(wd,f'B{r}',float(px['T'][i]),F_IN,nf='#,##0.00'); put(wd,f'C{r}',float(px['N'][i]),F_IN,nf='#,##0.00')
    put(wd,f'Q{r}',f'=INDEX(Inputs!$K${RP0}:$K${RP1},MATCH(A{r},Inputs!$J${RP0}:$J${RP1},1))',nf=NF_PCT2)
    put(wd,f'R{r}',f'=INDEX(Inputs!$O${GS0}:$O${GS1},MATCH(A{r},Inputs!$N${GS0}:$N${GS1},1))',nf=NF_PCT2)
    put(wd,f'F{r}',f'=CHOOSE({IN["rf"]},Q{r},R{r},0)',nf=NF_PCT2)
    put(wd,f'G{r}',f'=F{r}/{IN["td"]}',nf='0.00000%')
    put(wd,f'K{r}',f'=B{r}/B${R0}*100',nf='0.0'); put(wd,f'L{r}',f'=C{r}/C${R0}*100',nf='0.0'); put(wd,f'M{r}',f'=K{r}/L{r}*100',nf='0.0')
    put(wd,f'N{r}',f'=IF(MONTH(A{r})>=4,"FY"&TEXT(MOD(YEAR(A{r})+1,100),"00"),"FY"&TEXT(MOD(YEAR(A{r}),100),"00"))')
    put(wd,f'O{r}',f'=B{r}/MAX(B${R0}:B{r})-1',nf=NF_PCT); put(wd,f'P{r}',f'=C{r}/MAX(C${R0}:C{r})-1',nf=NF_PCT)
    if i>0:
        put(wd,f'D{r}',f'=B{r}/B{r-1}-1',nf='0.00%'); put(wd,f'E{r}',f'=C{r}/C{r-1}-1',nf='0.00%')
        put(wd,f'H{r}',f'=D{r}-G{r}',nf='0.00%'); put(wd,f'I{r}',f'=E{r}-G{r}',nf='0.00%')
        put(wd,f'S{r}',f'=D{r}-Q{r}/{IN["td"]}',nf='0.00%'); put(wd,f'T{r}',f'=E{r}-Q{r}/{IN["td"]}',nf='0.00%')
        put(wd,f'U{r}',f'=D{r}-R{r}/{IN["td"]}',nf='0.00%'); put(wd,f'V{r}',f'=E{r}-R{r}/{IN["td"]}',nf='0.00%')
        W=IN['roll']
        put(wd,f'J{r}',f'=IF({r}<{W}+5,"",SLOPE(INDEX($H$1:$H${R1},{r}-{W}+1):INDEX($H$1:$H${R1},{r}),INDEX($I$1:$I${R1},{r}-{W}+1):INDEX($I$1:$I${R1},{r})))',nf=NF_B)
widths(wd,{'A':11,'B':11,'C':14,'D':9,'E':9,'F':11,'G':11,'H':10,'I':10,'J':12,'K':13,'L':12,'M':13,'N':9,'O':11,'P':11,'Q':9,'R':9,'S':10,'T':10,'U':10,'V':10})
wd.freeze_panes='B5'

# ======================================================= WEEKLY
ww=sheet('Weekly','7F7F7F')
title(ww,'Weekly return engine (robustness: daily vs weekly betas)','Friday closes (last trading day on/before Friday). Used only on the Robustness sheet.')
hdr(ww,4,1,['Week ending (Fri)','Titan close','NIFTY 500 close','Titan return','NIFTY 500 return','Rf (annual)','Rf (weekly)','Titan excess','Market excess'],h=30)
fr=pd.date_range('2019-07-05',pd.Timestamp('2026-10-30'),freq='W-FRI')
WR0=5; WR1=WR0+len(fr)-1
for i,d in enumerate(fr):
    r=WR0+i
    put(ww,f'A{r}',d.to_pydatetime(),F_IN,nf=NF_D)
    pos=f'MATCH(A{r},Data!{DR},1)'
    put(ww,f'B{r}',f'=INDEX(Data!$B${R0}:$B${R1},{pos})',F_LINK,nf='#,##0.00'); put(ww,f'C{r}',f'=INDEX(Data!$C${R0}:$C${R1},{pos})',F_LINK,nf='#,##0.00')
    put(ww,f'F{r}',f'=INDEX(Data!$F${R0}:$F${R1},{pos})',F_LINK,nf=NF_PCT2); put(ww,f'G{r}',f'=F{r}/52',nf='0.0000%')
    if i>0:
        put(ww,f'D{r}',f'=B{r}/B{r-1}-1',nf='0.00%'); put(ww,f'E{r}',f'=C{r}/C{r-1}-1',nf='0.00%')
        put(ww,f'H{r}',f'=D{r}-G{r}',nf='0.00%'); put(ww,f'I{r}',f'=E{r}-G{r}',nf='0.00%')
widths(ww,{'A':16,'B':12,'C':14,'D':11,'E':12,'F':11,'G':11,'H':12,'I':12}); ww.freeze_panes='B5'

# ======================================================= SHOCKS (regressions)
wsx=sheet('Shocks','C00000')
title(wsx,'Task 2(b): CAPM regressions, 6 months before vs 6 months after each shock','Model: (Titan return - Rf) = alpha + beta x (NIFTY 500 return - Rf) + e, daily. All numbers are live SLOPE / INTERCEPT / STEYX / DEVSQ formulas over the exact window rows.')
put(wsx,'A3','Windows: pre = [event - N months, event day - 1]; post = [event day, event + N months - 1]. The event-day return is placed in the POST window (reaction day). SE(beta) = STEYX / SQRT(DEVSQ(x)).',F_SUB)
hdr(wsx,5,1,['ID','Shock','Period','Window start','Window end','First Data row','Last Data row','n (days)','Alpha (daily)','Beta','SE(beta)','t-stat (beta)','p-value H0: beta = 1','R-squared','95% CI low','95% CI high','Alpha (annualised)','Daily volatility of excess return','Titan cumulative return','NIFTY 500 cumulative return'],h=54)
for i in range(NS):
    ir=23+i
    for j,per in enumerate(['Pre','Post']):
        r=6+2*i+j
        put(wsx,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(wsx,f'B{r}',f'=Inputs!B{ir}',F_LINK); put(wsx,f'C{r}',per,F_B,al=AL_C)
        if j==0:
            put(wsx,f'D{r}',f'=EDATE(Inputs!$E{ir},-{IN["win"]})',nf=NF_D,al=AL_C); put(wsx,f'E{r}',f'=Inputs!$E{ir}-1',nf=NF_D,al=AL_C)
        else:
            put(wsx,f'D{r}',f'=Inputs!$E{ir}',nf=NF_D,al=AL_C); put(wsx,f'E{r}',f'=MIN(EDATE(Inputs!$E{ir},{IN["win"]})-1,MAX(Data!{DR}))',nf=NF_D,al=AL_C)
        put(wsx,f'F{r}',f'=MATCH(D{r}-1,Data!{DR},1)+5',al=AL_C); put(wsx,f'G{r}',f'=MATCH(E{r},Data!{DR},1)+4',al=AL_C)
        put(wsx,f'H{r}',f'=G{r}-F{r}+1',al=AL_C)
        y=rng('H',f'F{r}',f'G{r}'); x=rng('I',f'F{r}',f'G{r}')
        put(wsx,f'I{r}',f'=INTERCEPT({y},{x})',nf='0.0000%'); put(wsx,f'J{r}',f'=SLOPE({y},{x})',nf=NF_B,bold=True)
        put(wsx,f'K{r}',f'=STEYX({y},{x})/SQRT(DEVSQ({x}))',nf=NF_B); put(wsx,f'L{r}',f'=J{r}/K{r}',nf='0.0')
        put(wsx,f'M{r}',f'=TDIST(ABS((J{r}-1)/K{r}),H{r}-2,2)',nf=NF_P); put(wsx,f'N{r}',f'=RSQ({y},{x})',nf='0.00')
        put(wsx,f'O{r}',f'=J{r}-TINV({IN["alpha"]},H{r}-2)*K{r}',nf=NF_B); put(wsx,f'P{r}',f'=J{r}+TINV({IN["alpha"]},H{r}-2)*K{r}',nf=NF_B)
        put(wsx,f'Q{r}',f'=I{r}*{IN["td"]}',nf=NF_PCT); put(wsx,f'R{r}',f'=STDEV({y})',nf='0.00%')
        put(wsx,f'S{r}',f'=INDEX({dcol("B")},G{r})/INDEX({dcol("B")},F{r}-1)-1',nf=NF_PCTS); put(wsx,f'T{r}',f'=INDEX({dcol("C")},G{r})/INDEX({dcol("C")},F{r}-1)-1',nf=NF_PCTS)
        if j==1:
            for c in range(1,21): wsx.cell(row=r,column=c).border=Border(bottom=Side(style='thin',color='7F7F7F'))
# --- delta-beta table
sec(wsx,24,'Did systematic risk change? Test of beta(post) - beta(pre), independent windows (Welch-type z/t test)',1,20)
hdr(wsx,25,1,['ID','Shock','Beta pre','Beta post','Change in beta','SE of change','t-stat','df','p-value (two-sided)','95% CI low','95% CI high','Verdict','Other shocks inside window span','Featured','Alpha pre (ann.)','Alpha post (ann.)','R-sq pre','R-sq post','Reading','95% CI half-width (pre)','95% CI half-width (post)'],h=54)
for i in range(NS):
    r=26+i; a=6+2*i; b=a+1; ir=23+i
    put(wsx,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(wsx,f'B{r}',f'=Inputs!B{ir}',F_LINK)
    put(wsx,f'C{r}',f'=J{a}',nf=NF_B); put(wsx,f'D{r}',f'=J{b}',nf=NF_B); put(wsx,f'E{r}',f'=D{r}-C{r}',nf='+0.00;-0.00;0.00',bold=True)
    put(wsx,f'F{r}',f'=SQRT(K{a}^2+K{b}^2)',nf=NF_B); put(wsx,f'G{r}',f'=E{r}/F{r}',nf='0.00'); put(wsx,f'H{r}',f'=H{a}+H{b}-4',al=AL_C)
    put(wsx,f'I{r}',f'=TDIST(ABS(G{r}),H{r},2)',nf=NF_P,bold=True)
    put(wsx,f'J{r}',f'=E{r}-TINV({IN["alpha"]},H{r})*F{r}',nf='+0.00;-0.00;0.00'); put(wsx,f'K{r}',f'=E{r}+TINV({IN["alpha"]},H{r})*F{r}',nf='+0.00;-0.00;0.00')
    put(wsx,f'L{r}',f'=IF(I{r}<0.01,"*** 1% level",IF(I{r}<0.05,"** 5% level",IF(I{r}<0.1,"* 10% level","Not significant")))',al=AL_C)
    put(wsx,f'M{r}',f'=COUNTIFS(Inputs!$E$23:$E$30,">="&D{a},Inputs!$E$23:$E$30,"<="&E{b})-1',al=AL_C)
    put(wsx,f'N{r}',f'=Inputs!F{ir}',F_LINK,al=AL_C)
    put(wsx,f'O{r}',f'=Q{a}',nf=NF_PCT); put(wsx,f'P{r}',f'=Q{b}',nf=NF_PCT); put(wsx,f'Q{r}',f'=N{a}',nf='0.00'); put(wsx,f'R{r}',f'=N{b}',nf='0.00')
    put(wsx,f'S{r}',f'=IF(E{r}>0,"Riskier","Less risky")&" after shock (beta "&TEXT(C{r},"0.00")&" to "&TEXT(D{r},"0.00")&"); "&IF(D{r}>1,"aggressive stock (>1)","defensive stock (<1)")')
    put(wsx,f'T{r}',f'=TINV({IN["alpha"]},H{a}-2)*K{a}',nf=NF_B); put(wsx,f'U{r}',f'=TINV({IN["alpha"]},H{b}-2)*K{b}',nf=NF_B)
wsx.conditional_formatting.add('L26:L33',FormulaRule(formula=['LEFT(L26,1)="*"'],fill=FILL_G))
put(wsx,'A35','Reading guide: a significant positive change means Titan became more sensitive to market moves (higher systematic risk) after the shock. Windows that overlap other shocks (column M > 0) are flagged; the Robustness sheet tests event-buffer and window-length variants.',F_SUB,al=wrapal())
wsx.merge_cells('A35:S35'); wsx.row_dimensions[35].height=30
widths(wsx,{'A':6,'B':38,'C':8,'D':12,'E':12,'F':9,'G':9,'H':8,'I':12,'J':9,'K':9,'L':14,'M':14,'N':9,'O':10,'P':10,'Q':11,'R':11,'S':44,'T':12,'U':12})
wsx.freeze_panes='C6'
