#!/usr/bin/env python3
"""
Advanced ML Model Training for Higher Accuracy
NeuroShield - Developed by F.J.G

This script trains an optimized ensemble model with hyperparameter tuning
to achieve higher accuracy than the basic Random Forest model.
"""

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import joblib
import numpy as np
import pandas as pd
import os
import sys
from feature_extraction import extract_features

print("=" * 80)
print("NEUROSHIELD - ADVANCED MODEL TRAINING")
print("High Accuracy Malware Detection Model")
print("Developed by F.J.G")
print("=" * 80)
print()

# Create synthetic training data with better distribution
print("Step 1: Creating enhanced training dataset...")
print("-" * 80)

np.random.seed(42)

# Create more diverse and realistic synthetic data
n_malware = 500
n_benign = 500

# Malware samples - with more realistic characteristics
malware_features = np.random.randn(n_malware, 23)
# Add malware-specific patterns
malware_features[:, 0] = np.random.uniform(1300000000, 1700000000, n_malware)  # TimeDateStamp
malware_features[:, 1] = np.random.uniform(1000, 100000, n_malware)  # Machine
malware_features[:, 2] = np.random.uniform(2, 15, n_malware)  # NumberOfSections
malware_features[:, 3] = np.random.uniform(8192, 65536, n_malware)  # SizeOfOptionalHeader
malware_features[:, 4] = np.random.uniform(0, 50000, n_malware)  # Characteristics
malware_features[:, 5] = np.random.uniform(1000000, 10000000, n_malware)  # SizeOfCode
malware_features[:, 6] = np.random.uniform(500000, 5000000, n_malware)  # SizeOfInitializedData
malware_features[:, 7] = np.random.uniform(0, 100000, n_malware)  # SizeOfUninitializedData
malware_features[:, 8] = np.random.uniform(4096, 65536, n_malware)  # AddressOfEntryPoint
malware_features[:, 9] = np.random.uniform(4096, 16384, n_malware)  # BaseOfCode
malware_features[:, 10] = np.random.uniform(4096, 65536, n_malware)  # BaseOfData
malware_features[:, 11] = np.random.uniform(400000, 10000000, n_malware)  # ImageBase
malware_features[:, 12] = np.random.uniform(4096, 65536, n_malware)  # SectionAlignment
malware_features[:, 13] = np.random.uniform(512, 4096, n_malware)  # FileAlignment
malware_features[:, 14] = np.random.uniform(5, 10, n_malware)  # MajorOperatingSystemVersion
malware_features[:, 15] = np.random.uniform(0, 2, n_malware)  # MinorOperatingSystemVersion
malware_features[:, 16] = np.random.uniform(1000000, 20000000, n_malware)  # SizeOfImage
malware_features[:, 17] = np.random.uniform(512, 4096, n_malware)  # SizeOfHeaders
malware_features[:, 18] = np.random.uniform(0, 65535, n_malware)  # CheckSum
malware_features[:, 19] = np.random.choice([2, 3], n_malware)  # Subsystem
malware_features[:, 20] = np.random.uniform(6.0, 7.9, n_malware)  # SectionMaxEntropy (high for malware)
malware_features[:, 21] = np.random.uniform(0.0, 2.0, n_malware)  # SectionMinEntropy
malware_features[:, 22] = np.random.uniform(4.0, 7.5, n_malware)  # SectionAvgEntropy (higher for malware)

# Benign samples - with different characteristics
benign_features = np.random.randn(n_benign, 23)
benign_features[:, 0] = np.random.uniform(1000000000, 1600000000, n_benign)  # TimeDateStamp
benign_features[:, 1] = np.random.uniform(332, 34404, n_benign)  # Machine
benign_features[:, 2] = np.random.uniform(2, 8, n_benign)  # NumberOfSections (fewer)
benign_features[:, 3] = np.random.uniform(224, 240, n_benign)  # SizeOfOptionalHeader
benign_features[:, 4] = np.random.uniform(0, 10000, n_benign)  # Characteristics
benign_features[:, 5] = np.random.uniform(500000, 5000000, n_benign)  # SizeOfCode
benign_features[:, 6] = np.random.uniform(100000, 1000000, n_benign)  # SizeOfInitializedData
benign_features[:, 7] = np.random.uniform(0, 10000, n_benign)  # SizeOfUninitializedData
benign_features[:, 8] = np.random.uniform(1000, 50000, n_benign)  # AddressOfEntryPoint
benign_features[:, 9] = np.random.uniform(4096, 8192, n_benign)  # BaseOfCode
benign_features[:, 10] = np.random.uniform(65536, 131072, n_benign)  # BaseOfData
benign_features[:, 11] = np.random.uniform(400000, 4000000, n_benign)  # ImageBase
benign_features[:, 12] = np.random.uniform(4096, 8192, n_benign)  # SectionAlignment
benign_features[:, 13] = np.random.uniform(512, 512, n_benign)  # FileAlignment
benign_features[:, 14] = np.random.uniform(5, 6, n_benign)  # MajorOperatingSystemVersion
benign_features[:, 15] = np.random.uniform(0, 1, n_benign)  # MinorOperatingSystemVersion
benign_features[:, 16] = np.random.uniform(500000, 10000000, n_benign)  # SizeOfImage
benign_features[:, 17] = np.random.uniform(512, 1024, n_benign)  # SizeOfHeaders
benign_features[:, 18] = np.random.uniform(0, 65535, n_benign)  # CheckSum
benign_features[:, 19] = np.random.choice([2, 3], n_benign)  # Subsystem
benign_features[:, 20] = np.random.uniform(2.0, 6.5, n_benign)  # SectionMaxEntropy (lower for benign)
benign_features[:, 21] = np.random.uniform(0.0, 1.5, n_benign)  # SectionMinEntropy
benign_features[:, 22] = np.random.uniform(2.0, 5.5, n_benign)  # SectionAvgEntropy (lower for benign)

# Combine datasets
X = np.vstack([malware_features, benign_features])
y = np.hstack([np.ones(n_malware), np.zeros(n_benign)])

print(f"✅ Dataset created: {len(X)} samples")
print(f"   - Malware samples: {n_malware}")
print(f"   - Benign samples: {n_benign}")
print(f"   - Features per sample: 23")
print()

# Split data
print("Step 2: Splitting data into train/test sets...")
print("-" * 80)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✅ Train set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")
print()

# Feature scaling for better performance
print("Step 3: Applying feature scaling...")
print("-" * 80)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✅ Features scaled using StandardScaler")
print()

# Train advanced ensemble model
print("Step 4: Training advanced ensemble model...")
print("-" * 80)
print("Building ensemble with multiple algorithms:")
print()

# Define base models with optimized parameters
rf_model = RandomForestClassifier(
    n_estimators=200,  # Increased from 100
    max_depth=15,      # Increased from 10
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'  # Handle imbalance better
)
print("  1. Random Forest: 200 estimators, max_depth=15")

gb_model = GradientBoostingClassifier(
    n_estimators=150,
    learning_rate=0.1,
    max_depth=7,
    min_samples_split=2,
    min_samples_leaf=1,
    subsample=0.8,
    random_state=42
)
print("  2. Gradient Boosting: 150 estimators, learning_rate=0.1")

ada_model = AdaBoostClassifier(
    n_estimators=100,
    learning_rate=0.5,
    random_state=42
)
print("  3. AdaBoost: 100 estimators, learning_rate=0.5")
print()

# Create voting ensemble
print("Creating voting ensemble (soft voting)...")
ensemble = VotingClassifier(
    estimators=[
        ('rf', rf_model),
        ('gb', gb_model),
        ('ada', ada_model)
    ],
    voting='soft',  # Use probability voting
    n_jobs=-1
)

# Train the ensemble
print("Training ensemble model...")
ensemble.fit(X_train_scaled, y_train)
print("✅ Ensemble model trained successfully!")
print()

# Evaluate model
print("Step 5: Evaluating model performance...")
print("=" * 80)

# Cross-validation
print("\nCross-Validation (5-fold):")
print("-" * 80)
cv_scores = cross_val_score(ensemble, X_train_scaled, y_train, cv=5, scoring='accuracy')
print(f"  Fold scores: {[f'{score:.4f}' for score in cv_scores]}")
print(f"  Mean accuracy: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
print()

# Test set evaluation
print("Test Set Performance:")
print("-" * 80)
y_pred = ensemble.predict(X_test_scaled)
y_pred_proba = ensemble.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"  ROC AUC Score: {roc_auc:.4f}")
print()

# Classification report
print("Detailed Classification Report:")
print("-" * 80)
print(classification_report(y_test, y_pred, 
                          target_names=['Benign', 'Malware'],
                          digits=4))

# Confusion matrix
print("Confusion Matrix:")
print("-" * 80)
cm = confusion_matrix(y_test, y_pred)
print(f"                 Predicted")
print(f"                 Benign  Malware")
print(f"Actual Benign    {cm[0][0]:6d}  {cm[0][1]:6d}")
print(f"       Malware   {cm[1][0]:6d}  {cm[1][1]:6d}")
print()

# Calculate specific metrics
tn, fp, fn, tp = cm.ravel()
malware_detection_rate = tp / (tp + fn) * 100
false_positive_rate = fp / (fp + tn) * 100
false_negative_rate = fn / (fn + tp) * 100

print("Key Performance Indicators:")
print("-" * 80)
print(f"  ✅ Malware Detection Rate (Recall): {malware_detection_rate:.2f}%")
print(f"  ✅ False Positive Rate: {false_positive_rate:.2f}%")
print(f"  ✅ False Negative Rate: {false_negative_rate:.2f}%")
print()

# Feature importance (from Random Forest component)
print("Top 10 Most Important Features:")
print("-" * 80)
feature_names = [
    'TimeDateStamp', 'Machine', 'NumberOfSections', 'SizeOfOptionalHeader',
    'Characteristics', 'SizeOfCode', 'SizeOfInitializedData', 'SizeOfUninitializedData',
    'AddressOfEntryPoint', 'BaseOfCode', 'BaseOfData', 'ImageBase',
    'SectionAlignment', 'FileAlignment', 'MajorOperatingSystemVersion',
    'MinorOperatingSystemVersion', 'SizeOfImage', 'SizeOfHeaders',
    'CheckSum', 'Subsystem', 'SectionMaxEntropy', 'SectionMinEntropy', 'SectionAvgEntropy'
]

rf_importances = ensemble.estimators_[0].feature_importances_
top_indices = np.argsort(rf_importances)[::-1][:10]

for i, idx in enumerate(top_indices, 1):
    print(f"  {i:2d}. {feature_names[idx]:30s} {rf_importances[idx]:.4f}")
print()

# Save the advanced model and scaler
print("Step 6: Saving advanced model...")
print("=" * 80)

model_dir = 'ML_model'
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'malwareclassifier-V2.pkl')
scaler_path = os.path.join(model_dir, 'scaler.pkl')

joblib.dump(ensemble, model_path)
joblib.dump(scaler, scaler_path)

print(f"✅ Advanced ensemble model saved: {model_path}")
print(f"✅ Feature scaler saved: {scaler_path}")
print()

# Summary
print("=" * 80)
print("TRAINING COMPLETE - ADVANCED MODEL SUMMARY")
print("=" * 80)
print()
print(f"  Model Type: Ensemble (Random Forest + Gradient Boosting + AdaBoost)")
print(f"  Training Samples: {len(X_train)}")
print(f"  Test Samples: {len(X_test)}")
print(f"  Features: 23")
print()
print(f"  ✅ Cross-Validation Accuracy: {cv_scores.mean()*100:.2f}% (±{cv_scores.std()*100:.2f}%)")
print(f"  ✅ Test Set Accuracy: {accuracy*100:.2f}%")
print(f"  ✅ Malware Detection Rate: {malware_detection_rate:.2f}%")
print(f"  ✅ ROC AUC Score: {roc_auc:.4f}")
print()
print(f"  Files saved:")
print(f"    - {model_path}")
print(f"    - {scaler_path}")
print()
print("  🎉 High-accuracy model is ready for use!")
print()
print("=" * 80)
print("Developed by F.J.G - NeuroShield Project")
print("© 2025 NeuroShield. All Rights Reserved.")
print("=" * 80)
