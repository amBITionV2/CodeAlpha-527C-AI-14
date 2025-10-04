"""
SignSpeak AI - Production Backend API
Real AI-powered sign language communication system
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
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import real AI models
from models.real_gesture_recognition import RealGestureRecognizer
from models.real_speech_processing import RealSpeechProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class ProductionSignSpeakAI:
    """Production SignSpeak AI with real functionality"""
    
    def __init__(self):
        self.gesture_recognizer = None
        self.speech_processor = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize all AI systems"""
        try:
            logger.info("Initializing production SignSpeak AI...")
            
            # Initialize gesture recognition
            logger.info("Loading real gesture recognition system...")
            self.gesture_recognizer = RealGestureRecognizer()
            
            # Initialize speech processing
            logger.info("Loading real speech processing system...")
            self.speech_processor = RealSpeechProcessor()
            
            # Test systems
            self._test_systems()
            
            self.is_initialized = True
            logger.info("Production SignSpeak AI initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize production AI: {e}")
            return False
    
    def _test_systems(self):
        """Test all AI systems"""
        try:
            # Test gesture recognition
            if self.gesture_recognizer:
                available_gestures = self.gesture_recognizer.get_available_gestures()
                logger.info(f"Gesture recognition loaded: {len(available_gestures)} gestures available")
            
            # Test speech processing
            if self.speech_processor:
                languages = self.speech_processor.get_available_languages()
                logger.info(f"Speech processing loaded: {len(languages)} languages available")
                
        except Exception as e:
            logger.warning(f"System test failed: {e}")

# Initialize production AI
signspeak_ai = ProductionSignSpeakAI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if signspeak_ai.is_initialized else 'initializing',
        'message': 'SignSpeak AI Production API is running',
        'timestamp': datetime.now().isoformat(),
        'systems': {
            'gesture_recognition': signspeak_ai.gesture_recognizer is not None,
            'speech_processing': signspeak_ai.speech_processor is not None
        }
    })

@app.route('/recognize_gesture', methods=['POST'])
def recognize_gesture():
    """Real gesture recognition from camera input"""
    try:
        if not signspeak_ai.is_initialized:
            return jsonify({'error': 'AI systems not initialized'}), 503
        
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Process with real gesture recognition
        gesture, confidence = signspeak_ai.gesture_recognizer.predict_gesture(cv_image)
        
        # Get gesture information
        gesture_info = signspeak_ai.gesture_recognizer.get_gesture_info(gesture)
        
        return jsonify({
            'gesture': gesture,
            'confidence': confidence,
            'description': gesture_info.get('description', ''),
            'duration': gesture_info.get('duration', 1.0),
            'message': f'Recognized gesture: {gesture} with {confidence:.2f} confidence'
        })
        
    except Exception as e:
        logger.error(f"Error in gesture recognition: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    """Real speech-to-text conversion"""
    try:
        if not signspeak_ai.is_initialized:
            return jsonify({'error': 'AI systems not initialized'}), 503
        
        data = request.get_json()
        
        if 'audio' not in data:
            return jsonify({'error': 'No audio provided'}), 400
        
        # Get language preference
        language = data.get('language', 'en')
        
        # Decode base64 audio
        audio_data = base64.b64decode(data['audio'])
        
        # Process with real speech recognition
        text, confidence = signspeak_ai.speech_processor.speech_to_text(audio_data, language)
        
        return jsonify({
            'text': text,
            'confidence': confidence,
            'language': language,
            'message': f'Speech recognized: "{text}" with {confidence:.2f} confidence'
        })
        
    except Exception as e:
        logger.error(f"Error in speech recognition: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/text_to_gesture', methods=['POST'])
def text_to_gesture():
    """Convert text to gesture sequence using real mapping"""
    try:
        if not signspeak_ai.is_initialized:
            return jsonify({'error': 'AI systems not initialized'}), 503
        
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        
        # Convert text to gesture sequence using real mapping
        gesture_sequence = convert_text_to_gesture_sequence(text, signspeak_ai.gesture_recognizer)
        
        return jsonify({
            'gesture_sequence': gesture_sequence,
            'text': text,
            'message': f'Converted text to {len(gesture_sequence)} gestures'
        })
        
    except Exception as e:
        logger.error(f"Error in text-to-gesture conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    """Real text-to-speech conversion"""
    try:
        if not signspeak_ai.is_initialized:
            return jsonify({'error': 'AI systems not initialized'}), 503
        
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        language = data.get('language', 'en')
        
        # Process with real TTS
        audio_data = signspeak_ai.speech_processor.text_to_speech(text, language)
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            'audio': audio_base64,
            'text': text,
            'language': language,
            'message': 'Text converted to speech successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_available_gestures', methods=['GET'])
def get_available_gestures():
    """Get list of available gestures"""
    try:
        if not signspeak_ai.is_initialized or not signspeak_ai.gesture_recognizer:
            return jsonify({'error': 'Gesture recognition not available'}), 503
        
        gestures = signspeak_ai.gesture_recognizer.get_available_gestures()
        gesture_info = {}
        
        for gesture in gestures:
            info = signspeak_ai.gesture_recognizer.get_gesture_info(gesture)
            gesture_info[gesture] = {
                'description': info.get('description', ''),
                'duration': info.get('duration', 1.0),
                'confidence_threshold': info.get('confidence_threshold', 0.8)
            }
        
        return jsonify({
            'gestures': gesture_info,
            'count': len(gestures),
            'message': f'Found {len(gestures)} available gestures'
        })
        
    except Exception as e:
        logger.error(f"Error getting available gestures: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_available_languages', methods=['GET'])
def get_available_languages():
    """Get list of available languages"""
    try:
        if not signspeak_ai.is_initialized or not signspeak_ai.speech_processor:
            return jsonify({'error': 'Speech processing not available'}), 503
        
        languages = signspeak_ai.speech_processor.get_available_languages()
        
        return jsonify({
            'languages': languages,
            'count': len(languages),
            'message': f'Found {len(languages)} available languages'
        })
        
    except Exception as e:
        logger.error(f"Error getting available languages: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test_speech_recognition', methods=['POST'])
def test_speech_recognition():
    """Test speech recognition functionality"""
    try:
        if not signspeak_ai.is_initialized or not signspeak_ai.speech_processor:
            return jsonify({'error': 'Speech processing not available'}), 503
        
        success = signspeak_ai.speech_processor.test_speech_recognition()
        
        return jsonify({
            'success': success,
            'message': 'Speech recognition test completed' if success else 'Speech recognition test failed'
        })
        
    except Exception as e:
        logger.error(f"Error testing speech recognition: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test_text_to_speech', methods=['POST'])
def test_text_to_speech():
    """Test text-to-speech functionality"""
    try:
        if not signspeak_ai.is_initialized or not signspeak_ai.speech_processor:
            return jsonify({'error': 'Speech processing not available'}), 503
        
        data = request.get_json()
        test_text = data.get('text', 'Hello, this is a test')
        
        success = signspeak_ai.speech_processor.test_text_to_speech(test_text)
        
        return jsonify({
            'success': success,
            'message': 'Text-to-speech test completed' if success else 'Text-to-speech test failed'
        })
        
    except Exception as e:
        logger.error(f"Error testing text-to-speech: {str(e)}")
        return jsonify({'error': str(e)}), 500

def convert_text_to_gesture_sequence(text: str, gesture_recognizer) -> list:
    """Convert text to gesture sequence using real mapping"""
    words = text.lower().split()
    gesture_sequence = []
    
    # Word to gesture mapping
    word_to_gesture = {
        # Greetings
        'hello': 'HELLO', 'hi': 'HI', 'hey': 'HI', 'goodbye': 'GOODBYE',
        'bye': 'GOODBYE', 'welcome': 'WELCOME', 'farewell': 'GOODBYE',
        
        # Emotions
        'happy': 'HAPPY', 'sad': 'SAD', 'angry': 'ANGRY', 'excited': 'HAPPY',
        'surprised': 'SURPRISED', 'calm': 'HAPPY', 'confused': 'SURPRISED',
        
        # Responses
        'yes': 'YES', 'no': 'NO', 'maybe': 'MAYBE', 'ok': 'OK', 'okay': 'OK',
        'sure': 'YES', 'certainly': 'YES', 'absolutely': 'YES',
        
        # Polite words
        'please': 'PLEASE', 'thank': 'THANK_YOU', 'thanks': 'THANK_YOU',
        'thankyou': 'THANK_YOU', 'sorry': 'SORRY', 'excuse': 'EXCUSE_ME',
        'pardon': 'EXCUSE_ME',
        
        # Questions
        'what': 'WHAT', 'where': 'WHERE', 'when': 'WHEN', 'why': 'WHY',
        'how': 'HOW', 'who': 'WHO', 'which': 'WHAT',
        
        # Actions
        'come': 'COME', 'go': 'GO', 'stop': 'STOP', 'wait': 'WAIT',
        'help': 'HELP', 'learn': 'LEARN', 'teach': 'TEACH', 'practice': 'LEARN',
        'work': 'LEARN', 'play': 'LEARN', 'eat': 'LEARN', 'drink': 'LEARN',
        
        # Objects
        'book': 'BOOK', 'pen': 'PEN', 'computer': 'COMPUTER', 'phone': 'PHONE',
        'car': 'CAR', 'house': 'HOUSE', 'home': 'HOUSE', 'tree': 'HOUSE',
        'water': 'LEARN', 'food': 'LEARN', 'money': 'LEARN',
        
        # Family
        'mother': 'MOTHER', 'mom': 'MOTHER', 'father': 'FATHER', 'dad': 'FATHER',
        'sister': 'SISTER', 'brother': 'BROTHER', 'family': 'FAMILY',
        'friend': 'FRIEND', 'child': 'FRIEND', 'baby': 'FRIEND',
        
        # Colors
        'red': 'RED', 'blue': 'BLUE', 'green': 'GREEN', 'yellow': 'YELLOW',
        'black': 'BLACK', 'white': 'WHITE', 'pink': 'RED', 'purple': 'BLUE',
        
        # Numbers
        'one': 'ONE', 'two': 'TWO', 'three': 'THREE', 'four': 'FOUR', 'five': 'FIVE',
        'six': 'SIX', 'seven': 'SEVEN', 'eight': 'EIGHT', 'nine': 'NINE', 'ten': 'TEN',
        '1': 'ONE', '2': 'TWO', '3': 'THREE', '4': 'FOUR', '5': 'FIVE',
        '6': 'SIX', '7': 'SEVEN', '8': 'EIGHT', '9': 'NINE', '10': 'TEN'
    }
    
    # Convert words to gestures
    for word in words:
        # Clean word (remove punctuation)
        clean_word = ''.join(c for c in word if c.isalnum())
        
        if clean_word in word_to_gesture:
            gesture_name = word_to_gesture[clean_word]
            gesture_info = gesture_recognizer.get_gesture_info(gesture_name)
            
            gesture_sequence.append({
                'gesture': gesture_name,
                'duration': gesture_info.get('duration', 1.0),
                'description': gesture_info.get('description', ''),
                'word': clean_word
            })
        else:
            # For unknown words, use a default gesture
            gesture_sequence.append({
                'gesture': 'LEARN',
                'duration': 1.0,
                'description': 'Learning gesture',
                'word': clean_word
            })
    
    return gesture_sequence

if __name__ == '__main__':
    # Initialize production AI
    if signspeak_ai.initialize():
        logger.info("Starting SignSpeak AI Production API server...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.error("Failed to initialize production AI. Exiting...")
        sys.exit(1)
