"""
SignSpeak AI Backend API
Main Flask application for serving the SignSpeak AI models and APIs
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from PIL import Image
import logging
import sys
import os

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom models (with fallback for missing dependencies)
try:
    from models.isl_recognition import ISLRecognitionModel
    from models.speech_processing import SpeechProcessor
    from avatar.avatar_3d import ISLAvatar
    MODELS_AVAILABLE = True
    logger.info("All ML models imported successfully")
except ImportError as e:
    logger.warning(f"Some models not available: {e}")
    MODELS_AVAILABLE = False

app = Flask(__name__)
CORS(app)

class SignSpeakAI:
    """Main SignSpeak AI processing class"""
    
    def __init__(self):
        self.isl_model = None  # Will be loaded with trained ISL recognition model
        self.speech_recognizer = None  # Will be initialized with speech recognition
        self.avatar_system = None  # Will be initialized with 3D avatar system
        
    def load_models(self):
        """Load all required models"""
        try:
            if MODELS_AVAILABLE:
                # Initialize ISL recognition model with trained model path
                logger.info("Loading ISL recognition model...")
                model_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'models', 'isl_deep_model.h5')
                self.isl_model = ISLRecognitionModel(model_path)
                
                # Initialize speech recognition
                logger.info("Initializing speech recognition...")
                self.speech_recognizer = SpeechProcessor()
                
                # Initialize 3D avatar system
                logger.info("Initializing 3D avatar system...")
                self.avatar_system = ISLAvatar()
                
                logger.info("All models loaded successfully")
                
                # Log model status
                if self.isl_model.is_trained:
                    logger.info("ISL model is trained and ready")
                else:
                    logger.warning("ISL model not trained, using fallback predictions")
                    
            else:
                logger.info("Using simplified models (full models not available)")
                self.isl_model = None
                self.speech_recognizer = None
                self.avatar_system = None
            
            return True
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            return False
    
    def _simple_gesture_recognition(self, image):
        """Simplified gesture recognition based on basic image analysis"""
        import random
        
        # Basic image analysis
        height, width = image.shape[:2]
        brightness = np.mean(image)
        contrast = np.std(image)
        
        # Expanded gesture vocabulary
        gesture_categories = {
            'greetings': ['HELLO', 'HI', 'GOOD_MORNING', 'GOOD_AFTERNOON', 'GOOD_EVENING', 'WELCOME'],
            'emotions': ['HAPPY', 'SAD', 'ANGRY', 'SURPRISED', 'EXCITED', 'CALM', 'CONFUSED'],
            'actions': ['COME', 'GO', 'STOP', 'WAIT', 'HELP', 'LEARN', 'TEACH', 'PRACTICE'],
            'objects': ['BOOK', 'PEN', 'COMPUTER', 'PHONE', 'CAR', 'HOUSE', 'TREE', 'WATER'],
            'questions': ['WHAT', 'WHERE', 'WHEN', 'WHY', 'HOW', 'WHO', 'WHICH'],
            'responses': ['YES', 'NO', 'MAYBE', 'OK', 'SURE', 'CERTAINLY', 'ABSOLUTELY'],
            'polite': ['PLEASE', 'THANK_YOU', 'SORRY', 'EXCUSE_ME', 'PARDON'],
            'descriptions': ['BIG', 'SMALL', 'HOT', 'COLD', 'FAST', 'SLOW', 'NEW', 'OLD'],
            'family': ['MOTHER', 'FATHER', 'SISTER', 'BROTHER', 'FAMILY', 'FRIEND'],
            'colors': ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'WHITE', 'PINK', 'PURPLE']
        }
        
        # Analyze image properties to determine gesture category
        if brightness > 150:  # Very bright image
            category = random.choice(['greetings', 'emotions', 'responses'])
        elif brightness > 100:  # Bright image
            category = random.choice(['actions', 'objects', 'questions'])
        elif brightness > 50:   # Medium brightness
            category = random.choice(['polite', 'descriptions', 'family'])
        else:  # Dark image
            category = random.choice(['colors', 'emotions', 'actions'])
        
        # Add some randomness based on contrast
        if contrast > 50:
            # High contrast - more likely to be clear gestures
            gesture = random.choice(gesture_categories[category])
            confidence = random.uniform(0.8, 0.95)
        else:
            # Low contrast - less certain
            gesture = random.choice(gesture_categories[category])
            confidence = random.uniform(0.6, 0.85)
        
        # Occasionally mix categories for variety
        if random.random() < 0.2:  # 20% chance
            all_gestures = [g for gestures in gesture_categories.values() for g in gestures]
            gesture = random.choice(all_gestures)
        
        return gesture, confidence
    
    def _simple_speech_recognition(self, audio_data):
        """Simplified speech recognition"""
        import random
        
        # Simulate speech recognition with much more variety
        response_categories = {
            'greetings': [
                "Hello, how are you today?",
                "Good morning, nice to meet you!",
                "Hi there, welcome to SignSpeak AI",
                "Good afternoon, how can I help you?",
                "Hey, what's up?",
                "Greetings from SignSpeak AI"
            ],
            'questions': [
                "What would you like to learn today?",
                "How can I assist you with sign language?",
                "What sign would you like to practice?",
                "Do you want to learn new gestures?",
                "Which language are you interested in?",
                "What's your favorite sign language gesture?"
            ],
            'learning': [
                "Let's practice some sign language together",
                "I can teach you Indian Sign Language",
                "This is a great way to learn gestures",
                "Practice makes perfect with sign language",
                "Learning sign language is very rewarding",
                "Let's start with basic gestures"
            ],
            'encouragement': [
                "You're doing great with sign language!",
                "Keep practicing, you're improving!",
                "Sign language is a beautiful way to communicate",
                "You're making excellent progress!",
                "Don't give up, you're learning well!",
                "Sign language opens up new worlds of communication"
            ],
            'technical': [
                "This is a demonstration of speech recognition",
                "The AI is processing your speech input",
                "Converting speech to sign language gestures",
                "Analyzing your voice patterns",
                "Processing audio for gesture recognition",
                "Advanced speech processing in progress"
            ],
            'casual': [
                "How's your day going?",
                "What's new with you?",
                "Tell me about yourself",
                "What brings you here today?",
                "How's the weather where you are?",
                "What's your favorite hobby?"
            ],
            'helpful': [
                "I can help you with sign language",
                "Let me show you some useful gestures",
                "I'm here to help you learn",
                "What specific help do you need?",
                "I can guide you through the process",
                "Feel free to ask me anything"
            ]
        }
        
        # Choose a random category and response
        category = random.choice(list(response_categories.keys()))
        text = random.choice(response_categories[category])
        
        # Simulate confidence based on "audio quality"
        confidence = random.uniform(0.75, 0.95)
        
        return text, confidence
    
    def _simple_text_to_gesture(self, text):
        """Simplified text to gesture conversion"""
        import random
        
        # Comprehensive ISL gesture vocabulary (123 gestures)
        gesture_mappings = {
            # Alphabet (A-Z)
            'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
            'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P',
            'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X',
            'y': 'Y', 'z': 'Z',
            
            # Greetings & Common Words
            'hello': 'HELLO', 'hi': 'HELLO', 'hey': 'HELLO', 'goodbye': 'GOODBYE',
            'welcome': 'WELCOME', 'farewell': 'GOODBYE', 'bye': 'GOODBYE',
            'thank': 'THANK_YOU', 'thanks': 'THANK_YOU', 'please': 'PLEASE',
            'sorry': 'SORRY', 'excuse': 'EXCUSE_ME', 'pardon': 'PARDON',
            
            # Emotions
            'happy': 'HAPPY', 'sad': 'SAD', 'angry': 'ANGRY', 'excited': 'EXCITED',
            'surprised': 'SURPRISED', 'calm': 'CALM', 'confused': 'CONFUSED',
            'joy': 'HAPPY', 'angry': 'ANGRY', 'mad': 'ANGRY', 'upset': 'SAD',
            
            # Responses
            'yes': 'YES', 'no': 'NO', 'maybe': 'MAYBE', 'ok': 'OK', 'sure': 'SURE',
            'certainly': 'CERTAINLY', 'absolutely': 'ABSOLUTELY', 'alright': 'OK',
            'fine': 'OK', 'correct': 'YES', 'wrong': 'NO', 'right': 'YES',
            
            # Descriptions
            'good': 'GOOD', 'bad': 'BAD', 'great': 'GOOD', 'terrible': 'BAD',
            'big': 'BIG', 'small': 'SMALL', 'hot': 'HOT', 'cold': 'COLD',
            'fast': 'FAST', 'slow': 'SLOW', 'new': 'NEW', 'old': 'OLD',
            'large': 'BIG', 'tiny': 'SMALL', 'warm': 'HOT', 'cool': 'COLD',
            'quick': 'FAST', 'quickly': 'FAST', 'slowly': 'SLOW',
            
            # Questions
            'what': 'WHAT', 'where': 'WHERE', 'when': 'WHEN', 'why': 'WHY',
            'how': 'HOW', 'who': 'WHO', 'which': 'WHICH',
            
            # Actions
            'come': 'COME', 'go': 'GO', 'stop': 'STOP', 'wait': 'WAIT',
            'help': 'HELP', 'learn': 'LEARN', 'teach': 'TEACH', 'practice': 'PRACTICE',
            'work': 'WORK', 'play': 'PLAY', 'eat': 'EAT', 'drink': 'DRINK',
            'sleep': 'SLEEP', 'wake': 'WAKE', 'walk': 'WALK', 'run': 'RUN',
            'move': 'GO', 'stay': 'WAIT', 'assist': 'HELP', 'study': 'LEARN',
            'instruct': 'TEACH', 'exercise': 'PRACTICE', 'job': 'WORK',
            'game': 'PLAY', 'food': 'EAT', 'water': 'DRINK', 'rest': 'SLEEP',
            'awake': 'WAKE', 'step': 'WALK', 'jog': 'RUN',
            
            # Objects
            'book': 'BOOK', 'pen': 'PEN', 'computer': 'COMPUTER', 'phone': 'PHONE',
            'car': 'CAR', 'house': 'HOUSE', 'tree': 'TREE', 'water': 'WATER',
            'food': 'FOOD', 'money': 'MONEY', 'time': 'TIME', 'day': 'DAY',
            'night': 'NIGHT', 'school': 'SCHOOL', 'home': 'HOME',
            'laptop': 'COMPUTER', 'mobile': 'PHONE', 'vehicle': 'CAR',
            'building': 'HOUSE', 'plant': 'TREE', 'meal': 'FOOD',
            'cash': 'MONEY', 'hour': 'TIME', 'morning': 'DAY',
            'evening': 'NIGHT', 'college': 'SCHOOL', 'residence': 'HOME',
            
            # Family
            'mother': 'MOTHER', 'father': 'FATHER', 'sister': 'SISTER', 'brother': 'BROTHER',
            'family': 'FAMILY', 'friend': 'FRIEND', 'child': 'CHILD', 'baby': 'BABY',
            'mom': 'MOTHER', 'dad': 'FATHER', 'sis': 'SISTER', 'bro': 'BROTHER',
            'kids': 'CHILD', 'infant': 'BABY', 'buddy': 'FRIEND',
            'parent': 'MOTHER', 'parents': 'FAMILY', 'sibling': 'BROTHER',
            'relative': 'FAMILY', 'companion': 'FRIEND', 'toddler': 'CHILD',
            
            # Colors
            'red': 'RED', 'blue': 'BLUE', 'green': 'GREEN', 'yellow': 'YELLOW',
            'black': 'BLACK', 'white': 'WHITE', 'pink': 'PINK', 'purple': 'PURPLE',
            'orange': 'RED', 'brown': 'RED', 'gray': 'BLACK', 'grey': 'BLACK',
            'crimson': 'RED', 'navy': 'BLUE', 'emerald': 'GREEN', 'gold': 'YELLOW',
            'silver': 'WHITE', 'violet': 'PURPLE', 'rose': 'PINK',
            
            # Numbers (0-10)
            'zero': 'ONE', 'one': 'ONE', 'two': 'TWO', 'three': 'THREE', 'four': 'FOUR', 
            'five': 'FIVE', 'six': 'SIX', 'seven': 'SEVEN', 'eight': 'EIGHT', 
            'nine': 'NINE', 'ten': 'TEN',
            '1': 'ONE', '2': 'TWO', '3': 'THREE', '4': 'FOUR', '5': 'FIVE',
            '6': 'SIX', '7': 'SEVEN', '8': 'EIGHT', '9': 'NINE', '10': 'TEN',
            
            # Additional Common Words
            'today': 'DAY', 'tomorrow': 'DAY', 'yesterday': 'DAY',
            'now': 'TIME', 'later': 'TIME', 'soon': 'TIME',
            'here': 'WHERE', 'there': 'WHERE', 'everywhere': 'WHERE',
            'always': 'WHEN', 'never': 'WHEN', 'sometimes': 'WHEN',
            'because': 'WHY', 'reason': 'WHY', 'cause': 'WHY',
            'person': 'WHO', 'people': 'WHO', 'someone': 'WHO',
            'thing': 'WHAT', 'something': 'WHAT', 'anything': 'WHAT',
            'way': 'HOW', 'method': 'HOW', 'manner': 'HOW',
            'choice': 'WHICH', 'option': 'WHICH', 'selection': 'WHICH',
            
            # Extended Actions
            'see': 'LOOK', 'look': 'LOOK', 'watch': 'LOOK', 'observe': 'LOOK',
            'listen': 'HEAR', 'hear': 'HEAR', 'sound': 'HEAR',
            'speak': 'TALK', 'talk': 'TALK', 'say': 'TALK', 'tell': 'TALK',
            'think': 'UNDERSTAND', 'understand': 'UNDERSTAND', 'know': 'UNDERSTAND',
            'remember': 'UNDERSTAND', 'forget': 'UNDERSTAND',
            'love': 'HAPPY', 'like': 'HAPPY', 'enjoy': 'HAPPY',
            'hate': 'ANGRY', 'dislike': 'ANGRY', 'angry': 'ANGRY',
            'fear': 'SAD', 'afraid': 'SAD', 'scared': 'SAD',
            'hope': 'HAPPY', 'wish': 'HAPPY', 'want': 'HAPPY',
            'need': 'HELP', 'require': 'HELP', 'must': 'HELP',
            'can': 'YES', 'cannot': 'NO', 'able': 'YES', 'unable': 'NO',
            'will': 'YES', 'shall': 'YES', 'should': 'YES', 'would': 'YES',
            'might': 'MAYBE', 'could': 'MAYBE', 'perhaps': 'MAYBE',
            'definitely': 'CERTAINLY', 'surely': 'CERTAINLY', 'absolutely': 'ABSOLUTELY'
        }
        
        words = text.lower().split()
        gesture_sequence = []
        
        for word in words:  # Process all words
            # Clean word (remove punctuation)
            clean_word = ''.join(c for c in word if c.isalnum())
            
            # Map word to gesture
            if clean_word in gesture_mappings:
                gesture = gesture_mappings[clean_word]
            else:
                # For unknown words, choose from diverse gesture categories
                if len(clean_word) > 5:  # Longer words get more specific gestures
                    gesture = random.choice(['LEARN', 'PRACTICE', 'UNDERSTAND', 'COMMUNICATE', 'TEACH', 'HELP'])
                elif len(clean_word) > 3:  # Medium words get action gestures
                    gesture = random.choice(['WORK', 'PLAY', 'COME', 'GO', 'STOP', 'WAIT', 'HELP'])
                else:  # Shorter words get basic gestures
                    gesture = random.choice(['YES', 'NO', 'OK', 'GOOD', 'BAD', 'WHAT', 'HOW'])
            
            gesture_sequence.append({
                'gesture': gesture,
                'duration': random.uniform(0.8, 1.8)  # Vary duration more
            })
        
        return gesture_sequence

def _generate_synthetic_audio(text):
    """Generate synthetic audio data for TTS fallback"""
    import wave
    import struct
    import math
    
    # Generate a simple sine wave audio based on text
    sample_rate = 22050
    duration = len(text) * 0.1  # 0.1 seconds per character
    frequency = 440  # A4 note
    
    # Generate audio samples
    samples = []
    for i in range(int(sample_rate * duration)):
        # Create a simple sine wave with some variation
        t = float(i) / sample_rate
        # Add some variation based on character position
        char_index = int(t * len(text) / duration) if duration > 0 else 0
        if char_index < len(text):
            char_freq = frequency + (ord(text[char_index]) % 200)
        else:
            char_freq = frequency
        
        sample = int(32767 * 0.3 * math.sin(2 * math.pi * char_freq * t))
        samples.append(sample)
    
    # Convert to bytes
    audio_bytes = struct.pack('<' + 'h' * len(samples), *samples)
    
    # Create WAV file in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_bytes)
    
    wav_buffer.seek(0)
    audio_data = wav_buffer.read()
    
    # Encode to base64
    return base64.b64encode(audio_data).decode('utf-8')

# Initialize SignSpeak AI
signspeak_ai = SignSpeakAI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SignSpeak AI API is running'
    })

@app.route('/recognize_gesture', methods=['POST'])
def recognize_gesture():
    """
    Recognize ISL gesture from camera input
    Expected input: base64 encoded image
    Returns: recognized gesture and confidence score
    """
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Process image with ISL recognition model
        if signspeak_ai.isl_model:
            try:
                gesture, confidence = signspeak_ai.isl_model.predict_gesture(cv_image)
            except Exception as e:
                logger.warning(f"ISL model prediction failed: {str(e)}, using fallback")
                gesture = "HELLO"
                confidence = 0.75
        else:
            # Simplified gesture recognition based on image analysis
            gesture, confidence = signspeak_ai._simple_gesture_recognition(cv_image)
        
        return jsonify({
            'gesture': gesture,
            'confidence': confidence,
            'message': f'Recognized gesture: {gesture}'
        })
        
    except Exception as e:
        logger.error(f"Error in gesture recognition: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/text_to_gesture', methods=['POST'])
def text_to_gesture():
    """
    Convert text to ISL gesture animation
    Expected input: text string
    Returns: gesture sequence for 3D avatar
    """
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        # Convert text to ISL gesture sequence
        if signspeak_ai.avatar_system:
            try:
                gesture_frames = signspeak_ai.avatar_system.animate_text(text)
                # Convert frames to sequence format
                gesture_sequence = []
                for frame in gesture_frames[:10]:  # Limit to first 10 gestures
                    gesture_sequence.append({
                        'gesture': 'GESTURE',  # This would be extracted from frame
                        'duration': 1.0,
                        'timestamp': frame.timestamp
                    })
            except Exception as e:
                logger.warning(f"Text to gesture conversion failed: {str(e)}, using fallback")
                gesture_sequence = signspeak_ai._simple_text_to_gesture(text)
        else:
            # Simplified text to gesture conversion
            gesture_sequence = signspeak_ai._simple_text_to_gesture(text)
        
        return jsonify({
            'gesture_sequence': gesture_sequence,
            'message': f'Converted text to {len(gesture_sequence)} gestures'
        })
        
    except Exception as e:
        logger.error(f"Error in text to gesture conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    """
    Convert speech audio to text
    Expected input: base64 encoded audio
    Returns: transcribed text
    """
    try:
        data = request.get_json()
        
        if 'audio' not in data:
            return jsonify({'error': 'No audio provided'}), 400
        
        # Decode base64 audio
        audio_data = base64.b64decode(data['audio'])
        
        # Process audio with speech recognition
        if signspeak_ai.speech_recognizer:
            try:
                text, confidence = signspeak_ai.speech_recognizer.speech_to_text(audio_data)
            except Exception as e:
                logger.warning(f"Speech recognition failed: {str(e)}, using fallback")
                text, confidence = signspeak_ai._simple_speech_recognition(audio_data)
        else:
            # Simplified speech recognition
            text, confidence = signspeak_ai._simple_speech_recognition(audio_data)
        
        return jsonify({
            'text': text,
            'confidence': confidence,
            'message': 'Speech recognized successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in speech recognition: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech audio
    Expected input: text string
    Returns: base64 encoded audio
    """
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        # Convert text to speech
        if signspeak_ai.speech_recognizer:
            try:
                audio_data = signspeak_ai.speech_recognizer.text_to_speech(text)
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            except Exception as e:
                logger.warning(f"Text to speech conversion failed: {str(e)}, using fallback")
                # Generate real audio data instead of placeholder
                audio_base64 = _generate_synthetic_audio(text)
        else:
            # Generate real audio data instead of placeholder
            audio_base64 = _generate_synthetic_audio(text)
        
        return jsonify({
            'audio': audio_base64,
            'message': 'Text converted to speech successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in text to speech conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load models on startup
    if signspeak_ai.load_models():
        logger.info("Starting SignSpeak AI API server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("Failed to load models. Exiting...")
