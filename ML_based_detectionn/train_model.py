#!/usr/bin/env python3
"""
ML Model Training Script for NeuroShield Malware Detection

This script trains a Random Forest classifier on PE file features.
It can work with either a CSV dataset or extract features from PE files.

Usage:
    python train_model.py --dataset path/to/dataset.csv
    python train_model.py --extract-from-files path/to/malware path/to/benign
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Import feature extraction
from feature_extraction import extract_features

# Feature names expected by the model (23 features)
EXPECTED_FEATURES = [
    'MajorLinkerVersion', 'MinorOperatingSystemVersion', 'MajorSubsystemVersion',
    'SizeOfStackReserve', 'TimeDateStamp', 'MajorOperatingSystemVersion',
    'Characteristics', 'ImageBase', 'Subsystem', 'MinorImageVersion',
    'MinorSubsystemVersion', 'SizeOfInitializedData', 'DllCharacteristics',
    'DirectoryEntryExport', 'ImageDirectoryEntryExport', 'CheckSum',
    'DirectoryEntryImportSize', 'SectionMaxChar', 'MajorImageVersion',
    'AddressOfEntryPoint', 'SectionMinEntropy', 'SizeOfHeaders',
    'SectionMinVirtualsize'
]

def train_from_csv(csv_path):
    """Train model from CSV dataset"""
    print(f"\n{'='*60}")
    print("Training Model from CSV Dataset")
    print(f"{'='*60}\n")
    
    # Load dataset
    print(f"📁 Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} samples")
    
    # Check for required columns
    if 'Malware' not in df.columns:
        print("❌ Error: Dataset must have a 'Malware' column (target)")
        return None
    
    # Separate features and target
    # Drop non-feature columns (Name, Malware)
    X = df.drop(columns=['Malware', 'Name'] if 'Name' in df.columns else ['Malware'])
    y = df['Malware']
    
    print(f"\n📊 Dataset Information:")
    print(f"   - Total samples: {len(df)}")
    print(f"   - Malware samples: {sum(y == 1)} ({sum(y == 1)/len(y)*100:.1f}%)")
    print(f"   - Benign samples: {sum(y == 0)} ({sum(y == 0)/len(y)*100:.1f}%)")
    print(f"   - Features: {len(X.columns)}")
    
    return train_model(X, y)

def extract_features_from_files(malware_dir, benign_dir):
    """Extract features from PE files in directories"""
    print(f"\n{'='*60}")
    print("Extracting Features from PE Files")
    print(f"{'='*60}\n")
    
    features_list = []
    labels = []
    
    # Process malware files
    if os.path.exists(malware_dir):
        print(f"📁 Processing malware files from: {malware_dir}")
        malware_files = [f for f in os.listdir(malware_dir) if f.endswith(('.exe', '.dll'))]
        for i, filename in enumerate(malware_files, 1):
            filepath = os.path.join(malware_dir, filename)
            try:
                features = extract_features(filepath)
                features_list.append(features.iloc[0])
                labels.append(1)  # Malware
                print(f"   ✅ [{i}/{len(malware_files)}] {filename}")
            except Exception as e:
                print(f"   ⚠️  [{i}/{len(malware_files)}] {filename}: {str(e)}")
    
    # Process benign files
    if os.path.exists(benign_dir):
        print(f"\n📁 Processing benign files from: {benign_dir}")
        benign_files = [f for f in os.listdir(benign_dir) if f.endswith(('.exe', '.dll'))]
        for i, filename in enumerate(benign_files, 1):
            filepath = os.path.join(benign_dir, filename)
            try:
                features = extract_features(filepath)
                features_list.append(features.iloc[0])
                labels.append(0)  # Benign
                print(f"   ✅ [{i}/{len(benign_files)}] {filename}")
            except Exception as e:
                print(f"   ⚠️  [{i}/{len(benign_files)}] {filename}: {str(e)}")
    
    if not features_list:
        print("\n❌ No features extracted. Please provide valid PE files.")
        return None
    
    # Create DataFrame
    X = pd.DataFrame(features_list)
    y = pd.Series(labels)
    
    print(f"\n📊 Extracted Features:")
    print(f"   - Total samples: {len(X)}")
    print(f"   - Malware samples: {sum(y == 1)}")
    print(f"   - Benign samples: {sum(y == 0)}")
    
    return train_model(X, y)

def train_model(X, y):
    """Train the Random Forest model"""
    print(f"\n{'='*60}")
    print("Training Random Forest Classifier")
    print(f"{'='*60}\n")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Data Split:")
    print(f"   - Training samples: {len(X_train)}")
    print(f"   - Testing samples: {len(X_test)}")
    
    # Train model
    print(f"\n🤖 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print(f"✅ Model trained successfully!")
    
    # Evaluate on test set
    print(f"\n{'='*60}")
    print("Model Evaluation")
    print(f"{'='*60}\n")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"📈 Accuracy: {accuracy*100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Benign', 'Malware']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"                 Predicted")
    print(f"               Benign  Malware")
    print(f"Actual Benign    {cm[0][0]:>4}    {cm[0][1]:>4}")
    print(f"       Malware   {cm[1][0]:>4}    {cm[1][1]:>4}")
    
    # Cross-validation
    print(f"\n🔄 Performing 5-fold cross-validation...")
    cv_scores = cross_val_score(model, X, y, cv=5, n_jobs=-1)
    print(f"✅ Cross-validation scores: {cv_scores}")
    print(f"✅ Mean CV accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*2*100:.2f}%)")
    
    # Feature importance
    print(f"\n📊 Top 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['feature']:30s}: {row['importance']:.4f}")
    
    return model

def create_sample_model():
    """Create a sample model for demonstration purposes"""
    print(f"\n{'='*60}")
    print("Creating Sample/Demo Model")
    print(f"{'='*60}\n")
    
    print("⚠️  No dataset provided. Creating a sample model for demonstration.")
    print("   This model is for testing purposes only and should be replaced")
    print("   with a properly trained model using real malware/benign data.\n")
    
    # Create synthetic data matching the expected features
    n_samples = 1000
    n_malware = 700
    n_benign = 300
    
    # Generate random features that roughly match typical PE file characteristics
    np.random.seed(42)
    
    # Malware samples (tend to have certain characteristics)
    malware_data = {
        'MajorLinkerVersion': np.random.randint(8, 15, n_malware),
        'MinorOperatingSystemVersion': np.random.randint(0, 10, n_malware),
        'MajorSubsystemVersion': np.random.randint(4, 11, n_malware),
        'SizeOfStackReserve': np.random.randint(100000, 2000000, n_malware),
        'TimeDateStamp': np.random.randint(1000000000, 2000000000, n_malware),
        'MajorOperatingSystemVersion': np.random.randint(4, 11, n_malware),
        'Characteristics': np.random.randint(0, 65535, n_malware),
        'ImageBase': np.random.choice([65536, 4194304], n_malware),
        'Subsystem': np.random.randint(1, 4, n_malware),
        'MinorImageVersion': np.random.randint(0, 10, n_malware),
        'MinorSubsystemVersion': np.random.randint(0, 10, n_malware),
        'SizeOfInitializedData': np.random.randint(1000, 500000, n_malware),
        'DllCharacteristics': np.random.randint(0, 65535, n_malware),
        'DirectoryEntryExport': np.random.randint(0, 2, n_malware),
        'ImageDirectoryEntryExport': np.random.randint(0, 10000, n_malware),
        'CheckSum': np.random.randint(0, 1000000, n_malware),
        'DirectoryEntryImportSize': np.random.randint(100, 50000, n_malware),
        'SectionMaxChar': np.random.randint(3, 8, n_malware),
        'MajorImageVersion': np.random.randint(0, 10, n_malware),
        'AddressOfEntryPoint': np.random.randint(1000, 100000, n_malware),
        'SectionMinEntropy': np.random.uniform(4, 8, n_malware),  # Higher entropy for malware
        'SizeOfHeaders': np.random.randint(200, 2000, n_malware),
        'SectionMinVirtualsize': np.random.randint(1000, 50000, n_malware),
    }
    
    # Benign samples
    benign_data = {
        'MajorLinkerVersion': np.random.randint(8, 15, n_benign),
        'MinorOperatingSystemVersion': np.random.randint(0, 10, n_benign),
        'MajorSubsystemVersion': np.random.randint(4, 11, n_benign),
        'SizeOfStackReserve': np.random.randint(100000, 2000000, n_benign),
        'TimeDateStamp': np.random.randint(1000000000, 2000000000, n_benign),
        'MajorOperatingSystemVersion': np.random.randint(4, 11, n_benign),
        'Characteristics': np.random.randint(0, 65535, n_benign),
        'ImageBase': np.random.choice([65536, 4194304], n_benign),
        'Subsystem': np.random.randint(1, 4, n_benign),
        'MinorImageVersion': np.random.randint(0, 10, n_benign),
        'MinorSubsystemVersion': np.random.randint(0, 10, n_benign),
        'SizeOfInitializedData': np.random.randint(1000, 500000, n_benign),
        'DllCharacteristics': np.random.randint(0, 65535, n_benign),
        'DirectoryEntryExport': np.random.randint(0, 2, n_benign),
        'ImageDirectoryEntryExport': np.random.randint(0, 10000, n_benign),
        'CheckSum': np.random.randint(0, 1000000, n_benign),
        'DirectoryEntryImportSize': np.random.randint(100, 50000, n_benign),
        'SectionMaxChar': np.random.randint(3, 8, n_benign),
        'MajorImageVersion': np.random.randint(0, 10, n_benign),
        'AddressOfEntryPoint': np.random.randint(1000, 100000, n_benign),
        'SectionMinEntropy': np.random.uniform(1, 5, n_benign),  # Lower entropy for benign
        'SizeOfHeaders': np.random.randint(200, 2000, n_benign),
        'SectionMinVirtualsize': np.random.randint(1000, 50000, n_benign),
    }
    
    # Combine data
    X_malware = pd.DataFrame(malware_data)
    X_benign = pd.DataFrame(benign_data)
    X = pd.concat([X_malware, X_benign], ignore_index=True)
    y = pd.Series([1]*n_malware + [0]*n_benign)
    
    print(f"✅ Created synthetic dataset:")
    print(f"   - Total samples: {n_samples}")
    print(f"   - Malware samples: {n_malware}")
    print(f"   - Benign samples: {n_benign}")
    
    return train_model(X, y)

def save_model(model, output_path='ML_model/malwareclassifier-V2.pkl'):
    """Save the trained model"""
    print(f"\n{'='*60}")
    print("Saving Model")
    print(f"{'='*60}\n")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save model
    joblib.dump(model, output_path)
    file_size = os.path.getsize(output_path)
    print(f"✅ Model saved successfully!")
    print(f"   - Path: {output_path}")
    print(f"   - Size: {file_size/1024:.2f} KB")
    
    # Test loading
    print(f"\n🔍 Testing model loading...")
    loaded_model = joblib.load(output_path)
    print(f"✅ Model loaded successfully!")
    print(f"   - Type: {type(loaded_model).__name__}")
    print(f"   - Features: {loaded_model.n_features_in_}")
    
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Train malware detection model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train from CSV dataset
  python train_model.py --dataset /path/to/dataset_malwares.csv
  
  # Train by extracting features from PE files
  python train_model.py --extract-from-files /path/to/malware /path/to/benign
  
  # Create sample/demo model
  python train_model.py --create-sample
        """
    )
    
    parser.add_argument('--dataset', help='Path to CSV dataset file')
    parser.add_argument('--extract-from-files', nargs=2, metavar=('MALWARE_DIR', 'BENIGN_DIR'),
                        help='Extract features from PE files in directories')
    parser.add_argument('--create-sample', action='store_true',
                        help='Create a sample model for demonstration')
    parser.add_argument('--output', default='ML_model/malwareclassifier-V2.pkl',
                        help='Output path for trained model (default: ML_model/malwareclassifier-V2.pkl)')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("NeuroShield ML Model Training")
    print(f"{'='*60}")
    
    model = None
    
    # Train model based on input
    if args.dataset:
        if not os.path.exists(args.dataset):
            print(f"\n❌ Error: Dataset file not found: {args.dataset}")
            return 1
        model = train_from_csv(args.dataset)
    elif args.extract_from_files:
        malware_dir, benign_dir = args.extract_from_files
        model = extract_features_from_files(malware_dir, benign_dir)
    elif args.create_sample:
        model = create_sample_model()
    else:
        print("\n⚠️  No training data specified. Creating sample model...")
        print("   Use --help for usage information\n")
        model = create_sample_model()
    
    # Save model
    if model is not None:
        model_path = save_model(model, args.output)
        print(f"\n{'='*60}")
        print("🎉 Training Complete!")
        print(f"{'='*60}")
        print(f"\nYour model is ready at: {model_path}")
        print(f"\nTo use it in the application:")
        print(f"1. Ensure the model is at: ML_model/malwareclassifier-V2.pkl")
        print(f"2. Start the Flask app: python app.py")
        print(f"3. Upload PE files for analysis at http://localhost:5000")
        return 0
    else:
        print("\n❌ Model training failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())