from enum import Enum


class Text_Type(Enum):
    # Lineages
    L_CAMPAIGN = 5
    L_SUBRACE = 10
    L_DESCRIPTION = 15
    L_CATEGORY = 20
    L_CATEGORY_DESCRIPTION = 25
    L_CATEGORY_EXPANSION = 30
    L_SUBCATEGORY = 35
    L_SUBCATEGORY_DESCRIPTION = 40
    L_TABLE_NAME = 45
    L_TABLE = 50
    # Classes
    C_MAIN_DESCRIPTION = 55
    C_MULTICLASS_REQ = 60
    C_MAIN_CLASS_INFO_TABLE = 65
    C_CLASS_FEATURES = 66
    C_BASIC_FEATURES = 70
    C_BASIC_FEATURES_CATEGORY = 75
    C_BASIC_FEATURES_CATEGORY_DESCRIPTION = 80
    C_SPECIAL_FEATURES_CATEGORY = 85
    C_SPECIAL_FEATURES_CATEGORY_TABLE = 90
    C_FEATURES_DESCRIPTION = 95
    C_FEATURES_EXPANSION = 100
