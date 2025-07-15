#!/usr/bin/env python3
"""
Main execution script for ZOQ Restaurant Data Analysis
Run this file to execute the complete analysis pipeline
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🚀 Starting ZOQ Restaurant Data Analysis Pipeline")
    print("=" * 60)
    
    # Step 1: Data Processing
    print("📊 Step 1: Processing Data...")
    from data_processor import ZOQDataProcessor
    
    processor = ZOQDataProcessor()
    processor.run_full_analysis()
    
    # Step 2: Comprehensive Analysis
    print("\n🔍 Step 2: Running Analysis...")
    from analysis_functions import create_analyzer
    
    analyzer = create_analyzer()
    insights = analyzer.run_comprehensive_analysis()
    
    # Step 3: Generate Visualizations
    print("\n🎨 Step 3: Generating Visualizations...")
    try:
        from visualization_utils import create_visualizer
        import pandas as pd
        
        visualizer = create_visualizer()
        orders_df = pd.read_csv('data/processed/cleaned_orders.csv')
        visualizer.generate_all_visualizations(orders_df, insights)
    except Exception as e:
        print(f"⚠️ Visualization generation failed: {e}")
    
    # Step 4: Generate Reports
    print("\n📄 Step 4: Generating Reports...")
    try:
        from report_generator import create_report_generator
        
        report_generator = create_report_generator()
        report_generator.save_all_reports(insights)
    except Exception as e:
        print(f"⚠️ Report generation failed: {e}")
    
    print("\n✅ Analysis Pipeline Completed!")
    print("📁 Check the following directories:")
    print("  • data/processed/     - Processed data files")
    print("  • visualizations/     - Charts and graphs")
    print("  • reports/           - Business reports")

if __name__ == "__main__":
    main()
    print("🚀 ZOQ Restaurant Data Analysis Pipeline Finished Successfully!")