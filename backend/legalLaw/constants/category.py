from enum import Enum

class LegalCategory(Enum):
    CONSTITUTIONAL = "Constitutional"
    CIVIL = "Civil"
    CRIMINAL = "Criminal"
    COMMERCIAL = "Commercial"
    LABOR = "Labor"
    FAMILY = "Family"
    INVESTMENT = "Investment"
    HUMAN_RIGHTS = "Human Rights"

    @classmethod
    def choices(cls):
        return [(category.value, category.value) for category in cls]

    @classmethod
    def values(cls):
        return [category.value for category in cls]
