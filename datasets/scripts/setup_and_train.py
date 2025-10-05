"""
Setup and Train ISL Models
Complete pipeline to generate training data and train models
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from generate_training_data import ISLTrainingDataGenerator
from train_model import ISLModelTrainer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to setup and train ISL models"""
    logger.info("Starting ISL model setup and training...")
    
    try:
        # Step 1: Generate training data
        logger.info("Step 1: Generating training data...")
        generator = ISLTrainingDataGenerator()
        
        # Generate full dataset
        dataset = generator.generate_full_dataset(samples_per_gesture=100)
        
        # Create training splits
        splits = generator.create_training_splits()
        
        logger.info("Training data generation completed!")
        
        # Step 2: Train models
        logger.info("Step 2: Training models...")
        trainer = ISLModelTrainer()
        
        # Run complete training
        report = trainer.run_complete_training(epochs=50, batch_size=16)
        
        logger.info("Model training completed!")
        
        # Step 3: Summary
        logger.info("=" * 60)
        logger.info("TRAINING COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info(f"Total gestures: {len(dataset)}")
        logger.info(f"Total samples: {sum(len(data) for data in dataset.values())}")
        logger.info(f"Models saved to: {trainer.model_dir}")
        logger.info(f"Report saved to: {trainer.model_dir / 'model_report.json'}")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Setup and training failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
