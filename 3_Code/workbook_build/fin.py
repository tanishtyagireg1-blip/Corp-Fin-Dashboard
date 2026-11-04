# Consolidated financials, Titan Company Ltd (Rs crore). Columns = FY19..FY26.
# Source rule: latest restated figure available (comparative column of the following year's AR where present).
# FY19 taken from AR 2019-20 (reported in Rs lakh -> divided by 100).
FY = ['FY19','FY20','FY21','FY22','FY23','FY24','FY25','FY26']

# (key, label, [FY19..FY26], unit, source/comment)
IS = [
 ('rev','Revenue from operations',[19778.52,21052,21644,28799,40575,51084,60456,87584],'Rs cr','Consolidated P&L'),
 ('oi','Other income',[182.94,153,186,234,308,533,486,552],'Rs cr','Consolidated P&L'),
 ('fin','Finance costs (total)',[52.54,166,203,218,300,619,953,1180],'Rs cr','Consolidated P&L; note "Finance costs"'),
 ('fin_b','  of which: interest on borrowings',[10.69,23,34,15,52,314,551,610],'Rs cr','Finance-cost note'),
 ('fin_l','  of which: interest on lease liabilities',[0,106,114,116,134,193,222,247],'Rs cr','Finance-cost note (Ind AS 116 from FY20)'),
 ('fin_g','  of which: interest on gold on loan',[42.54,37,55,87,109,112,174,320],'Rs cr','Finance-cost note'),
 ('fin_o','  of which: others',[-0.69,0,0,0,5,0,6,3],'Rs cr','Finance-cost note'),
 ('da','Depreciation & amortisation',[162.84,348,375,399,441,584,693,826],'Rs cr','Consolidated P&L'),
 ('pbt0','Profit before exceptional items & tax',[1956.89,2102,1327,2958,4447,4623,4535,6902],'Rs cr','Consolidated P&L (after share of associates/JV)'),
 ('exc','Exceptional items (expense)',[0,0,0,54,0,0,0,101],'Rs cr','Consolidated P&L'),
 ('pbt','Profit before tax',[1956.89,2102,1327,2904,4447,4623,4535,6801],'Rs cr','Consolidated P&L'),
 ('tax','Total tax expense',[568.24,609,353,706,1173,1127,1198,1728],'Rs cr','Consolidated P&L'),
 ('pat','Profit for the year',[1388.65,1493,974,2198,3274,3496,3337,5073],'Rs cr','Consolidated P&L'),
 ('eps','Basic EPS (Rs)',[15.82,16.91,10.96,24.48,36.61,39.40,37.62,57.19],'Rs','Consolidated P&L'),
 ('dps','Dividend per share declared for the year (Rs)',[5.00,4.00,4.00,7.50,10.00,11.00,11.00,15.00],'Rs','Board proposals (AR "Dividend" / AGM notice); FY26 proposed 8 May 2026'),
]
BS = [
 ('ppe_n','Property, plant & equipment (net)',[1182.31,1285,1216,1218,1343,1737,1854,2684],'Rs cr','Consolidated B/S'),
 ('cwip','Capital work-in-progress',[28.95,11,19,69,133,88,93,135],'Rs cr','Consolidated B/S'),
 ('ppe_g','Gross block of PP&E (owned assets)',[1516,1746,1796,1929,2185,2732,3035,4112],'Rs cr','PP&E note (gross carrying amount, 31 Mar)'),
 ('rou','Right-of-use assets (net)',[0,935,917,973,1285,1543,1774,2195],'Rs cr','Consolidated B/S (Ind AS 116 from 1 Apr 2019)'),
 ('inv','Inventories',[7038.82,8103,8408,13609,16584,19051,28184,42743],'Rs cr','Consolidated B/S'),
 ('cinv','Current investments',[69.22,114,2805,15,2164,1666,1337,2249],'Rs cr','Consolidated B/S'),
 ('cash','Cash & cash equivalents',[429.53,75,181,219,232,409,407,873],'Rs cr','Consolidated B/S'),
 ('bank','Other bank balances',[636.95,306,379,1354,1111,1117,1177,1044],'Rs cr','Consolidated B/S'),
 ('ta','TOTAL ASSETS',[11715.25,13550,16452,21194,27023,31550,40647,60561],'Rs cr','Consolidated B/S'),
 ('eq','Total equity (incl. NCI)',[6084.23,6673,7502,9333,11904,9393,11624,15703],'Rs cr','Consolidated B/S'),
 ('b_nc','Borrowings - non-current',[31.67,17,9,2,0,3302,595,93],'Rs cr','Consolidated B/S'),
 ('b_c','Borrowings - current',[0.08,706,163,516,2195,4536,9691,11285],'Rs cr','Consolidated B/S (FY21 as restated in AR 2021-22)'),
 ('gold','Gold on loan (metal loan)',[2352.90,1585,4210,5398,5299,5341,7810,16070],'Rs cr','Consolidated B/S, current financial liability'),
 ('l_nc','Lease liabilities - non-current',[0,1056,1059,1138,1607,2032,2318,2712],'Rs cr','Consolidated B/S'),
 ('l_c','Lease liabilities - current',[0,187,197,221,266,317,363,461],'Rs cr','Consolidated B/S'),
 ('ncl','TOTAL non-current liabilities',[169.09,1249,1236,1349,1855,5628,3230,5065],'Rs cr','Consolidated B/S'),
 ('cl','TOTAL current liabilities',[5461.93,5628,7714,10512,13264,16529,25793,39793],'Rs cr','Consolidated B/S'),
 ('put','Memo: put-option liability for Damas minority (debt-like)',[0,0,0,0,0,0,0,1668],'Rs cr','AR 2025-26, note 40 (included in other financial liabilities)'),
]
CF = [
 ('cfo','Net cash from operating activities',[1242.92,-348,4139,-724,1370,1695,-541,5590],'Rs cr','Consolidated cash flow'),
 ('dgold','  of which: increase/(decrease) in gold on loan',[740.88,-768,2625,1188,-99,42,2468,7304],'Rs cr','Consolidated cash flow (gold on loan is classed as operating)'),
 ('capex','Capex (purchase of PP&E, intangibles, inv. property)',[264.72,355,146,224,432,691,494,902],'Rs cr','Consolidated cash flow'),
 ('divpd','Dividends paid (cash)',[397.38,536,355,355,666,888,976,976],'Rs cr','Consolidated cash flow (FY19-20 include DDT)'),
 ('bb','Share buy-backs',[0,0,0,0,0,0,0,0],'Rs cr','AR: company "has not undertaken any buy-back"'),
 ('tsy','Acquisition of treasury shares / ESOP rights',[0,0,0,0,0,437,6,0],'Rs cr','FY24: 236 treasury + 201 ESOP rights; FY25: 6'),
 ('nci','Acquisition of non-controlling interest (CaratLane)',[0,0,0,0,0,4696,1,0],'Rs cr','Consolidated cash flow, financing'),
 ('acq','Business acquisition, net of cash (Damas)',[0,0,0,0,0,0,0,1171],'Rs cr','AR 2025-26 cash flow / note 40'),
]
def all_rows(): return IS+BS+CF

REPO = [  # effective date, repo %, note
 ('2019-07-01',5.75,'RBI MPC 6 Jun 2019 (rate in force at start of dataset)'),
 ('2019-08-07',5.40,'RBI MPC 7 Aug 2019'),
 ('2019-10-04',5.15,'RBI MPC 4 Oct 2019'),
 ('2020-03-27',4.40,'RBI emergency MPC (COVID-19)'),
 ('2020-05-22',4.00,'RBI off-cycle (COVID-19)'),
 ('2022-05-04',4.40,'RBI off-cycle hike - start of tightening cycle'),
 ('2022-06-08',4.90,'RBI MPC 8 Jun 2022'),
 ('2022-08-05',5.40,'RBI MPC 5 Aug 2022'),
 ('2022-09-30',5.90,'RBI MPC 30 Sep 2022'),
 ('2022-12-07',6.25,'RBI MPC 7 Dec 2022'),
 ('2023-02-08',6.50,'RBI MPC 8 Feb 2023'),
 ('2025-02-07',6.25,'RBI MPC 7 Feb 2025'),
 ('2025-04-09',6.00,'RBI MPC 9 Apr 2025'),
 ('2025-06-06',5.50,'RBI MPC 6 Jun 2025 (50 bp)'),
 ('2025-12-05',5.25,'RBI MPC Dec 2025'),
 ('2026-10-07',5.50,'RBI MPC 7 Oct 2026 (+25 bp; per Business Standard)'),
]
GSEC = [  # month start, 10Y yield % (FRED / OECD monthly average)
 ('2019-07',6.59772500),('2019-08',6.61912),('2019-09',6.81335),('2019-10',6.5418),('2019-11',6.63498),('2019-12',6.848575),
 ('2020-01',6.8218),('2020-02',6.65965),('2020-03',6.701575),('2020-04',6.76515),('2020-05',5.91544),('2020-06',5.8551),
 ('2020-07',5.81452),('2020-08',6.0105),('2020-09',6.024675),('2020-10',5.94484),('2020-11',5.8952),('2020-12',5.8929),
 ('2021-01',5.94162),('2021-02',6.1935),('2021-03',6.350775),('2021-04',6.2801),('2021-05',6.225375),('2021-06',6.267675),
 ('2021-07',6.20842),('2021-08',6.280325),('2021-09',6.1883),('2021-10',6.35978),('2021-11',6.354375),('2021-12',6.44032),
 ('2022-01',6.643025),('2022-02',6.750475),('2022-03',6.819825),('2022-04',7.1058),('2022-05',7.38565),('2022-06',7.529625),
 ('2022-07',7.40206),('2022-08',7.27475),('2022-09',7.280374),('2022-10',7.464925),('2022-11',7.357575),('2022-12',7.29416),
 ('2023-01',7.39),('2023-02',7.334525),('2023-03',7.36),('2023-04',7.18),('2023-05',7.0125),('2023-06',7.054),
 ('2023-07',7.1125),('2023-08',7.185),('2023-09',7.172),('2023-10',7.35),('2023-11',7.27),('2023-12',7.224),
 ('2024-01',7.2025),('2024-02',7.09),('2024-03',7.068),('2024-04',7.15),('2024-05',7.054),('2024-06',7.0225),
 ('2024-07',7.0075),('2024-08',6.91),('2024-09',6.8325),('2024-10',6.785),('2024-11',6.812),('2024-12',6.7775),
 ('2025-01',6.758),('2025-02',6.7325),('2025-03',6.6825),('2025-04',6.455),('2025-05',6.272),('2025-06',6.3075),
 ('2025-07',6.35),('2025-08',6.522),('2025-09',6.585),('2025-10',6.482),('2025-11',6.5375),('2025-12',6.6325),
 ('2026-01',6.732),('2026-02',6.77),('2026-03',6.84),('2026-04',7.05),('2026-05',7.02),('2026-06',6.89),
 ('2026-07',6.78),('2026-08',6.84),('2026-09',7.06),
]
SHOCKS = [  # id, name, category, date, featured, channel, source
 ('S1','COVID-19 national lockdown','Pandemic / demand','2020-03-25',1,'Demand collapse (stores shut), liquidity stress, gold-price spike','PM address 24 Mar 2020; lockdown from 25 Mar 2020 (brief: Mar-May 2020)'),
 ('S2','Stimulus package & repo cut to 4.00%','Monetary / fiscal','2020-05-22',0,'Cheaper liquidity, risk-on rotation','RBI off-cycle cut 22 May 2020; Atmanirbhar package 12 May 2020'),
 ('S3','Second COVID-19 wave','Pandemic / demand','2021-05-03',0,'Regional lockdowns, wedding-season disruption','Peak of second wave early May 2021 (brief: May 2021)'),
 ('S4','Russia-Ukraine war','Geopolitical / commodity','2022-02-24',0,'Commodity & gold volatility, global risk-off','Invasion began 24 Feb 2022'),
 ('S5','RBI rate-hike cycle (4.00% -> 6.50%)','Monetary','2022-05-04',1,'Cost of debt up, discount rates up, valuation de-rating','RBI off-cycle hike 4 May 2022; cycle ended 8 Feb 2023'),
 ('S6','Adani-Hindenburg shock','Market confidence','2023-01-25',0,'Index-level sentiment, FPI outflows','Hindenburg report 24 Jan 2023; first trading day 25 Jan'),
 ('S7','US tariff escalation & H-1B fee','Trade policy','2025-08-27',0,'Export demand, sentiment, rupee','50% US tariff on India effective 27 Aug 2025; H-1B USD 100k fee 19 Sep 2025'),
 ('S8','US/Israel-Iran war & oil shock','Geopolitical / commodity','2026-03-02',1,'Oil & gold surge, rupee weakness, inflation, later RBI hike (Oct 2026)','Strikes 28 Feb 2026; markets reacted 2 Mar 2026; Brent peak ~USD 118 late Mar'),
]
