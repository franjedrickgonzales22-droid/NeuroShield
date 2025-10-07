import pefile
import pandas as pd
import math
from typing import List

# Function to calculate entropy of a section
def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    # Use a frequency table to avoid repeated count() calls
    length = len(data)
    if length == 0:
        return 0.0
    counts: List[int] = [0] * 256
    for b in data:
        counts[b] += 1
    entropy = 0.0
    for count in counts:
        if count:
            p_x = count / length
            entropy -= p_x * math.log(p_x, 2)
    return entropy

def extract_features(file_path: str) -> pd.DataFrame:
    pe = pefile.PE(file_path)

    # Extract the specified 23 features in the given order
    features = {
        'MajorLinkerVersion': pe.OPTIONAL_HEADER.MajorLinkerVersion,
        'MinorOperatingSystemVersion': pe.OPTIONAL_HEADER.MinorOperatingSystemVersion,
        'MajorSubsystemVersion': pe.OPTIONAL_HEADER.MajorSubsystemVersion,
        'SizeOfStackReserve': pe.OPTIONAL_HEADER.SizeOfStackReserve,
        'TimeDateStamp': pe.FILE_HEADER.TimeDateStamp,
        'MajorOperatingSystemVersion': pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
        'Characteristics': pe.FILE_HEADER.Characteristics,
        'ImageBase': pe.OPTIONAL_HEADER.ImageBase,
        'Subsystem': pe.OPTIONAL_HEADER.Subsystem,
        'MinorImageVersion': pe.OPTIONAL_HEADER.MinorImageVersion,
        'MinorSubsystemVersion': pe.OPTIONAL_HEADER.MinorSubsystemVersion,
        'SizeOfInitializedData': pe.OPTIONAL_HEADER.SizeOfInitializedData,
        'DllCharacteristics': pe.OPTIONAL_HEADER.DllCharacteristics,
        'DirectoryEntryExport': 1 if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0,
        'ImageDirectoryEntryExport': pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].Size if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT') else 0,
        'CheckSum': pe.OPTIONAL_HEADER.CheckSum,
        'DirectoryEntryImportSize': pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].Size if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT') else 0,
        'SectionMaxChar': len(pe.sections),  # Example calculation for demonstration
        'MajorImageVersion': pe.OPTIONAL_HEADER.MajorImageVersion,
        'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
        'SectionMinEntropy': None,  # Placeholder, will be calculated
        'SizeOfHeaders': pe.OPTIONAL_HEADER.SizeOfHeaders,
        'SectionMinVirtualsize': None  # Placeholder, will be calculated
    }

    # Calculate SectionMinEntropy
    entropies = [calculate_entropy(section.get_data()) for section in pe.sections]
    if entropies:
        features['SectionMinEntropy'] = min(entropies)

    # Calculate SectionMinVirtualsize (example calculation)
    features['SectionMinVirtualsize'] = min(section.Misc_VirtualSize for section in pe.sections)

    return pd.DataFrame([features])
