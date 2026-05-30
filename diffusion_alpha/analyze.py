"""
Diffusion / RL-exposure public-market screen — empirical test.

Tests the report's thesis against live data on two axes the memo never separated:
  1. RL-exposure  : how trainable/automatable the firm's core workflow chains are
  2. deploy_friction: how structurally resistant that automation is to actually
                      hitting the P&L (regulation, unions, physical world, compliance,
                      legacy integration) -- the "deployment bottleneck" axis.

And the firm-level taxonomy that is the report's real intellectual content:
  reseller   = sells labor INTO the workflow (loses if it automates)
  platform   = owns the system-of-record / software rails (ambiguous)
  incumbent  = internalizes the workflow + the productivity gain (beneficiary)
  control    = instrumented physical/ops control layer ("hidden" RL exposure)
  builder    = AI infrastructure (control group for the rotation hypothesis)

Question being answered: does the exposure axis explain 1Y returns, or is the
cross-section really a builder-vs-deployer rotation + idiosyncratic catalysts?
"""
import json, time, warnings, sys
import numpy as np
import pandas as pd
import requests
warnings.filterwarnings("ignore")

H = {"User-Agent": "Mozilla/5.0"}

# ticker, name, cluster, taxonomy, rl_exposure(0-100), deploy_friction(0-100)
# scores are the report's reasoning made explicit & ordinal, not precise truth.
UNIV = [
    # ---- labor resellers / BPO (low friction: pure digital, easy to displace) ----
    ("ACN","Accenture","BPO/IT","reseller",70,35),
    ("CTSH","Cognizant","BPO/IT","reseller",78,30),
    ("G","Genpact","BPO/F&A","reseller",90,25),
    ("CNXC","Concentrix","Customer ops","reseller",92,20),
    ("EXLS","EXLService","Analytics BPO","reseller",88,28),
    ("TASK","TaskUs","Digital ops","reseller",90,18),
    ("CNDT","Conduent","BPO","reseller",85,30),
    ("WNS","WNS Holdings","BPO/F&A","reseller",88,25),
    # ---- platform / software rails (own the workflow; ambiguous sign) ----
    ("ADP","ADP","Payroll/HCM","platform",60,45),
    ("PAYX","Paychex","Payroll/HCM","platform",60,45),
    ("WDAY","Workday","HCM software","platform",45,50),
    ("PAYC","Paycom","Payroll software","platform",55,45),
    ("INTU","Intuit","Tax/SMB software","platform",58,40),
    ("ORCL","Oracle","Enterprise software","platform",40,55),
    ("SAP","SAP","Enterprise software","platform",40,55),
    # ---- incumbents who internalize the gain (high friction: compliance) ----
    ("JPM","JPMorgan","Banking","incumbent",55,75),
    ("BAC","Bank of America","Banking","incumbent",55,75),
    ("WFC","Wells Fargo","Banking","incumbent",55,78),
    ("AXP","American Express","Cards","incumbent",55,70),
    ("SCHW","Schwab","Brokerage","incumbent",58,68),
    ("MS","Morgan Stanley","Brokerage","incumbent",50,70),
    ("GS","Goldman Sachs","Brokerage","incumbent",50,70),
    ("UNH","UnitedHealth","Health ins","incumbent",60,80),
    ("ELV","Elevance","Health ins","incumbent",60,80),
    ("CI","Cigna","Health ins","incumbent",58,80),
    ("PGR","Progressive","P&C ins","incumbent",58,65),
    ("ALL","Allstate","P&C ins","incumbent",55,65),
    ("CB","Chubb","P&C ins","incumbent",52,68),
    ("TRV","Travelers","P&C ins","incumbent",52,68),
    ("AIG","AIG","Insurance","incumbent",50,70),
    ("MET","MetLife","Insurance","incumbent",50,70),
    # ---- control layer ("hidden" RL exposure, very high friction) ----
    ("NEE","NextEra","Utility/grid","control",45,88),
    ("DUK","Duke Energy","Utility/grid","control",42,88),
    ("SO","Southern Co","Utility/grid","control",42,88),
    ("CEG","Constellation","Utility/power","control",45,85),
    ("UNP","Union Pacific","Rail","control",48,82),
    ("CSX","CSX","Rail","control",48,82),
    ("NSC","Norfolk Southern","Rail","control",48,82),
    ("UPS","UPS","Parcel/logistics","control",55,60),
    ("FDX","FedEx","Parcel/logistics","control",55,60),
    ("LIN","Linde","Industrial gas","control",40,80),
    ("DOW","Dow","Chemicals","control",40,78),
    # ---- AI infrastructure builders (control group for rotation test) ----
    ("NVDA","Nvidia","AI builder","builder",10,30),
    ("MSFT","Microsoft","AI builder","builder",15,35),
    ("GOOGL","Alphabet","AI builder","builder",15,35),
    ("AVGO","Broadcom","AI builder","builder",10,30),
    ("PLTR","Palantir","AI deployer","builder",20,40),
    # ---- market benchmark ----
    ("SPY","S&P 500","Benchmark","market",0,0),
]

def chart_total_return(tk):
    """1Y total return from adjclose (dividends reinvested)."""
    for host in ("query1","query2"):
        try:
            u=f"https://{host}.finance.yahoo.com/v8/finance/chart/{tk}?range=1y&interval=1d&events=div"
            r=requests.get(u,headers=H,timeout=20); r.raise_for_status()
            res=r.json()["chart"]["result"][0]
            adj=res["indicators"]["adjclose"][0]["adjclose"]
            adj=[c for c in adj if c is not None]
            if len(adj)>20:
                return (adj[-1]/adj[0]-1)*100.0, adj
        except Exception:
            time.sleep(0.4)
    return np.nan, None

def fundamentals(tk):
    """trailing PE + market cap via yfinance (handles crumb auth)."""
    import yfinance as yf
    try:
        fi=yf.Ticker(tk).get_info()
        pe=fi.get("trailingPE", np.nan)
        mc=fi.get("marketCap", np.nan)
        return pe, mc
    except Exception:
        return np.nan, np.nan

rows=[]
for tk,name,cluster,tax,rl,fr in UNIV:
    tr,adj=chart_total_return(tk)
    pe,mc=fundamentals(tk)
    rows.append(dict(ticker=tk,name=name,cluster=cluster,tax=tax,
                     rl=rl,friction=fr,ret1y=tr,pe=pe,mcap=mc))
    print(f"{tk:6s} ret1y={tr:7.1f}%  PE={pe if isinstance(pe,(int,float)) and pe==pe else float('nan'):7} "
          f"mcap={ (mc/1e9 if mc==mc else float('nan')) :7.1f}B  [{tax}]")
    time.sleep(0.25)

df=pd.DataFrame(rows)
df.to_csv("/home/user/expriments/diffusion_alpha/data.csv",index=False)
print("\nsaved data.csv with", len(df), "rows")
