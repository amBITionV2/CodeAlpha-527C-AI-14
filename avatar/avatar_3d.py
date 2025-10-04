"""
3D Avatar System for SignSpeak AI
Handles 3D avatar creation and ISL gesture animation
"""

import numpy as np
import json
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass
import math

logger = logging.getLogger(__name__)

@dataclass
class Joint:
    """Represents a 3D joint in the avatar skeleton"""
    name: str
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    parent: Optional[str] = None
    children: List[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []

@dataclass
class GestureFrame:
    """Represents a single frame of a gesture animation"""
    timestamp: float
    joints: Dict[str, Joint]
    
class ISLAvatar:
    """3D Avatar system for Indian Sign Language gesture animation"""
    
    def __init__(self):
        self.skeleton = self._create_skeleton()
        self.gesture_database = self._load_gesture_database()
        self.current_pose = {}
        self.animation_speed = 1.0
        
    def _create_skeleton(self) -> Dict[str, Joint]:
        """Create the basic human skeleton structure for ISL gestures"""
        skeleton = {
            # Head and neck
            'head': Joint('head', (0, 1.8, 0), (0, 0, 0)),
            'neck': Joint('neck', (0, 1.6, 0), (0, 0, 0), children=['head']),
            
            # Left arm
            'left_shoulder': Joint('left_shoulder', (-0.3, 1.5, 0), (0, 0, 0), children=['left_elbow']),
            'left_elbow': Joint('left_elbow', (-0.5, 1.2, 0), (0, 0, 0), parent='left_shoulder', children=['left_wrist']),
            'left_wrist': Joint('left_wrist', (-0.7, 0.9, 0), (0, 0, 0), parent='left_elbow', children=['left_hand']),
            'left_hand': Joint('left_hand', (-0.8, 0.7, 0), (0, 0, 0), parent='left_wrist'),
            
            # Right arm
            'right_shoulder': Joint('right_shoulder', (0.3, 1.5, 0), (0, 0, 0), children=['right_elbow']),
            'right_elbow': Joint('right_elbow', (0.5, 1.2, 0), (0, 0, 0), parent='right_shoulder', children=['right_wrist']),
            'right_wrist': Joint('right_wrist', (0.7, 0.9, 0), (0, 0, 0), parent='right_elbow', children=['right_hand']),
            'right_hand': Joint('right_hand', (0.8, 0.7, 0), (0, 0, 0), parent='right_wrist'),
            
            # Torso
            'spine': Joint('spine', (0, 1.3, 0), (0, 0, 0), children=['left_shoulder', 'right_shoulder', 'neck']),
            'hip': Joint('hip', (0, 0.9, 0), (0, 0, 0), children=['spine']),
        }
        
        # Set parent relationships
        for joint_name, joint in skeleton.items():
            if joint.parent:
                skeleton[joint.parent].children.append(joint_name)
        
        return skeleton
    
    def _load_gesture_database(self) -> Dict[str, List[GestureFrame]]:
        """Load ISL gesture database with predefined animations"""
        gestures = {
            'HELLO': self._create_hello_gesture(),
            'THANK_YOU': self._create_thank_you_gesture(),
            'YES': self._create_yes_gesture(),
            'NO': self._create_no_gesture(),
            'GOOD': self._create_good_gesture(),
            'BAD': self._create_bad_gesture(),
            'WATER': self._create_water_gesture(),
            'FOOD': self._create_food_gesture(),
            'HOME': self._create_home_gesture(),
            'SCHOOL': self._create_school_gesture(),
        }
        
        return gestures
    
    def _create_hello_gesture(self) -> List[GestureFrame]:
        """Create HELLO gesture animation"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Wave motion
        for i in range(10):
            t = i / 9.0
            joints = self.skeleton.copy()
            
            # Right hand wave
            wave_angle = math.sin(t * math.pi * 2) * 0.3
            joints['right_wrist'].rotation = (0, 0, wave_angle)
            joints['right_hand'].rotation = (0, 0, wave_angle)
            
            frames.append(GestureFrame(t * 2.0, joints))
        
        return frames
    
    def _create_thank_you_gesture(self) -> List[GestureFrame]:
        """Create THANK YOU gesture animation"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Both hands to chest
        for i in range(15):
            t = i / 14.0
            joints = self.skeleton.copy()
            
            # Move both hands to chest
            chest_y = 1.2 + t * 0.3
            joints['left_hand'].position = (-0.2, chest_y, 0.1)
            joints['right_hand'].position = (0.2, chest_y, 0.1)
            
            frames.append(GestureFrame(t * 1.5, joints))
        
        return frames
    
    def _create_yes_gesture(self) -> List[GestureFrame]:
        """Create YES gesture animation (nodding)"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Nodding motion
        for i in range(8):
            t = i / 7.0
            joints = self.skeleton.copy()
            
            # Head nod
            nod_angle = math.sin(t * math.pi) * 0.2
            joints['head'].rotation = (nod_angle, 0, 0)
            joints['neck'].rotation = (nod_angle, 0, 0)
            
            frames.append(GestureFrame(t * 1.0, joints))
        
        return frames
    
    def _create_no_gesture(self) -> List[GestureFrame]:
        """Create NO gesture animation (head shake)"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Head shake motion
        for i in range(12):
            t = i / 11.0
            joints = self.skeleton.copy()
            
            # Head shake
            shake_angle = math.sin(t * math.pi * 4) * 0.3
            joints['head'].rotation = (0, 0, shake_angle)
            joints['neck'].rotation = (0, 0, shake_angle)
            
            frames.append(GestureFrame(t * 1.2, joints))
        
        return frames
    
    def _create_good_gesture(self) -> List[GestureFrame]:
        """Create GOOD gesture animation (thumbs up)"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Thumbs up motion
        for i in range(10):
            t = i / 9.0
            joints = self.skeleton.copy()
            
            # Right hand thumbs up
            joints['right_hand'].rotation = (0, 0, 1.57)  # 90 degrees
            joints['right_wrist'].rotation = (0, 0, 0.3)
            
            frames.append(GestureFrame(t * 1.0, joints))
        
        return frames
    
    def _create_bad_gesture(self) -> List[GestureFrame]:
        """Create BAD gesture animation (thumbs down)"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Thumbs down motion
        for i in range(10):
            t = i / 9.0
            joints = self.skeleton.copy()
            
            # Right hand thumbs down
            joints['right_hand'].rotation = (0, 0, -1.57)  # -90 degrees
            joints['right_wrist'].rotation = (0, 0, -0.3)
            
            frames.append(GestureFrame(t * 1.0, joints))
        
        return frames
    
    def _create_water_gesture(self) -> List[GestureFrame]:
        """Create WATER gesture animation"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Water drinking motion
        for i in range(15):
            t = i / 14.0
            joints = self.skeleton.copy()
            
            # Hand to mouth motion
            mouth_y = 1.6 - t * 0.4
            joints['right_hand'].position = (0.1, mouth_y, 0.2)
            joints['right_elbow'].rotation = (0, 0, t * 0.5)
            
            frames.append(GestureFrame(t * 2.0, joints))
        
        return frames
    
    def _create_food_gesture(self) -> List[GestureFrame]:
        """Create FOOD gesture animation"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Eating motion
        for i in range(12):
            t = i / 11.0
            joints = self.skeleton.copy()
            
            # Hand to mouth and back
            mouth_y = 1.6 - abs(t - 0.5) * 0.8
            joints['right_hand'].position = (0.1, mouth_y, 0.2)
            
            frames.append(GestureFrame(t * 1.5, joints))
        
        return frames
    
    def _create_home_gesture(self) -> List[GestureFrame]:
        """Create HOME gesture animation"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # House shape with hands
        for i in range(20):
            t = i / 19.0
            joints = self.skeleton.copy()
            
            # Create house shape
            if t < 0.5:
                # Building up
                height = t * 0.4
                joints['left_hand'].position = (-0.3, 1.2 + height, 0.1)
                joints['right_hand'].position = (0.3, 1.2 + height, 0.1)
            else:
                # Roof
                roof_t = (t - 0.5) * 2
                joints['left_hand'].position = (-0.3, 1.4, 0.1)
                joints['right_hand'].position = (0.3, 1.4, 0.1)
            
            frames.append(GestureFrame(t * 2.5, joints))
        
        return frames
    
    def _create_school_gesture(self) -> List[GestureFrame]:
        """Create SCHOOL gesture animation"""
        frames = []
        
        # Initial position
        initial_joints = self.skeleton.copy()
        frames.append(GestureFrame(0.0, initial_joints))
        
        # Writing motion
        for i in range(15):
            t = i / 14.0
            joints = self.skeleton.copy()
            
            # Writing motion with right hand
            joints['right_hand'].position = (0.2 + t * 0.3, 1.0, 0.1)
            joints['right_wrist'].rotation = (0, 0, t * 0.2)
            
            frames.append(GestureFrame(t * 2.0, joints))
        
        return frames
    
    def animate_gesture(self, gesture_name: str, duration: float = None) -> List[GestureFrame]:
        """
        Animate a specific ISL gesture
        
        Args:
            gesture_name: Name of the gesture to animate
            duration: Optional duration override
            
        Returns:
            List of animation frames
        """
        if gesture_name not in self.gesture_database:
            logger.warning(f"Gesture '{gesture_name}' not found in database")
            return []
        
        gesture_frames = self.gesture_database[gesture_name]
        
        if duration:
            # Scale animation to desired duration
            original_duration = gesture_frames[-1].timestamp
            scale_factor = duration / original_duration
            
            scaled_frames = []
            for frame in gesture_frames:
                scaled_frame = GestureFrame(
                    frame.timestamp * scale_factor,
                    frame.joints
                )
                scaled_frames.append(scaled_frame)
            
            return scaled_frames
        
        return gesture_frames
    
    def animate_text(self, text: str) -> List[GestureFrame]:
        """
        Convert text to sequence of ISL gesture animations
        
        Args:
            text: Text to convert to gestures
            
        Returns:
            List of animation frames for the entire text
        """
        words = text.upper().split()
        all_frames = []
        current_time = 0.0
        
        for word in words:
            if word in self.gesture_database:
                gesture_frames = self.animate_gesture(word)
                
                # Offset timestamps
                for frame in gesture_frames:
                    offset_frame = GestureFrame(
                        frame.timestamp + current_time,
                        frame.joints
                    )
                    all_frames.append(offset_frame)
                
                # Add pause between words
                current_time += gesture_frames[-1].timestamp + 0.5
            else:
                # Spell out unknown words
                for letter in word:
                    if letter in self.gesture_database:
                        gesture_frames = self.animate_gesture(letter)
                        
                        for frame in gesture_frames:
                            offset_frame = GestureFrame(
                                frame.timestamp + current_time,
                                frame.joints
                            )
                            all_frames.append(offset_frame)
                        
                        current_time += gesture_frames[-1].timestamp + 0.2
        
        return all_frames
    
    def get_available_gestures(self) -> List[str]:
        """Get list of available ISL gestures"""
        return list(self.gesture_database.keys())
    
    def export_animation(self, frames: List[GestureFrame], format: str = 'json') -> str:
        """
        Export animation frames to specified format
        
        Args:
            frames: Animation frames to export
            format: Export format ('json', 'bvh', 'fbx')
            
        Returns:
            Exported animation data
        """
        if format == 'json':
            animation_data = {
                'frames': [],
                'duration': frames[-1].timestamp if frames else 0.0
            }
            
            for frame in frames:
                frame_data = {
                    'timestamp': frame.timestamp,
                    'joints': {}
                }
                
                for joint_name, joint in frame.joints.items():
                    frame_data['joints'][joint_name] = {
                        'position': joint.position,
                        'rotation': joint.rotation
                    }
                
                animation_data['frames'].append(frame_data)
            
            return json.dumps(animation_data, indent=2)
        
        else:
            logger.warning(f"Export format '{format}' not supported yet")
            return ""

# Example usage and testing
if __name__ == "__main__":
    # Initialize avatar
    avatar = ISLAvatar()
    
    # Test gesture animation
    print("Available gestures:", avatar.get_available_gestures())
    
    # Animate a single gesture
    hello_frames = avatar.animate_gesture('HELLO')
    print(f"HELLO gesture has {len(hello_frames)} frames")
    
    # Animate text
    text_frames = avatar.animate_text("HELLO THANK YOU")
    print(f"Text animation has {len(text_frames)} frames")
    
    # Export animation
    animation_json = avatar.export_animation(hello_frames)
    print("Animation exported successfully")
