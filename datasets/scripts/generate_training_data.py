"""
Generate Synthetic Training Data for ISL Recognition
Creates realistic training data using MediaPipe and computer vision techniques
"""

import cv2
import numpy as np
import mediapipe as mp
import os
import json
import random
import math
from typing import List, Dict, Tuple
import logging
from tqdm import tqdm
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

class ISLTrainingDataGenerator:
    """Generate synthetic training data for ISL gesture recognition"""
    
    def __init__(self, output_dir: str = "datasets/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # MediaPipe solutions
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize MediaPipe
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # ISL gesture definitions
        self.gesture_definitions = self._define_isl_gestures()
        
        # Background images for realistic training
        self.backgrounds = self._create_backgrounds()
        
        logger.info("ISL Training Data Generator initialized")
    
    def _define_isl_gestures(self) -> Dict:
        """Define ISL gesture patterns and characteristics"""
        return {
            # Alphabet gestures
            'A': {
                'description': 'Fist with thumb extended',
                'hand_pose': 'fist_thumb_up',
                'complexity': 'simple',
                'variations': 5
            },
            'B': {
                'description': 'All fingers extended, palm facing forward',
                'hand_pose': 'open_palm',
                'complexity': 'simple',
                'variations': 5
            },
            'C': {
                'description': 'Curved hand like letter C',
                'hand_pose': 'curved_hand',
                'complexity': 'medium',
                'variations': 8
            },
            'D': {
                'description': 'Index finger extended, other fingers closed',
                'hand_pose': 'pointing',
                'complexity': 'simple',
                'variations': 5
            },
            'E': {
                'description': 'All fingers closed except thumb',
                'hand_pose': 'thumbs_up',
                'complexity': 'simple',
                'variations': 5
            },
            'F': {
                'description': 'Index and thumb touching, other fingers extended',
                'hand_pose': 'ok_sign',
                'complexity': 'medium',
                'variations': 6
            },
            'G': {
                'description': 'Index finger pointing, thumb extended',
                'hand_pose': 'gun_gesture',
                'complexity': 'medium',
                'variations': 6
            },
            'H': {
                'description': 'Index and middle fingers extended',
                'hand_pose': 'peace_sign',
                'complexity': 'simple',
                'variations': 5
            },
            'I': {
                'description': 'Pinky finger extended',
                'hand_pose': 'pinky_up',
                'complexity': 'simple',
                'variations': 5
            },
            'J': {
                'description': 'Pinky extended with hook motion',
                'hand_pose': 'pinky_hook',
                'complexity': 'medium',
                'variations': 6
            },
            'K': {
                'description': 'Index and middle fingers extended, spread apart',
                'hand_pose': 'v_sign',
                'complexity': 'medium',
                'variations': 6
            },
            'L': {
                'description': 'Index finger and thumb extended, L shape',
                'hand_pose': 'l_shape',
                'complexity': 'medium',
                'variations': 6
            },
            'M': {
                'description': 'Three fingers down, thumb and pinky extended',
                'hand_pose': 'rock_on',
                'complexity': 'medium',
                'variations': 6
            },
            'N': {
                'description': 'Index and middle fingers down, others extended',
                'hand_pose': 'two_fingers_down',
                'complexity': 'medium',
                'variations': 6
            },
            'O': {
                'description': 'All fingers touching, forming circle',
                'hand_pose': 'circle_hand',
                'complexity': 'medium',
                'variations': 8
            },
            'P': {
                'description': 'Index finger pointing down, thumb extended',
                'hand_pose': 'point_down',
                'complexity': 'medium',
                'variations': 6
            },
            'Q': {
                'description': 'Index finger and thumb extended, others closed',
                'hand_pose': 'pinch_gesture',
                'complexity': 'medium',
                'variations': 6
            },
            'R': {
                'description': 'Index and middle fingers crossed',
                'hand_pose': 'crossed_fingers',
                'complexity': 'hard',
                'variations': 8
            },
            'S': {
                'description': 'Fist with thumb over fingers',
                'hand_pose': 'fist_thumb_over',
                'complexity': 'medium',
                'variations': 6
            },
            'T': {
                'description': 'Fist with thumb between index and middle finger',
                'hand_pose': 'fist_thumb_between',
                'complexity': 'hard',
                'variations': 8
            },
            'U': {
                'description': 'Index and middle fingers together, extended',
                'hand_pose': 'two_fingers_together',
                'complexity': 'simple',
                'variations': 5
            },
            'V': {
                'description': 'Index and middle fingers extended, spread apart',
                'hand_pose': 'v_sign',
                'complexity': 'simple',
                'variations': 5
            },
            'W': {
                'description': 'Index, middle, and ring fingers extended',
                'hand_pose': 'three_fingers',
                'complexity': 'medium',
                'variations': 6
            },
            'X': {
                'description': 'Index finger bent, others extended',
                'hand_pose': 'bent_index',
                'complexity': 'medium',
                'variations': 6
            },
            'Y': {
                'description': 'Thumb and pinky extended, others closed',
                'hand_pose': 'hang_loose',
                'complexity': 'medium',
                'variations': 6
            },
            'Z': {
                'description': 'Index finger extended, moving in Z pattern',
                'hand_pose': 'z_motion',
                'complexity': 'hard',
                'variations': 10
            },
            
            # Common words
            'HELLO': {
                'description': 'Wave motion with open hand',
                'hand_pose': 'wave',
                'complexity': 'simple',
                'variations': 8
            },
            'THANK_YOU': {
                'description': 'Hand to chest, palm facing in',
                'hand_pose': 'hand_to_chest',
                'complexity': 'simple',
                'variations': 6
            },
            'PLEASE': {
                'description': 'Circular motion with open hand',
                'hand_pose': 'circular_motion',
                'complexity': 'medium',
                'variations': 8
            },
            'SORRY': {
                'description': 'Fist to chest, circular motion',
                'hand_pose': 'fist_to_chest',
                'complexity': 'medium',
                'variations': 6
            },
            'YES': {
                'description': 'Nodding motion with fist',
                'hand_pose': 'nodding_fist',
                'complexity': 'simple',
                'variations': 5
            },
            'NO': {
                'description': 'Shaking motion with index finger',
                'hand_pose': 'shaking_finger',
                'complexity': 'simple',
                'variations': 5
            },
            'GOOD': {
                'description': 'Thumbs up gesture',
                'hand_pose': 'thumbs_up',
                'complexity': 'simple',
                'variations': 5
            },
            'BAD': {
                'description': 'Thumbs down gesture',
                'hand_pose': 'thumbs_down',
                'complexity': 'simple',
                'variations': 5
            }
        }
    
    def _create_backgrounds(self) -> List[np.ndarray]:
        """Create various background images for realistic training"""
        backgrounds = []
        
        # Solid color backgrounds
        colors = [
            (255, 255, 255),  # White
            (200, 200, 200),  # Light gray
            (100, 100, 100),  # Dark gray
            (50, 50, 50),     # Very dark gray
            (240, 240, 240),  # Off-white
        ]
        
        for color in colors:
            bg = np.full((480, 640, 3), color, dtype=np.uint8)
            backgrounds.append(bg)
        
        # Gradient backgrounds
        for i in range(5):
            bg = np.zeros((480, 640, 3), dtype=np.uint8)
            for y in range(480):
                intensity = int(255 * (y / 480))
                bg[y, :] = [intensity, intensity, intensity]
            backgrounds.append(bg)
        
        # Textured backgrounds
        for i in range(3):
            bg = np.random.randint(100, 200, (480, 640, 3), dtype=np.uint8)
            # Add some noise
            noise = np.random.randint(-20, 20, (480, 640, 3), dtype=np.int16)
            bg = np.clip(bg.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            backgrounds.append(bg)
        
        return backgrounds
    
    def _generate_hand_landmarks(self, gesture: str, variation: int) -> List[Tuple[float, float, float]]:
        """Generate hand landmarks for a specific gesture variation"""
        gesture_def = self.gesture_definitions[gesture]
        base_landmarks = self._get_base_hand_landmarks()
        
        # Apply gesture-specific modifications
        modified_landmarks = self._apply_gesture_modifications(
            base_landmarks, gesture_def, variation
        )
        
        return modified_landmarks
    
    def _get_base_hand_landmarks(self) -> List[Tuple[float, float, float]]:
        """Get base hand landmark positions"""
        # MediaPipe hand landmarks (21 points)
        landmarks = [
            # Wrist
            (0.5, 0.8, 0.0),
            # Thumb
            (0.45, 0.75, 0.0), (0.42, 0.7, 0.0), (0.4, 0.65, 0.0), (0.38, 0.6, 0.0),
            # Index finger
            (0.55, 0.75, 0.0), (0.58, 0.7, 0.0), (0.6, 0.65, 0.0), (0.62, 0.6, 0.0),
            # Middle finger
            (0.5, 0.75, 0.0), (0.5, 0.7, 0.0), (0.5, 0.65, 0.0), (0.5, 0.6, 0.0),
            # Ring finger
            (0.45, 0.75, 0.0), (0.45, 0.7, 0.0), (0.45, 0.65, 0.0), (0.45, 0.6, 0.0),
            # Pinky
            (0.4, 0.75, 0.0), (0.4, 0.7, 0.0), (0.4, 0.65, 0.0), (0.4, 0.6, 0.0)
        ]
        
        return landmarks
    
    def _apply_gesture_modifications(self, landmarks: List[Tuple[float, float, float]], 
                                   gesture_def: Dict, variation: int) -> List[Tuple[float, float, float]]:
        """Apply gesture-specific modifications to landmarks"""
        modified = landmarks.copy()
        
        # Add variation based on gesture type
        variation_factor = (variation - 1) / max(1, gesture_def['variations'] - 1)
        
        if gesture_def['hand_pose'] == 'fist_thumb_up':
            # Make a fist with thumb up
            for i in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:  # All fingers except thumb
                x, y, z = modified[i]
                modified[i] = (x, y + 0.1, z)  # Bend fingers down
            
            # Keep thumb extended
            for i in [1, 2, 3, 4]:  # Thumb
                x, y, z = modified[i]
                modified[i] = (x - 0.05, y - 0.05, z)  # Thumb up
        
        elif gesture_def['hand_pose'] == 'open_palm':
            # All fingers extended
            for i in range(1, 21):
                x, y, z = modified[i]
                modified[i] = (x, y - 0.1, z)  # Extend all fingers
        
        elif gesture_def['hand_pose'] == 'pointing':
            # Only index finger extended
            for i in [5, 6, 7, 8]:  # Index finger
                x, y, z = modified[i]
                modified[i] = (x, y - 0.1, z)  # Extend index
            
            # Bend other fingers
            for i in [1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
                x, y, z = modified[i]
                modified[i] = (x, y + 0.1, z)  # Bend other fingers
        
        elif gesture_def['hand_pose'] == 'thumbs_up':
            # Only thumb extended
            for i in [1, 2, 3, 4]:  # Thumb
                x, y, z = modified[i]
                modified[i] = (x - 0.05, y - 0.1, z)  # Thumb up
            
            # Bend other fingers
            for i in range(5, 21):
                x, y, z = modified[i]
                modified[i] = (x, y + 0.1, z)  # Bend other fingers
        
        elif gesture_def['hand_pose'] == 'peace_sign':
            # Index and middle fingers extended
            for i in [5, 6, 7, 8, 9, 10, 11, 12]:  # Index and middle
                x, y, z = modified[i]
                modified[i] = (x, y - 0.1, z)  # Extend index and middle
            
            # Bend other fingers
            for i in [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20]:
                x, y, z = modified[i]
                modified[i] = (x, y + 0.1, z)  # Bend other fingers
        
        elif gesture_def['hand_pose'] == 'wave':
            # Open palm with slight rotation
            for i in range(1, 21):
                x, y, z = modified[i]
                modified[i] = (x, y - 0.1, z)  # Extend all fingers
            
            # Add rotation variation
            rotation = variation_factor * 0.3 - 0.15
            for i in range(21):
                x, y, z = modified[i]
                new_x = x + rotation * (y - 0.5)
                modified[i] = (new_x, y, z)
        
        # Add random variation
        for i in range(21):
            x, y, z = modified[i]
            noise_x = (random.random() - 0.5) * 0.02 * variation_factor
            noise_y = (random.random() - 0.5) * 0.02 * variation_factor
            noise_z = (random.random() - 0.5) * 0.01 * variation_factor
            
            modified[i] = (
                max(0, min(1, x + noise_x)),
                max(0, min(1, y + noise_y)),
                z + noise_z
            )
        
        return modified
    
    def _create_hand_image(self, landmarks: List[Tuple[float, float, float]], 
                          background: np.ndarray) -> np.ndarray:
        """Create hand image from landmarks"""
        image = background.copy()
        height, width = image.shape[:2]
        
        # Draw hand skeleton
        hand_connections = [
            # Thumb
            (0, 1), (1, 2), (2, 3), (3, 4),
            # Index finger
            (0, 5), (5, 6), (6, 7), (7, 8),
            # Middle finger
            (0, 9), (9, 10), (10, 11), (11, 12),
            # Ring finger
            (0, 13), (13, 14), (14, 15), (15, 16),
            # Pinky
            (0, 17), (17, 18), (18, 19), (19, 20)
        ]
        
        # Draw connections
        for start_idx, end_idx in hand_connections:
            start_point = landmarks[start_idx]
            end_point = landmarks[end_idx]
            
            # Convert normalized coordinates to pixel coordinates
            start_pixel = (
                int(start_point[0] * width),
                int(start_point[1] * height)
            )
            end_pixel = (
                int(end_point[0] * width),
                int(end_point[1] * height)
            )
            
            # Draw line
            cv2.line(image, start_pixel, end_pixel, (0, 0, 0), 3)
        
        # Draw landmarks
        for landmark in landmarks:
            pixel_x = int(landmark[0] * width)
            pixel_y = int(landmark[1] * height)
            cv2.circle(image, (pixel_x, pixel_y), 5, (255, 0, 0), -1)
        
        return image
    
    def generate_gesture_dataset(self, gesture: str, num_samples: int = 100) -> List[Dict]:
        """Generate dataset for a specific gesture"""
        gesture_dir = self.output_dir / gesture
        gesture_dir.mkdir(exist_ok=True)
        
        dataset = []
        gesture_def = self.gesture_definitions[gesture]
        
        logger.info(f"Generating {num_samples} samples for gesture: {gesture}")
        
        for i in tqdm(range(num_samples), desc=f"Generating {gesture}"):
            # Select random variation
            variation = random.randint(1, gesture_def['variations'])
            
            # Select random background
            background = random.choice(self.backgrounds)
            
            # Generate landmarks
            landmarks = self._generate_hand_landmarks(gesture, variation)
            
            # Create image
            image = self._create_hand_image(landmarks, background)
            
            # Add some realistic variations
            image = self._add_realistic_variations(image)
            
            # Save image
            image_filename = f"{gesture}_{i:04d}.jpg"
            image_path = gesture_dir / image_filename
            cv2.imwrite(str(image_path), image)
            
            # Create sample data
            sample = {
                'image_path': str(image_path),
                'gesture': gesture,
                'variation': variation,
                'landmarks': landmarks,
                'description': gesture_def['description'],
                'complexity': gesture_def['complexity']
            }
            
            dataset.append(sample)
        
        # Save dataset metadata
        metadata_path = gesture_dir / f"{gesture}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        logger.info(f"Generated {len(dataset)} samples for {gesture}")
        return dataset
    
    def _add_realistic_variations(self, image: np.ndarray) -> np.ndarray:
        """Add realistic variations to the image"""
        # Random brightness adjustment
        brightness = random.uniform(0.8, 1.2)
        image = cv2.convertScaleAbs(image, alpha=brightness, beta=0)
        
        # Random contrast adjustment
        contrast = random.uniform(0.9, 1.1)
        image = cv2.convertScaleAbs(image, alpha=contrast, beta=0)
        
        # Random noise
        noise = np.random.randint(-10, 10, image.shape, dtype=np.int16)
        image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Random blur (sometimes)
        if random.random() < 0.1:  # 10% chance
            blur_kernel = random.choice([3, 5])
            image = cv2.GaussianBlur(image, (blur_kernel, blur_kernel), 0)
        
        return image
    
    def generate_full_dataset(self, samples_per_gesture: int = 100) -> Dict:
        """Generate complete ISL dataset"""
        logger.info(f"Generating full ISL dataset with {samples_per_gesture} samples per gesture")
        
        full_dataset = {}
        total_samples = 0
        
        for gesture in tqdm(self.gesture_definitions.keys(), desc="Generating full dataset"):
            try:
                gesture_data = self.generate_gesture_dataset(gesture, samples_per_gesture)
                full_dataset[gesture] = gesture_data
                total_samples += len(gesture_data)
            except Exception as e:
                logger.error(f"Error generating data for {gesture}: {str(e)}")
                continue
        
        # Save full dataset metadata
        dataset_metadata = {
            'total_gestures': len(full_dataset),
            'total_samples': total_samples,
            'samples_per_gesture': samples_per_gesture,
            'gestures': list(full_dataset.keys()),
            'generation_timestamp': str(pd.Timestamp.now()) if 'pd' in globals() else str(__import__('datetime').datetime.now())
        }
        
        metadata_path = self.output_dir / "dataset_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(dataset_metadata, f, indent=2)
        
        logger.info(f"Generated complete dataset: {total_samples} samples across {len(full_dataset)} gestures")
        return full_dataset
    
    def create_training_splits(self, train_ratio: float = 0.7, val_ratio: float = 0.2) -> Dict:
        """Create train/validation/test splits"""
        logger.info("Creating training splits...")
        
        # Load all generated data
        all_data = []
        for gesture_dir in self.output_dir.iterdir():
            if gesture_dir.is_dir() and gesture_dir.name in self.gesture_definitions:
                metadata_path = gesture_dir / f"{gesture_dir.name}_metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        gesture_data = json.load(f)
                        all_data.extend(gesture_data)
        
        # Shuffle data
        random.shuffle(all_data)
        
        # Split data
        total_samples = len(all_data)
        train_end = int(total_samples * train_ratio)
        val_end = int(total_samples * (train_ratio + val_ratio))
        
        train_data = all_data[:train_end]
        val_data = all_data[train_end:val_end]
        test_data = all_data[val_end:]
        
        # Save splits
        splits = {
            'train': train_data,
            'validation': val_data,
            'test': test_data
        }
        
        for split_name, split_data in splits.items():
            split_path = self.output_dir / f"{split_name}_split.json"
            with open(split_path, 'w') as f:
                json.dump(split_data, f, indent=2)
            
            logger.info(f"{split_name.capitalize()} split: {len(split_data)} samples")
        
        return splits

# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = ISLTrainingDataGenerator()
    
    # Generate full dataset
    dataset = generator.generate_full_dataset(samples_per_gesture=50)
    
    # Create training splits
    splits = generator.create_training_splits()
    
    print("Training data generation completed!")
    print(f"Total gestures: {len(dataset)}")
    print(f"Total samples: {sum(len(data) for data in dataset.values())}")
