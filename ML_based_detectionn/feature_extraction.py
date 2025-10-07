import pefile
import pandas as pd
import math

# Function to calculate entropy of a section
def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def extract_features(file_path):
    try:
        pe = pefile.PE(file_path)
    except (pefile.PEFormatError, OSError, IOError) as e:
        # Return default features if PE parsing fails
        print(f"Error parsing PE file {file_path}: {e}")
        return pd.DataFrame([{
            'MajorLinkerVersion': 0, 'MinorOperatingSystemVersion': 0, 'MajorSubsystemVersion': 0,
            'SizeOfStackReserve': 0, 'TimeDateStamp': 0, 'MajorOperatingSystemVersion': 0,
            'Characteristics': 0, 'ImageBase': 0, 'Subsystem': 0, 'MinorImageVersion': 0,
            'MinorSubsystemVersion': 0, 'SizeOfInitializedData': 0, 'DllCharacteristics': 0,
            'DirectoryEntryExport': 0, 'ImageDirectoryEntryExport': 0, 'CheckSum': 0,
            'DirectoryEntryImportSize': 0, 'SectionMaxChar': 0, 'MajorImageVersion': 0,
            'AddressOfEntryPoint': 0, 'SectionMinEntropy': 0, 'SizeOfHeaders': 0,
            'SectionMinVirtualsize': 0
        }])

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
    entropies = []
    try:
        for section in pe.sections:
            entropy = calculate_entropy(section.get_data())
            entropies.append(entropy)
        
        if entropies:
            features['SectionMinEntropy'] = min(entropies)
        else:
            features['SectionMinEntropy'] = 0
    except Exception as e:
        print(f"Error calculating section entropy: {e}")
        features['SectionMinEntropy'] = 0

    # Calculate SectionMinVirtualsize (example calculation)
    try:
        if pe.sections:
            features['SectionMinVirtualsize'] = min(section.Misc_VirtualSize for section in pe.sections)
        else:
            features['SectionMinVirtualsize'] = 0
    except Exception as e:
        print(f"Error calculating section virtual size: {e}")
        features['SectionMinVirtualsize'] = 0

    return pd.DataFrame([features])
