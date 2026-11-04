TITAN COMPANY LTD - CORPORATE FINANCE WAI PROJECT: ANNEXURE
Tanish Tyagi | M56D-26 | Section D | IIM Ranchi, Term II

1_Dashboard/index.html     Interactive dashboard. Double-click to open in any browser; no internet or install needed. Light/dark theme, date-range filter, per-shock beta view, scenario selector, interest-rate stress sliders.
2_Workbook/                Titan_WAI_Analysis.xlsx - full analysis with live formulas (start at the README and Summary sheets; Checks sheet holds the 17 integrity tests and the Excel-vs-Python beta comparison).
3_Code/workbook_build/     Python (openpyxl) scripts that build the workbook: run_all.py runs build1..build7. pycheck.py recomputes the betas independently (statsmodels). load.py reads the NSE price files; fin.py holds the annual-report inputs.
3_Code/report/             extract.py (workbook -> data.json), figs.py and figs2.py (report figures), report.py (builds the PDF report).
3_Code/dashboard/          mk.py (workbook -> data.js), index.src.html (template), build.py (embeds the data to make index.html).
4_Data/raw_market_data/    NSE Titan daily prices (4 files) and NIFTY 500 price-index files (8 files), as supplied.
4_Data/derived/            CSV exports of the key workbook sheets (daily prices and returns, financials FY19-FY26, assumptions, shock results, policy ratios, WACC/ROIC/EVA) and data.json used by the report and dashboard.
5_Report/                  Titan_WAI_Report.pdf (main report) and AI_Contribution_Statement.pdf.

Notes
- The build scripts contain absolute paths from the working environment (for example /home/claude/... and the folder of NSE files in load.py). Edit these paths to re-run them. The workbook and dashboard need no re-running to be read.
- Financial statements are from Titan annual reports FY2019-20 to FY2025-26 (consolidated). They are not reproduced here; see the Sources sheet in the workbook.
- Risk-free rate: RBI repo rate (daily series) for beta; 10-year G-sec yield each March for WACC. Equity risk premium 6% is an assumption.
- NIFTY 500 file is a price index (no dividends).
