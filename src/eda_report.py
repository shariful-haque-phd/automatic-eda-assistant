import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def make_report(df):
    lines=["# Exploratory Data Analysis Report","",
           f"- Rows: **{len(df):,}**",
           f"- Columns: **{df.shape[1]:,}**",
           f"- Duplicate rows: **{int(df.duplicated().sum()):,}**",""]
    lines += ["## Missing data","", "| Column | Missing | Percent |","|---|---:|---:|"]
    for c in df.columns:
        lines.append(f"| {c} | {int(df[c].isna().sum())} | {df[c].isna().mean()*100:.2f}% |")
    num=df.select_dtypes(include=np.number)
    if not num.empty:
        lines += ["","## Numeric summary","", num.describe().round(3).to_markdown(), ""]
        corr=num.corr(numeric_only=True)
        lines += ["## Correlations","",corr.round(3).to_markdown(),""]
        high=[]
        for i,a in enumerate(corr.columns):
            for b in corr.columns[i+1:]:
                if abs(corr.loc[a,b])>=0.8:
                    high.append((a,b,float(corr.loc[a,b])))
        if high:
            lines += ["### Strong correlations"]
            for a,b,v in high: lines.append(f"- `{a}` and `{b}`: {v:.3f}")
        clean=num.dropna()
        if len(clean)>=20 and clean.shape[1]>=1:
            model=IsolationForest(contamination="auto",random_state=42)
            flags=model.fit_predict(clean)
            lines += ["","## Potential anomalies","",
                      f"Isolation Forest flagged **{int((flags==-1).sum())}** of **{len(clean)}** complete numeric rows for review."]
    lines += ["","## Review notes","",
              "- Missing values should be interpreted using domain context before imputation.",
              "- Correlation does not establish causation.",
              "- Anomaly flags are screening signals rather than proof of bad data."]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--output",default="report.md")
    a=ap.parse_args(); df=pd.read_csv(a.csv)
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(make_report(df),encoding="utf-8")
    print(f"Wrote {out}")

if __name__=="__main__": main()
