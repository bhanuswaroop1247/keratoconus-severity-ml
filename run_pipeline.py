"""
Master Pipeline Execution Script
Runs the complete ML pipeline from data generation to model evaluation.
"""

import sys
import time


def print_section(title: str):
    """Print formatted section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def run_step(step_name: str, module_path: str):
    """
    Run a pipeline step.
    
    Args:
        step_name: Name of the step
        module_path: Path to the module to execute
    """
    print_section(f"STEP: {step_name}")
    start_time = time.time()
    
    try:
        # Import and run the module
        module_name = module_path.replace('/', '.').replace('.py', '')
        module = __import__(module_name, fromlist=['main'])
        if hasattr(module, 'main'):
            module.main()
        
        elapsed = time.time() - start_time
        print(f"\n✓ {step_name} completed in {elapsed:.2f} seconds\n")
        return True
        
    except Exception as e:
        print(f"\n✗ {step_name} failed with error:")
        print(f"  {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Execute the complete ML pipeline."""
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║         KERATOCONUS SEVERITY STAGING - ML PIPELINE                         ║
    ║                                                                            ║
    ║         Complete End-to-End Machine Learning System                        ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    pipeline_start = time.time()
    
    # Define pipeline steps
    steps = [
        ("1. Data Generation", "src.data_generator"),
        ("2. Data Preprocessing", "src.preprocessing"),
        ("3. Feature Selection", "src.feature_selection"),
        ("4. Model Training", "src.train"),
        ("5. Model Evaluation", "src.evaluate")
    ]
    
    # Execute pipeline
    results = []
    for step_name, module_path in steps:
        success = run_step(step_name, module_path)
        results.append((step_name, success))
        
        if not success:
            print("\n⚠️  Pipeline execution halted due to error.\n")
            sys.exit(1)
    
    # Print summary
    total_time = time.time() - pipeline_start
    
    print_section("PIPELINE EXECUTION SUMMARY")
    
    for step_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status:12} - {step_name}")
    
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    print(f"Average time per step: {total_time/len(steps):.2f} seconds")
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║                      ✓ PIPELINE COMPLETED SUCCESSFULLY                     ║
    ║                                                                            ║
    ║  Next steps:                                                               ║
    ║  1. Review generated plots in models/ directory                            ║
    ║  2. Check performance metrics in models/cv_results.csv                     ║
    ║  3. Launch web app: streamlit run app/streamlit_app.py                     ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
