from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

FEATURES = ["prev_snaps", "years_exp", "starter_prev", "scheme_match"]
TARGET = "year1_snaps"

def train(df):
    X = df[FEATURES]
    y = df[TARGET]

    model = Pipeline([
        ("scale", StandardScaler()),
        ("reg", Ridge(alpha=1.0))
    ])

    model.fit(X, y)
    return model

def predict(df, model):
    df["expected_snaps"] = model.predict(df[FEATURES])
    return df

