import json
import pandas as pd
from gecko import GECKOExperiment

df = pd.read_csv("example_data.csv")

exp = GECKOExperiment(
    time_column="time",
    failure_column="failure",
    feature_columns=["vibration","temperature","current","pressure"],
    failure_horizon=25,
    horizons=(3,7,23),
    max_false_alarm_rate=0.05,
    random_state=23,
)

result = exp.run(df)
print(json.dumps(result, indent=2))
