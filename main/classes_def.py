from typing import Union, NamedTuple
from character_def import Dice, Features, Attributes


class HitPoints(NamedTuple):
    dice: Dice
    hit_points_at_1st_level: int
    hit_points_at_higher_levels: Union[
        Dice, int]


class ModelClassLevel(NamedTuple):
    features: list[Features]
    proficiency_bonus: int


class ModelClassLevelArtificer(ModelClassLevel):
    infusions_known: int
    infused_items: int
    cantrips_known: int
    spell_slot: list[int]


class ModelClassLevelBarbarian(ModelClassLevel):
    rages: int
    rage_damage: int


class ModelClassLevelBard(ModelClassLevel):
    cantrips_known: int
    spells_known: int
    spell_slot: list[int]


class ModelClassLevelCleric(ModelClassLevel):
    cantrips_known: list[int]
    spell_slot: list[int]


class ModelClassLevelDruid(ModelClassLevel):
    cantrips_known: list[int]
    spell_slot: list[int]


class ModelClassLevelMonk(ModelClassLevel):
    martial_arts: Dice
    ki_points: int
    unarmored_movement: int


class ModelClassLevelPaladin(ModelClassLevel):
    spell_slot: list[int]


class ModelClassLevelRanger(ModelClassLevel):
    spells_known: int
    spell_slot: list[int]


class ModelClassLevelRogue(ModelClassLevel):
    sneak_attack: Dice


class ModelClassLevelSorcerer(ModelClassLevel):
    sorcery_points: int
    cantrips_known: int
    spells_known: int
    spell_slot: list[int]


class ModelClassLevelWarlock(ModelClassLevel):
    cantrips_known: int
    spells_known: int
    spell_slots: int
    slot_level: int
    invocations_known: int


class ModelClassLevelWizard(ModelClassLevel):
    cantrips_known: int
    spell_slot: list[int]


class Path(NamedTuple):
    features: list[Features]


class ModelClass(NamedTuple):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]


def test(a):
    return a

################## CLASSES DEFINITION #########################


class ModelClassArtificer(ModelClass):
    name: str = 'Artificer'
    multiclass: Attributes = Attributes(INT=13)
    equipment: list[str] = []
    subclasses: list[Path] = []
    class_levels: list[ModelClassLevelArtificer] = [ModelClassLevelArtificer()]
    spell_save_dc: int
    spell_attack_modifier: int


class ModelClassBarbarian(ModelClass):
    name: str = 'Barbarian'
    multiclass: Attributes = Attributes(STR=13)
    equipment: list[str] = []
    subclasses: list[Path] = []
    class_levels: list[ModelClassLevelBarbarian] = [ModelClassLevelBarbarian()]


class ModelClassBard(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelBard]


class ModelClassCleric(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelCleric]


class ModelClassDruid(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelDruid]


class ModelClassFighter(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevel]


class ModelClassMonk(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelMonk]


class ModelClassPaladin(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelPaladin]


class ModelClassRanger(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelRanger]


class ModelClassRogue(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelRogue]


class ModelClassSorcerer(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelSorcerer]


class ModelClassWarlock(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelWarlock]


class ModelClassWizard(ModelClass):
    name: str
    multiclass: Attributes
    equipment: list[str]
    subclasses: list[Path]
    class_levels: list[ModelClassLevelWizard]
