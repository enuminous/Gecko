import pandas as pd
from features import build_gecko_features
from gecko import GECKOExperiment

def test_features():
    df = pd.read_csv("example_data.csv")
    gf = build_gecko_features(
        df,
        ["vibration","temperature","current","pressure"],
        horizons=(3,7,23),
    )
    assert len(gf) == len(df)
    assert "gecko_degradation_score" in gf.columns
    assert gf["gecko_degradation_score"].between(0,1).all()

def test_experiment_runs():
    df = pd.read_csv("example_data.csv")
    exp = GECKOExperiment(
        time_column="time",
        failure_column="failure",
        feature_columns=["vibration","temperature","current","pressure"],
        failure_horizon=25,
    )
    out = exp.run(df)
    assert "results" in out
    assert "gecko" in out["results"]
    assert "ewma" in out["results"]
