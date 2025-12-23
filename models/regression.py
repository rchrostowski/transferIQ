import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

FEATURES = [
    "prev_snaps",
    "years_exp",
    "starter_prev",
    "scheme_match",
    "nil_cost"
]

TARGET = "year1_snaps"

NIL_MAP = {
    "Low": 1,
    "Mid": 2,
    "High": 3
}

def train_model(df):
    df = df.copy()
    df["nil_cost"] = df["nil_bucket"].map(NIL_MAP)

    X = df[FEATURES]
    y = df[TARGET]

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("reg", ElasticNet(alpha=0.3, l1_ratio=0.5))
    ])

    model.fit(X, y)
    return model

def predict(df, model):
    df = df.copy()
    df["nil_cost"] = df["nil_bucket"].map(NIL_MAP)
    df["expected_snaps"] = model.predict(df[FEATURES])
    return df

