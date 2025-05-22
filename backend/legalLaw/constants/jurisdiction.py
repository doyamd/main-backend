from enum import Enum

class Jurisdiction(Enum):
    FEDERAL = "Federal Government"
    ADDIS_ABABA = "Addis Ababa Municipality"
    OROMIA = "Oromia Regional State"
    TIGRAY = "Tigray Regional State"
    AMHARA = "Amhara Regional State"
    SNNPR = "Southern Nations, Nationalities, and Peoples' Regional State (SNNPR)"
    SIDAMA = "Sidama Regional State"
    AFAR = "Afar Regional State"
    SOMALI = "Somali Regional State"
    BENISHANGUL_GUMUZ = "Benishangul-Gumuz Regional State"
    GAMBELA = "Gambela Regional State"
    HARARI = "Harari Regional State"
    DIRE_DAWA = "Dire Dawa City Administration"

    @classmethod
    def choices(cls):
        return [(jurisdiction.value, jurisdiction.value) for jurisdiction in cls]

    @classmethod
    def values(cls):
        return [jurisdiction.value for jurisdiction in cls]
