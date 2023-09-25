from enum import StrEnum


class CardStatus(StrEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    BLOCKED = "BLOCKED"
    ISSUANCE = "ISSUANCE"


class BlockReason(StrEnum):
    STOLEN = "Card was stolen"
    LOST = "Card was lost"
    SUSPICIOUS = "Suspicious transactions"
    NO_NEED = "I no longer need to use this card"
    OTHER = "Other"


class Currency(StrEnum):
    EUR = "EUR"
    USD = "USD"
    # CHF = "CHF"
    # PLN = "PLN"
    # CZK = "CZK"
    # GBP = "GBP"


class Branch(StrEnum):
    Berlin_1 = "Berlin, Bd de Dixmude 40"
    Berlin_2 = "Berlin, Kloosterstrat 132"
    Bruxelles_1 = "Bruxelles, Rue Stevin 31/47"
    Bruxelles_2 = "Bruxelles, Rue de la Loi 106"
    Madrid_1 = "Madrid, C. Gran Vía, 62"
    Madrid_2 = "Madrid, Calles, C.del Marqués de Villamagna, 3"
    Paris_1 = "Paris, 18 Rue du 4 Septembre"
    Paris_2 = "Paris, 25 Rue Jean Giraudoux"
    Prague = "Prague, Palác Astra, Václavské nám. 773/4"
    Rome = "Rome, Via Parigi, 13/15"
    Sofia = "Sofia, bul. Kniaz Aleksandar Dondukov 13"
    Stockholm = "Stockholm, Humlegårdsgatan 12B"


class City(StrEnum):
    Berlin = "Berlin"
    Bruxelles = "Bruxelles"
    Madrid = "Madrid"
    Paris = "Paris"
    Prague = "Prague"
    Rome = "Rome"
    Sofia = "Sofia"
    Stockholm = "Stockholm"


class CardProducts(StrEnum):
    Standard = "Standard"
    Premium = "Premium"
    Virtual = "Virtual"


class PaymentSystem(StrEnum):
    # VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    # AMERICAN_EXPRESS = "AMERICAN_EXPRESS"
    # CHINA_UNIONPAY = "CHINA_UNIONPAY"
    # JCB = "JCB"
    # DINERS_CLUB = "DINERS_CLUB"
    # DISCOVER = "DISCOVER"
