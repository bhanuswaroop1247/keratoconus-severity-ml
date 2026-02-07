"""
Model Training Module
Trains Random Forest classifier on keratoconus data.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score
import joblib


def main():
    """Main execution function."""
    print("="*80)
    print("MODEL TRAINING")
    print("="*80 + "\n")
    
    # Load data
    print("Loading training data...")
    df = pd.read_csv("data/processed/selected_features_data.csv")
    
    X = df[['Rm_B', 'Rm_F', 'Pachy_Min']]
    y = df['Severity']
    
    print(f"Dataset shape: {X.shape}")
    print(f"Features: {X.columns.tolist()}")
    print(f"\nFeature ranges:")
    print(f"  Rm_B: {X['Rm_B'].min():.2f} - {X['Rm_B'].max():.2f} mm")
    print(f"  Rm_F: {X['Rm_F'].min():.2f} - {X['Rm_F'].max():.2f} mm")
    print(f"  Pachy_Min: {X['Pachy_Min'].min():.0f} - {X['Pachy_Min'].max():.0f} µm")
    
    # Train Random Forest
    print("\n" + "="*80)
    print("TRAINING RANDOM FOREST")
    print("="*80 + "\n")
    
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    
    # Cross-validation
    print("Performing 6-fold cross-validation...")
    cv = StratifiedKFold(n_splits=6, shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf, X, y, cv=cv, scoring='accuracy')
    
    print(f"  ✓ CV Accuracy: {cv_scores.mean()*100:.2f}% (±{cv_scores.std()*100:.2f}%)")
    
    # Train on full dataset
    print("\nTraining on full dataset...")
    rf.fit(X, y)
    
    train_pred = rf.predict(X)
    train_acc = accuracy_score(y, train_pred)
    print(f"  ✓ Training Accuracy: {train_acc*100:.2f}%")
    
    # Save model
    joblib.dump(rf, "models/rf_kc_severity.pkl")
    print(f"\n✓ Model saved to: models/rf_kc_severity.pkl")
    
    # Save CV results
    results = pd.DataFrame({
        'Model': ['Random Forest'],
        'CV_Accuracy': [cv_scores.mean() * 100],
        'CV_Std': [cv_scores.std() * 100],
        'Train_Accuracy': [train_acc * 100]
    })
    results.to_csv("models/cv_results.csv", index=False)
    print(f"✓ Results saved to: models/cv_results.csv")
    
    print("\n" + "="*80)
    print("✓ Training complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
