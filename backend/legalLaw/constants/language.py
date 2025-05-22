from enum import Enum

class Language(Enum):
    ENGLISH = "English"
    AMHARIC = "Amharic"
    OROMO = "Oromo"
    TIGRINYA = "Tigrinya"
    SOMALI = "Somali"
    AFAR = "Afar"
    SIDAMO = "Sidamo"
    WOLAYTTA = "Wolaytta"
    GURAGE = "Gurage"
    HADIYYA = "Hadiyya"
    GAMO = "Gamo"
    KAFFA = "Kaffa"
    HARARI = "Harari"
    BENCH = "Bench"
    SHEKO = "Sheko"
    ANUAK = "Anuak"
    NUER = "Nuer"
    SHANQUELLA = "Shanqella"
    KONSO = "Konso"
    SILTE = "Silt'e"
    AGAW = "Agaw"

    @classmethod
    def choices(cls):
        return [(language.value, language.value) for language in cls]

    @classmethod
    def values(cls):
        return [language.value for language in cls]
