import json, datetime as dt, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
D=json.load(open('data.json'))
B,O,G,N='#2A78D6','#EB6834','#8A8F98','#1F3864'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#9aa0a6','axes.titlesize':9,'axes.titleweight':'bold','axes.titlecolor':N})
px=D['prices']; dates=[dt.datetime.strptime(p[0],'%Y-%m-%d') for p in px]
t=np.array([p[1] for p in px]); n=np.array([p[2] for p in px]); ti=t/t[0]*100; ni=n/n[0]*100
fig,ax=plt.subplots(figsize=(7.2,2.7),dpi=220)
ax.plot(dates,ti,color=B,lw=1.3,label='Titan'); ax.plot(dates,ni,color=G,lw=1.3,label='NIFTY 500 (price index)')
feat={'S1','S5','S8'}
for s in D['shock_reg']:
    d=dt.datetime.strptime(s[3],'%Y-%m-%d'); i=min(range(len(dates)),key=lambda k:abs((dates[k]-d).days))
    f=s[0] in feat
    ax.axvline(d,color=O if f else '#c9ccd1',lw=1.1 if f else 0.7,ls='-' if f else '--',zorder=0)
    ax.text(d,455,s[0],ha='left' if s[0]=='S2' else ('right' if s[0]=='S1' else 'center'),va='top',fontsize=7,color=O if f else G,fontweight='bold' if f else 'normal')
ax.set_ylim(40,470); ax.set_ylabel('Index (1 Jul 2019 = 100)'); ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0.0,0.86),ncol=2)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y')); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
ax.grid(axis='y',color='#e6e8eb',lw=0.5); plt.tight_layout(); plt.savefig('fig1.png'); plt.close()
# fig2 beta pre/post with CI
S=D['shocks']; ids=[s[0] for s in S]; pre=[s[2] for s in S]; post=[s[3] for s in S]; cip=[s[19] for s in S]; ciq=[s[20] for s in S]; p=[s[8] for s in S]
fig,ax=plt.subplots(figsize=(3.55,2.7),dpi=220); x=np.arange(8); w=0.38
ax.bar(x-w/2,pre,w,color=G,label='6 months before'); ax.bar(x+w/2,post,w,color=B,label='6 months after')
ax.errorbar(x-w/2,pre,yerr=cip,fmt='none',ecolor=N,lw=0.8,capsize=1.5); ax.errorbar(x+w/2,post,yerr=ciq,fmt='none',ecolor=N,lw=0.8,capsize=1.5)
ax.axhline(1,color=O,lw=0.9,ls='--'); ax.set_xticks(x); ax.set_xticklabels([f'{i}\n{"**" if q<0.01 else ("*" if q<0.1 else "")}' for i,q in zip(ids,p)],fontsize=7)
ax.set_ylabel('CAPM beta (95% CI)'); ax.set_title('Beta before vs after each shock'); ax.legend(frameon=False,fontsize=6.5,loc='upper left',ncol=1); ax.set_ylim(0,2.25); ax.grid(axis='y',color='#e6e8eb',lw=0.5)
plt.tight_layout(); plt.savefig('fig2.png'); plt.close()
# fig3 policy panels
def row(k,key):
    for r in D[k]:
        if r[0] and str(r[0]).startswith(key): return r[1:9]
fy=['FY19','FY20','FY21','FY22','FY23','FY24','FY25','FY26']
de=row('ratios','D/E - borrowings + gold on loan + leases'); de1=row('ratios','D/E - borrowings only'); cov=row('ratios','Interest coverage = EBIT'); gfa=row('ratios','Gross fixed assets / total'); pay=row('ratios','Dividend payout')
roic=row('wacc','ROIC ='); wacc=row('wacc','WACC')
fig,axs=plt.subplots(1,3,figsize=(7.2,2.2),dpi=220)
a=axs[0]; a.plot(fy[1:],de[1:],color=B,marker='o',ms=3,label='All debt (incl. gold, leases)'); a.plot(fy[1:],de1[1:],color=G,marker='o',ms=3,label='Borrowings only'); a.set_title('Debt / equity (x)'); a.legend(frameon=False,fontsize=6,loc='upper left')
a=axs[1]; a.plot(fy[1:],cov[1:],color=O,marker='o',ms=3); a.axhline(5,color=G,ls='--',lw=0.8); a.text(6.2,5.4,'5x floor',fontsize=6,color=G,ha='right'); a.set_title('Interest cover, EBIT / finance costs (x)')
a=axs[2]; a.plot(fy[1:],[v for v in roic[1:]],color=B,marker='o',ms=3,label='ROIC'); a.plot(fy[1:],[v for v in wacc[1:]],color=O,marker='o',ms=3,label='WACC'); a.set_title('ROIC vs WACC'); a.legend(frameon=False,fontsize=6.5,loc='upper right'); a.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1,decimals=0))
for a in axs: a.tick_params(labelsize=6.5); a.grid(axis='y',color='#e6e8eb',lw=0.5); a.set_xticks(range(len(a.get_lines()[0].get_xdata()))); a.tick_params(axis='x',labelrotation=45)
plt.tight_layout(); plt.savefig('fig3.png'); plt.close()
# fig4 value: excess over Ke by year + EVA
V=D['verdict'][1:9]; lab=[v[0].split(' ')[0]+('*' if 'FY20' in v[0] or 'FY27' in v[0] else '') for v in V]
exv=[v[7]/1000 for v in V]
fig,ax=plt.subplots(figsize=(3.55,2.3),dpi=220)
ax.bar(lab,exv,color=[B if e>0 else O for e in exv],width=0.6); ax.axhline(0,color='#666',lw=0.6); ax.set_title('Excess value over cost of equity (Rs 000 cr)'); ax.tick_params(labelsize=6.5); ax.grid(axis='y',color='#e6e8eb',lw=0.5)
plt.tight_layout(); plt.savefig('fig4.png'); plt.close()
print('ok')
