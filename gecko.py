from dataclasses import dataclass
import numpy as np
import pandas as pd

from features import build_gecko_features
from baselines import zscore_score, ewma_score, slope_score, LogisticRaw
from metrics import future_failure_labels, threshold_at_fpr, warning_metrics

@dataclass
class GECKOExperiment:
    time_column: str
    failure_column: str
    feature_columns: list
    failure_horizon: int = 25
    horizons: tuple = (3,7,23)
    max_false_alarm_rate: float = 0.05
    train_fraction: float = 0.60
    random_state: int = 23

    def run(self, df):
        df = df.sort_values(self.time_column).reset_index(drop=True).copy()
        cut = max(20, int(len(df)*self.train_fraction))

        failure = df[self.failure_column].astype(int).to_numpy()
        future_y = future_failure_labels(failure, self.failure_horizon)

        gf = build_gecko_features(df, self.feature_columns, self.horizons)
        gecko_score = gf["gecko_degradation_score"].to_numpy()

        z = zscore_score(df, self.feature_columns, max(self.horizons))
        ewma = ewma_score(df, self.feature_columns)
        slope = slope_score(df, self.feature_columns)

        raw = df[self.feature_columns].astype(float).copy()
        for c in self.feature_columns:
            raw[f"{c}__dx"] = raw[c].diff().fillna(0.0)
        raw = raw.ffill().fillna(0.0)

        logit = LogisticRaw(self.random_state).fit(raw.iloc[:cut], future_y[:cut])
        logit_score = np.concatenate([
            logit.predict_proba(raw.iloc[:cut]),
            logit.predict_proba(raw.iloc[cut:])
        ])

        scores = {
            "gecko": gecko_score,
            "zscore": z,
            "ewma": ewma,
            "slope": slope,
            "logistic_raw": logit_score,
        }

        results = {}
        for name, score in scores.items():
            threshold = threshold_at_fpr(
                future_y[:cut],
                score[:cut],
                self.max_false_alarm_rate
            )
            results[name] = warning_metrics(
                failure[cut:],
                future_y[cut:],
                score[cut:],
                threshold
            )

        return {
            "n_total": len(df),
            "train_n": cut,
            "test_n": len(df)-cut,
            "failure_horizon": self.failure_horizon,
            "max_false_alarm_rate": self.max_false_alarm_rate,
            "results": results,
            "primary_rule": (
                "Compare GECKO against conventional baselines at approximately matched "
                "training-segment false-alarm thresholds."
            )
        }
