"""
Data Preprocessing Module
Simple preprocessing for keratoconus data.
"""

import pandas as pd


def main():
    """Main execution function."""
    print("="*60)
    print("DATA PREPROCESSING")
    print("="*60 + "\n")
    
    # Load raw data
    print("Loading raw data...")
    df = pd.read_csv("data/raw/synthetic_pentacam_79_features.csv")
    
    print(f"✓ Loaded {df.shape[0]} samples with {df.shape[1]-1} features")
    print(f"\nFeature ranges:")
    print(f"  Rm_B: {df['Rm_B'].min():.2f} - {df['Rm_B'].max():.2f} mm")
    print(f"  Rm_F: {df['Rm_F'].min():.2f} - {df['Rm_F'].max():.2f} mm")
    print(f"  Pachy_Min: {df['Pachy_Min'].min():.0f} - {df['Pachy_Min'].max():.0f} µm")
    
    # For this simple case, no preprocessing needed
    # Just save as processed
    df.to_csv("data/processed/preprocessed_data.csv", index=False)
    
    print(f"\n✓ Preprocessed data saved to: data/processed/preprocessed_data.csv")
    print(f"✓ Shape: {df.shape}")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
