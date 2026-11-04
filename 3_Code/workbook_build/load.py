import pandas as pd, glob, numpy as np
D='/mnt/user-data/attachments/3e7a3412-e2cd-5966-a58c-4a988cff0d2e/'
def num(s): return pd.to_numeric(s.astype(str).str.replace(',','').str.strip(),errors='coerce')
t=[]
for f in sorted(glob.glob(D+'*TITAN-EQ-N.csv')):
    d=pd.read_csv(f,encoding='utf-8-sig'); d.columns=[c.strip() for c in d.columns]
    t.append(d)
t=pd.concat(t); t['Date']=pd.to_datetime(t['Date'].str.strip(),format='%d-%b-%Y')
for c in ['Prev Close','Open Price','High Price','Low Price','Close Price','Total Traded Quantity']: t[c]=num(t[c])
t=t.sort_values('Date').drop_duplicates('Date')
n=pd.concat([pd.read_csv(f) for f in glob.glob(D+'*NIFTY_500*.csv')])
n['Date']=pd.to_datetime(n['Date'],format='%d %b %Y'); n['Close']=num(n['Close'])
n=n.sort_values('Date').drop_duplicates('Date')
