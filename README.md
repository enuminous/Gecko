# GECKO

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/Gecko) · This repository is linked through its source; GitHub Pages is not enabled.
<!-- ENUMINOUS-NETWORK:END -->

**Gradient Evaluation of Coherence and Kinetic Outliers**

GECKO is an EFMW-derived framework for mechanical degradation and condition monitoring.

Its narrow question is:

> Do changes in the relationships among machine signals reveal degradation earlier than conventional single-sensor thresholds?

## Intended uses

- motors
- pumps
- turbines
- bearings
- vehicles
- industrial robots
- HVAC systems
- rotating machinery
- battery systems
- other multichannel mechanical systems

## Core signal path

```text
sensor state
→ robust normalization
→ velocity / acceleration
→ pairwise mechanical relations
→ contradiction drift
→ multiscale persistence
→ degradation score
→ probability of near-term failure
```

## Flat-stack repository

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
gecko.py
features.py
baselines.py
metrics.py
freeze.py
forecast_schema.json
example_config.yaml
example_data.csv
example_run.py
test_gecko.py
MANIFEST.sha256
```

## Scientific hypothesis

> In degrading machinery, relational changes among sensor channels may become detectable before any one channel crosses a conventional fault threshold.

GECKO is not assumed to outperform conventional monitoring.

## Baselines

Included:

- raw-feature logistic model
- z-score threshold score
- EWMA deviation score
- slope/persistence score
- base-rate predictor

## Primary endpoint

For a frozen failure horizon:

> At matched false-alarm rates, does GECKO improve sensitivity or warning lead time relative to conventional baselines?

Secondary metrics:

- Brier score
- log loss
- ROC-AUC
- average precision
- calibration
- lead time

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python example_run.py
```

## Tests

```bash
pytest -q
```

## Minimal usage

```python
import pandas as pd
from gecko import GECKOExperiment

df = pd.read_csv("example_data.csv")

exp = GECKOExperiment(
    time_column="time",
    failure_column="failure",
    feature_columns=["vibration", "temperature", "current", "pressure"],
    failure_horizon=25,
    horizons=(3, 7, 23),
)

print(exp.run(df))
```

## Freeze discipline

Before prospective use, freeze:

- sensor channels
- sampling interval
- failure definition
- warning horizon
- preprocessing
- feature equations
- score weights
- thresholds
- baselines
- metrics
- exclusions
- compute budget
- random seeds

Then run:

```bash
python freeze.py
```

## Negative results

If standard condition-monitoring methods match or beat GECKO, then GECKO has not demonstrated incremental predictive value.

## Status

Research software. Experimental. Not validated for safety-critical maintenance decisions.
