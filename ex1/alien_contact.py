from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def custom_validation_rules(self) -> AlienContact:
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals must include a received message")

        return self


def display_contact(contact: AlienContact) -> str:
    lines: list[str] = [
        "Valid contact report:",
        f"ID:{contact.contact_id}",
        f"Type: {contact.contact_type}",
        f"Location: {contact.location}",
        f"Signal: {contact.signal_strength} / 10",
        f"Duration: {contact.duration_minutes} minutes",
        f"Witnesses: {contact.witness_count}",
        f"Message: {contact.message_received!r}",
    ]
    return "\n".join(lines)


def main() -> None:

    print("Alien Contact Log Validation")
    print("=" * 40)

    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-08-12T22:30:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False,
    )
    print(display_contact(valid_contact))

    print("\n" + "=" * 40)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-08-13T01:15:00",
            location="Nevada Desert",
            contact_type=ContactType.telepathic,
            signal_strength=6.2,
            duration_minutes=20,
            witness_count=2,
            message_received=None,
            is_verified=False,
        )
    except ValidationError as exc:
        first_error = exc.errors()[0]
        print(first_error["ctx"]["error"])


if __name__ == "__main__":
    main()
