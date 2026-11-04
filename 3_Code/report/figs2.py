import json, datetime as dt, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
D=json.load(open('/home/claude/dash/data.js'))
B,O,G,N,T,P='#2A78D6','#EB6834','#8A8F98','#1F3864','#2CA58D','#9467BD'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#9aa0a6','axes.titlesize':9,'axes.titleweight':'bold','axes.titlecolor':N})
dates=[dt.datetime.strptime(d,'%Y-%m-%d') for d in D['dates']]; rb=[np.nan if v is None else v for v in D['rb']]
SH=D['shocks']
# fig5 rolling beta
fig,ax=plt.subplots(figsize=(7.2,2.4),dpi=220)
ax.plot(dates,rb,color=B,lw=1.2); ax.axhline(1,color=G,lw=0.8,ls='--')
for s in SH:
    d=dt.datetime.strptime(s['date'],'%Y-%m-%d'); f=s['feat']
    ax.axvline(d,color=O if f else '#c9ccd1',lw=1.1 if f else 0.7,ls='-' if f else '--',zorder=0)
    ax.text(d,1.52,s['id'],ha='center',va='top',fontsize=7,color=O if f else G,fontweight='bold' if f else 'normal')
ax.set_ylim(0.2,1.55); ax.set_ylabel('Rolling 126-day beta'); ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y')); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,7)))
ax.grid(axis='y',color='#e6e8eb',lw=0.5); plt.tight_layout(); plt.savefig('fig5.png'); plt.close()
# fig6 CAR paths
fig,axs=plt.subplots(1,3,figsize=(7.2,2.1),dpi=220,sharey=True)
for ax,sid in zip(axs,['S1','S5','S8']):
    s=[x for x in SH if x['id']==sid][0]; p=D['car'][sid]
    ax.plot([a for a,b in p],[b*100 for a,b in p],color=B,lw=1.3); ax.axhline(0,color=G,lw=0.7,ls='--'); ax.axvline(0,color=O,lw=0.9)
    ax.set_title(f"{sid}: CAR[-1,+1] = {s['car']*100:+.1f}% (p = {s['carP']:.2f})",fontsize=7.5); ax.set_xlabel('Days from event',fontsize=7); ax.grid(axis='y',color='#e6e8eb',lw=0.5)
axs[0].set_ylabel('Cumulative abnormal return (%)'); plt.tight_layout(); plt.savefig('fig6.png'); plt.close()
# fig7 WACC curve + rate stress
cv=D['curve']; B0=D['cfBase']
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.2,2.4),dpi=220)
w=[r[0]*100 for r in cv]; wc=[r[3]*100 for r in cv]; ok=[r[6]=='Yes' for r in cv]
a1.plot(w,wc,color=G,lw=1); a1.scatter([x for x,o in zip(w,ok) if o],[y for y,o in zip(wc,ok) if o],color=B,s=14,zorder=3,label='cover at least 5x'); a1.scatter([x for x,o in zip(w,ok) if not o],[y for y,o in zip(wc,ok) if not o],color=O,s=14,zorder=3,label='cover below 5x')
a1.set_xlabel('Debt / (debt + equity), %'); a1.set_ylabel('WACC, %'); a1.set_title('WACC vs leverage (illustrative)'); a1.legend(frameon=False,fontsize=6.5); a1.grid(axis='y',color='#e6e8eb',lw=0.5)
bp=np.arange(0,401,25)
for h,c,l in [(0,O,'unhedged'),(0.5,P,'50% hedged'),(0.75,B,'75% hedged')]:
    a2.plot(bp,[B0['ebit']/(B0['fin']+b/1e4*B0['repricing']*(1-h)) for b in bp],color=c,lw=1.3,label=l)
a2.axhline(5,color=G,lw=0.8,ls='--'); a2.text(5,5.1,'5x floor',fontsize=6.5,color=G); a2.axvline(250,color='#c9ccd1',lw=0.7,ls=':'); a2.text(252,max(7,B0['ebit']/B0['fin'])-0.5,'2022 cycle',fontsize=6.5,color=G)
a2.set_xlabel('Rate shock (bp)'); a2.set_ylabel('Interest cover (x)'); a2.set_title('Cover under a rate shock, FY26 base'); a2.legend(frameon=False,fontsize=6.5); a2.grid(axis='y',color='#e6e8eb',lw=0.5)
plt.tight_layout(); plt.savefig('fig7.png'); plt.close()
# fig8 scenarios
xs=['FY26','FY27','FY28','FY29','FY30','FY31']; col={'A':B,'B':T,'C':O,'D':P}; ls={'A':'-','B':'-','C':'--','D':'--'}; nm={'A':'A status quo','B':'B recommended','C':'C status quo, stress','D':'D recommended, stress'}
fig,axs=plt.subplots(1,3,figsize=(7.2,2.3),dpi=220)
for ax,k,t in zip(axs,['cover','de','eva'],['Interest cover (x)','D/E, all debt (x)','EVA (Rs cr)']):
    for c in 'ABCD': ax.plot(xs,D['scen'][c][k],color=col[c],ls=ls[c],lw=1.3,marker='o',ms=2.5,label=nm[c])
    ax.set_title(t,fontsize=8); ax.grid(axis='y',color='#e6e8eb',lw=0.5); ax.tick_params(axis='x',labelsize=6.5)
axs[0].axhline(5,color=G,lw=0.8,ls='--'); axs[1].axhline(2,color=G,lw=0.8,ls='--'); axs[2].axhline(0,color=G,lw=0.6)
axs[0].legend(frameon=False,fontsize=6,loc='upper left'); plt.tight_layout(); plt.savefig('fig8.png'); plt.close()
print(D['scen']['A']['eva'],D['scen']['C']['eva'])
