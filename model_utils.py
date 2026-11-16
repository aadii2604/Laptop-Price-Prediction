import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = "data/laptops.csv"
CAT = ["Brand", "Storage_Type", "Processor", "GPU", "Resolution"]
NUM = ["Ram_GB", "Storage_GB", "Screen_Size"]
TARGET = "Price"


def _pipe(model):
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
                             ("num", StandardScaler(), NUM)])
    return Pipeline([("pre", pre), ("model", model)])


def train(path=DATA_PATH):
    """Trains Ridge and Random Forest, returns (best_pipeline, metrics_df, dataframe)."""
    df = pd.read_csv(path)
    X, y = df[CAT + NUM], df[TARGET]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    candidates = {"Ridge Regression": _pipe(Ridge(alpha=1.0)),
                  "Random Forest": _pipe(RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))}
    rows, best, best_r2 = [], None, -9
    for name, p in candidates.items():
        p.fit(Xtr, ytr)
        pred = p.predict(Xte)
        r2, mae = r2_score(yte, pred), mean_absolute_error(yte, pred)
        rows.append({"Model": name, "R2": round(r2, 4), "MAE": round(mae)})
        if r2 > best_r2:
            best, best_r2 = p, r2
    return best, pd.DataFrame(rows), df
