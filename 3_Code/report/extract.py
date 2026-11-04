import json, datetime as dt
from openpyxl import load_workbook
wb=load_workbook('/home/claude/out/Titan_WAI_Analysis.xlsx',data_only=True)
def f(v):
    return v.strftime('%Y-%m-%d') if isinstance(v,(dt.datetime,dt.date)) else v
D={}
d=wb['Data']
D['prices']=[[f(d.cell(row=r,column=1).value),d.cell(row=r,column=2).value,d.cell(row=r,column=3).value,d.cell(row=r,column=10).value] for r in range(5,1828)]
s=wb['Shocks']
D['shocks']=[[f(s.cell(row=r,column=c).value) for c in range(1,22)] for r in range(26,34)]
D['shock_regr']=[[f(s.cell(row=r,column=c).value) for c in range(1,21)] for r in range(6,22)]
inp=wb['Inputs']
D['shock_reg']=[[f(inp.cell(row=r,column=c).value) for c in range(1,9)] for r in range(23,31)]
def grid(name,r0,r1,c1):
    ws=wb[name]; return [[f(ws.cell(row=r,column=c).value) for c in range(1,c1+1)] for r in range(r0,r1+1)]
D['ratios']=grid('Ratios',4,70,9); D['wacc']=grid('WACC',4,50,9); D['tsr']=grid('TSR_Alpha',4,24,20)
D['verdict']=grid('Verdict',4,16,14); D['cf']=grid('Counterfactual',4,110,12); D['scen']=grid('Scenarios',4,130,14)
D['es']=grid('EventStudy',5,13,17); D['rob']=grid('Robustness',5,13,15); D['ret']=grid('Returns',4,14,17)
D['fin']=grid('Financials',4,60,10)
json.dump(D,open('data.json','w'),default=str)
for k in ('shocks','es','ret'):
    print(k)
    for r in D[k]: print([round(x,3) if isinstance(x,float) else x for x in r])
