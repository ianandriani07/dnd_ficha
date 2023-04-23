from typing import Optional, Union, NamedTuple
from classes_def import ModelClassArtificer, ModelClassBarbarian, ModelClassBard, ModelClassCleric, ModelClassDruid, ModelClassFighter, ModelClassMonk, ModelClassPaladin, ModelClassRanger, ModelClassRogue, ModelClassSorcerer, ModelClassWarlock, ModelClassWizard
from races_def import Race


class SavingThrows(NamedTuple):
    STR: bool
    DEX: bool
    CONS: bool
    INT: bool
    WIS: bool
    CHAR: bool


class Skills(NamedTuple):
    strength: Optional[bool]
    athletics: Optional[bool]
    dexterity: Optional[bool]
    acrobatics: Optional[bool]
    sleight_of_hand: Optional[bool]
    stealth: Optional[bool]
    intelligence: Optional[bool]
    arcana: Optional[bool]
    history: Optional[bool]
    investigation: Optional[bool]
    nature: Optional[bool]
    religion: Optional[bool]
    wisdom: Optional[bool]
    animal_handling: Optional[bool]
    insight: Optional[bool]
    medicine: Optional[bool]
    perception: Optional[bool]
    survival: Optional[bool]
    charisma: Optional[bool]
    deception: Optional[bool]
    intimidation: Optional[bool]
    performance: Optional[bool]
    persuasion: Optional[bool]


class Dice(NamedTuple):
    # ndy
    n: int
    y: int
    bonus: Optional[int]


class Attributes(NamedTuple):
    STR: int = 0
    DEX: int = 0
    CONS: int = 0
    INT: int = 0
    WIS: int = 0
    CHAR: int = 0


class Features(NamedTuple):
    name: str
    description_per_level: dict[int, str]


class Proficiencies(NamedTuple):
    armor: str
    weapons: str
    tools: str
    saving_throws: SavingThrows
    skills: Skills


class TrueClass:
    name: str
    level: int
    hit_points: int
    _class: Union[ModelClassArtificer,
                  ModelClassBarbarian,
                  ModelClassBard,
                  ModelClassCleric,
                  ModelClassDruid,
                  ModelClassFighter,
                  ModelClassMonk,
                  ModelClassPaladin,
                  ModelClassRanger,
                  ModelClassRogue,
                  ModelClassSorcerer,
                  ModelClassWarlock,
                  ModelClassWizard]
    race: Race
    background: str
    equipment: list[str]
    proficiencies: Proficiencies
    cantrips: Optional[str]
    spells: Optional[str]
    features: list[Features]
