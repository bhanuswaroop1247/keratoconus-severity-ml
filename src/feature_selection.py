"""
Feature Selection Module
Selects the 3 most important features.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    """Main execution function."""
    print("="*60)
    print("FEATURE SELECTION")
    print("="*60 + "\n")
    
    # Load preprocessed data
    print("Loading preprocessed data...")
    df = pd.read_csv("data/processed/preprocessed_data.csv")
    
    # We already have only 3 features, so just save them
    selected_features = ['Rm_B', 'Rm_F', 'Pachy_Min']
    
    print(f"✓ Selected features: {selected_features}")
    
    # Save
    df.to_csv("data/processed/selected_features_data.csv", index=False)
    print(f"✓ Saved to: data/processed/selected_features_data.csv")
    
    # Create simple visualization
    plot_df = df.copy()
    
    try:
        g = sns.pairplot(
            plot_df,
            hue='Severity',
            palette='Set1',
            diag_kind='hist',
            plot_kws={'alpha': 0.6, 's': 30},
            height=3
        )
        
        g.fig.suptitle('Feature Relationships by Severity', 
                      y=1.02, fontsize=16, fontweight='bold')
        
        plt.savefig('models/feature_pairplot.png', dpi=300, bbox_inches='tight')
        print(f"✓ Pairplot saved to: models/feature_pairplot.png")
        plt.close()
    except:
        print("  (Skipping visualization)")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
