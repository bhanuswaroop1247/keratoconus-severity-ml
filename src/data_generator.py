"""
Synthetic Pentacam Data Generator
Generates synthetic corneal tomography data for keratoconus severity staging.
"""

import numpy as np
import pandas as pd
from pathlib import Path


class PentacamDataGenerator:
    """Generates synthetic Pentacam data with 3 key features."""
    
    def __init__(self, n_per_class=130, random_state=42):
        """
        Initialize the data generator.
        
        Args:
            n_per_class: Number of samples per severity stage
            random_state: Random seed for reproducibility
        """
        self.n_per_class = n_per_class
        self.random_state = random_state
        self.severity_stages = [0, 1, 2, 3, 4]
        np.random.seed(random_state)
        
    def _generate_stage_data(self, stage):
        """
        Generate data for a specific severity stage.
        
        Args:
            stage: Severity stage (0-4)
            
        Returns:
            pd.DataFrame: Generated data for the stage
        """
        n = self.n_per_class
        
        # Severity-dependent parameters
        pachy_min_mean = 520 - stage * 30      # Thins with severity
        rm_b_mean = 6.5 - stage * 0.4          # Posterior curvature steepens
        rm_f_mean = 7.8 - stage * 0.35         # Anterior curvature steepens
        
        data = {
            "Severity": np.full(n, stage),
            "Rm_B": np.random.normal(rm_b_mean, 0.25, n),
            "Rm_F": np.random.normal(rm_f_mean, 0.3, n),
            "Pachy_Min": np.random.normal(pachy_min_mean, 20, n),
        }
        
        return pd.DataFrame(data)
    
    def generate_dataset(self, output_path=None):
        """
        Generate complete dataset with all severity stages.
        
        Args:
            output_path: Path to save CSV file
            
        Returns:
            pd.DataFrame: Complete dataset
        """
        print("🔬 Generating Synthetic Pentacam Dataset...")
        print(f"   Samples per class: {self.n_per_class}")
        print(f"   Severity stages: {self.severity_stages}")
        
        # Generate data for each stage
        stage_data = []
        for stage in self.severity_stages:
            print(f"   ✓ Generating Stage {stage} data...")
            df_stage = self._generate_stage_data(stage)
            stage_data.append(df_stage)
        
        # Concatenate all stages
        df_complete = pd.concat(stage_data, ignore_index=True)
        
        # Shuffle
        df_complete = df_complete.sample(frac=1, random_state=self.random_state).reset_index(drop=True)
        
        print(f"\n✅ Dataset Generated Successfully!")
        print(f"   Total samples: {len(df_complete)}")
        print(f"   Total features: {len(df_complete.columns) - 1}")
        print(f"   Dataset shape: {df_complete.shape}")
        
        # Display class distribution
        print(f"\n📊 Class Distribution:")
        for stage in self.severity_stages:
            count = (df_complete['Severity'] == stage).sum()
            print(f"   Stage {stage}: {count} samples")
        
        # Save if path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df_complete.to_csv(output_path, index=False)
            print(f"\n💾 Saved to: {output_path}")
        
        # Display statistics
        print(f"\n📋 Feature Statistics:")
        print(f"   Rm_B: {df_complete['Rm_B'].min():.2f} - {df_complete['Rm_B'].max():.2f} mm")
        print(f"   Rm_F: {df_complete['Rm_F'].min():.2f} - {df_complete['Rm_F'].max():.2f} mm")
        print(f"   Pachy_Min: {df_complete['Pachy_Min'].min():.0f} - {df_complete['Pachy_Min'].max():.0f} µm")
        
        return df_complete


def main():
    """Main execution function."""
    # Initialize generator
    generator = PentacamDataGenerator(n_per_class=130, random_state=42)
    
    # Generate and save dataset
    output_path = "data/raw/synthetic_pentacam_79_features.csv"
    df = generator.generate_dataset(output_path)
    
    # Display sample
    print("\n📋 Sample Data (first 5 rows):")
    print(df.head())


if __name__ == "__main__":
    main()
