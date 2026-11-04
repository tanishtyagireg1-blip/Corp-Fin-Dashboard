# ======================================================= chart helpers
from openpyxl.chart.legend import LegendEntry
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, Font as DFont
SER=['2A78D6','EB6834','8A8F98','1F3864','2CA58D','9467BD','D62728','7F7F7F']
def axfont(ax,sz=900):
    ax.txPr=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=sz,latin=DFont(typeface=FONT))),endParaRPr=CharacterProperties())])
def style_chart(ch,ttl,xt=None,yt=None,w=22,h=9.5):
    ch.title=ttl; ch.width=w; ch.height=h
    if xt: ch.x_axis.title=xt
    if yt: ch.y_axis.title=yt
    ch.x_axis.delete=False; ch.y_axis.delete=False
    ch.y_axis.majorGridlines.spPr=GraphicalProperties(ln=None);
    from openpyxl.drawing.line import LineProperties
    ch.y_axis.majorGridlines.spPr=GraphicalProperties(ln=LineProperties(solidFill='E3E6EA',w=6350))
    axfont(ch.x_axis); axfont(ch.y_axis)
    if ch.legend is not None: ch.legend.position='b'
    ch.x_axis.tickLblPos='low'
def line_ser(ws,xcol,ycol,r0,r1,name,color,w=15875,dash=None,xws=None):
    xr=Reference(xws or ws,min_col=xcol,min_row=r0,max_row=r1); yr=Reference(ws,min_col=ycol,min_row=r0,max_row=r1)
    s=Series(yr,xr,title=name); s.marker.symbol='none'; s.smooth=False
    s.graphicalProperties.line.solidFill=color; s.graphicalProperties.line.width=w
    if dash: s.graphicalProperties.line.dashStyle=dash
    return s
def mark_ser(xws,xcol,xr0,ycol_ws,ycol,yr0,name,color,sym='diamond',size=9,label=True,yws=None):
    xr=Reference(xws,min_col=xcol,min_row=xr0,max_row=xr0); yr=Reference(yws or ycol_ws,min_col=ycol,min_row=yr0,max_row=yr0)
    s=Series(yr,xr,title=name); s.marker=Marker(symbol=sym,size=size); s.marker.graphicalProperties=GraphicalProperties(solidFill=color)
    s.graphicalProperties.line.noFill=True
    if label:
        s.dLbls=DataLabelList(); s.dLbls.showSerName=True; s.dLbls.showVal=False; s.dLbls.showCatName=False; s.dLbls.showLegendKey=False; s.dLbls.position='t'
        s.dLbls.txPr=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=CharacterProperties(sz=800,b=True,solidFill=color,latin=DFont(typeface=FONT))),endParaRPr=CharacterProperties())])
    return s
def hide_legend_from(ch,k,total):
    ch.legend.legendEntry=[LegendEntry(idx=i,delete=True) for i in range(k,total)]
D0,D1=43647,46700   # axis date serial bounds

# ======================================================= PRICE TREND
wp=sheet('PriceTrend','2A78D6')
title(wp,'Task 2(a): price trend, Titan vs NIFTY 500, with shock dates','Indexed to 100 on 1 Jul 2019. Markers show the eight shock event days (labels = shock ID, see Inputs).')
hdr(wp,4,1,['ID','Event day','Titan index at event','NIFTY index at event','Titan drawdown at event','Titan relative index at event'],h=42)
for i in range(NS):
    r=5+i; ir=23+i
    put(wp,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(wp,f'B{r}',f'=Inputs!E{ir}',F_LINK,nf=NF_D,al=AL_C)
    pos=f'MATCH(B{r},Data!{DR},0)'
    put(wp,f'C{r}',f'=INDEX(Data!$K${R0}:$K${R1},{pos})',F_LINK,nf='0.0'); put(wp,f'D{r}',f'=INDEX(Data!$L${R0}:$L${R1},{pos})',F_LINK,nf='0.0')
    put(wp,f'E{r}',f'=INDEX(Data!$O${R0}:$O${R1},{pos})',F_LINK,nf=NF_PCT); put(wp,f'F{r}',f'=INDEX(Data!$M${R0}:$M${R1},{pos})',F_LINK,nf='0.0')
# calendar-year table
sec(wp,15,'Calendar-year price returns (price only; dividends excluded - see TSR_Alpha for total return)',1,8)
hdr(wp,16,1,['Period','Start date (base close)','End date','Titan start','Titan end','Titan return','NIFTY 500 return','Titan minus NIFTY'],h=34)
cal=[('2019 (Jul-Dec)',None,'2019-12-31'),('2020','2019-12-31','2020-12-31'),('2021','2020-12-31','2021-12-31'),('2022','2021-12-31','2022-12-31'),('2023','2022-12-31','2023-12-31'),
     ('2024','2023-12-31','2024-12-31'),('2025','2024-12-31','2025-12-31'),('2026 YTD (to 4 Nov)','2025-12-31','2026-12-31')]
for k,(lab,s,e) in enumerate(cal):
    r=17+k
    put(wp,f'A{r}',lab,F_B)
    if s is None: put(wp,f'B{r}',f'=Data!$A${R0}',F_LINK,nf=NF_D,al=AL_C)
    else: put(wp,f'B{r}',dt.datetime.strptime(s,'%Y-%m-%d'),F_IN,nf=NF_D,al=AL_C)
    put(wp,f'C{r}',dt.datetime.strptime(e,'%Y-%m-%d'),F_IN,nf=NF_D,al=AL_C)
    ps=f'MATCH(B{r},Data!{DR},1)'; pe=f'MATCH(C{r},Data!{DR},1)'
    put(wp,f'D{r}',f'=INDEX(Data!$B${R0}:$B${R1},{ps})',F_LINK,nf='#,##0'); put(wp,f'E{r}',f'=INDEX(Data!$B${R0}:$B${R1},{pe})',F_LINK,nf='#,##0')
    put(wp,f'F{r}',f'=E{r}/D{r}-1',nf=NF_PCTS); put(wp,f'G{r}',f'=INDEX(Data!$C${R0}:$C${R1},{pe})/INDEX(Data!$C${R0}:$C${R1},{ps})-1',nf=NF_PCTS)
    put(wp,f'H{r}',f'=F{r}-G{r}',nf='+0.0%;-0.0%;0.0%',bold=True)
put(wp,'A26','Whole period',F_B); put(wp,'B26',f'=Data!$A${R0}',F_LINK,nf=NF_D,al=AL_C); put(wp,'C26',f'=Data!$A${R1}',F_LINK,nf=NF_D,al=AL_C)
put(wp,'D26',f'=Data!$B${R0}',F_LINK,nf='#,##0'); put(wp,'E26',f'=Data!$B${R1}',F_LINK,nf='#,##0'); put(wp,'F26','=E26/D26-1',nf=NF_PCTS)
put(wp,'G26',f'=Data!$C${R1}/Data!$C${R0}-1',nf=NF_PCTS); put(wp,'H26','=F26-G26',nf='+0.0%;-0.0%;0.0%',bold=True)
for c in range(1,9): wp.cell(row=26,column=c).border=Border(top=Side(style='thin',color='7F7F7F'))
put(wp,'A27','Annualised (CAGR)',F_B); put(wp,'F27',f'=(1+F26)^(365.25/(C26-B26))-1',nf=NF_PCT); put(wp,'G27',f'=(1+G26)^(365.25/(C26-B26))-1',nf=NF_PCT); put(wp,'H27','=F27-G27',nf='+0.0%;-0.0%;0.0%',bold=True)
# chart 1: indexed price with shock markers
ch=ScatterChart(); ch.style=2; ch.scatterStyle='lineMarker'
ch.series.append(line_ser(wd,1,11,R0,R1,'Titan Company',BLUE,19050)); ch.series.append(line_ser(wd,1,12,R0,R1,'NIFTY 500',GREY,15875))
for i in range(NS):
    ch.series.append(mark_ser(wp,2,5+i,wp,3,5+i,f'S{i+1}',ORANGE))
style_chart(ch,'Titan vs NIFTY 500, indexed (100 = 1 Jul 2019), with shock event days','Date','Index level',w=24,h=10.5)
ch.x_axis.number_format='mmm-yy'; ch.x_axis.scaling.min=D0; ch.x_axis.scaling.max=D1; ch.x_axis.majorUnit=365.25; ch.y_axis.scaling.min=0
hide_legend_from(ch,2,2+NS); wp.add_chart(ch,'A29')
# chart 2: relative performance
ch2=ScatterChart(); ch2.style=2
ch2.series.append(line_ser(wd,1,13,R0,R1,'Titan relative to NIFTY 500 (100 = start)',BLUE,19050))
ch2.series.append(line_ser(wd,1,13,R0,R0+1,'',GREY))  # placeholder removed below
ch2.series.pop()
for i in range(NS): ch2.series.append(mark_ser(wp,2,5+i,wp,6,5+i,f'S{i+1}',ORANGE))
style_chart(ch2,'Relative performance: Titan index / NIFTY 500 index','Date','Relative index',w=24,h=9)
ch2.x_axis.number_format='mmm-yy'; ch2.x_axis.scaling.min=D0; ch2.x_axis.scaling.max=D1; ch2.x_axis.majorUnit=365.25; ch2.y_axis.scaling.min=60
hide_legend_from(ch2,1,1+NS); wp.add_chart(ch2,'A51')
# chart 3: drawdowns
ch3=ScatterChart(); ch3.style=2
ch3.series.append(line_ser(wd,1,15,R0,R1,'Titan drawdown',BLUE,15875)); ch3.series.append(line_ser(wd,1,16,R0,R1,'NIFTY 500 drawdown',GREY,15875))
style_chart(ch3,'Drawdown from running peak','Date','Drawdown',w=24,h=8.5)
ch3.x_axis.number_format='mmm-yy'; ch3.x_axis.scaling.min=D0; ch3.x_axis.scaling.max=D1; ch3.x_axis.majorUnit=365.25; ch3.y_axis.number_format='0%'
wp.add_chart(ch3,'A71')
# chart 4: calendar-year bars
ch4=BarChart(); ch4.type='col'; ch4.grouping='clustered'
ch4.add_data(Reference(wp,min_col=6,min_row=16,max_row=24),titles_from_data=True); ch4.add_data(Reference(wp,min_col=7,min_row=16,max_row=24),titles_from_data=True)
ch4.set_categories(Reference(wp,min_col=1,min_row=17,max_row=24))
ch4.series[0].graphicalProperties.solidFill=BLUE; ch4.series[1].graphicalProperties.solidFill=GREY
style_chart(ch4,'Calendar-year price return: Titan vs NIFTY 500',None,'Return',w=16,h=8.5); ch4.y_axis.number_format='0%'
wp.add_chart(ch4,'K4')
widths(wp,{'A':22,'B':16,'C':16,'D':14,'E':14,'F':14,'G':15,'H':15})

# ======================================================= ROLLING BETA
wr=sheet('Rolling','C00000')
title(wr,'Task 2(b): rolling beta (126-day window) with shock markers','Beta of Titan vs NIFTY 500 over a trailing window (Inputs!B8). Dashed line = market beta of 1.')
hdr(wr,4,1,['ID','Event day','Rolling beta at event','Beta = 1 line (x)','Beta = 1 line (y)'],h=34)
for i in range(NS):
    r=5+i; ir=23+i
    put(wr,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(wr,f'B{r}',f'=Inputs!E{ir}',F_LINK,nf=NF_D,al=AL_C)
    put(wr,f'C{r}',f'=INDEX(Data!$J${R0}:$J${R1},MATCH(B{r},Data!{DR},0))',F_LINK,nf=NF_B)
put(wr,'D5',D0,F_IN,nf=NF_D); put(wr,'D6',D1-60,F_IN,nf=NF_D); put(wr,'E5',1,F_IN); put(wr,'E6',1,F_IN)
put(wr,'A15','Rolling-beta statistics',F_SEC)
labs=[('Mean rolling beta',f'=AVERAGE(Data!$J$131:$J${R1})',NF_B),('Minimum',f'=MIN(Data!$J$131:$J${R1})',NF_B),('Maximum',f'=MAX(Data!$J$131:$J${R1})',NF_B),
      ('Latest (4 Nov 2026)',f'=Data!$J${R1}',NF_B),('Days with beta > 1',f'=COUNTIF(Data!$J$131:$J${R1},">1")',"0"),('Share of days with beta > 1',f'=COUNTIF(Data!$J$131:$J${R1},">1")/COUNT(Data!$J$131:$J${R1})',NF_PCT)]
for k,(l,f,nf) in enumerate(labs):
    put(wr,f'A{16+k}',l); put(wr,f'C{16+k}',f,F_LINK,nf=nf,al=AL_C)
chr_=ScatterChart(); chr_.style=2
chr_.series.append(line_ser(wd,1,10,131,R1,'Rolling beta (126d)',BLUE,19050))
xr=Reference(wr,min_col=4,min_row=5,max_row=6); yr=Reference(wr,min_col=5,min_row=5,max_row=6)
s1=Series(yr,xr,title='Beta = 1'); s1.marker.symbol='none'; s1.graphicalProperties.line.solidFill=GREY; s1.graphicalProperties.line.dashStyle='dash'; s1.graphicalProperties.line.width=12700; chr_.series.append(s1)
for i in range(NS): chr_.series.append(mark_ser(wr,2,5+i,wr,3,5+i,f'S{i+1}',ORANGE))
style_chart(chr_,'Titan rolling beta vs NIFTY 500 (trailing 126 trading days)','Date','Beta',w=24,h=11)
chr_.x_axis.number_format='mmm-yy'; chr_.x_axis.scaling.min=43800; chr_.x_axis.scaling.max=D1; chr_.x_axis.majorUnit=365.25; chr_.y_axis.scaling.min=0; chr_.y_axis.number_format='0.0'
hide_legend_from(chr_,2,2+NS); wr.add_chart(chr_,'A24')
widths(wr,{'A':28,'B':14,'C':20,'D':16,'E':16})

# ======================================================= BETA CHARTS
wbc=sheet('Beta_Charts','C00000')
title(wbc,'Task 2(b): beta before vs after each shock (with 95% confidence intervals)','Whiskers are 95% confidence intervals around each beta. Featured shocks (deep-dive) are S1, S5, S8.')
hdr(wbc,4,1,['ID','Shock','Beta pre','Beta post','Change','p-value','Verdict','CI half-width pre','CI half-width post'],h=34)
for i in range(NS):
    r=5+i; sr=26+i
    put(wbc,f'A{r}',f'=Shocks!A{sr}',F_LINK,al=AL_C); put(wbc,f'B{r}',f'=Shocks!B{sr}',F_LINK)
    put(wbc,f'C{r}',f'=Shocks!C{sr}',F_LINK,nf=NF_B); put(wbc,f'D{r}',f'=Shocks!D{sr}',F_LINK,nf=NF_B); put(wbc,f'E{r}',f'=Shocks!E{sr}',F_LINK,nf='+0.00;-0.00;0.00')
    put(wbc,f'F{r}',f'=Shocks!I{sr}',F_LINK,nf=NF_P); put(wbc,f'G{r}',f'=Shocks!L{sr}',F_LINK); put(wbc,f'H{r}',f'=Shocks!T{sr}',F_LINK,nf=NF_B); put(wbc,f'I{r}',f'=Shocks!U{sr}',F_LINK,nf=NF_B)
chb=BarChart(); chb.type='col'; chb.grouping='clustered'; chb.gapWidth=60
chb.add_data(Reference(wbc,min_col=3,min_row=4,max_row=12),titles_from_data=True); chb.add_data(Reference(wbc,min_col=4,min_row=4,max_row=12),titles_from_data=True)
chb.set_categories(Reference(wbc,min_col=1,min_row=5,max_row=12))
chb.series[0].graphicalProperties.solidFill=GREY; chb.series[1].graphicalProperties.solidFill=BLUE
for sr_,col in ((chb.series[0],'H'),(chb.series[1],'I')):
    eb=ErrorBars(errDir='y',errBarType='both',errValType='cust',noEndCap=False)
    eb.plus=NumDataSource(numRef=NumRef(f=f"'Beta_Charts'!${col}$5:${col}$12")); eb.minus=NumDataSource(numRef=NumRef(f=f"'Beta_Charts'!${col}$5:${col}$12"))
    sr_.errBars=eb
style_chart(chb,'Beta (pre-shock vs post-shock), 95% CI whiskers','Shock','Beta',w=22,h=10); chb.y_axis.scaling.min=0
wbc.add_chart(chb,'A15')
chd=BarChart(); chd.type='col'; chd.gapWidth=80
chd.add_data(Reference(wbc,min_col=5,min_row=4,max_row=12),titles_from_data=True); chd.set_categories(Reference(wbc,min_col=1,min_row=5,max_row=12))
chd.series[0].graphicalProperties.solidFill=ORANGE; chd.legend=None
chd.legend=None; style_chart(chd,'Change in beta (post minus pre)','Shock','Delta beta',w=14,h=10)
wbc.add_chart(chd,'M15')
widths(wbc,{'A':6,'B':38,'C':10,'D':10,'E':10,'F':10,'G':16,'H':14,'I':14})

# ======================================================= EVENT STUDY
we=sheet('EventStudy','C00000')
title(we,'Task 2(a)/(b): event study - market-model abnormal returns around each shock','AR(t) = R(Titan,t) - [alpha + beta x R(NIFTY,t)], market model estimated on days [-(gap+length), -gap]. CAR = cumulative abnormal return. t-test: CAR / (sigma x sqrt(days)).')
hdr(we,5,1,['ID','Shock','Event row (Data)','Estimation start row','Estimation end row','Alpha (daily)','Beta (market model)','Sigma (resid. s.d.)','Est. days','CAR [-1,+1]','t-stat','p-value','CAR [0,+5]','t-stat','p-value','CAR [-10,+10]','t-stat','p-value','AR on day 0','t-stat day 0'],h=44)
EL0=19   # long table first data row
for i in range(NS):
    r=6+i; ir=23+i
    put(we,f'A{r}',f'=Inputs!A{ir}',F_LINK,al=AL_C); put(we,f'B{r}',f'=Inputs!B{ir}',F_LINK)
    put(we,f'C{r}',f'=MATCH(Inputs!E{ir},Data!{DR},0)+4',F_LINK,al=AL_C)
    put(we,f'E{r}',f'=C{r}-{IN["gap"]}',al=AL_C); put(we,f'D{r}',f'=E{r}-{IN["estn"]}+1',al=AL_C); put(we,f'I{r}',f'=E{r}-D{r}+1',al=AL_C)
    y=rng('D',f'D{r}',f'E{r}'); x=rng('E',f'D{r}',f'E{r}')
    put(we,f'F{r}',f'=INTERCEPT({y},{x})',nf='0.0000%'); put(we,f'G{r}',f'=SLOPE({y},{x})',nf=NF_B); put(we,f'H{r}',f'=STEYX({y},{x})',nf='0.00%')
    a=EL0+21*i; b=a+20
    A_=f'$A${EL0}:$A${EL0+21*NS-1}'; B_=f'$B${EL0}:$B${EL0+21*NS-1}'; H_=f'$H${EL0}:$H${EL0+21*NS-1}'
    for (c1,c2,c3,lo,hi,L) in (('J','K','L',-1,1,3),('M','N','O',0,5,6),('P','Q','R',-10,10,21)):
        put(we,f'{c1}{r}',f'=SUMIFS({H_},{A_},A{r},{B_},">={lo}",{B_},"<={hi}")',nf='+0.0%;-0.0%;0.0%',bold=True)
        put(we,f'{c2}{r}',f'={c1}{r}/(H{r}*SQRT({L}))',nf='0.00'); put(we,f'{c3}{r}',f'=TDIST(ABS({c2}{r}),I{r}-2,2)',nf=NF_P)
    put(we,f'S{r}',f'=SUMIFS({H_},{A_},A{r},{B_},0)',nf='+0.0%;-0.0%;0.0%'); put(we,f'T{r}',f'=S{r}/H{r}',nf='0.00')
we.conditional_formatting.add('L6:L13',CellIsRule(operator='lessThan',formula=['0.05'],fill=FILL_G)); we.conditional_formatting.add('O6:O13',CellIsRule(operator='lessThan',formula=['0.05'],fill=FILL_G)); we.conditional_formatting.add('R6:R13',CellIsRule(operator='lessThan',formula=['0.05'],fill=FILL_G))
put(we,'A15','Green = abnormal return significant at 5%. Day-0 = first session on/after the event date. Overlapping shocks (e.g. S1/S2, S4/S5) share event windows - interpret CARs jointly.',F_SUB)
hdr(we,18,1,['ID','t (days from event)','Data row','Date','Titan return','NIFTY 500 return','Expected return','Abnormal return (AR)','CAR from t = -10','AR t-stat'],h=34)
for i in range(NS):
    pr=6+i
    for k,tt in enumerate(range(-10,11)):
        r=EL0+21*i+k
        put(we,f'A{r}',f'=$A${pr}',al=AL_C); put(we,f'B{r}',tt,F_IN,al=AL_C)
        put(we,f'C{r}',f'=$C${pr}+B{r}',al=AL_C); put(we,f'D{r}',f'=INDEX(Data!$A$1:$A${R1},C{r})',F_LINK,nf=NF_D)
        put(we,f'E{r}',f'=INDEX(Data!$D$1:$D${R1},C{r})',F_LINK,nf='0.00%'); put(we,f'F{r}',f'=INDEX(Data!$E$1:$E${R1},C{r})',F_LINK,nf='0.00%')
        put(we,f'G{r}',f'=$F${pr}+$G${pr}*F{r}',nf='0.00%'); put(we,f'H{r}',f'=E{r}-G{r}',nf='+0.00%;-0.00%;0.00%')
        put(we,f'I{r}',f'=H{r}' if k==0 else f'=I{r-1}+H{r}',nf='+0.0%;-0.0%;0.0%'); put(we,f'J{r}',f'=H{r}/$H${pr}',nf='0.00')
EP0=EL0+21*NS+4   # CAR path matrix
sec(we,EP0-2,'CAR paths (for charts): cumulative abnormal return from t = -10, by shock',1,10)
hdr(we,EP0-1,1,['t']+[f'S{k+1}' for k in range(NS)],h=20)
for k,tt in enumerate(range(-10,11)):
    r=EP0+k; put(we,f'A{r}',tt,F_IN,al=AL_C)
    for i in range(NS):
        col=CL(2+i); put(we,f'{col}{r}',f'=SUMIFS($I${EL0}:$I${EL0+21*NS-1},$A${EL0}:$A${EL0+21*NS-1},{col}${EP0-1},$B${EL0}:$B${EL0+21*NS-1},$A{r})',nf='+0.0%;-0.0%;0.0%')
che=ScatterChart(); che.style=2
for i,idx in enumerate([0,4,7]):
    xr=Reference(we,min_col=1,min_row=EP0,max_row=EP0+20); yr=Reference(we,min_col=2+idx,min_row=EP0-1,max_row=EP0+20)
    s=Series(Reference(we,min_col=2+idx,min_row=EP0,max_row=EP0+20),xr,title=f'S{idx+1} '+F.SHOCKS[idx][1]); s.marker=Marker(symbol='circle',size=4); s.smooth=False
    s.graphicalProperties.line.solidFill=[BLUE,ORANGE,'2CA58D'][i]; s.graphicalProperties.line.width=22225; s.marker.graphicalProperties=GraphicalProperties(solidFill=[BLUE,ORANGE,'2CA58D'][i])
    che.series.append(s)
style_chart(che,'Cumulative abnormal return around featured shocks (t = 0 is the first session on/after the event)','Trading days from event','CAR',w=22,h=10)
che.y_axis.number_format='0%'; che.x_axis.scaling.min=-10; che.x_axis.scaling.max=10; che.x_axis.majorUnit=2
we.add_chart(che,f'L{EP0-2}')
widths(we,{'A':6,'B':36,'C':10,'D':12,'E':12,'F':11,'G':11,'H':11,'I':9,'J':11,'K':8,'L':8,'M':10,'N':8,'O':8,'P':11,'Q':8,'R':8,'S':10,'T':9})
we.freeze_panes='C6'

# ======================================================= RETURNS (firm vs market before/after shocks)
wrt=sheet('Returns','2A78D6')
title(wrt,'Task 2(a): Titan vs NIFTY 500 returns before and after each shock','Cumulative price return over each 6-month window, excess return over the market, annualised volatility and event-window CARs. All linked to Shocks / EventStudy.')
hdr(wrt,4,1,['ID','Shock','Titan pre','Titan post','NIFTY pre','NIFTY post','Excess pre (Titan - NIFTY)','Excess post','Change in excess','Titan vol pre (ann.)','Titan vol post (ann.)','NIFTY vol pre (ann.)','NIFTY vol post (ann.)','Titan Sharpe pre','Titan Sharpe post','CAR [-1,+1]','CAR [-10,+10]'],h=54)
for i in range(NS):
    r=5+i; a=6+2*i; b=a+1
    put(wrt,f'A{r}',f'=Inputs!A{23+i}',F_LINK,al=AL_C); put(wrt,f'B{r}',f'=Inputs!B{23+i}',F_LINK)
    put(wrt,f'C{r}',f'=Shocks!S{a}',F_LINK,nf=NF_PCTS); put(wrt,f'D{r}',f'=Shocks!S{b}',F_LINK,nf=NF_PCTS); put(wrt,f'E{r}',f'=Shocks!T{a}',F_LINK,nf=NF_PCTS); put(wrt,f'F{r}',f'=Shocks!T{b}',F_LINK,nf=NF_PCTS)
    put(wrt,f'G{r}',f'=C{r}-E{r}',nf='+0.0%;-0.0%;0.0%',bold=True); put(wrt,f'H{r}',f'=D{r}-F{r}',nf='+0.0%;-0.0%;0.0%',bold=True); put(wrt,f'I{r}',f'=H{r}-G{r}',nf='+0.0%;-0.0%;0.0%')
    put(wrt,f'J{r}',f'=Shocks!R{a}*SQRT({IN["td"]})',F_LINK,nf=NF_PCT); put(wrt,f'K{r}',f'=Shocks!R{b}*SQRT({IN["td"]})',F_LINK,nf=NF_PCT)
    put(wrt,f'L{r}',f'=STDEV({rng("I",f"Shocks!F{a}",f"Shocks!G{a}")})*SQRT({IN["td"]})',nf=NF_PCT); put(wrt,f'M{r}',f'=STDEV({rng("I",f"Shocks!F{b}",f"Shocks!G{b}")})*SQRT({IN["td"]})',nf=NF_PCT)
    put(wrt,f'N{r}',f'=AVERAGE({rng("H",f"Shocks!F{a}",f"Shocks!G{a}")})*{IN["td"]}/J{r}',nf='0.00'); put(wrt,f'O{r}',f'=AVERAGE({rng("H",f"Shocks!F{b}",f"Shocks!G{b}")})*{IN["td"]}/K{r}',nf='0.00')
    put(wrt,f'P{r}',f'=EventStudy!J{6+i}',F_LINK,nf='+0.0%;-0.0%;0.0%'); put(wrt,f'Q{r}',f'=EventStudy!P{6+i}',F_LINK,nf='+0.0%;-0.0%;0.0%')
chr2=BarChart(); chr2.type='col'; chr2.gapWidth=60
chr2.add_data(Reference(wrt,min_col=7,min_row=4,max_row=12),titles_from_data=True); chr2.add_data(Reference(wrt,min_col=8,min_row=4,max_row=12),titles_from_data=True)
chr2.set_categories(Reference(wrt,min_col=1,min_row=5,max_row=12)); chr2.series[0].graphicalProperties.solidFill=GREY; chr2.series[1].graphicalProperties.solidFill=BLUE
style_chart(chr2,'Titan excess return over NIFTY 500: 6 months before vs 6 months after','Shock','Excess cumulative return',w=20,h=9); chr2.y_axis.number_format='0%'
wrt.add_chart(chr2,'A15')
chr3=BarChart(); chr3.type='col'; chr3.gapWidth=60
chr3.add_data(Reference(wrt,min_col=10,min_row=4,max_row=12),titles_from_data=True); chr3.add_data(Reference(wrt,min_col=11,min_row=4,max_row=12),titles_from_data=True)
chr3.set_categories(Reference(wrt,min_col=1,min_row=5,max_row=12)); chr3.series[0].graphicalProperties.solidFill=GREY; chr3.series[1].graphicalProperties.solidFill=ORANGE
style_chart(chr3,'Titan annualised volatility: before vs after','Shock','Volatility',w=16,h=9); chr3.y_axis.number_format='0%'
wrt.add_chart(chr3,'L15')
widths(wrt,{'A':6,'B':38,'C':10,'D':10,'E':10,'F':10,'G':14,'H':11,'I':11,'J':12,'K':12,'L':12,'M':12,'N':10,'O':10,'P':11,'Q':12})
wrt.freeze_panes='C5'
