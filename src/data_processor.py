#!/usr/bin/env python3
"""
ZOQ Restaurant Data Analysis - Main Data Processor
Author: Azib Malik
Date: 2024

This script processes raw restaurant data to generate insights for business optimization.
Handles data cleaning, transformation, and preliminary analysis.
"""

import pandas as pd
import numpy as np
import sqlite3
import warnings
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

class ZOQDataProcessor:
    """Main class for processing ZOQ restaurant data"""
    
    def __init__(self, data_path='data/'):
        self.data_path = data_path
        self.raw_data_path = os.path.join(data_path, 'raw/')
        self.processed_data_path = os.path.join(data_path, 'processed/')
        self.create_directories()
        
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.processed_data_path, exist_ok=True)
        
    def load_raw_data(self):
        """Load all raw data files"""
        logger.info("Loading raw data files...")
        
        try:
            # Load main datasets
            self.orders_df = pd.read_csv(os.path.join(self.raw_data_path, 'customer_orders_2023.csv'))
            self.visits_df = pd.read_csv(os.path.join(self.raw_data_path, 'customer_visits_2023.csv'))
            self.satisfaction_df = pd.read_csv(os.path.join(self.raw_data_path, 'customer_satisfaction_2023.csv'))
            self.menu_df = pd.read_csv(os.path.join(self.raw_data_path, 'menu_items.csv'))
            
            logger.info(f"Loaded {len(self.orders_df)} order records")
            logger.info(f"Loaded {len(self.visits_df)} visit records")
            logger.info(f"Loaded {len(self.satisfaction_df)} satisfaction records")
            logger.info(f"Loaded {len(self.menu_df)} menu items")
            
            return True
            
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            self.generate_sample_data()
            return False
            
    def generate_sample_data(self):
        """Generate sample data for demonstration purposes"""
        logger.info("Generating sample data for demonstration...")
        
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate menu items
        menu_items = [
            ('Grilled Chicken Caesar Salad', 'Salad', 14.99),
            ('Beef Tenderloin Steak', 'Main Course', 28.99),
            ('Salmon Teriyaki', 'Main Course', 22.99),
            ('Vegetarian Pasta', 'Main Course', 16.99),
            ('Mushroom Risotto', 'Main Course', 18.99),
            ('Chocolate Lava Cake', 'Dessert', 8.99),
            ('Tiramisu', 'Dessert', 7.99),
            ('Garlic Bread', 'Appetizer', 5.99),
            ('Calamari Rings', 'Appetizer', 9.99),
            ('House Wine', 'Beverage', 12.99)
        ]
        
        self.menu_df = pd.DataFrame(menu_items, columns=['item_name', 'category', 'price'])
        self.menu_df['item_id'] = range(1, len(self.menu_df) + 1)
        
        # Generate customer orders (3200+ records)
        n_orders = 3200
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        
        orders_data = []
        for i in range(n_orders):
            order_date = start_date + timedelta(days=np.random.randint(0, 365))
            customer_id = np.random.randint(1, 800)  # 800 unique customers
            item_id = np.random.choice(self.menu_df['item_id'].values)
            quantity = np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05])
            
            item_price = self.menu_df[self.menu_df['item_id'] == item_id]['price'].iloc[0]
            total_amount = item_price * quantity
            
            orders_data.append({
                'order_id': i + 1,
                'customer_id': customer_id,
                'order_date': order_date.strftime('%Y-%m-%d'),
                'order_time': f"{np.random.randint(11, 22):02d}:{np.random.randint(0, 60):02d}",
                'item_id': item_id,
                'quantity': quantity,
                'total_amount': round(total_amount, 2)
            })
            
        self.orders_df = pd.DataFrame(orders_data)
        
        # Generate customer visits (2800+ records)
        n_visits = 2800
        visits_data = []
        
        for i in range(n_visits):
            visit_date = start_date + timedelta(days=np.random.randint(0, 365))
            customer_id = np.random.randint(1, 800)
            party_size = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.15, 0.35, 0.25, 0.15, 0.07, 0.03])
            
            # Duration based on meal type (lunch vs dinner)
            hour = np.random.randint(11, 22)
            if hour < 15:  # Lunch
                duration = np.random.normal(45, 15)
            else:  # Dinner
                duration = np.random.normal(72, 20)
            
            duration = max(30, int(duration))  # Minimum 30 minutes
            
            visits_data.append({
                'visit_id': i + 1,
                'customer_id': customer_id,
                'visit_date': visit_date.strftime('%Y-%m-%d'),
                'visit_time': f"{hour:02d}:{np.random.randint(0, 60):02d}",
                'party_size': party_size,
                'duration_minutes': duration
            })
            
        self.visits_df = pd.DataFrame(visits_data)
        
        # Generate satisfaction surveys (2500+ records)
        n_surveys = 2500
        satisfaction_data = []
        
        for i in range(n_surveys):
            customer_id = np.random.randint(1, 800)
            survey_date = start_date + timedelta(days=np.random.randint(0, 365))
            
            # Generate ratings (1-5 scale, weighted toward positive)
            overall_rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.25, 0.35, 0.25])
            food_quality = np.random.choice([1, 2, 3, 4, 5], p=[0.03, 0.07, 0.2, 0.4, 0.3])
            service_quality = np.random.choice([1, 2, 3, 4, 5], p=[0.04, 0.08, 0.23, 0.38, 0.27])
            atmosphere = np.random.choice([1, 2, 3, 4, 5], p=[0.02, 0.06, 0.22, 0.42, 0.28])
            
            satisfaction_data.append({
                'survey_id': i + 1,
                'customer_id': customer_id,
                'survey_date': survey_date.strftime('%Y-%m-%d'),
                'overall_rating': overall_rating,
                'food_quality': food_quality,
                'service_quality': service_quality,
                'atmosphere': atmosphere,
                'would_recommend': 1 if overall_rating >= 4 else 0
            })
            
        self.satisfaction_df = pd.DataFrame(satisfaction_data)
        
        # Save sample data
        self.save_raw_data()
        logger.info("Sample data generated successfully")
        
    def save_raw_data(self):
        """Save raw data to CSV files"""
        self.orders_df.to_csv(os.path.join(self.raw_data_path, 'customer_orders_2023.csv'), index=False)
        self.visits_df.to_csv(os.path.join(self.raw_data_path, 'customer_visits_2023.csv'), index=False)
        self.satisfaction_df.to_csv(os.path.join(self.raw_data_path, 'customer_satisfaction_2023.csv'), index=False)
        self.menu_df.to_csv(os.path.join(self.raw_data_path, 'menu_items.csv'), index=False)
        
    def clean_data(self):
        """Clean and validate data"""
        logger.info("Cleaning data...")
        
        # Clean orders data
        self.orders_df['order_date'] = pd.to_datetime(self.orders_df['order_date'])
        self.orders_df = self.orders_df.dropna()
        self.orders_df = self.orders_df[self.orders_df['quantity'] > 0]
        self.orders_df = self.orders_df[self.orders_df['total_amount'] > 0]
        
        # Clean visits data
        self.visits_df['visit_date'] = pd.to_datetime(self.visits_df['visit_date'])
        self.visits_df = self.visits_df.dropna()
        self.visits_df = self.visits_df[self.visits_df['duration_minutes'] > 0]
        
        # Clean satisfaction data
        self.satisfaction_df['survey_date'] = pd.to_datetime(self.satisfaction_df['survey_date'])
        self.satisfaction_df = self.satisfaction_df.dropna()
        
        logger.info("Data cleaning completed")
        
    def analyze_customer_behavior(self):
        """Analyze customer behavior patterns"""
        logger.info("Analyzing customer behavior...")
        
        # Merge orders with visits for comprehensive analysis
        customer_data = self.orders_df.merge(
            self.visits_df[['customer_id', 'visit_date', 'party_size', 'duration_minutes']], 
            on='customer_id', 
            how='left'
        )
        
        # Customer segmentation
        customer_metrics = customer_data.groupby('customer_id').agg({
            'order_id': 'count',
            'total_amount': ['sum', 'mean'],
            'visit_date': 'nunique'
        }).round(2)
        
        customer_metrics.columns = ['total_orders', 'total_spent', 'avg_order_value', 'visit_frequency']
        
        # Categorize customers
        customer_metrics['customer_segment'] = pd.cut(
            customer_metrics['total_spent'], 
            bins=[0, 100, 300, 500, float('inf')], 
            labels=['Low Value', 'Medium Value', 'High Value', 'VIP']
        )
        
        return customer_metrics
        
    def analyze_menu_performance(self):
        """Analyze menu item performance"""
        logger.info("Analyzing menu performance...")
        
        # Merge orders with menu items
        menu_performance = self.orders_df.merge(self.menu_df, on='item_id')
        
        # Calculate performance metrics
        item_metrics = menu_performance.groupby(['item_id', 'item_name', 'category']).agg({
            'order_id': 'count',
            'quantity': 'sum',
            'total_amount': 'sum'
        }).reset_index()
        
        item_metrics.columns = ['item_id', 'item_name', 'category', 'order_count', 'total_quantity', 'revenue']
        
        # Calculate percentages
        total_orders = item_metrics['order_count'].sum()
        item_metrics['order_percentage'] = (item_metrics['order_count'] / total_orders * 100).round(2)
        
        # Rank items
        item_metrics['popularity_rank'] = item_metrics['order_count'].rank(ascending=False, method='min')
        item_metrics['revenue_rank'] = item_metrics['revenue'].rank(ascending=False, method='min')
        
        return item_metrics.sort_values('order_count', ascending=False)
        
    def analyze_time_patterns(self):
        """Analyze temporal patterns in orders and visits"""
        logger.info("Analyzing time patterns...")
        
        # Extract time features
        self.orders_df['hour'] = pd.to_datetime(self.orders_df['order_time'], format='%H:%M').dt.hour
        self.orders_df['month'] = self.orders_df['order_date'].dt.month
        self.orders_df['day_of_week'] = self.orders_df['order_date'].dt.dayofweek
        self.orders_df['day_name'] = self.orders_df['order_date'].dt.day_name()
        
        # Peak hours analysis
        hourly_orders = self.orders_df.groupby('hour').size().reset_index(name='order_count')
        
        # Monthly trends
        monthly_orders = self.orders_df.groupby('month').agg({
            'order_id': 'count',
            'total_amount': 'sum'
        }).reset_index()
        
        # Day of week patterns
        weekly_orders = self.orders_df.groupby('day_name').agg({
            'order_id': 'count',
            'total_amount': 'sum'
        }).reset_index()
        
        return {
            'hourly': hourly_orders,
            'monthly': monthly_orders,
            'weekly': weekly_orders
        }
        
    def generate_insights(self):
        """Generate business insights and recommendations"""
        logger.info("Generating business insights...")
        
        # Key metrics
        total_orders = len(self.orders_df)
        total_revenue = self.orders_df['total_amount'].sum()
        avg_order_value = self.orders_df['total_amount'].mean()
        unique_customers = self.orders_df['customer_id'].nunique()
        
        # Customer behavior insights
        customer_metrics = self.analyze_customer_behavior()
        
        # Menu performance insights
        menu_metrics = self.analyze_menu_performance()
        
        # Time pattern insights
        time_patterns = self.analyze_time_patterns()
        
        # Satisfaction insights
        avg_satisfaction = self.satisfaction_df['overall_rating'].mean()
        recommendation_rate = self.satisfaction_df['would_recommend'].mean()
        
        insights = {
            'overview': {
                'total_orders': total_orders,
                'total_revenue': round(total_revenue, 2),
                'avg_order_value': round(avg_order_value, 2),
                'unique_customers': unique_customers,
                'avg_satisfaction': round(avg_satisfaction, 2),
                'recommendation_rate': round(recommendation_rate * 100, 1)
            },
            'top_dishes': menu_metrics.head(10),
            'peak_hour': time_patterns['hourly'].loc[time_patterns['hourly']['order_count'].idxmax(), 'hour'],
            'customer_segments': customer_metrics['customer_segment'].value_counts(),
            'monthly_trends': time_patterns['monthly']
        }
        
        return insights
        
    def save_processed_data(self):
        """Save processed data and insights"""
        logger.info("Saving processed data...")
        
        # Save cleaned datasets
        self.orders_df.to_csv(os.path.join(self.processed_data_path, 'cleaned_orders.csv'), index=False)
        self.visits_df.to_csv(os.path.join(self.processed_data_path, 'cleaned_visits.csv'), index=False)
        self.satisfaction_df.to_csv(os.path.join(self.processed_data_path, 'cleaned_satisfaction.csv'), index=False)
        
        # Save analysis results
        customer_metrics = self.analyze_customer_behavior()
        menu_metrics = self.analyze_menu_performance()
        
        customer_metrics.to_csv(os.path.join(self.processed_data_path, 'customer_analysis.csv'))
        menu_metrics.to_csv(os.path.join(self.processed_data_path, 'menu_analysis.csv'), index=False)
        
        logger.info("Processed data saved successfully")
        
    def run_full_analysis(self):
        """Run the complete data processing pipeline"""
        logger.info("Starting ZOQ Restaurant Data Analysis...")
        
        # Load data
        if not self.load_raw_data():
            logger.info("Using generated sample data")
            
        # Clean data
        self.clean_data()
        
        # Generate insights
        insights = self.generate_insights()
        
        # Save processed data
        self.save_processed_data()
        
        # Print summary
        logger.info("=" * 50)
        logger.info("ANALYSIS SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Total Orders Processed: {insights['overview']['total_orders']:,}")
        logger.info(f"Total Revenue: ${insights['overview']['total_revenue']:,.2f}")
        logger.info(f"Average Order Value: ${insights['overview']['avg_order_value']:.2f}")
        logger.info(f"Unique Customers: {insights['overview']['unique_customers']:,}")
        logger.info(f"Average Satisfaction: {insights['overview']['avg_satisfaction']:.1f}/5.0")
        logger.info(f"Recommendation Rate: {insights['overview']['recommendation_rate']:.1f}%")
        logger.info(f"Peak Dining Hour: {insights['peak_hour']}:00")
        logger.info("=" * 50)
        
        return insights

def main():
    """Main execution function"""
    processor = ZOQDataProcessor()
    insights = processor.run_full_analysis()
    
    print("\n🎉 Analysis completed successfully!")
    print("📊 Processed data saved to 'data/processed/' directory")
    print("📈 Ready for visualization and reporting")

if __name__ == "__main__":
    main()