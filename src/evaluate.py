"""
Model Evaluation Module
Evaluates trained models and generates performance reports.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    confusion_matrix, classification_report,
    accuracy_score, precision_score, recall_score,
    f1_score, fbeta_score
)
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from typing import Dict
import warnings
warnings.filterwarnings('ignore')


class ModelEvaluator:
    """Evaluate trained ML models."""
    
    def __init__(self, model_path: str = None):
        """Initialize the evaluator."""
        self.model = None
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Load trained model."""
        self.model = joblib.load(model_path)
        print(f"✓ Model loaded from: {model_path}")
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict:
        """Evaluate model performance."""
        if self.model is None:
            raise ValueError("No model loaded")
        
        # Make predictions
        y_pred = self.model.predict(X)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y, y_pred) * 100,
            'precision': precision_score(y, y_pred, average='weighted', zero_division=0) * 100,
            'recall': recall_score(y, y_pred, average='weighted', zero_division=0) * 100,
            'f1': f1_score(y, y_pred, average='weighted', zero_division=0) * 100,
            'f2': fbeta_score(y, y_pred, beta=2, average='weighted', zero_division=0) * 100
        }
        
        return metrics, y_pred
    
    def plot_confusion_matrix(self, 
                             y_true: np.ndarray,
                             y_pred: np.ndarray,
                             save_path: str = None):
        """Plot confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=[f'Stage {i}' for i in range(5)],
            yticklabels=[f'Stage {i}' for i in range(5)],
            cbar_kws={'label': 'Count'}
        )
        
        plt.title('Confusion Matrix - Keratoconus Severity Staging', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.ylabel('True Stage', fontsize=12)
        plt.xlabel('Predicted Stage', fontsize=12)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Confusion matrix saved to: {save_path}")
        
        plt.close()
    
    def print_classification_report(self, 
                                   y_true: np.ndarray,
                                   y_pred: np.ndarray):
        """Print detailed classification report."""
        target_names = [f'Stage {i}' for i in range(5)]
        
        print(f"\n{'='*80}")
        print("DETAILED CLASSIFICATION REPORT")
        print(f"{'='*80}\n")
        
        report = classification_report(
            y_true, y_pred,
            target_names=target_names,
            digits=4
        )
        print(report)
        print(f"{'='*80}\n")
    
    def print_performance_summary(self, metrics: Dict):
        """Print performance summary."""
        print(f"\n{'='*80}")
        print("PERFORMANCE SUMMARY")
        print(f"{'='*80}\n")
        
        print(f"Accuracy:  {metrics['accuracy']:.2f}%")
        print(f"Precision: {metrics['precision']:.2f}%")
        print(f"Recall:    {metrics['recall']:.2f}%")
        print(f"F1-score:  {metrics['f1']:.2f}%")
        print(f"F2-score:  {metrics['f2']:.2f}%")
        
        print(f"\n{'='*80}\n")


def main():
    """Main execution function."""
    print("="*80)
    print("MODEL EVALUATION")
    print("="*80 + "\n")
    
    # Load UNSCALED data from raw source (same as training)
    print("Loading test data from raw source...")
    df_raw = pd.read_csv("data/raw/synthetic_pentacam_79_features.csv")
    
    # Use the same 3 features as training
    X = df_raw[['Rm_B', 'Rm_F', 'Pachy_Min']]
    y = df_raw['Severity']
    
    print(f"Test set size: {len(y)} samples")
    print(f"Features: {X.columns.tolist()}")
    print(f"\nFeature ranges (UNSCALED):")
    print(f"  Rm_B: {X['Rm_B'].min():.2f} - {X['Rm_B'].max():.2f} mm")
    print(f"  Rm_F: {X['Rm_F'].min():.2f} - {X['Rm_F'].max():.2f} mm")
    print(f"  Pachy_Min: {X['Pachy_Min'].min():.0f} - {X['Pachy_Min'].max():.0f} µm\n")
    
    # Initialize evaluator
    evaluator = ModelEvaluator("models/rf_kc_severity.pkl")
    
    # Evaluate
    print("Evaluating model performance...\n")
    metrics, y_pred = evaluator.evaluate(X, y)
    
    # Print results
    evaluator.print_performance_summary(metrics)
    evaluator.print_classification_report(y, y_pred)
    
    # Plot confusion matrix
    evaluator.plot_confusion_matrix(
        y, y_pred,
        save_path="models/confusion_matrix.png"
    )
    
    # Save metrics
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv("models/evaluation_metrics.csv", index=False)
    print("✓ Evaluation metrics saved to: models/evaluation_metrics.csv")
    
    # Test with specific cases
    print("\n" + "="*80)
    print("TESTING WITH CLINICAL CASES")
    print("="*80 + "\n")
    
    test_cases = [
        {"name": "Normal (Stage 0)", "Rm_B": 6.4, "Rm_F": 7.7, "Pachy_Min": 518, "expected": 0},
        {"name": "Mild (Stage 1)", "Rm_B": 6.0, "Rm_F": 7.3, "Pachy_Min": 481, "expected": 1},
        {"name": "Moderate (Stage 2)", "Rm_B": 5.7, "Rm_F": 7.0, "Pachy_Min": 448, "expected": 2},
        {"name": "Advanced (Stage 3)", "Rm_B": 5.1, "Rm_F": 6.7, "Pachy_Min": 391, "expected": 3},
        {"name": "Severe (Stage 4)", "Rm_B": 4.6, "Rm_F": 6.0, "Pachy_Min": 395, "expected": 4},
    ]
    
    for case in test_cases:
        test_input = pd.DataFrame({
            'Rm_B': [case['Rm_B']],
            'Rm_F': [case['Rm_F']],
            'Pachy_Min': [case['Pachy_Min']]
        })
        
        pred = evaluator.model.predict(test_input)[0]
        proba = evaluator.model.predict_proba(test_input)[0]
        
        status = "✓" if pred == case['expected'] else "✗"
        
        print(f"{status} {case['name']}:")
        print(f"   Expected: Stage {case['expected']}, Predicted: Stage {pred}")
        print(f"   Confidence: {proba[pred]*100:.1f}%\n")
    
    print("="*80)
    print("✓ Evaluation complete!")
    print("="*80)


if __name__ == "__main__":
    main()
