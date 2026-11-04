import json, numpy as np, statsmodels.api as sm
from openpyxl import load_workbook
wb=load_workbook('/home/claude/wai/t5r.xlsx',data_only=True)
d=wb['Data']; sh=wb['Shocks']
y=np.array([d.cell(row=r,column=8).value for r in range(1,1828)],dtype=object); x=np.array([d.cell(row=r,column=9).value for r in range(1,1828)],dtype=object)
out=[]
for i in range(8):
    a=6+2*i; res={}
    seg={}
    for k,rr in (('pre',a),('post',a+1)):
        f,l=sh.cell(row=rr,column=6).value,sh.cell(row=rr,column=7).value
        yy=np.array(y[f-1:l],float); xx=np.array(x[f-1:l],float); seg[k]=(yy,xx)
        b,a0=np.polyfit(xx,yy,1); res[k]=float(b); res[k+'_n']=len(yy)
    Y=np.concatenate([seg['pre'][0],seg['post'][0]]); X=np.concatenate([seg['pre'][1],seg['post'][1]]); D=np.concatenate([np.zeros(len(seg['pre'][0])),np.ones(len(seg['post'][0]))])
    m=sm.OLS(Y,sm.add_constant(np.column_stack([X,D,D*X]))).fit()
    res['dummy_d']=float(m.params[3]); res['dummy_t']=float(m.tvalues[3]); res['dummy_p']=float(m.pvalues[3])
    out.append(res)
json.dump(out,open('/home/claude/wai/pyvals.json','w'),indent=1); print(out[0],out[7])
