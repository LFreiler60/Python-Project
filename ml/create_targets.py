from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIRECTORY = PROJECT_ROOT / "data" / "processed"


def create_targets(station_id):
    """Pair current weather with flight category one hour later."""

    station_id = station_id.strip().upper()

    input_path = (
        PROCESSED_DIRECTORY
        / f"{station_id}_processed.csv"
    )

    if not input_path.exists():
        print(f"Processed data not found: {input_path}")
        return None

    data = pd.read_csv(
        input_path,
        parse_dates=["observation_time"],
    )

    data = data.sort_values("observation_time")

    data["target_time"] = (
        data["observation_time"]
        + pd.Timedelta(hours=1)
    )

    future_categories = data[
        ["observation_time", "flight_category"]
    ].rename(
        columns={
            "observation_time": "future_observation_time",
            "flight_category": "future_flight_category",
        }
    )

    training_data = pd.merge_asof(
        data.sort_values("target_time"),
        future_categories.sort_values(
            "future_observation_time"
        ),
        left_on="target_time",
        right_on="future_observation_time",
        direction="nearest",
        tolerance=pd.Timedelta(minutes=20),
    )

    training_data = training_data.dropna(
        subset=["future_flight_category"]
    )

    output_path = (
        PROCESSED_DIRECTORY
        / f"{station_id}_training.csv"
    )

    training_data.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Saved {len(training_data)} training rows "
        f"to {output_path}"
    )

    return output_path


def main():
    station_id = input(
        "Enter an ICAO station identifier: "
    )

    create_targets(station_id)


if __name__ == "__main__":
    main()