# from typing import TypedDict
from typing import Optional
from character_def import Features, Attributes


class Duration:
    hours: int
    minutes: int
    seconds: int


class RacialSpells:
    name: str
    casting_time: int
    range: str
    components: str
    duration: Duration
    description: str


class Race:
    name: str
    description: str
    source: str
    ability_score_increase: Attributes
    age: int
    alignment: str
    size: str
    speed: int
    racial_features: Optional[list[Features]]
    racial_spells: Optional[list[RacialSpells]]
    languages: str
