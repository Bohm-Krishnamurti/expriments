"""
Decompose the cross-section. Does RL-exposure explain returns, or is it
builder-vs-deployer rotation + deployment-friction protection?
"""
import numpy as np, pandas as pd
pd.set_option("display.width",200); pd.set_option("display.max_columns",20)

df=pd.read_csv("/home/user/expriments/diffusion_alpha/data.csv")
mkt=float(df.loc[df.ticker=="SPY","ret1y"].iloc[0])
df=df[df.tax!="market"].dropna(subset=["ret1y"]).copy()
df["excess"]=df["ret1y"]-mkt          # return vs S&P 500
print(f"S&P 500 1Y total return (benchmark): {mkt:+.1f}%\n")

# ---------- 1. group means ----------
print("="*72)
print("1. MEAN 1Y RETURN BY TAXONOMY  (vs market +{:.0f}%)".format(mkt))
print("="*72)
g=df.groupby("tax").agg(n=("ret1y","size"),ret=("ret1y","mean"),
                        excess=("excess","mean"),rl=("rl","mean"),
                        friction=("friction","mean")).round(1)
print(g.sort_values("ret"))

# ---------- 2. correlations ----------
print("\n"+"="*72); print("2. WHAT CORRELATES WITH 1Y RETURN?"); print("="*72)
sub=df[df.tax!="builder"]   # test on the exposure universe itself
for col in ["rl","friction"]:
    r=np.corrcoef(sub[col],sub["ret1y"])[0,1]
    print(f"   corr(ret1y, {col:9s}) = {r:+.2f}   (ex-builders, n={len(sub)})")
# interaction: rl among LOW vs HIGH friction
lo=sub[sub.friction<50]; hi=sub[sub.friction>=50]
print(f"\n   RL-exposure effect, LOW friction (<50):  corr={np.corrcoef(lo.rl,lo.ret1y)[0,1]:+.2f}  n={len(lo)}  meanRet={lo.ret1y.mean():+.1f}%")
print(f"   RL-exposure effect, HIGH friction(>=50): corr={np.corrcoef(hi.rl,hi.ret1y)[0,1]:+.2f}  n={len(hi)}  meanRet={hi.ret1y.mean():+.1f}%")

# ---------- 3. quadrant grid ----------
print("\n"+"="*72); print("3. EXPOSURE x FRICTION QUADRANTS  (mean 1Y return)"); print("="*72)
sub=sub.copy()
sub["RLband"]=np.where(sub.rl>=60,"hiRL","loRL")
sub["FRband"]=np.where(sub.friction>=55,"hiFriction","loFriction")
q=sub.pivot_table(index="RLband",columns="FRband",values="ret1y",aggfunc="mean").round(1)
qn=sub.pivot_table(index="RLband",columns="FRband",values="ret1y",aggfunc="size")
print("mean return:\n",q,"\n\ncount:\n",qn)

# ---------- 4. OLS: ret ~ rl + friction (+interaction), ex builders ----------
print("\n"+"="*72); print("4. OLS  ret1y ~ rl + friction + rl*friction  (ex-builders)"); print("="*72)
X=sub[["rl","friction"]].values.astype(float)
inter=(sub.rl*sub.friction).values.reshape(-1,1)
X=np.hstack([np.ones((len(sub),1)),X,inter])
y=sub.ret1y.values.astype(float)
beta,res,rank,sv=np.linalg.lstsq(X,y,rcond=None)
yhat=X@beta; ss_res=((y-yhat)**2).sum(); ss_tot=((y-y.mean())**2).sum()
names=["intercept","rl","friction","rl*friction"]
for nme,b in zip(names,beta): print(f"   {nme:12s} {b:+.3f}")
print(f"   R^2 = {1-ss_res/ss_tot:.2f}   (n={len(sub)})")

# ---------- 5. builder vs deployer rotation ----------
print("\n"+"="*72); print("5. THE ROTATION (what the market actually rewarded)"); print("="*72)
bld=df[df.tax=="builder"]; dep=df[df.tax.isin(["reseller","platform"])]
print(f"   AI infrastructure builders : mean {bld.ret1y.mean():+.1f}%  (n={len(bld)})")
print(f"   AI 'deployers' resel+platfm: mean {dep.ret1y.mean():+.1f}%  (n={len(dep)})")
print(f"   spread                     :      {bld.ret1y.mean()-dep.ret1y.mean():+.1f} pts")

# ---------- 6. within-bucket dispersion = where relative value lives ----------
print("\n"+"="*72); print("6. WITHIN-BUCKET DISPERSION (pairs / relative-value edge)"); print("="*72)
for t in ["reseller","platform","incumbent","control"]:
    s=df[df.tax==t].sort_values("ret1y")
    best=s.iloc[-1]; worst=s.iloc[0]
    print(f"   {t:10s} spread {best.ret1y-worst.ret1y:5.0f} pts  | best {best.ticker} {best.ret1y:+.0f}%  worst {worst.ticker} {worst.ret1y:+.0f}%  | std {s.ret1y.std():.0f}")

# ---------- 7. the un-run control-layer screen ----------
print("\n"+"="*72); print("7. 'HIDDEN' CONTROL-LAYER, RANKED BY HOW MUCH THEY LAGGED MARKET"); print("="*72)
ctrl=df[df.tax=="control"].sort_values("excess")
print(ctrl[["ticker","name","ret1y","excess","rl","friction","pe"]].to_string(index=False))

df.to_csv("/home/user/expriments/diffusion_alpha/data_scored.csv",index=False)
