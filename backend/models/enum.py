import enum

class RadioType(enum.StrEnum):
    """Network radio types with modern standards included."""
    GSM = "GSM"       # 2G
    CDMA = "CDMA"     # 2G alternative
    UMTS = "UMTS"     # 3G
    WCDMA = "WCDMA"   # 3G alternative
    LTE = "LTE"       # 4G
    NR = "NR"         # 5G
    TETRA = "TETRA"   # Specialized networks