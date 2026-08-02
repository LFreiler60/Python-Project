#takes raw JSON from API and converts it into a clean table that ML model can use 
#creates CSV file with metar observations




import csv
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from ml.features import extract_ceiling


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIRECTORY = PROJECT_ROOT / "data" / "processed"


def parse_visibility(value):
    """Convert an API visibility value to statute miles."""

    if value is None:
        return None

    text = str(value).strip().replace("+", "")

    try:
        return float(text)
    except ValueError:
        return float(Fraction(text))


def convert_observation(observation):
    """Convert one raw METAR into a flat dictionary."""

    temperature = observation.get("temp")
    dewpoint = observation.get("dewp")

    if temperature is not None and dewpoint is not None:
        dewpoint_spread = round(
            temperature - dewpoint,
            1
        )
    else:
        dewpoint_spread = None

    observation_timestamp = observation.get("obsTime")

    if observation_timestamp is not None:
        observation_time = datetime.fromtimestamp(
            observation_timestamp,
            tz=timezone.utc,
        ).isoformat()
    else:
        observation_time = None

    clouds = observation.get("clouds", [])

    return {
        "station": observation.get("icaoId"),
        "observation_time": observation_time,
        "temperature_c": temperature,
        "dewpoint_c": dewpoint,
        "dewpoint_spread_c": dewpoint_spread,
        "wind_direction_deg": observation.get("wdir"),
        "wind_speed_kt": observation.get("wspd"),
        "visibility_sm": parse_visibility(
            observation.get("visib")
        ),
        "ceiling_ft": extract_ceiling(clouds),
        "flight_category": observation.get("fltCat"),
    }


def process_station(station_id):
    """Convert a station's raw JSON into a processed CSV."""

    station_id = station_id.strip().upper()

    input_path = (
        RAW_DATA_DIRECTORY
        / f"{station_id}_metars.json"
    )

    if not input_path.exists():
        print(f"Raw data file not found: {input_path}")
        return None

    with input_path.open("r", encoding="utf-8") as file:
        observations = json.load(file)

    processed_rows = [
        convert_observation(observation)
        for observation in observations
    ]

    #sorts data in chronological order-oldest to newest
    processed_rows.sort(
    key=lambda row: row["observation_time"] or ""
    )

    PROCESSED_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        PROCESSED_DATA_DIRECTORY
        / f"{station_id}_processed.csv"
    )

    fieldnames = list(processed_rows[0].keys())

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(processed_rows)

    print(
        f"Saved {len(processed_rows)} processed observations "
        f"to {output_path}"
    )

    return output_path


def main():
    station_id = input(
        "Enter an ICAO station identifier: "
    )

    process_station(station_id)


if __name__ == "__main__":
    main()
