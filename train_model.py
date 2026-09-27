from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
MODEL_PATH = ROOT / "modelo_risco_defasagem.joblib"


def harmonize(df, year):
    y = int(year)
    d = df.copy()
    d["defas"] = d["Defas"] if y == 2022 else d["Defasagem"]
    d["pedra"] = d["Pedra 22"] if y == 2022 else d[f"Pedra {y}"]
    d["pedra_cat"] = d["pedra"].astype(str).replace({"Agata": "Ágata"})
    return d


def transition(years, year):
    current = years[year].set_index("RA")
    next_year = years[year + 1].set_index("RA")
    common = current.index.intersection(next_year.index)
    X = current.loc[common].copy()
    y = (next_year.loc[common, "defas"] < 0).astype(int)
    return X, y


def main():
    raw = {
        y: pd.read_excel(DATA_PATH, sheet_name=f"PEDE{y}")
        for y in [2022, 2023, 2024]
    }
    years = {y: harmonize(raw[y], y) for y in raw}

    X22, y23 = transition(years, 2022)
    X23, y24 = transition(years, 2023)

    features = ["IAN", "IDA", "IEG", "IAA", "IPS", "IPV", "pedra_cat"]
    numeric = ["IAN", "IDA", "IEG", "IAA", "IPS", "IPV"]
    categorical = ["pedra_cat"]

    X = pd.concat([X22[features], X23[features]], ignore_index=True)
    y = pd.concat([y23, y24], ignore_index=True)

    preprocessor = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical),
    ])

    model = Pipeline([
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ])

    # Modelo de produção: após a avaliação temporal no notebook,
    # aproveitamos os dois ciclos rotulados disponíveis para treinar
    # o artefato que será utilizado pela aplicação.
    model.fit(X, y)

    artifact = {
        "model": model,
        "features": features,
        "training_periods": "2022→2023 + 2023→2024",
        "target": "Defasagem < 0 no ciclo seguinte",
        "thresholds": {"low": 0.30, "high": 0.70},
    }
    joblib.dump(artifact, MODEL_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")
    print(f"Observações de treinamento: {len(X)}")
    print(f"Taxa de risco no treinamento: {y.mean():.3f}")


if __name__ == "__main__":
    main()
