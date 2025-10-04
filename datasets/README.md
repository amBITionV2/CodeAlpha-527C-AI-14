# SignSpeak AI Dataset Structure

This directory contains datasets and training data for the SignSpeak AI project.

## Dataset Organization

```
datasets/
├── raw/                          # Raw video and image data
│   ├── isl_gestures/            # ISL gesture videos
│   ├── hand_landmarks/          # Extracted hand landmark data
│   └── pose_data/               # Body pose data
├── processed/                   # Processed and cleaned data
│   ├── training/               # Training dataset
│   ├── validation/             # Validation dataset
│   └── test/                   # Test dataset
├── annotations/                 # Gesture annotations and labels
├── models/                     # Trained model checkpoints
└── scripts/                    # Data processing scripts
```

## ISL Gesture Categories

### Basic Gestures (26 letters + numbers)
- A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
- 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

### Common Words (50+ words)
- Greetings: HELLO, HI, GOODBYE, THANK_YOU, PLEASE, SORRY
- Emotions: HAPPY, SAD, ANGRY, SURPRISED, WORRIED
- Family: FATHER, MOTHER, BROTHER, SISTER, FAMILY, FRIEND
- Objects: WATER, FOOD, HOME, SCHOOL, WORK, MONEY, BOOK, CAR
- Time: TODAY, TOMORROW, YESTERDAY, NOW, LATER, TIME
- Questions: HOW, WHAT, WHERE, WHEN, WHY, WHO
- Actions: EAT, DRINK, SLEEP, WORK, STUDY, PLAY, GO, COME

### Complex Phrases (20+ phrases)
- "HOW ARE YOU?"
- "WHAT IS YOUR NAME?"
- "WHERE ARE YOU FROM?"
- "THANK YOU VERY MUCH"
- "NICE TO MEET YOU"

## Data Collection Guidelines

### Video Specifications
- **Resolution**: 1080p (1920x1080) minimum
- **Frame Rate**: 30 FPS
- **Duration**: 2-5 seconds per gesture
- **Lighting**: Well-lit environment, consistent lighting
- **Background**: Plain background preferred
- **Camera Angle**: Front-facing, chest level

### Signer Requirements
- **Age Range**: 18-65 years
- **Hand Dominance**: Both left and right-handed signers
- **Experience**: Native ISL users preferred
- **Diversity**: Include signers from different regions of India

### Annotation Standards
- **Gesture Boundaries**: Clear start and end points
- **Hand Shape**: Detailed hand shape classification
- **Movement**: Direction and speed of movement
- **Location**: Spatial location of gestures
- **Facial Expression**: Important for context

## Dataset Statistics

| Category | Count | Videos | Signers |
|----------|-------|--------|---------|
| Letters | 26 | 2,600 | 10 |
| Numbers | 10 | 1,000 | 10 |
| Words | 50 | 5,000 | 20 |
| Phrases | 20 | 2,000 | 15 |
| **Total** | **106** | **10,600** | **25** |

## Data Processing Pipeline

1. **Video Collection**: Record ISL gestures using standardized protocol
2. **Preprocessing**: Extract frames, normalize lighting, resize
3. **Landmark Extraction**: Use MediaPipe to extract hand, pose, and face landmarks
4. **Annotation**: Label gestures with timestamps and classifications
5. **Augmentation**: Apply data augmentation techniques
6. **Splitting**: Divide into training (70%), validation (20%), test (10%)

## Quality Assurance

### Data Validation
- [ ] Video quality check (resolution, lighting, stability)
- [ ] Gesture accuracy verification
- [ ] Annotation consistency review
- [ ] Signer diversity validation

### Privacy and Ethics
- [ ] Informed consent from all signers
- [ ] Data anonymization
- [ ] Secure storage and access controls
- [ ] Ethical use guidelines

## Usage Instructions

### For Researchers
1. Download the processed dataset
2. Use provided scripts for data loading
3. Follow the training pipeline in `scripts/train_model.py`
4. Evaluate using standard metrics

### For Contributors
1. Follow data collection guidelines
2. Use provided annotation tools
3. Submit data through proper channels
4. Maintain quality standards

## Citation

If you use this dataset in your research, please cite:

```
@dataset{signspeak_ai_2024,
  title={SignSpeak AI: Indian Sign Language Dataset},
  author={SignSpeak AI Team},
  year={2024},
  url={https://github.com/yourusername/SignSpeak-AI}
}
```

## Contact

For questions about the dataset or to contribute data, please contact:
- Email: dataset@signspeak-ai.com
- GitHub Issues: [SignSpeak AI Issues](https://github.com/yourusername/SignSpeak-AI/issues)
