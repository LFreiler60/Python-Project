import json
from pathlib import Path

from services.aviation_weather import AviationWx


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"


def collect_metars(station_id, hours=72):
    """Download METAR observations and save them as JSON."""

    station_id = station_id.strip().upper()

    aviation_weather = AviationWx()

    observations = aviation_weather.get_metar(
        station_id,
        hours=hours,
    )

    if not observations:
        print(f"No observations found for {station_id}.")
        return None

    RAW_DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        RAW_DATA_DIRECTORY
        / f"{station_id}_metars.json"
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            observations,
            file,
            indent=2,
        )

    print(
        f"Saved {len(observations)} observations "
        f"to {output_path}"
    )

    return output_path


def main():
    station_id = input(
        "Enter an ICAO station identifier: "
    )

    collect_metars(station_id)


if __name__ == "__main__":
    main()