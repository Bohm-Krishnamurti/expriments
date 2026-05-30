import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df=pd.read_csv("/home/user/expriments/diffusion_alpha/data_scored.csv")
mkt=29.8
col={"reseller":"#d62728","platform":"#ff7f0e","incumbent":"#1f77b4",
     "control":"#2ca02c","builder":"#9467bd"}

fig,ax=plt.subplots(1,2,figsize=(15,6.5))

# panel 1: return vs deployment friction (the variable that actually works)
a=ax[0]
for t,c in col.items():
    s=df[df.tax==t]
    a.scatter(s.friction,s.ret1y,s=70+s.rl*1.4,c=c,alpha=.8,edgecolor="k",lw=.4,label=t)
for _,r in df.iterrows():
    a.annotate(r.ticker,(r.friction,r.ret1y),fontsize=6.5,xytext=(3,3),textcoords="offset points")
a.axhline(mkt,ls="--",c="gray"); a.text(2,mkt+2,f"S&P +{mkt:.0f}%",color="gray",fontsize=8)
a.axhline(0,ls=":",c="k",lw=.5)
z=np.polyfit(df[df.tax!="builder"].friction,df[df.tax!="builder"].ret1y,1)
xs=np.linspace(15,90,10); a.plot(xs,np.polyval(z,xs),c="k",lw=1,alpha=.5)
a.set_xlabel("Deployment friction  (regulation / unions / physical / compliance)  -->")
a.set_ylabel("1Y total return  %")
a.set_title("Returns sort by FRICTION, not AI-exposure\n(dot size = RL-exposure score)",fontsize=11)
a.legend(fontsize=8,loc="upper left"); a.grid(alpha=.2)

# panel 2: quadrant means
a=ax[1]
sub=df[df.tax!="builder"].copy()
sub["RLband"]=np.where(sub.rl>=60,"High RL-exposure","Low RL-exposure")
sub["FRband"]=np.where(sub.friction>=55,"High friction","Low friction")
q=sub.pivot_table(index="RLband",columns="FRband",values="ret1y",aggfunc="mean")
q=q.reindex(index=["High RL-exposure","Low RL-exposure"],columns=["Low friction","High friction"])
x=np.arange(2); w=.36
a.bar(x-w/2,q["Low friction"],w,label="Low friction",color="#d62728",alpha=.85)
a.bar(x+w/2,q["High friction"],w,label="High friction",color="#2ca02c",alpha=.85)
for i,v in enumerate(q["Low friction"]): a.text(i-w/2,v-4 if v<0 else v+1,f"{v:+.0f}%",ha="center",fontsize=10)
for i,v in enumerate(q["High friction"]): a.text(i+w/2,v+1,f"{v:+.0f}%",ha="center",fontsize=10)
a.set_xticks(x); a.set_xticklabels(q.index)
a.axhline(0,c="k",lw=.6); a.axhline(mkt,ls="--",c="gray"); a.text(-.4,mkt+1,f"S&P +{mkt:.0f}%",color="gray",fontsize=8)
a.set_ylabel("mean 1Y total return %")
a.set_title("Same exposure, opposite outcome:\nfriction is the whole story",fontsize=11)
a.legend(fontsize=9)
plt.tight_layout()
plt.savefig("/home/user/expriments/diffusion_alpha/figure.png",dpi=130,bbox_inches="tight")
print("saved figure.png")
