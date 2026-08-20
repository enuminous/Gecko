import numpy as np
import pandas as pd

EPS = 1e-8

def robust_z(s, window=23):
    s = s.astype(float)
    med = s.rolling(window, min_periods=3).median()
    mad = (s-med).abs().rolling(window, min_periods=3).median()
    return ((s-med)/(1.4826*mad+EPS)).replace([np.inf,-np.inf], np.nan).fillna(0.0)

def build_gecko_features(df, feature_columns, horizons=(3,7,23)):
    out = pd.DataFrame(index=df.index)
    x = df[feature_columns].astype(float).copy()

    local_cols = []
    for c in feature_columns:
        out[f"{c}__z"] = robust_z(x[c], max(horizons))
        out[f"{c}__velocity"] = x[c].diff().fillna(0.0)
        out[f"{c}__accel"] = x[c].diff().diff().fillna(0.0)
        local_cols.extend([f"{c}__z", f"{c}__velocity", f"{c}__accel"])

    # Pairwise "mechanical coherence": relationships that drift under degradation.
    contradiction_cols = []
    for i, a in enumerate(feature_columns):
        for b in feature_columns[i+1:]:
            diff = x[a] - x[b]
            ratio = x[a] / (x[b].abs() + EPS)
            corr = x[a].rolling(max(horizons), min_periods=3).corr(x[b])

            d = f"pair__{a}__{b}__diff_z"
            r = f"pair__{a}__{b}__ratio_z"
            c = f"pair__{a}__{b}__corr_loss"

            out[d] = robust_z(diff, max(horizons)).abs()
            out[r] = robust_z(ratio, max(horizons)).abs()
            out[c] = (1.0 - corr.abs()).fillna(0.0)

            contradiction_cols.extend([d,r,c])

    out["kinetic_outlier"] = out[local_cols].abs().mean(axis=1)

    if contradiction_cols:
        out["coherence_loss"] = out[contradiction_cols].abs().mean(axis=1)
    else:
        out["coherence_loss"] = 0.0

    out["gradient_loss"] = out["coherence_loss"].diff().clip(lower=0).fillna(0.0)
    out["kinetic_gradient"] = out["kinetic_outlier"].diff().clip(lower=0).fillna(0.0)

    for h in horizons:
        out[f"coherence_loss_mean_{h}"] = out["coherence_loss"].rolling(h, min_periods=1).mean()
        out[f"kinetic_outlier_mean_{h}"] = out["kinetic_outlier"].rolling(h, min_periods=1).mean()
        out[f"gradient_loss_mean_{h}"] = out["gradient_loss"].rolling(h, min_periods=1).mean()
        out[f"kinetic_gradient_mean_{h}"] = out["kinetic_gradient"].rolling(h, min_periods=1).mean()

    components = [
        out["coherence_loss"],
        out["kinetic_outlier"],
        out["gradient_loss"],
        out["kinetic_gradient"],
    ]
    for h in horizons:
        components.extend([
            out[f"coherence_loss_mean_{h}"],
            out[f"kinetic_outlier_mean_{h}"],
            out[f"gradient_loss_mean_{h}"],
            out[f"kinetic_gradient_mean_{h}"],
        ])

    ranked = pd.concat(components, axis=1).rank(pct=True)
    out["gecko_degradation_score"] = ranked.mean(axis=1).fillna(0.0)

    return out.replace([np.inf,-np.inf], np.nan).fillna(0.0)
