"""
Unit tests for ISL Recognition Model
"""

import unittest
import numpy as np
import tensorflow as tf
from unittest.mock import Mock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models.isl_recognition import ISLRecognitionModel

class TestISLRecognitionModel(unittest.TestCase):
    """Test cases for ISL Recognition Model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.model = ISLRecognitionModel()
        self.test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    def test_model_creation(self):
        """Test model architecture creation"""
        model = self.model.create_model()
        
        # Check model structure
        self.assertIsInstance(model, tf.keras.Model)
        self.assertEqual(len(model.layers), 12)  # Expected number of layers
        
        # Check input shape
        self.assertEqual(model.input_shape, (None, 224, 224, 3))
        
        # Check output shape
        self.assertEqual(model.output_shape, (None, len(self.model.gesture_classes)))
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        processed = self.model.preprocess_image(self.test_image)
        
        # Check shape
        self.assertEqual(processed.shape, (1, 224, 224, 3))
        
        # Check data type and range
        self.assertEqual(processed.dtype, np.float32)
        self.assertTrue(np.all(processed >= 0.0))
        self.assertTrue(np.all(processed <= 1.0))
    
    def test_extract_landmarks(self):
        """Test landmark extraction"""
        landmarks = self.model.extract_landmarks(self.test_image)
        
        # Check structure
        self.assertIn('hands', landmarks)
        self.assertIn('pose', landmarks)
        self.assertIn('face', landmarks)
        
        # Check data types
        self.assertIsInstance(landmarks['hands'], list)
        self.assertIsInstance(landmarks['pose'], list)
        self.assertIsInstance(landmarks['face'], list)
    
    def test_gesture_classes(self):
        """Test gesture classes are properly defined"""
        self.assertGreater(len(self.model.gesture_classes), 0)
        self.assertIn('HELLO', self.model.gesture_classes)
        self.assertIn('THANK_YOU', self.model.gesture_classes)
        self.assertIn('YES', self.model.gesture_classes)
        self.assertIn('NO', self.model.gesture_classes)
    
    @patch('tensorflow.keras.models.load_model')
    def test_load_model(self, mock_load_model):
        """Test model loading"""
        mock_model = Mock()
        mock_load_model.return_value = mock_model
        
        self.model.load_model('test_model.h5')
        
        mock_load_model.assert_called_once_with('test_model.h5')
        self.assertEqual(self.model.model, mock_model)
    
    @patch('tensorflow.keras.models.load_model')
    def test_load_model_error(self, mock_load_model):
        """Test model loading error handling"""
        mock_load_model.side_effect = Exception("Model not found")
        
        with self.assertRaises(Exception):
            self.model.load_model('nonexistent_model.h5')
    
    def test_predict_gesture_no_model(self):
        """Test prediction without loaded model"""
        with self.assertRaises(ValueError):
            self.model.predict_gesture(self.test_image)
    
    @patch.object(ISLRecognitionModel, 'model')
    def test_predict_gesture(self, mock_model):
        """Test gesture prediction"""
        # Mock model prediction
        mock_predictions = np.array([[0.1, 0.8, 0.1]])  # High confidence for index 1
        mock_model.predict.return_value = mock_predictions
        
        gesture, confidence = self.model.predict_gesture(self.test_image)
        
        # Check results
        self.assertEqual(gesture, self.model.gesture_classes[1])
        self.assertEqual(confidence, 0.8)
    
    def test_save_model_no_model(self):
        """Test saving model without loaded model"""
        with self.assertRaises(ValueError):
            self.model.save_model('test_model.h5')
    
    @patch.object(ISLRecognitionModel, 'model')
    def test_save_model(self, mock_model):
        """Test model saving"""
        mock_model.save.return_value = None
        
        self.model.save_model('test_model.h5')
        
        mock_model.save.assert_called_once_with('test_model.h5')

class TestISLRecognitionIntegration(unittest.TestCase):
    """Integration tests for ISL Recognition"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.model = ISLRecognitionModel()
    
    def test_full_pipeline(self):
        """Test complete recognition pipeline"""
        # Create test image
        test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Extract landmarks
        landmarks = self.model.extract_landmarks(test_image)
        self.assertIsInstance(landmarks, dict)
        
        # Preprocess image
        processed = self.model.preprocess_image(test_image)
        self.assertEqual(processed.shape, (1, 224, 224, 3))
    
    def test_model_compilation(self):
        """Test model compilation"""
        model = self.model.create_model()
        
        # Check optimizer
        self.assertIsInstance(model.optimizer, tf.keras.optimizers.Adam)
        
        # Check loss function
        self.assertEqual(model.loss, 'categorical_crossentropy')
        
        # Check metrics
        self.assertIn('accuracy', model.metrics_names)

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
