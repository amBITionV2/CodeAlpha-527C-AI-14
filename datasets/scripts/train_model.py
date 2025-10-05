"""
Train ISL Recognition Model
Complete training pipeline for ISL gesture recognition
"""

import os
import sys
import json
import numpy as np
import cv2
import pickle
import joblib
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from tqdm import tqdm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import matplotlib.pyplot as plt
import seaborn as sns

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from models.isl_recognition import ISLRecognitionModel

logger = logging.getLogger(__name__)

class ISLModelTrainer:
    """Complete training pipeline for ISL recognition models"""
    
    def __init__(self, data_dir: str = "datasets/raw", model_dir: str = "datasets/models"):
        self.data_dir = Path(data_dir)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize model
        self.model = ISLRecognitionModel()
        
        # Training data
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None
        self.X_test = None
        self.y_test = None
        
        # Results
        self.training_history = {}
        self.evaluation_results = {}
        
        logger.info("ISL Model Trainer initialized")
    
    def load_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load and preprocess training data"""
        logger.info("Loading training data...")
        
        # Load dataset splits
        train_path = self.data_dir / "train_split.json"
        val_path = self.data_dir / "validation_split.json"
        test_path = self.data_dir / "test_split.json"
        
        if not all([train_path.exists(), val_path.exists(), test_path.exists()]):
            logger.error("Training splits not found. Please generate training data first.")
            return None, None
        
        # Load splits
        with open(train_path, 'r') as f:
            train_data = json.load(f)
        with open(val_path, 'r') as f:
            val_data = json.load(f)
        with open(test_path, 'r') as f:
            test_data = json.load(f)
        
        # Process training data
        X_train, y_train = self._process_data_split(train_data)
        X_val, y_val = self._process_data_split(val_data)
        X_test, y_test = self._process_data_split(test_data)
        
        # Store data
        self.X_train = X_train
        self.y_train = y_train
        self.X_val = X_val
        self.y_val = y_val
        self.X_test = X_test
        self.y_test = y_test
        
        logger.info(f"Loaded training data: {len(X_train)} train, {len(X_val)} val, {len(X_test)} test")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def _process_data_split(self, data_split: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Process a data split into features and labels"""
        features = []
        labels = []
        
        for sample in tqdm(data_split, desc="Processing data"):
            try:
                # Load image
                image_path = sample['image_path']
                if not os.path.exists(image_path):
                    continue
                
                image = cv2.imread(image_path)
                if image is None:
                    continue
                
                # Extract landmarks
                landmarks = self.model.extract_landmarks(image)
                if not landmarks['combined']:
                    continue
                
                # Get label
                gesture = sample['gesture']
                if gesture not in self.model.class_to_idx:
                    continue
                
                label = self.model.class_to_idx[gesture]
                
                features.append(landmarks['combined'])
                labels.append(label)
                
            except Exception as e:
                logger.warning(f"Error processing sample: {str(e)}")
                continue
        
        return np.array(features), np.array(labels)
    
    def train_deep_learning_model(self, epochs: int = 100, batch_size: int = 32) -> Dict:
        """Train deep learning model"""
        logger.info("Training deep learning model...")
        
        if self.X_train is None:
            logger.error("Training data not loaded")
            return {}
        
        # Normalize features
        self.model.scaler = StandardScaler()
        X_train_scaled = self.model.scaler.fit_transform(self.X_train)
        X_val_scaled = self.model.scaler.transform(self.X_val) if self.X_val is not None else None
        
        # Train model
        history = self.model.train_model(
            X_train_scaled, self.y_train,
            X_val_scaled, self.y_val,
            epochs=epochs,
            batch_size=batch_size
        )
        
        self.training_history['deep_learning'] = history
        
        # Save model
        model_path = self.model_dir / "isl_deep_model.h5"
        self.model.save_model(str(model_path))
        
        logger.info("Deep learning model training completed")
        return history
    
    def train_ensemble_model(self) -> Dict:
        """Train ensemble model"""
        logger.info("Training ensemble model...")
        
        if self.X_train is None:
            logger.error("Training data not loaded")
            return {}
        
        # Normalize features
        if self.model.scaler is None:
            self.model.scaler = StandardScaler()
            X_train_scaled = self.model.scaler.fit_transform(self.X_train)
        else:
            X_train_scaled = self.model.scaler.transform(self.X_train)
        
        # Train ensemble model
        ensemble_results = self.model.train_ensemble_model(X_train_scaled, self.y_train)
        
        self.training_history['ensemble'] = ensemble_results
        
        # Save ensemble model
        ensemble_path = self.model_dir / "isl_ensemble_model.pkl"
        joblib.dump(self.model.ensemble_model, ensemble_path)
        
        logger.info("Ensemble model training completed")
        return ensemble_results
    
    def evaluate_models(self) -> Dict:
        """Evaluate trained models"""
        logger.info("Evaluating models...")
        
        if self.X_test is None:
            logger.error("Test data not loaded")
            return {}
        
        results = {}
        
        # Normalize test features
        if self.model.scaler is not None:
            X_test_scaled = self.model.scaler.transform(self.X_test)
        else:
            X_test_scaled = self.X_test
        
        # Evaluate deep learning model
        if self.model.model is not None:
            dl_results = self.model.evaluate_model(X_test_scaled, self.y_test)
            results['deep_learning'] = dl_results
            logger.info(f"Deep Learning - Accuracy: {dl_results.get('accuracy', 0):.4f}")
        
        # Evaluate ensemble model
        if hasattr(self.model, 'ensemble_model') and self.model.ensemble_model is not None:
            y_pred = self.model.ensemble_model.predict(X_test_scaled)
            y_pred_proba = self.model.ensemble_model.predict_proba(X_test_scaled)
            
            accuracy = accuracy_score(self.y_test, y_pred)
            
            # Classification report
            class_names = [self.model.idx_to_class[i] for i in range(self.model.num_classes)]
            report = classification_report(self.y_test, y_pred, target_names=class_names, output_dict=True)
            
            ensemble_results = {
                'accuracy': accuracy,
                'classification_report': report,
                'confusion_matrix': confusion_matrix(self.y_test, y_pred).tolist()
            }
            
            results['ensemble'] = ensemble_results
            logger.info(f"Ensemble - Accuracy: {accuracy:.4f}")
        
        self.evaluation_results = results
        
        # Save evaluation results
        results_path = self.model_dir / "evaluation_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def plot_training_history(self):
        """Plot training history"""
        if not self.training_history:
            logger.warning("No training history to plot")
            return
        
        # Plot deep learning training history
        if 'deep_learning' in self.training_history:
            history = self.training_history['deep_learning']
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Accuracy
            axes[0, 0].plot(history['accuracy'], label='Training')
            if 'val_accuracy' in history:
                axes[0, 0].plot(history['val_accuracy'], label='Validation')
            axes[0, 0].set_title('Model Accuracy')
            axes[0, 0].set_xlabel('Epoch')
            axes[0, 0].set_ylabel('Accuracy')
            axes[0, 0].legend()
            
            # Loss
            axes[0, 1].plot(history['loss'], label='Training')
            if 'val_loss' in history:
                axes[0, 1].plot(history['val_loss'], label='Validation')
            axes[0, 1].set_title('Model Loss')
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('Loss')
            axes[0, 1].legend()
            
            # Top-3 Accuracy
            if 'top_3_accuracy' in history:
                axes[1, 0].plot(history['top_3_accuracy'], label='Training')
                if 'val_top_3_accuracy' in history:
                    axes[1, 0].plot(history['val_top_3_accuracy'], label='Validation')
                axes[1, 0].set_title('Top-3 Accuracy')
                axes[1, 0].set_xlabel('Epoch')
                axes[1, 0].set_ylabel('Top-3 Accuracy')
                axes[1, 0].legend()
            
            # Learning Rate
            if 'lr' in history:
                axes[1, 1].plot(history['lr'])
                axes[1, 1].set_title('Learning Rate')
                axes[1, 1].set_xlabel('Epoch')
                axes[1, 1].set_ylabel('Learning Rate')
            
            plt.tight_layout()
            
            # Save plot
            plot_path = self.model_dir / "training_history.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info(f"Training history plot saved to {plot_path}")
    
    def plot_confusion_matrix(self):
        """Plot confusion matrix"""
        if not self.evaluation_results:
            logger.warning("No evaluation results to plot")
            return
        
        # Plot confusion matrix for ensemble model
        if 'ensemble' in self.evaluation_results:
            cm = np.array(self.evaluation_results['ensemble']['confusion_matrix'])
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                       xticklabels=self.model.gesture_classes,
                       yticklabels=self.model.gesture_classes)
            plt.title('Confusion Matrix - Ensemble Model')
            plt.xlabel('Predicted')
            plt.ylabel('Actual')
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            
            # Save plot
            plot_path = self.model_dir / "confusion_matrix.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info(f"Confusion matrix plot saved to {plot_path}")
    
    def generate_model_report(self):
        """Generate comprehensive model report"""
        logger.info("Generating model report...")
        
        report = {
            'model_info': {
                'gesture_classes': self.model.gesture_classes,
                'num_classes': self.model.num_classes,
                'input_shape': self.model.input_shape
            },
            'training_data': {
                'train_samples': len(self.X_train) if self.X_train is not None else 0,
                'val_samples': len(self.X_val) if self.X_val is not None else 0,
                'test_samples': len(self.X_test) if self.X_test is not None else 0
            },
            'training_history': self.training_history,
            'evaluation_results': self.evaluation_results,
            'model_files': {
                'deep_learning': str(self.model_dir / "isl_deep_model.h5"),
                'ensemble': str(self.model_dir / "isl_ensemble_model.pkl"),
                'scaler': str(self.model_dir / "isl_deep_model_scaler.pkl"),
                'mappings': str(self.model_dir / "isl_deep_model_mappings.json")
            }
        }
        
        # Save report
        report_path = self.model_dir / "model_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Model report saved to {report_path}")
        return report
    
    def run_complete_training(self, epochs: int = 100, batch_size: int = 32) -> Dict:
        """Run complete training pipeline"""
        logger.info("Starting complete training pipeline...")
        
        try:
            # Load data
            self.load_training_data()
            
            # Train deep learning model
            self.train_deep_learning_model(epochs, batch_size)
            
            # Train ensemble model
            self.train_ensemble_model()
            
            # Evaluate models
            self.evaluate_models()
            
            # Generate plots
            self.plot_training_history()
            self.plot_confusion_matrix()
            
            # Generate report
            report = self.generate_model_report()
            
            logger.info("Complete training pipeline finished successfully!")
            return report
            
        except Exception as e:
            logger.error(f"Training pipeline failed: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    # Initialize trainer
    trainer = ISLModelTrainer()
    
    # Run complete training
    report = trainer.run_complete_training(epochs=50, batch_size=16)
    
    print("Training completed!")
    print(f"Model report saved to: {trainer.model_dir / 'model_report.json'}")
