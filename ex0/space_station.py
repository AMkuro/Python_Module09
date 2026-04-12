from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> str:
    status_msg: str = (
        "Operational" if station.is_operational else "Not Operational"
    )
    lines: list[str] = [
        "Valid station created",
        f"ID: {station.station_id}",
        f"Name: {station.name}",
        f"Crew: {station.crew_size} people",
        f"Power: {station.power_level}%",
        f"Oxygen: {station.oxygen_level}%",
        f"Status: {status_msg}",
    ]
    return "\n".join(lines)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-04-10T12:30:00",
        notes="Primary orbital research station.",
    )
    print(display_station(valid_station))

    print("\n" + "=" * 40)
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="BAD001",
            name="Broken Station",
            crew_size=25,
            power_level=70.0,
            oxygen_level=88.0,
            last_maintenance="2026-04-01T08:00:00",
        )
    except ValidationError as exc:
        print(exc.errors()[0]["msg"])


# def test() -> None:
#     from generated_data.space_stations import SPACE_STATIONS
#
#     try:
#         stations = [
#             SpaceStation.model_validate(data) for data in SPACE_STATIONS
#         ]
#     except ValidationError as exc:
#         print("Validation error:")
#         print(exc)
#         return
#
#     print("=== Space Station Data Validation ===")
#     for station in stations:
#         print(display_station(station))
#         print("-" * 40)


if __name__ == "__main__":
    main()
    # test()
