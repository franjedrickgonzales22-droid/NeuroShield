import pefile
import pandas as pd
import math
import logging

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
    except Exception as e:
        logging.error(f"Error parsing PE file {file_path}: {str(e)}")
        raise ValueError(f"Invalid PE file: {str(e)}")

    try:
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
            'SectionMaxChar': len(pe.sections),
            'MajorImageVersion': pe.OPTIONAL_HEADER.MajorImageVersion,
            'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            'SectionMinEntropy': 0,  # Will be calculated
            'SizeOfHeaders': pe.OPTIONAL_HEADER.SizeOfHeaders,
            'SectionMinVirtualsize': 0  # Will be calculated
        }

        # Calculate SectionMinEntropy
        entropies = []
        for section in pe.sections:
            try:
                entropy = calculate_entropy(section.get_data())
                entropies.append(entropy)
            except Exception as e:
                logging.warning(f"Error calculating entropy for section: {str(e)}")
                entropies.append(0)

        if entropies:
            features['SectionMinEntropy'] = min(entropies)

        # Calculate SectionMinVirtualsize
        try:
            virtual_sizes = [section.Misc_VirtualSize for section in pe.sections if hasattr(section, 'Misc_VirtualSize')]
            if virtual_sizes:
                features['SectionMinVirtualsize'] = min(virtual_sizes)
        except Exception as e:
            logging.warning(f"Error calculating virtual sizes: {str(e)}")
            features['SectionMinVirtualsize'] = 0

        return pd.DataFrame([features])
        
    except Exception as e:
        logging.error(f"Error extracting features from {file_path}: {str(e)}")
        raise ValueError(f"Feature extraction failed: {str(e)}")
    finally:
        # Clean up PE object
        try:
            pe.close()
        except:
            pass
