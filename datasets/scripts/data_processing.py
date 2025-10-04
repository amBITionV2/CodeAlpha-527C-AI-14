"""
Data Processing Scripts for SignSpeak AI
Handles video preprocessing, landmark extraction, and dataset preparation
"""

import cv2
import numpy as np
import mediapipe as mp
import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging
from tqdm import tqdm
import pickle

logger = logging.getLogger(__name__)

class ISLDataProcessor:
    """Processes ISL gesture videos and extracts features"""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_face = mp.solutions.face_mesh
        
        # Initialize MediaPipe solutions
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.face = self.mp_face.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # ISL gesture classes
        self.gesture_classes = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'HELLO', 'THANK_YOU', 'PLEASE', 'SORRY', 'YES', 'NO', 'GOOD', 'BAD', 'HAPPY', 'SAD',
            'FATHER', 'MOTHER', 'BROTHER', 'SISTER', 'FRIEND', 'FAMILY',
            'WATER', 'FOOD', 'HOME', 'SCHOOL', 'WORK', 'MONEY',
            'TIME', 'TODAY', 'TOMORROW', 'YESTERDAY', 'NOW', 'LATER',
            'HOW', 'WHAT', 'WHERE', 'WHEN', 'WHY', 'WHO'
        ]
    
    def extract_landmarks_from_video(self, video_path: str) -> Dict:
        """
        Extract landmarks from a video file
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary containing extracted landmarks and metadata
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Could not open video: {video_path}")
            return {}
        
        landmarks_data = {
            'video_path': video_path,
            'frames': [],
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        }
        
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Extract landmarks
            frame_landmarks = self._extract_frame_landmarks(rgb_frame)
            frame_landmarks['frame_idx'] = frame_idx
            frame_landmarks['timestamp'] = frame_idx / landmarks_data['fps']
            
            landmarks_data['frames'].append(frame_landmarks)
            frame_idx += 1
        
        cap.release()
        return landmarks_data
    
    def _extract_frame_landmarks(self, frame: np.ndarray) -> Dict:
        """Extract landmarks from a single frame"""
        landmarks = {
            'hands': [],
            'pose': [],
            'face': [],
            'timestamp': 0.0
        }
        
        # Extract hand landmarks
        hand_results = self.hands.process(frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                hand_points = []
                for landmark in hand_landmarks.landmark:
                    hand_points.extend([landmark.x, landmark.y, landmark.z])
                landmarks['hands'].append(hand_points)
        
        # Extract pose landmarks
        pose_results = self.pose.process(frame)
        if pose_results.pose_landmarks:
            pose_points = []
            for landmark in pose_results.pose_landmarks.landmark:
                pose_points.extend([landmark.x, landmark.y, landmark.z])
            landmarks['pose'] = pose_points
        
        # Extract face landmarks
        face_results = self.face.process(frame)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                face_points = []
                for landmark in face_landmarks.landmark:
                    face_points.extend([landmark.x, landmark.y, landmark.z])
                landmarks['face'] = face_points
        
        return landmarks
    
    def preprocess_video(self, video_path: str, output_path: str, target_resolution: Tuple[int, int] = (224, 224)) -> bool:
        """
        Preprocess video: resize, normalize, and save
        
        Args:
            video_path: Input video path
            output_path: Output video path
            target_resolution: Target resolution (width, height)
            
        Returns:
            Success status
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return False
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, target_resolution)
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Resize frame
                resized_frame = cv2.resize(frame, target_resolution)
                
                # Normalize lighting
                normalized_frame = self._normalize_lighting(resized_frame)
                
                # Write frame
                out.write(normalized_frame)
            
            cap.release()
            out.release()
            return True
            
        except Exception as e:
            logger.error(f"Error preprocessing video: {str(e)}")
            return False
    
    def _normalize_lighting(self, frame: np.ndarray) -> np.ndarray:
        """Normalize lighting in frame"""
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        
        # Convert back to BGR
        normalized = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return normalized
    
    def create_dataset_splits(self, data_dir: str, output_dir: str, train_ratio: float = 0.7, val_ratio: float = 0.2) -> bool:
        """
        Create train/validation/test splits from dataset
        
        Args:
            data_dir: Directory containing gesture videos
            output_dir: Output directory for splits
            train_ratio: Training set ratio
            val_ratio: Validation set ratio
            
        Returns:
            Success status
        """
        try:
            # Create output directories
            os.makedirs(os.path.join(output_dir, 'train'), exist_ok=True)
            os.makedirs(os.path.join(output_dir, 'validation'), exist_ok=True)
            os.makedirs(os.path.join(output_dir, 'test'), exist_ok=True)
            
            # Get all gesture directories
            gesture_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
            
            for gesture in gesture_dirs:
                gesture_path = os.path.join(data_dir, gesture)
                video_files = [f for f in os.listdir(gesture_path) if f.endswith('.mp4')]
                
                # Shuffle videos
                np.random.shuffle(video_files)
                
                # Calculate split indices
                n_videos = len(video_files)
                train_end = int(n_videos * train_ratio)
                val_end = int(n_videos * (train_ratio + val_ratio))
                
                # Split videos
                train_videos = video_files[:train_end]
                val_videos = video_files[train_end:val_end]
                test_videos = video_files[val_end:]
                
                # Copy videos to respective directories
                self._copy_videos_to_split(gesture_path, train_videos, os.path.join(output_dir, 'train', gesture))
                self._copy_videos_to_split(gesture_path, val_videos, os.path.join(output_dir, 'validation', gesture))
                self._copy_videos_to_split(gesture_path, test_videos, os.path.join(output_dir, 'test', gesture))
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating dataset splits: {str(e)}")
            return False
    
    def _copy_videos_to_split(self, source_dir: str, video_files: List[str], target_dir: str):
        """Copy video files to target directory"""
        os.makedirs(target_dir, exist_ok=True)
        
        for video_file in video_files:
            source_path = os.path.join(source_dir, video_file)
            target_path = os.path.join(target_dir, video_file)
            
            if os.path.exists(source_path):
                import shutil
                shutil.copy2(source_path, target_path)
    
    def extract_features_batch(self, video_dir: str, output_dir: str) -> bool:
        """
        Extract features from all videos in directory
        
        Args:
            video_dir: Directory containing videos
            output_dir: Output directory for features
            
        Returns:
            Success status
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Get all video files
            video_files = []
            for root, dirs, files in os.walk(video_dir):
                for file in files:
                    if file.endswith('.mp4'):
                        video_files.append(os.path.join(root, file))
            
            logger.info(f"Processing {len(video_files)} videos...")
            
            # Process each video
            for video_path in tqdm(video_files, desc="Extracting features"):
                try:
                    # Extract landmarks
                    landmarks_data = self.extract_landmarks_from_video(video_path)
                    
                    if landmarks_data:
                        # Save landmarks
                        relative_path = os.path.relpath(video_path, video_dir)
                        output_path = os.path.join(output_dir, relative_path.replace('.mp4', '.json'))
                        
                        # Create output directory
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        
                        # Save landmarks
                        with open(output_path, 'w') as f:
                            json.dump(landmarks_data, f, indent=2)
                    
                except Exception as e:
                    logger.error(f"Error processing {video_path}: {str(e)}")
                    continue
            
            return True
            
        except Exception as e:
            logger.error(f"Error in batch feature extraction: {str(e)}")
            return False
    
    def create_annotation_file(self, data_dir: str, output_path: str) -> bool:
        """
        Create annotation file for the dataset
        
        Args:
            data_dir: Directory containing gesture data
            output_path: Output annotation file path
            
        Returns:
            Success status
        """
        try:
            annotations = []
            
            # Walk through data directory
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    if file.endswith('.mp4'):
                        video_path = os.path.join(root, file)
                        gesture_name = os.path.basename(root)
                        
                        # Get video properties
                        cap = cv2.VideoCapture(video_path)
                        if cap.isOpened():
                            fps = cap.get(cv2.CAP_PROP_FPS)
                            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                            duration = frame_count / fps
                            cap.release()
                            
                            annotation = {
                                'video_path': video_path,
                                'gesture': gesture_name,
                                'fps': fps,
                                'frame_count': frame_count,
                                'duration': duration,
                                'label': self.gesture_classes.index(gesture_name) if gesture_name in self.gesture_classes else -1
                            }
                            
                            annotations.append(annotation)
            
            # Save annotations
            with open(output_path, 'w') as f:
                json.dump(annotations, f, indent=2)
            
            logger.info(f"Created annotation file with {len(annotations)} entries")
            return True
            
        except Exception as e:
            logger.error(f"Error creating annotation file: {str(e)}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Initialize processor
    processor = ISLDataProcessor()
    
    # Example: Process a single video
    video_path = "datasets/raw/isl_gestures/HELLO/video_001.mp4"
    landmarks = processor.extract_landmarks_from_video(video_path)
    print(f"Extracted landmarks from {len(landmarks.get('frames', []))} frames")
    
    # Example: Create dataset splits
    processor.create_dataset_splits("datasets/raw", "datasets/processed")
    
    # Example: Extract features from all videos
    processor.extract_features_batch("datasets/processed", "datasets/features")
    
    # Example: Create annotation file
    processor.create_annotation_file("datasets/processed", "datasets/annotations.json")
