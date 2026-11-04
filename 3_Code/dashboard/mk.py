import json, datetime as dt
from openpyxl import load_workbook
wb=load_workbook('/home/claude/out/Titan_WAI_Analysis.xlsx',data_only=True)
D0=json.load(open('/home/claude/rep/data.json'))
out={}
d=wb['Data']
out['dates']=[d.cell(row=r,column=1).value.strftime('%Y-%m-%d') for r in range(5,1828)]
t=[d.cell(row=r,column=2).value for r in range(5,1828)]; n=[d.cell(row=r,column=3).value for r in range(5,1828)]
out['titan']=[round(x/t[0]*100,2) for x in t]; out['nifty']=[round(x/n[0]*100,2) for x in n]
out['tclose']=t
out['rb']=[(round(d.cell(row=r,column=10).value,3) if isinstance(d.cell(row=r,column=10).value,(int,float)) else None) for r in range(5,1828)]
out['dd']=[round(d.cell(row=r,column=15).value,4) for r in range(5,1828)]
S=D0['shocks']; REG=D0['shock_reg']; ES=D0['es'][1:9]; RET=D0['ret'][1:9]; ROB=D0['rob'][1:9]
chan={'S1':'Demand / liquidity: stores shut, discretionary spend collapses','S2':'Monetary and fiscal relief: repo cut to 4.00%, stimulus','S3':'Demand: regional lockdowns in the second wave','S4':'Commodity and geopolitical: gold, oil, risk-off','S5':'Cost of capital: repo rate 4.00% to 6.50%','S6':'Governance and sentiment: market-wide shock','S7':'Trade: US tariffs on India, export sentiment','S8':'Commodity and geopolitical: gold, oil, rates'}
out['shocks']=[]
for i in range(8):
    s=S[i]; r=REG[i]; e=ES[i]; rt=RET[i]; rb=ROB[i]
    out['shocks'].append(dict(id=s[0],name=s[1],date=r[3],feat=r[5]==1,chan=chan[s[0]],pre=s[2],post=s[3],chg=s[4],se=s[5],t=s[6],df=s[7],p=s[8],lo=s[9],hi=s[10],verdict=s[11],ciPre=s[19],ciPost=s[20],car=e[9],carP=e[11],car5=e[12],car5P=e[14],car21=e[15],
        titanPre=rt[2],titanPost=rt[3],niftyPre=rt[4],niftyPost=rt[5],volPre=rt[9],volPost=rt[10],specs=rb[2:11],valid=rb[11],same=rb[12],alphaPre=s[14],alphaPost=s[15],r2pre=s[16],r2post=s[17]))
out['specNames']=['Base (6m)','3-month','12-month','Exclude +-5d','Exclude +-10d','Rf = 0','Rf = repo','Rf = 10Y G-sec','Weekly']
# event study paths
es=wb['EventStudy']
paths={}
for r in range(19,19+8*21):
    sid=es.cell(row=r,column=1).value; k=es.cell(row=r,column=2).value; car=es.cell(row=r,column=9).value
    if sid: paths.setdefault(sid,[]).append([k,round(car,5)])
out['car']=paths
def row(name,label,col0=2,n=8):
    ws=wb[name]
    for r in range(1,ws.max_row+1):
        v=ws.cell(row=r,column=1).value
        if isinstance(v,str) and v.startswith(label): return [ws.cell(row=r,column=c).value for c in range(col0,col0+n)]
    raise KeyError(label)
FY=['FY19','FY20','FY21','FY22','FY23','FY24','FY25','FY26']
R=lambda l:row('Ratios',l); W=lambda l:row('WACC',l)
out['fy']=FY
out['ratios']=dict(gfa=R('Gross fixed assets / total'),capex=R('Capex (cash)'),capexdep=R('Capex / depreciation'),de1=R('D/E - borrowings only'),de2=R('D/E - borrowings + gold on loan'),de3=R('D/E - borrowings + gold on loan + leases'),
  cov=R('Interest coverage = EBIT'),cov4=R('Operating EBIT / finance'),payout=R('Dividend payout'),dps=R('Dividend per share'),eps=R('EPS (Rs)'),liqb=R('Cash reserves / borrowings'),fcf=R('Free cash flow'),liq=R('Cash reserves: cash'),
  borrow=R('Borrowings (non-current'),gold=R('Gold on loan,'),lease=R('Lease liabilities'),goldinv=R('Gold on loan / inventories'),st=R('Short-term share'),invd=R('Inventory days'),roe=R('ROE'),divpd=R('Dividends paid in the year'),opm=R('Operating EBIT margin'))
out['wacc']=dict(beta=W('Raw beta'),badj=W('Blume-adjusted'),ke=W('Cost of equity'),kd=W('Pre-tax cost of debt'),wacc=W('WACC'),roic=W('ROIC ='),spread=W('ROIC - WACC'),eva=W('EVA ='),pe=W('P/E'),pb=W('Price / book'),mcap=W('Market capitalisation'))
v=D0['verdict'][1:9]
out['value']=[dict(fy=x[0].split(' ')[0],tsr=x[2],nifty=x[3],ke=x[5],exKe=x[6],exVal=x[7],alpha=x[8],spread=x[9],eva=x[10],mv=x[11],fv=x[12],comb=x[13],shocks=x[1]) for x in v]
# scenarios
ws=wb['Scenarios']; cases={}
cur=None
for r in range(24,ws.max_row+1):
    a=ws.cell(row=r,column=1).value
    if isinstance(a,str) and a.startswith('Case '): cur=a[5]; cases[cur]=dict(name=a[8:]); continue
    if cur and isinstance(a,str):
        key={'Revenue (Rs cr)':'rev','Interest cover':'cover','D/E (all debt)':'de','ROIC (NOPAT':'roic','EVA = (ROIC':'eva','Total debt incl.':'debt','Borrowings (plug':'bor','Free cash flow to firm':'fcff','Profit after tax':'pat','Dividends paid':'div','Cash reserves':'cash'}
        for k,vv in key.items():
            if a.startswith(k) and vv not in cases[cur]: cases[cur][vv]=[ws.cell(row=r,column=c).value for c in range(2,8)]
out['scen']=cases
out['scenSummary']=[[ws.cell(row=r,column=c).value for c in range(10,15)] for r in range(5,16)]
cf=wb['Counterfactual']
out['curve']=[[cf.cell(row=r,column=c).value for c in (1,4,6,7,8,9,10)] for r in range(14,27)]
out['cfBase']=dict(repricing=cf['B61'].value,ebit=cf['C11'].value,fin=wb['Financials']['I'+str([r for r in range(1,60) if wb['Financials'].cell(row=r,column=1).value=='Finance costs (total)'][0] if any(wb['Financials'].cell(row=r,column=1).value=='Finance costs (total)' for r in range(1,60)) else 1)].value if False else None)
# base constants
fin=wb['Financials']
def frow(lbl):
    for r in range(1,70):
        v=fin.cell(row=r,column=1).value
        if isinstance(v,str) and v.startswith(lbl): return [fin.cell(row=r,column=c).value for c in range(2,10)]
out['cfBase']=dict(repricing=cf['B61'].value,ebit=cf['C11'].value,fin=frow('Finance costs')[-1],eps=frow('Basic EPS')[-1],tax=wb['Inputs']['B13'].value,shares=wb['Inputs']['B14'].value)
out['rob']=D0['rob']
out['kpi']=dict(titanRet=out['tclose'][-1]/out['tclose'][0]-1,niftyRet=out['nifty'][-1]/100-1,beta=wb['TSR_Alpha']['B20'].value,alpha=wb['TSR_Alpha']['B22'].value,cagrT=wb['TSR_Alpha']['G16'].value,cagrN=wb['TSR_Alpha']['H16'].value,cumT=wb['TSR_Alpha']['D16'].value,cumN=wb['TSR_Alpha']['E16'].value,exVal=wb['Verdict']['H14'].value,eva=wb['Verdict']['K14'].value,rbMean=wb['Rolling']['B'+str(1)].value if False else None)
json.dump(out,open('data.js','w'),default=str)
print({k:(len(v) if hasattr(v,'__len__') else v) for k,v in out.items()}); print(out['cfBase']); print(list(cases['A'].keys())); print(out['kpi'])
