from enum import Enum

class Region(str, Enum):
    wnam = "wnam"
    enam = "enam"
    weur = "weur"
    eeur = "eeur"
    apac = "apac"
    auto = "auto"