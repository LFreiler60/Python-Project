from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
)
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIRECTORY = PROJECT_ROOT / "data" / "processed"
MODEL_DIRECTORY = PROJECT_ROOT / "models"

FEATURE_NAMES = [
    "temperature_c",
    "dewpoint_c",
    "dewpoint_spread_c",
    "wind_direction_deg",
    "wind_speed_kt",
    "visibility_sm",
    "ceiling_ft",
    "current_category_code",
]

CATEGORY_CODES = {
    "LIFR": 0,
    "IFR": 1,
    "MVFR": 2,
    "VFR": 3,
}

CATEGORY_LABELS = [
    "LIFR",
    "IFR",
    "MVFR",
    "VFR",
]


def prepare_features(data):
    """Create numeric model inputs from processed weather data."""

    features = data[
        [
            "temperature_c",
            "dewpoint_c",
            "dewpoint_spread_c",
            "wind_direction_deg",
            "wind_speed_kt",
            "visibility_sm",
            "ceiling_ft",
        ]
    ].copy()

    for column in features.columns:
        features[column] = pd.to_numeric(
            features[column],
            errors="coerce",
        )

    features["ceiling_ft"] = (
        features["ceiling_ft"].fillna(12000)
    )

    features["current_category_code"] = (
        data["flight_category"].map(CATEGORY_CODES)
    )

    return features[FEATURE_NAMES]


def train_model(station_id):
    """Train and evaluate a flight-category model."""

    station_id = station_id.strip().upper()

    input_path = (
        PROCESSED_DIRECTORY
        / f"{station_id}_training.csv"
    )

    if not input_path.exists():
        print(f"Training data not found: {input_path}")
        return None

    data = pd.read_csv(
        input_path,
        parse_dates=["observation_time"],
    )

    data = data.dropna(
        subset=["future_flight_category"]
    ).sort_values("observation_time")

    split_index = int(len(data) * 0.8)

    training_rows = data.iloc[:split_index]
    testing_rows = data.iloc[split_index:]

    X_train = prepare_features(training_rows)
    y_train = training_rows["future_flight_category"]

    X_test = prepare_features(testing_rows)
    y_test = testing_rows["future_flight_category"]

    model = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=300,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    baseline_predictions = testing_rows[
        "flight_category"
    ]

    print(f"Training rows: {len(training_rows)}")
    print(f"Testing rows: {len(testing_rows)}")

    print(
        "Baseline accuracy:",
        accuracy_score(
            y_test,
            baseline_predictions,
        ),
    )

    print(
        "Model accuracy:",
        accuracy_score(
            y_test,
            predictions,
        ),
    )

    print(
        "Balanced accuracy:",
        balanced_accuracy_score(
            y_test,
            predictions,
        ),
    )

    print(
        classification_report(
            y_test,
            predictions,
            labels=CATEGORY_LABELS,
            zero_division=0,
        )
    )

    MODEL_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        MODEL_DIRECTORY
        / f"{station_id}_flight_category_model.joblib"
    )

    joblib.dump(
        {
            "model": model,
            "feature_names": FEATURE_NAMES,
            "category_codes": CATEGORY_CODES,
        },
        output_path,
    )

    print(f"Saved model to {output_path}")

    return output_path


def main():
    station_id = input(
        "Enter an ICAO station identifier: "
    )

    train_model(station_id)


if __name__ == "__main__":
    main()